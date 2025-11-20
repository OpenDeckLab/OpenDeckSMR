# -*- coding: utf-8 -*-
# =================================================================================
# File        : sensors.py
# Description : [This file contains the class Sensor and the Sensors of the engine]
# Author      : [Safran SA / Safran Tech / DST ]
# Created     : [2025-06-02]
# Updated     : [2025-06-02]
# Version     : [v1.0]
#
# ================================================================================

class Sensor:
    """
    A class defining generic sensors.

    Attributes
    ----------
    description: str
        description of the sensor
    name: str
        name of the sensor
    unit: str
        unit of the measurement
    """
    def __init__(self):
        self.name = None
        self.description = None
        self.unit = None
        return None

    def __str__(self):
        return "Description: " + self.description + "\n" + "Unit: " + self.unit


class HPC_Tout(Sensor):

    def __init__(self):
        self.name = "HPC_Tout"
        self.description = "High-Pressure Compressor outlet temperature"
        self.unit = "Kelvin"


class HP_Nmech(Sensor):
    
    def __init__(self):
        self.name = "HP_Nmech"
        self.description = "High-Pressure shaft rotational speed"
        self.unit = "RPM"


class HPC_Tin(Sensor):
    def __init__(self):
        self.name = "HPC_Tin"
        self.description = "High-Pressure Compressor inlet temperature"
        self.unit = "Kelvin"


class LPT_Tin(Sensor):
    def __init__(self):
        self.name = "LPT_Tin"
        self.description = "Low-Pressure Turbine inlet temperature"
        self.unit = "Kelvin"


class LPT_Tout(Sensor):
    def __init__(self):
        self.name = "LPT_Tout"
        self.description = "Low-Pressure Turbine outlet temperature"
        self.unit = "Kelvin"

class Fuel_flow(Sensor):
    def __init__(self):
        self.name = "Fuel_flow"
        self.description = "Fuel flow rate"
        self.unit = "kg/s"


class HPC_Pout_st(Sensor):
    def __init__(self):
        self.name = "HPC_Pout_st"
        self.description = "High-Pressure Compressor outlet static pressure"
        self.unit = "Pa"


class LP_Nmech(Sensor):
    
    def __init__(self):
        self.name = "LP_Nmech"
        self.description = "Low-Pressure shaft rotational speed"
        self.unit = "RPM"

class Thrust(Sensor):
    
    def __init__(self):
        self.name = "Thrust"
        self.description = "Net produced thrust"
        self.unit = "N"