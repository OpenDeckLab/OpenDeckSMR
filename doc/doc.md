# Turbofan Engine

## What is a Turbofan Engine?

A **turbofan engine** is a type of jet engine widely used in modern aircraft. It combines a gas turbine core with a large fan at the front, producing thrust both from the fan and the core exhaust nozzles. The engine is composed of several main modules:

- **Fan (CmpFan):** The rotating compressing module at the front, mounted on the Low-Pressure spool, supplying air to both the bypass and core flows.
- **Booster Compressor (CmpBst):** Also mounted on the Low-Pressure spool, this compressor further compresses the core flow air coming from the fan.
- **High-Pressure Compressor (CmpH):** This compressor is mounted on the High-Pressure spool and heavily compresses the air before combustion.
- **Combustor:** Burns fuel mixed with compressed air to generate hot, high-pressure gases.
- **High-Pressure Turbine (TrbH):** Extracts energy from the hot gases to drive the high-pressure compressor.
- **Low-Pressure Turbine (TrbL):** Extracts energy to drive the booster and fan.

![
  Engine
](schema_2c2f.png)

---

## How is the turbofan engine modeled in this package?

This package simulates a turbofan engine using a *state-based* approach. The *state* describes deviations (usually denoted `deg_`) from the nominal values of efficiency and mass flow for each main module. This structure allows easy simulation of degradation or other variations in engine performance. It solves thermodynamic equations to return measurements corresponding to a state of the degradation.

The simulator distinguishes three kind of parameters: health states, context parameters and sensors parameters. Context parameters include the command which controls the engine (low-pressure spool speed for high power ratings or thrust for cruise) and the flight conditions at which the engine operates. Both are attributes of the **Context** class. The sensors are the measurements that are consequences of the previous parameters, and are found in the **Sensors** class.

### Health States
#### State Labels

Each state variable represents a deviation/delta from the nominal value for efficiency (`Eff`) or corrected mass flow (`Wc`) in a module, applied as a scaling factor to the module map. The **state labels** are:

| State Label                  | Module                 | Quantity          |
|------------------------------|------------------------|-------------------|
| deg_CmpBst_s_mapEff_in       | Booster Compressor     | Efficiency        |
| deg_CmpBst_s_mapWc_in        | Booster Compressor     | Mass Flow         |
| deg_CmpFan_s_mapEff_in       | Fan                    | Efficiency        |
| deg_CmpFan_s_mapWc_in        | Fan                    | Mass Flow         |
| deg_CmpH_s_mapEff_in         | High-Pressure Compressor | Efficiency      |
| deg_CmpH_s_mapWc_in          | High-Pressure Compressor | Mass Flow       |
| deg_TrbH_s_mapEff_in         | High-Pressure Turbine  | Efficiency        |
| deg_TrbH_s_mapWc_in          | High-Pressure Turbine  | Mass Flow         |
| deg_TrbL_s_mapEff_in         | Low-Pressure Turbine   | Efficiency        |
| deg_TrbL_s_mapWc_in          | Low-Pressure Turbine   | Mass Flow         |

The impact on component pressure ratio is calculated automatically based on the mass flow scaling factor using the slope of the running line.

#### State Bounds

State variables have predefined bounds, expressing the possible degradation or variation for each module for which the code has been preliminary tested.
These bounds are in the constants.py file.

```python
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
```
- For example:  
  - **deg_CmpFan_s_mapEff_in** can take values from -0.05 (max degradation of 5 %pt) to 0.0 (nominal).
  - **deg_CmpFan_s_mapWc_in** goes from -0.05 to +0.03, etc.

---
### **Context**

A **Context** represents the operational environment in which the OpenDeckSMR system is running, primarily defined by its *flight condition*.  
The `ContextDeckSMR` class acts as a container, associating a context name (such as "Cruise 1" for a cruise operating point) with a specific instance of `FlightCondDeckSMR`.  
A context thus encapsulates all the necessary information to accurately reproduce the engine's scenario during simulation or analysis, and can be extended in the future to include additional factors like weather, pollution, and other relevant data.

The information in a *flight condition* are:
- **PHASE_TYPE** (`str`): The flight phase or engine throttle position, to choose between `MTO` for the take-off rating, `MCL` for max-climb and `CR` for cruise.
- **DTAMB** (`float`): Delta to Standard Ambient Temperature (in K). This represents the difference between the current ambient temperature and the standard atmospheric temperature at the given altitude.
- **ALT** (`float`): Altitude (in ft).
- **MACH** (`float`): Aircraft flight Mach Number.
- **COMMAND** (`float`): The required thrust (in lbf), only used for the cruise condition.

Please note that the **COMMAND** variable is only used to define the required thrust for the cruise `CR` condition.
The take-off `MTO` and climb `MCL` conditions do not use this variable as they calculate their thrust value based on a flat-rating power management logic.

The user can define their own operating contexts and flight conditions in the following manner:
```python
from odsmr.context import  FlightCondDeckSMR, ContextDeckSMR

user_defined_take_off_context = ContextDeckSMR(
  name="takeoff_point_1",
  flight_condition=FlightCondDeckSMR(
    DTAMB=15,
    ALT=0,
    MACH=0.15,  
    COMMAND=120000, # not used
    PHASE_TYPE="MTO"
    )
  )
```

Otherwise, the code comes with the following predefined standard **operating contexts**, representative of typical engine snapshots:

- `CRUISE`
- `CLIMB1`
- `CLIMB2`
- `TAKEOFF`

These can be simply imported from the `predefined_flight_conditions.py` and are ready to use, as shown below:
```python
from odsmr.predefined_flight_conditions import Cruise_DeckSMR, Takeoff_DeckSMR, Climb1_DeckSMR, Climb2_DeckSMR
```
Furthermore, each predefined context has corresponding flight condition parameter bounds (also included in the `constants.py` file),
that can be used to change their values. For example, for cruise:

| Variable               | Range          | Description                                                    |
|------------------------|----------------|----------------------------------------------------------------|
| DTAMB                  | 9.0 – 11.0     | Ambient temperature deviation from ISA (K)                     |
| ALT                    | 34,900 – 35,100| Altitude (ft)                                                  |
| MACH                   | 0.76 – 0.80    | Mach number                                                    |
| COMMAND                | 24,900 – 25,100| Thrust command (lbf)                                 |

Bounds are only used with the provided sampling functions (`sample_from_bounds`) to generate random flight conditions, as shown below:
```python
from odsmr.context import  FlightCondDeckSMR, ContextDeckSMR
from odsmr.helpers import sample_from_bounds
from odsmr.constants import FLIGHT_CONDITIONS_BOUNDS

# Define a random take-off context:
fc = sample_from_bounds(FLIGHT_CONDITIONS_BOUNDS["TAKEOFF"])

random_takeoff_context = ContextDeckSMR(
  name="Sampled_takeoff_point",
  flight_condition=FlightCondDeckSMR(
      DTAMB=fc["DTAMB"],
      ALT=fc["ALT"], 
      MACH=fc["MACH"],  
      COMMAND=fc["COMMAND"],
      PHASE_TYPE="MTO"
  )
)
```

All the above can be combined in a single list of contexts:
```python
list_context = [user_defined_take_off_context, Takeoff_DeckSMR, random_takeoff_context]
```
Generally speaking, the user can define their own additional contexts and corresponding bounds if they wish to, but there is no guarantee that the code will produce acceptable results for any condition given.

**Summary:**  
> A *flight condition* precisely describes the physical situation of the engine; a *context* groups this condition under a descriptive name, offering a broader operational framework for analysis or simulation. For now, the *context* has no other attributes, but this could evolve in future versions of the package.
---

### **Sensors**

The package defines a list of simulated sensors measuring key engine variables, such as:

- `HPC_Tout` – High-Pressure Compressor outlet temperature in K
- `HP_Nmech` – High-Pressure shaft rotational speed in rpm
- `HPC_Tin` – High-Pressure Compressor inlet temperature in K
- `LPT_Tin` – Low-Pressure Turbine inlet temperature in K
- `LPT_Tout` – Low-Pressure Turbine outlet temperature in K
- `Fuel_flow` – Fuel flow rate in kg/s
- `HPC_Pout_st` – High-Pressure Compressor outlet static pressure in Pa
- `LP_Nmech` – Low-Pressure shaft rotational speed (power management control variable) in rpm

The sensors for which the measurement output is required by the engine simulation should be imported from the `sensors.py` module and compiled to a list that will be fed to the simulator function (explained further on in this guide). Example:
```python
from odsmr.sensors import HPC_Tout, HP_Nmech, HPC_Tin, LPT_Tin, Fuel_flow, HPC_Pout_st, LP_Nmech

list_sensors = [ HPC_Tout(), HP_Nmech(), HPC_Tin(), LPT_Tin(), Fuel_flow(), HPC_Pout_st(), LP_Nmech()]
```

## Simulation functions

The `generation_functions.py` module defines two functions for calling the engine simulator:
- `decksmr_1for1` calls the simulator with a list of contexts and a corresponding list of health states (one-to-one correspondance between the two). The simulator will run for each respective line of the two lists and produce a dataframe of results, containing the context information, health-states and the list of required engine sensor measurements (also given as argument to the function).
- `decksmr_1forall` calls the simulator on the cross-product of all combinations between the provided list of contexts and list of health states. The simulator will run for each resulting combination and produce a dataframe of results, containing the context information, health-states and the list of required engine sensor measurements.

Below, we provide a very minimal example of calling the simulator for one user provided operating context:
```python
from odsmr.context import  FlightCondDeckSMR, ContextDeckSMR
from odsmr.sensors import HPC_Tout, HP_Nmech, HPC_Tin, LPT_Tin, Fuel_flow, HPC_Pout_st, LP_Nmech
from odsmr.generation_functions import decksmr_1forall
from odsmr.constants import ROOT_OPENDECK

# We define a list of sensors:
list_sensors = [
  HPC_Tout(),
  HP_Nmech(),
  HPC_Tin(),
  LPT_Tin(),
  Fuel_flow(),
  HPC_Pout_st(),
  LP_Nmech()
  ]

# We define a list of one operating context/flight condition
list_context = [
  ContextDeckSMR(
    name="takeoff_point_1",
    flight_condition=FlightCondDeckSMR(
      DTAMB=15,
      ALT=0,
      MACH=0.15,  
      COMMAND=120000, # not used
      PHASE_TYPE="MTO"
      )
    )
]

# Define a list of one health state, for example a perfectly healthy engine:
list_of_state_values = [np.zeros(10)]

# Run the engine simulation
all_info_df = decksmr_1forall(list_state_value=list_of_state_values,
                        list_context=list_context,
                        list_sensors=list_sensors, sim_root=ROOT_OPENDECK)

print(all_info_df.shape)

# Dataframe contains the values of the sensors for one health state at the asked context
all_info_df.head()
```

## Note on "Convergence" variable

The proposed simulator solves thermodynamic equations with a non-linear solver.
In consequence, it can happen that the algorithm either does not converge on a solution or does return a solution, but
outside the valid operating bounds. In both cases, the output variable called `Convergence` will
explain what happened.

## Tutorials
Head to the example notebooks to the get a better idea of how to use the engine simulator!
