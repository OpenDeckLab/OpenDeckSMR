# -*- coding: utf-8 -*-
# =================================================================================
# File        : flight_conditions.py
# Description : [This file contains the class Sensor and the Sensors of the engine]
# Author      : [Safran SA / Safran Tech / DST]
# Created     : [2023-03-09]
# Updated     : [2025-10-20]
# Version     : [v1.0]
#
# ================================================================================
from odsmr.context import ContextDeckSMR, FlightCondDeckSMR
from odsmr.constants import FlightPhaseType


Cruise_DeckSMR = ContextDeckSMR(
    name="Cruise_DeckSMR",
    flight_condition=FlightCondDeckSMR(
        PHASE_TYPE=FlightPhaseType.CRUISE.value,
        DTAMB=10.0,  # Delta to Standard Temperature in Kelvin
        ALT=35000,  # Altitude
        MACH=0.78,  # Free Stream Mach Number
        COMMAND=25000,  # Specific command
    )
)

Takeoff_DeckSMR = ContextDeckSMR(
    name="Takeoff_DeckSMR",
    flight_condition=FlightCondDeckSMR(
        PHASE_TYPE=FlightPhaseType.TAKEOFF.value,
        DTAMB=15.0,  # Delta to Standard Temperature in Kelvin
        ALT=0.0,  # Altitude
        MACH=0.0,  # Free Stream Mach Number
        COMMAND=120000,  # Specific command, no effect on MTO, MCL1 & MCL2, value is just ref
    )
)

Climb1_DeckSMR = ContextDeckSMR(
    name="Climb1_DeckSMR",
    flight_condition=FlightCondDeckSMR(
        PHASE_TYPE=FlightPhaseType.CLIMB.value,
        DTAMB=10.0,  # Delta to Standard Temperature in Kelvin
        ALT=15000,  # Altitude
        MACH=0.55,  # Mach number
        COMMAND=120000,  # Specific command, no effect on MTO, MCL1 & MCL2, value is just ref
    )
)

Climb2_DeckSMR = ContextDeckSMR(
    name="Climb2_DeckSMR",
    flight_condition=FlightCondDeckSMR(
        PHASE_TYPE=FlightPhaseType.CLIMB.value,
        DTAMB=10.0,  # Delta to Standard Temperature in Kelvin
        ALT=35000,  # Altitude
        MACH=0.78,  # Mach number
        COMMAND=120000,  # Specific command, no effect on MTO, MCL1 & MCL2, value is just ref
    )
)