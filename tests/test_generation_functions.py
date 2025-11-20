"""
Unit tests for simulation orchestration functions.
"""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import Mock, patch

from odsmr.generation_functions import decksmr_1forall, decksmr_1for1
from odsmr.sensors import HPC_Tout, HP_Nmech, Fuel_flow, LP_Nmech
from odsmr.context import ContextDeckSMR, FlightCondDeckSMR
from odsmr.constants import ROOT_OPENDECK


class TestDeckSMRSimulation:
    """Test suite for DeckSMR simulation functions."""
    
    @pytest.fixture
    def real_sensors(self):
        """Create real sensor instances."""
        return [
            HPC_Tout(),
            HP_Nmech(), 
            Fuel_flow(),
            LP_Nmech()
        ]
    
    @pytest.fixture
    def flight_conditions(self):
        """Create test flight conditions."""
        cruise = FlightCondDeckSMR(
            PHASE_TYPE="CR",
            DTAMB=10.0,
            ALT=35000,
            MACH=0.78,
            COMMAND=25000.0
        )
        
        takeoff = FlightCondDeckSMR(
            PHASE_TYPE="MTO",
            DTAMB=15.0,
            ALT=0,
            MACH=0.0,
            COMMAND=25000.0
        )
        
        return cruise, takeoff
    
    @pytest.fixture
    def contexts(self, flight_conditions):
        """Create test contexts."""
        cruise_fc, takeoff_fc = flight_conditions
        
        cruise_ctx = ContextDeckSMR("cruise", cruise_fc)
        takeoff_ctx = ContextDeckSMR("takeoff", takeoff_fc)
        
        return [cruise_ctx, takeoff_ctx]
    
    @pytest.fixture
    def state_values(self):
        """Create test state values."""
        # 10 state values matching STATE_LABELS length
        state1 = np.array([0.0, -0.01, 0.0, 0.005, -0.02, 0.01, 0.0, -0.005, 0.0, 0.0])
        state2 = np.array([-0.01, 0.0, -0.005, 0.0, 0.0, -0.01, 0.005, 0.0, -0.01, 0.005])
        
        return [state1, state2]
    
    @pytest.fixture
    def mock_simulation_results(self):
        """Create realistic simulation results."""
        return pd.DataFrame({
            'HPC_Tout': [750.5, 755.2],     # Kelvin
            'HP_Nmech': [15500, 15800],     # RPM
            'Fuel_flow': [0.45, 0.47],      # Kg/s
            'LP_Nmech': [8500, 8650],       # RPM
            'Convergence': [True, True],
            'extra_col': [1, 2]  # Should be filtered out
        })
    
    @patch('odsmr.generation_functions.DeckSMR')
    def test_decksmr_1forall_basic(self, mock_decksmr_class, real_sensors, contexts, 
                                   state_values, mock_simulation_results):
        """Test basic functionality of decksmr_1forall."""
        # Setup mock
        mock_simulator = Mock()
        mock_simulator.run_simulation_multi_parameters.return_value = mock_simulation_results
        mock_decksmr_class.return_value = mock_simulator
        
        # Run function with real ROOT_OPENDECK
        result = decksmr_1forall(
            list_state_value=state_values,
            list_context=contexts,
            list_sensors=real_sensors,
            sim_root=ROOT_OPENDECK
        )
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(contexts) * len(state_values)  # 2 contexts * 2 states = 4 rows
        
        # Check sensor columns are present
        assert 'HPC_Tout' in result.columns
        assert 'HP_Nmech' in result.columns
        assert 'Fuel_flow' in result.columns
        assert 'LP_Nmech' in result.columns
        
        # Check context columns are present
        assert 'context_name' in result.columns
        assert 'phase_type' in result.columns
        assert 'DTAMB' in result.columns
        assert 'ALT' in result.columns
        
        # Check state columns are present (from STATE_LABELS)
        assert 'deg_CmpBst_s_mapEff_in' in result.columns
        assert 'deg_CmpFan_s_mapEff_in' in result.columns
        
        # Check convergence column
        assert 'Convergence' in result.columns
        
        # Verify DeckSMR was called with correct ROOT
        mock_decksmr_class.assert_called_with(ROOT=ROOT_OPENDECK)
        assert mock_decksmr_class.call_count == len(contexts)

    @patch('odsmr.generation_functions.DeckSMR')
    def test_decksmr_1for1_basic(self, mock_decksmr_class, real_sensors, contexts, 
                                 state_values, mock_simulation_results):
        """Test basic functionality of decksmr_1for1."""
        # Setup mock
        mock_simulator = Mock()
        mock_simulator.run_simulation_multi_parameters.return_value = mock_simulation_results
        mock_decksmr_class.return_value = mock_simulator
        
        # Run function with real ROOT_OPENDECK
        result = decksmr_1for1(
            list_state_value=state_values,
            list_context=contexts,
            list_sensors=real_sensors,
            sim_root=ROOT_OPENDECK
        )
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(state_values)  # Should be 2 rows
        
        # Check sensor columns are present
        assert 'HPC_Tout' in result.columns
        assert 'HP_Nmech' in result.columns
        assert 'Fuel_flow' in result.columns
        assert 'LP_Nmech' in result.columns
        
        # Verify DeckSMR was called with correct ROOT
        mock_decksmr_class.assert_called_once_with(ROOT=ROOT_OPENDECK)

    def test_decksmr_1for1_length_mismatch(self, real_sensors, contexts, state_values):
        """Test that decksmr_1for1 raises ValueError when lengths don't match."""
        with pytest.raises(ValueError, match="should have the same size"):
            decksmr_1for1(
                list_state_value=[state_values[0]],  # Only 1 state
                list_context=contexts,  # 2 contexts
                list_sensors=real_sensors,
                sim_root=ROOT_OPENDECK
            )
