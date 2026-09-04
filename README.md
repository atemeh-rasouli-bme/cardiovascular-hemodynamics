# Python-based Cardiovascular Hemodynamics Analysis of a Cardiac Assist Balloon

## Overview

This project presents a Python-based analysis pipeline for cardiovascular hemodynamics obtained from COMSOL Multiphysics simulations.

The project investigates the effect of an external cardiac assist balloon on ventricular hemodynamics using a coupled fluid–structure interaction (FSI) model.

## Simulation Cases

- **NB** — Healthy biventricular model without balloon
- **LV** — External compression of the left ventricle
- **BV** — External compression of both ventricles

## Main Outputs

The analysis focuses on:

- Aortic and pulmonary outlet velocity
- Aortic and pulmonary outlet pressure
- Left and right ventricular von Mises stress
- Mitral and tricuspid stress
- Quantitative comparison between NB, LV, and BV configurations
## Key Figures

### Aortic Velocity

![Aortic velocity comparison](figures/NB_LV_BV_aortic_velocity.png)

### Aortic Outlet Pressure

![Aortic pressure comparison](figures/NB_LV_BV_aortic_pressure.png)

### Left Ventricular Von Mises Stress

![LV von Mises stress comparison](figures/NB_LV_BV_lv_von_mises_stress.png)

### Right Ventricular Von Mises Stress

![RV von Mises stress comparison](figures/NB_LV_BV_rv_von_mises_stress.png)

### Mitral Valve Stress

![Mitral stress comparison](figures/NB_LV_BV_mitral_stress_x.png)

### Tricuspid Valve Stress

![Tricuspid stress comparison](figures/NB_LV_BV_tricuspid_stress_x.png)

## Tools

- COMSOL Multiphysics
- Python
- NumPy
- Pandas
- Matplotlib
- CSV-based data processing

## Research Context

The underlying computational model was developed as part of cardiovascular biomechanics research investigating a blood-contact-free cardiac assist concept.

The Python pipeline is used to organize, process, and compare numerical simulation results.

## Key Findings

The comparative analysis shows that balloon assistance substantially alters ventricular and valvular stress and flow velocity, while outlet pressures remain comparatively stable across the simulated configurations.

Compared with the baseline NB case:

- LV mean aortic velocity increased by approximately **188.5%**
- BV mean aortic velocity increased by approximately **105.4%**
- LV peak LV von Mises stress increased by approximately **281.1%**
- BV peak LV von Mises stress increased by approximately **149.8%**
- LV peak RV von Mises stress increased by approximately **192.5%**
- BV peak RV von Mises stress increased by approximately **259.3%**

These results represent numerical observations from the computational model and should not be interpreted as clinical outcomes.

## Project Goals

1. Extract simulation data from COMSOL reports.
2. Convert raw numerical results into structured datasets.
3. Analyze temporal hemodynamic responses.
4. Compare different cardiac compression strategies.
5. Generate publication-quality figures.
6. Demonstrate reproducible computational biomechanics analysis.

## Project Structure

cardiovascular-hemodynamics/
├── data/
│   ├── raw/
│   │   └── COMSOL_Complete_Research_Database (2).md
│   └── processed/
├── src/
│   ├── data_processing.py
│   ├── extract_lv_von_mises.py
│   ├── extract_mitral_stress.py
│   ├── extract_rv_von_mises.py
│   └── extract_tricuspid_stress.py
├── analysis.py
├── dashboard.py
├── requirements.txt
└── README.md

## Reproducibility

The processed datasets are stored as CSV files, while the generated comparative figures are stored as PNG files.

The analysis scripts provide a reproducible workflow for processing and visualizing the simulation outputs.

## Status

The main COMSOL data extraction, processing, comparative analysis, and visualization stages are complete.

The project is currently organized as a reproducible computational biomechanics portfolio project.