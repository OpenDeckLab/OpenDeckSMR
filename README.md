# OpenDeckSMR

## Description
This repository contains the code for a generic/hypothetic and free aircraft engine simulator.
It contains all the necessary functions to generate engine measurement data for given health indicators and flight conditions.

Currently, the software functions only in Linux environments; a windows version will be added in the future.

## Installation
```bash
git clone https://github.com/OpenDeckLab/OpenDeckSMR.git OpenDeckSMR
cd OpenDeckSMR
pip install -e .
```

## Usage
Please check the [documentation](doc/doc.md) and example notebooks for more information ([StepByStep](notebooks/Demo_StepByStep.ipynb), [DemoGeneration1](notebooks/Demo_1forall_generation.ipynb), [DemoGeneration2](notebooks/Demo_1for1_generation.ipynb)).

## Target users and applications
OpenDeckSMR is designed for researchers, engineers, and students working in the fields of health monitoring and digital twin development. The simulator provides a flexible code for generating synthetic engine measurement data under various flight conditions and health states, making it particularly useful for algorithm development, validation, and benchmarking in areas such as fault detection, prognostics, and condition-based maintenance. The expected outcome is to enable users to experiment with realistic datasets without requiring access to proprietary engine models or costly test benches, fostering innovation and collaboration in the aerospace community.

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
License Creative Commons [CC-BY-NC-ND](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)
(Attribution, Non Commercial Use, No modification)

Don't forget to check the [Disclaimer](DISCLAIMER.md)

## Project status
Alpha version.

## How to cite us ?
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17804895.svg)](https://doi.org/10.5281/zenodo.17804895)

