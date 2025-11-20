# OpenDeckSMR

## Description
This repository contains the code for a generic/hypothetic and free aircraft engine simulator.
It contains all the necessary functions to generate engine measurement data for given health indicators and flight conditions.

Currently, the software functions only in Linux environments; a windows version will be added in the future.

## Installation
```bash
git clone TBD OpenDeckSMR
cd OpenDeckSMR
pip install -e .
```

## Usage
Please check the [documentation](doc/doc.md) and example notebooks for more information ([StepByStep](notebooks/Demo_StepByStep.ipynb), [DemoGeneration1](notebooks/Demo_1forall_generation.ipynb), [DemoGeneration2](notebooks/Demo_1for1_generation.ipynb)).

## Support
Please create an issue in this repository.

## Original authors
+ Safran SA / Safran Tech (P. Giannakakis, S. Razakarivony, S. Thepaut, D. Q. Vu)
+ Aristotle University of Thessaloniki / Laboratory of Fluid Mechanics and Turbomachinery (M. Psaropoulos, V. Gkoutzamanis, A. Kalfas)

## Acknowledgements
The executable was made with the [PROOSIS(c) simulation platform](https://www.ecosimpro.com/products/proosis/), developed by Empresarios Agrupados Internacional, S.A..

The component maps used for this model have been kindly provided by:
- [Dr. Joachim Kurzke](https://www.kurzke-consulting.de/)
- [GasTurb GmbH](https://www.gasturb.com/)

Special thanks to Dr. Kurzke for his advice with regards to the choice of the appropriate component maps.

## License
License Creative Commons CC-BY-NC-ND
(Attribution, Non Commercial Use, No modification)

Don't forget to check the [Disclaimer](DISCLAIMER.md)

## Project status
Alpha version.
