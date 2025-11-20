# -*- coding: utf-8 -*-
# =================================================================================
# File        : constants.py
# Description : [This file contains the constants of the package]
# Author      : [Safran SA / Safran Tech / DST]
# Created     : [2023-06-02]
# Updated     : [2025-10-20]
# Version     : [v1.0]
#
# =================================================================================

import os

from enum import Enum
from importlib.resources import files


def get_executable_path():
    """
    Get the path for the DeckSMR executable.
    
    Returns:
        str: Path to the DeckSMR executable
        
    Raises:
        FileNotFoundError: If executable not found
    """
    resource = files("odsmr.bin").joinpath("DeckSMR")
    path = str(resource)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Executable not found at {path}")

    return path

# Executable path
ROOT_OPENDECK = get_executable_path()


# Component degradation state labels
STATE_LABELS = [
    "deg_CmpBst_s_mapEff_in",   # Booster compressor efficiency
    "deg_CmpBst_s_mapWc_in",    # Booster compressor flow capacity
    "deg_CmpFan_s_mapEff_in",   # Fan efficiency
    "deg_CmpFan_s_mapWc_in",    # Fan flow capacity
    "deg_CmpH_s_mapEff_in",     # High pressure compressor efficiency
    "deg_CmpH_s_mapWc_in",      # High pressure compressor flow capacity
    "deg_TrbH_s_mapEff_in",     # High pressure turbine efficiency
    "deg_TrbH_s_mapWc_in",      # High pressure turbine flow capacity
    "deg_TrbL_s_mapEff_in",     # Low pressure turbine efficiency
    "deg_TrbL_s_mapWc_in",      # Low pressure turbine flow capacity
]


# Degradation parameter bounds (min, max)
STATE_BOUNDS = {
    "deg_CmpFan_s_mapEff_in": (-0.05, 0.0),
    "deg_CmpFan_s_mapWc_in": (-0.05, 0.03),
    "deg_CmpBst_s_mapEff_in": (-0.05, 0.0),
    "deg_CmpBst_s_mapWc_in": (-0.05, 0.03),
    "deg_CmpH_s_mapEff_in": (-0.05, 0.0),
    "deg_CmpH_s_mapWc_in": (-0.05, 0.03),
    "deg_TrbH_s_mapEff_in": (-0.05, 0.0),
    "deg_TrbH_s_mapWc_in": (-0.05, 0.05),
    "deg_TrbL_s_mapEff_in": (-0.05, 0.0),
    "deg_TrbL_s_mapWc_in": (-0.05, 0.05),
}


class FlightPhaseType(str, Enum):
    """Flight phase enumeration."""
    CRUISE = "CR"
    TAKEOFF = "MTO"
    CLIMB = "MCL"


# FLIGHT BOUNDS
CRUISE_BOUNDS = {
    "DTAMB": (9.0, 11.0), # Ambient temperature delta (°C)
    "ALT": (34900, 35100), # Altitude (ft)
    "MACH": (0.76, 0.80), # Mach number
    "COMMAND": (24900.0, 25100.0), # Thrust command (lbf)
}

TAKEOFF_BOUNDS = {
    "DTAMB": (14.0, 16.0),
    "ALT": (0, 100),
    "MACH": (0.0, 0.0001)
}

CLIMB_BOUNDS = {
    "DTAMB": (9.0, 11.0),
    "ALT": (15000, 35000),
    "MACH": (0.54, 0.56)
}

FLIGHT_CONDITIONS_BOUNDS = {
    FlightPhaseType.CRUISE: CRUISE_BOUNDS,
    FlightPhaseType.TAKEOFF: TAKEOFF_BOUNDS,
    FlightPhaseType.CLIMB: CLIMB_BOUNDS,
}
