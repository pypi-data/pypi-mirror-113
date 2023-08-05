import logging
import time

from pyHepMC3 import HepMC3 as hm

from mcconv import detect_mc_type
from .formats.beagle import BeagleReader
from .generic_reader import GenericTextReader, UnparsedTextEvent
from .formats.lund import parse_lund_particles, parse_lund_particle_tokens
from .file_types import McFileTypes
from .eic_smear_reader import EicTreeReader, EicSmearEventData

logger = logging.getLogger("mcconv.hepmc_convert")


def hepmc_convert(input_file, output_file, input_type, hepmc_vers, progress_func=None, nskip=0, nprocess=0):

    # Choose the output format: hepmc 2 or 3 writer
    if hepmc_vers == 2 or hepmc_vers == "2" or (isinstance(hepmc_vers, str) and hepmc_vers.lower() == "hepmc2"):
        writer = hm.WriterAsciiHepMC2(output_file)
    else:
        writer = hm.WriterAscii(output_file)

    # What is the input type? Is it known?
    if not input_type or input_type == McFileTypes.UNKNOWN:
        logger.debug("Input file type is not given or UNKNOWN. Trying autodetect")

        # Input type is unknown, trying autodetection
        input_type = detect_mc_type(input_file)

    # If it is still UNKNOWN - we where unable to detect. Error raising
    if input_type == McFileTypes.UNKNOWN:
        raise ValueError("File format is UNKNOWN")

    # Set event reader according to file type
    if input_type == McFileTypes.EIC_SMEAR:
        reader = EicTreeReader()
    else:
        reader = GenericTextReader()

        if input_type == McFileTypes.BEAGLE:
            reader.particle_tokens_len = 18

    # Open input file
    reader.open(input_file)

    # This is basically the same as with statement. But HepMcWriter doesn't implement __enter__() etc.
    hepmc_event = hm.GenEvent(hm.Units.GEV, hm.Units.MM)
    start_time = time.time()
    try:
        # Iterate events
        for evt_index, source_event in enumerate(reader.events(nskip, nprocess)):

            # What conversion function to use?
            if input_type == McFileTypes.EIC_SMEAR:
                eic_smear_to_hepmc(hepmc_event, source_event)
            else:
                lund_to_hepmc(hepmc_event, source_event, flavour=input_type)

            # Write event
            writer.write_event(hepmc_event)

            # call progress func, so one could work on it
            if progress_func:
                progress_func(evt_index, hepmc_event)

            hepmc_event.clear()
    finally:
        # closing everything (we are not using with statement as it is not supported by HepMC)
        writer.close()
        reader.close()
        hepmc_event.clear()
        logger.info(f"Time for the conversion = {time.time() - start_time} sec")


def add_hepmc_attribute(obj, name, str_value, val_type):
    if val_type == int:
        obj.add_attribute(name, hm.IntAttribute(int(str_value)))
    if val_type == float:
        obj.add_attribute(name, hm.FloatAttribute(float(str_value)))
    if val_type == str:
        obj.add_attribute(name, hm.StringAttribute(str_value))


def lund_to_hepmc(hepmc_evt, unparsed_event, rules=None, flavour=McFileTypes.LUND):
    """
        Rules define columns, that are used for extraction of parameters

        rules = {
            "px": 6,        # Column where px is stored
            "py": 7,        # Column where py is stored
            "pz": 8,        # Column where pz is stored
            "e": 9,         # Energy
            "pid": 2,       # PID of particle (PDG code)
            "status": 1,    # Status
            "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data
            "prt_attrs": {"life_time": (1, float)},     # In LUND GemC the second col. (index 1) is life time.
                                                        # If that is need to be stored, that is how to store it

        }
        rules["px"]
        rules["py"]
        rules["pz"]
        rules["e"]
        rules["pid"]
        rules["status"]
        rules["evt_attrs"]
        rules["prt_attrs"]

    """
    assert isinstance(unparsed_event, UnparsedTextEvent)

    if not rules:
        prt_col_px = 6
        prt_col_py = 7
        prt_col_pz = 8
        prt_col_e = 9
        prt_col_pid = 3
        prt_col_status = 2
        evt_attrs = {"weight": (9, float)}
        prt_attrs = {}

        # Lund GEMC format has status and PID at different types
        if flavour == McFileTypes.LUND_GEMC:
            prt_col_pid = 3
            prt_col_status = 2

        if flavour == McFileTypes.PYTHIA6_EIC:
            # No event weight for pythia6
            evt_attrs = {"weight": (9, float)}

        if flavour == McFileTypes.BEAGLE:
            prt_col_px = 7
            prt_col_py = 8
            prt_col_pz = 9
            prt_col_e = 10
    else:
        prt_col_px = rules["px"]
        prt_col_py = rules["py"]
        prt_col_pz = rules["pz"]
        prt_col_e = rules["e"]
        prt_col_pid = rules["pid"]
        prt_col_status = rules["status"]
        evt_attrs = rules["evt_attrs"]
        prt_attrs = rules["prt_attrs"]

    hepmc_evt.add_attribute("start_line_index", hm.IntAttribute(unparsed_event.start_line_index))

    v1 = hm.GenVertex()
    hepmc_evt.add_vertex(v1)

    #particles = parse_lund_particles(unparsed_event)
    for particle_line in unparsed_event.unparsed_particles:

        # Parse main columns with 4 vectors
        px = float(particle_line[prt_col_px])
        py = float(particle_line[prt_col_py])
        pz = float(particle_line[prt_col_pz])
        energy = float(particle_line[prt_col_e])
        pid = int(particle_line[prt_col_pid])
        status = int(particle_line[prt_col_status])

        # Take only final state particle
        if status != 1:
            continue

        # Create a hepmc particle
        hm_particle = hm.GenParticle(hm.FourVector(px, py, pz, energy), pid, status)

        # Add particle level attributes
        for name, params in prt_attrs.items():
            column_index, field_type = params
            add_hepmc_attribute(hm_particle, name, column_index, field_type)

        # Add particle to event
        hepmc_evt.add_particle(hm_particle)

        # Add event level attributes
        for name, params in evt_attrs.items():
            column_index, field_type = params
            add_hepmc_attribute(hm_particle, name, column_index, field_type)

    return hepmc_evt


def eic_smear_to_hepmc(hepmc_evt, source_evt):
    """

    """
    assert isinstance(source_evt, EicSmearEventData)

    v1 = hm.GenVertex()
    hepmc_evt.add_vertex(v1)

    #particles = parse_lund_particles(unparsed_event)
    for particle in source_evt.particles:

        # Create a hepmc particle
        hm_particle = hm.GenParticle(hm.FourVector(particle.px, particle.py, particle.pz, particle.energy),
                                     particle.pid,
                                     particle.status)

        # Add particle to event
        hepmc_evt.add_particle(hm_particle)

    return hepmc_evt