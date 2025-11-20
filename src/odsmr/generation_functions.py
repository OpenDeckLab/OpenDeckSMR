# -*- coding: utf-8 -*-
# =================================================================================
# File        : generation_functions.py
# Description : [This file contains the functions to call to generate measures]
# Author      : [Safran SA / Safran Tech / DST]
# Created     : [2023-03-06]
# Updated     : [2025-06-03]
# Version     : [v1.0]
#
# =================================================================================
import numpy as np
import pandas as pd
from typing import List

from odsmr.sensors import Sensor
from odsmr.context import ContextDeckSMR
from odsmr.wrapping import DeckSMR
from odsmr.constants import STATE_LABELS
from odsmr.helpers import dict_to_array, array_to_dict


def decksmr_1forall(list_state_value: List[np.ndarray],
                    list_context: List[ContextDeckSMR],
                    list_sensors: List[Sensor],
                    sim_root: str) -> pd.DataFrame:
    """
    This function takes a list of state values, a list of contexts, and outputs
    the measurements for all state_values for the same list of contexts.

    Args:
        list_state_value (List[np.ndarray]): list of the states you want
        measurements from
        list_context (List[ContextDeckSMR]): list of contexts. Remember
        same context list will be apply to all states points
        list_sensors (List[Sensor]): list of sensors.
        sim_root (str): root of the DeckSMR

    Returns:
        all_context_measures_df (List[pd.DataFrame]): list of the measurements.
        The keys of the dataframe indicate name of the flight condition and 
        name of the sensor
    """

    # For each context, launch a series of simulations
    all_context_measures_df = []
    for context in list_context:
        inputs_set_list = []
        for i in range(len(list_state_value)):
            inputs_set_list.append(
                context.flight_condition.__dict__
                )

        list_dict_parameters = []
        for state_value in list_state_value:
            list_dict_parameters.append(array_to_dict(state_value, keys=STATE_LABELS))

        simulator = DeckSMR(ROOT=sim_root)
        df = simulator.run_simulation_multi_parameters(
            inputs=inputs_set_list, list_parameters=list_dict_parameters
        )

        df_measured = df.loc[:, [sensor.name for sensor in list_sensors]]
        df_measured['context_name'] = context.name
        df_measured['phase_type'] = context.flight_condition.PHASE_TYPE
        df_measured['DTAMB'] = context.flight_condition.DTAMB
        df_measured['ALT'] = context.flight_condition.ALT
        df_measured['COMMAND'] = context.flight_condition.COMMAND
        df_measured['MACH'] = context.flight_condition.MACH
        df_measured['Convergence'] = df['Convergence']
        
        for state_label in STATE_LABELS:
            df_measured[state_label] = np.nan

        for id_state, state_label in enumerate(STATE_LABELS):
            for j, state_value in enumerate(list_state_value):
                df_measured.at[j, state_label] = state_value[id_state]

        all_context_measures_df.append(df_measured)
    all_context_measures_df = pd.concat(all_context_measures_df, axis=0, ignore_index=True)
    return all_context_measures_df


def decksmr_1for1(list_state_value: List[np.ndarray],
                    list_context: List[ContextDeckSMR],
                    list_sensors: List[Sensor],
                    sim_root: str) -> pd.DataFrame:
    """ This function takes a list of state values, a list of contexts, and outputs
    the measurements for each state value with corresponding contexts

    Args:
        list_state_value (List[np.ndarray]): list of the states you want
        measurements from
        list_context (List[ContextDeckSMR]): list of contexts. Remember
        on context will be apply for each states point
        list_sensors (List[Sensor]): list of sensors.
        sim_root (str): root of the DeckSMR

    Raises:
        ValueError: if you don't give one for one state - context, it will
        raise a ValueError.

    Returns:
        all_context_measures_df (List[pd.DataFrame]): list of the measurements.
        The keys of the dataframe indicate name of the flight condition and 
        name of the sensor
    """

    # in this function, you need one context for each state
    if len(list_context) != len(list_state_value):
        raise ValueError(
            'list_state_value and list_context should have the same size. '
            'If you want combinations, use decksmr_1forall function'
        )
    all_context_measures_df = []
    # Prepare inputs: one context per state
    inputs_set_list = [
        context.flight_condition.__dict__
        for context in list_context
    ]

    # Convert state arrays to parameter dictionaries
    list_dict_parameters = [
        array_to_dict(state_value, keys=STATE_LABELS)
        for state_value in list_state_value
    ]

    # Run simulation
    simulator = DeckSMR(ROOT=sim_root)
    df = simulator.run_simulation_multi_parameters(
        inputs=inputs_set_list, list_parameters=list_dict_parameters
    )
    
    # Build the output dataframe
    df_measured = df.loc[:, [sensor.name for sensor in list_sensors]]
    df_measured['Convergence'] = df['Convergence']

    for state_label in STATE_LABELS:
        df_measured[state_label] = np.nan

    for id_state, state_label in enumerate(STATE_LABELS):
        for j, state_value in enumerate(list_state_value):
            df_measured.at[j, state_label] = state_value[id_state]

    for j, context in enumerate(list_context):
        df_measured.at[j,'context_name'] = context.name
        df_measured.at[j,'phase_type'] = context.flight_condition.PHASE_TYPE
        df_measured.at[j,'DTAMB'] = context.flight_condition.DTAMB
        df_measured.at[j,'ALT'] = context.flight_condition.ALT
        df_measured.at[j,'COMMAND'] = context.flight_condition.COMMAND
        df_measured.at[j,'MACH'] = context.flight_condition.MACH

    all_context_measures_df.append(df_measured)
    all_context_measures_df = pd.concat(all_context_measures_df, axis=0)
    return all_context_measures_df

