"""
Unit tests for context.
"""
import pytest
from odsmr.context import FlightCondDeckSMR, ContextDeckSMR

def test_flight_condition_validation():
    """Test FlightCondDeckSMR validation."""
    # Test valid creation
    fc = FlightCondDeckSMR("CR", 10.0, 35000, 0.78, 25000.0)
    assert fc.PHASE_TYPE == "CR"
    
    # Test invalid cases
    with pytest.raises(TypeError):
        FlightCondDeckSMR(123, 10.0, 35000, 0.78, 25000.0)  # PHASE_TYPE not string
        
    with pytest.raises(ValueError):
        FlightCondDeckSMR("CR", 10.0, -1000, 0.78, 25000.0)  # Negative altitude
        
    with pytest.raises(ValueError):
        FlightCondDeckSMR("CR", 10.0, 35000, -0.5, 25000.0)  # Negative Mach

def test_context_creation():
    """Test ContextDeckSMR creation and validation."""
    fc = FlightCondDeckSMR("CR", 10.0, 35000, 0.78, 25000.0)
    
    # Valid context
    ctx = ContextDeckSMR("test", fc)
    assert ctx.name == "test"
    assert ctx.flight_condition == fc
    
    # Default name
    ctx2 = ContextDeckSMR(flight_condition=fc)
    assert ctx2.name == "DefaultName"
    
    # Invalid cases
    with pytest.raises(ValueError):
        ContextDeckSMR("test", None)  # No flight condition
        
    with pytest.raises(TypeError):
        ContextDeckSMR("test", "not_a_flight_condition")