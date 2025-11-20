# -*- coding: utf-8 -*-
# =================================================================================
# File        : context.py
# Description : [This file contains the context class]
# Author      : [Safran SA / Safran Tech / DST]
# Created     : [2023-03-06]
# Updated     : [2025-10-20]
# Version     : [v1.0]
#
# =================================================================================
from dataclasses import dataclass

@dataclass
class FlightCondDeckSMR:
    """
    Flight conditions for DeckSMR engine simulations.
    
    Attributes:
        PHASE_TYPE (str): Flight phase identifier ('CR', 'MTO', 'MCL')
        DTAMB (float): Delta to standard temperature (°C)
        ALT (float): Altitude (ft)
        MACH (float): Free stream Mach number
        COMMAND (float): Thrust command (lbf). No effect for MCL1, MCL2 and TakeOff phases
    """

    PHASE_TYPE: str  # Flight phase type identifier (e.g., 'CR', 'MTO', 'MCL')
    DTAMB: float # Delta to Standard Temperature in Kelvin
    ALT: float  # Altitude
    MACH: float  # Free Stream Mach Number
    COMMAND: float  # commande, no effect for MCL1, MCL2 and TakeOff

    def __post_init__(self):
        """Validate flight condition parameters."""
        if not isinstance(self.PHASE_TYPE, str):
            raise TypeError("PHASE_TYPE must be a string")
        if self.PHASE_TYPE not in ['MCL', 'MTO', 'CR']:
            raise TypeError("PHASE_TYPE must be a string amongst 'MCL', 'CR','MTO'")
        if self.ALT < 0:
            raise ValueError("Altitude must be non-negative")
        if self.MACH < 0:
            raise ValueError("Mach number must be non-negative")


class ContextDeckSMR:
    """
    Context manager for DeckSMR simulations.

    This class encapsulates flight conditions and simulation parameters
    for Open Deck SMR operations.

    Attributes:
        name (str): Context identifier name
        flight_condition (FlightCondDeckSMR): Flight condition parameters

    Example:
        >>> flight_cond = FlightCondDeckSMR(
        ...     PHASE_TYPE="CR", DTAMB=10.0, ALT=35000, MACH=0.78, 
        ...     COMMAND=25000.0
        ... )
        >>> context = ContextDeckSMR("cruise_context", flight_cond)
        >>> print(context)
    """

    def __init__(
        self,
        name: str = None,
        flight_condition: FlightCondDeckSMR = None
    ):
        """
        Initialize DeckSMR context.
        
        Args:
            name: Context identifier. Defaults to "DefaultName" if None
            flight_condition: Flight condition object
            
        Raises:
            TypeError: If flight_condition is not a FlightCondDeckSMR instance
        """
        if flight_condition is None:
            raise ValueError("flight_condition cannot be None")
        
        if isinstance(flight_condition, FlightCondDeckSMR):
            self.flight_condition = flight_condition
        else:
            raise TypeError("The params of ContextDeckSMR should contain a FlightCondDeckSMR")
        if name is None:
            name = "DefaultName"
        self.name = name

    def get_label_flight_condition(self):
        """
       Print all the features labels of associated flight conditions.

       Parameters
       ----------
       None

       Returns
       -------
       dictionary_keys  of self.flight_condition
       """
        return self.flight_condition.__dict__.keys()

    def get_value_flight_condition(self):
        """
        Print all the features values of associated flight conditions.

        Parameters
        ----------
        None

        Returns
        -------
        dictionary_values  of self.flight_condition
        """
        return self.flight_condition.__dict__.values()

    def __repr__(self):
        """Detailed string representation."""
        return (
            f"ContextDeckSMR(name='{self.name}', "
            f"flight_condition={self.flight_condition})"
        )
    
    def __str__(self):
        """Human-readable string representation."""
        fc = self.flight_condition
        return (
            f"DeckSMR Context '{self.name}': {fc.PHASE_TYPE} phase at "
            f"ALT={fc.ALT}ft, MACH={fc.MACH:.2f}, DTAMB={fc.DTAMB}°C"
        )