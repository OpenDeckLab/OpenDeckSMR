# -*- coding: utf-8 -*-
# =================================================================================
# File        : generation_functions.py
# Description : [This file contains the functions to call to generate measures]
# Author      : [Safran SA / Safran Tech / DST ]
# Created     : [2023-02-03]
# Updated     : [2025-06-03]
# Version     : [v1.0]
#
# =================================================================================
import numpy as np
import pandas as pd


def dict_to_array(dictionary):
    """
    A function to convert a dictionary to an array
    ...
    Parameters
    ----------
    dictionary: dict
        the input dictionary
    ...
    Return
    -------
    the numpy array contain values of the input dictionary
    """

    if isinstance(dictionary, dict):
        return np.fromiter(dictionary.values(), dtype=float)
    elif isinstance(dictionary, np.ndarray):
        return dictionary


def array_to_dict(array, keys=None):
    """
    A function to convert an array to a dict
    ...
    Parameters
    ----------
    array: np.ndarray
        the input array
    keys: List
        the list of keys of output dict
    ...
    Return
    -------
    the dictionary with keys taken from the input keys and values taken from input array.
    If not key is provided, use coord+order of the numpy array as key.
    """
    if keys is not None:
        return {key: float(val) for key, val in zip(keys, array)}
    else:
        return {"coord" + str(key): val for key, val in enumerate(array)}


def sample_from_bounds(parameters_bounds):
    """
    A function that samples a number between 2 bounds given as a dictionary with an uniform distribution

    Args:
        parameters_bounds (dict): a dictionary of the parameter bounds. Example: 
        parameters_bounds = {"param1": (0.1, 7.9), "param2": (-0.9, 0.99)}

    Returns:
        samples (dict): a dictionary with the sampled values. Example:
        {"param1": 0.3, "param2": -0.1}
    """
    samples = {}
    for param, (min_bound, max_bound) in parameters_bounds.items():
        if min_bound >= max_bound:
            raise ValueError(f"Invalid bounds for {param}: min ({min_bound}) >= max ({max_bound})")
        samples[param] = np.random.uniform(min_bound, max_bound)

    samples.setdefault('COMMAND', 25000)

    return samples


def extract_info(
    df: pd.DataFrame, 
    list_variables_name: list, 
    context_name: bool = True, 
    phase_type: bool = True, 
    flight_conditions: bool = True
) -> pd.DataFrame:
    """
    Extract specific columns from DataFrame.
    
    Args:
        df: Input DataFrame
        list_variables_name: List of variable columns to extract
        context_name: Include context_name column
        phase_name: Include phase_type column  
        flight_conditions: Include flight condition columns
        
    Returns:
        DataFrame with selected columns
    """
    local_variables = list(list_variables_name)
    
    if context_name and 'context_name' in df.columns:
        local_variables.append('context_name')
    if phase_type and 'phase_type' in df.columns:
        local_variables.append('phase_type')
    if flight_conditions:
        flight_cols = ['DTAMB', 'ALT', 'MACH', 'COMMAND']
        local_variables.extend([col for col in flight_cols if col in df.columns])
    
    # Remove duplicates while preserving order
    local_variables = list(dict.fromkeys(local_variables))
    
    return df[local_variables]