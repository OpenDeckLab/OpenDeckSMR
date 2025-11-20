"""
Tests for DeckSMR wrapper.
"""

import pytest
import pandas as pd
from unittest.mock import patch, Mock
from odsmr.wrapping import DeckSMR, get_key_value
from odsmr.constants import ROOT_OPENDECK


class TestDeckSMR:

    def test_get_key_value(self):
        """Test helper function get_key_value."""
        data = {"a": 1.5, "b": 2.0}
        assert get_key_value(data, "a") == 1.5
        assert get_key_value(data, "missing") == 0.0
        assert get_key_value(data, "missing", 5.0) == 5.0
    
    def test_decksmr_init(self):
        """Test DeckSMR initialization."""
        # Valid init
        simulator = DeckSMR(ROOT_OPENDECK)
        assert simulator.ROOT == ROOT_OPENDECK
        assert isinstance(simulator.RAWKDATA, pd.DataFrame)
        assert "MTO" in simulator.RAWKDATA.index
        
        # Invalid init
        with pytest.raises(ValueError, match="You should have set a root name"):
            DeckSMR(None)
    
    @patch('odsmr.wrapping.subprocess.run')
    def test_simulation_basic(self, mock_subprocess):
        """Test basic simulation run."""
        # Mock subprocess output
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = """
        Convergence:True
        Fuel_flow:0.45
        HPC_Tout:750.5
        HP_Nmech:15500.0
        Thrust:25000.0
        """
        mock_subprocess.return_value = mock_result
        
        # Run simulation
        simulator = DeckSMR("/fake/path")
        inputs = [{"PHASE_TYPE": "CR", "ALT": 35000, "DTAMB": 10.0, "MACH": 0.78, 
                  "COMMAND": 25000.0}]
        params = [{"deg_CmpBst_s_mapWc_in": 0.1}]
        
        result = simulator.run_simulation_multi_parameters(inputs, params)
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert "Fuel_flow" in result.columns
        assert "Convergence" in result.columns
        assert result.iloc[0]["Fuel_flow"] == 0.45
    
    def test_length_mismatch(self):
        """Test error when inputs/params lengths don't match."""
        simulator = DeckSMR(ROOT_OPENDECK)
        inputs = [{"PHASE_TYPE": "CR", "ALT": 35000, "DTAMB": 10.0, "MACH": 0.78, 
                  "COMMAND": 25000.0}]
        parameters = [
        {},
        {}
        ]
        with pytest.raises(ValueError, match="len of inputs & parameters not matching"):
            simulator.run_simulation_multi_parameters(inputs, parameters)