# Python-based Cardiovascular Hemodynamics Analysis of a Cardiac Assist Balloon

## Overview

This project presents a Python-based computational analysis pipeline for cardiovascular hemodynamics obtained from COMSOL Multiphysics simulations.

The project investigates the numerical response of a cardiac assist balloon using a coupled fluid–structure interaction (FSI) model and compares three simulation configurations.

## Simulation Cases

* **NB** — Healthy biventricular model without balloon
* **LV** — External compression of the left ventricle
* **BV** — External compression of both ventricles

## Research Questions

The analysis investigates how external cardiac assist balloon compression affects:

* Aortic and pulmonary blood flow velocity
* Aortic and pulmonary outlet pressure
* Left and right ventricular von Mises stress
* Mitral and tricuspid valve stress

The assisted configurations (LV and BV) are quantitatively compared with the healthy biventricular baseline (NB).

## Methods

The computational workflow combines COMSOL Multiphysics simulation outputs with Python-based data processing and visualization.

### Computational Workflow

1. **COMSOL Multiphysics simulation**

   * Fluid–structure interaction (FSI) modelling
   * Cardiovascular flow and structural mechanics
   * Three simulation configurations: NB, LV, and BV

2. **Data extraction**

   * Time-dependent pressure and velocity data
   * Ventricular von Mises stress
   * Mitral and tricuspid stress

3. **Python data processing**

   * Conversion of simulation outputs into structured CSV datasets
   * Numerical analysis using NumPy and Pandas
   * Calculation of mean, minimum, maximum, and relative changes

4. **Comparative analysis**

   * Comparison of LV and BV configurations against the NB baseline
   * Evaluation of hemodynamic and structural responses

5. **Visualization**

   * Generation of comparative figures using Matplotlib
   * Visualization of temporal simulation responses and key outcome metrics

### Pipeline

**COMSOL Simulation → Data Extraction → Python Processing → Quantitative Analysis → Visualization → Comparative Results**

## Key Findings

The computational comparison indicates substantial changes in flow velocity and ventricular and valvular stress across the simulated balloon-assisted configurations, while mean outlet pressures remain comparatively stable.

Relative to the NB baseline:

* **LV mean aortic velocity:** +188.5%
* **BV mean aortic velocity:** +105.4%
* **LV peak LV von Mises stress:** +281.1%
* **BV peak LV von Mises stress:** +149.8%
* **LV peak RV von Mises stress:** +192.5%
* **BV peak RV von Mises stress:** +259.3%

These values represent numerical observations from the computational model and should not be interpreted as clinical outcomes.

## Results Summary

| Metric                          |        NB |        LV |        BV |
| ------------------------------- | --------: | --------: | --------: |
| Mean aortic velocity (cm/s)     |      9.93 |     28.65 |     20.39 |
| Mean pulmonary velocity (cm/s)  |     11.89 |     26.12 |     24.80 |
| Mean aortic pressure (Pa)       | 10,781.05 | 10,646.59 | 10,731.97 |
| Mean pulmonary pressure (Pa)    |  3,760.91 |  3,707.70 |  3,709.45 |
| Peak LV von Mises stress (N/m²) |    25,388 |    96,753 |    63,423 |
| Peak RV von Mises stress (N/m²) |    25,545 |    74,723 |    91,791 |
| Peak mitral stress (N/m)        |      4.77 |     23.43 |     11.21 |
| Peak tricuspid stress (N/m)     |      0.88 |      2.12 |      3.35 |

**NB:** Healthy biventricular model without balloon
**LV:** External compression of the left ventricle
**BV:** External compression of both ventricles

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

* COMSOL Multiphysics
* Python
* NumPy
* Pandas
* Matplotlib

## Research Context

The underlying computational model was developed as part of cardiovascular biomechanics research investigating a blood-contact-free cardiac assist concept.

The Python pipeline organizes, processes, and compares numerical simulation results from the computational model.

## Project Structure

```text
cardiovascular-hemodynamics/
├── data/
│   ├── raw/
│   │   └── COMSOL_Complete_Research_Database (2).md
│   └── processed/
├── figures/
│   ├── NB_LV_BV_aortic_pressure.png
│   ├── NB_LV_BV_aortic_velocity.png
│   ├── NB_LV_BV_lv_von_mises_stress.png
│   ├── NB_LV_BV_rv_von_mises_stress.png
│   ├── NB_LV_BV_mitral_stress_x.png
│   └── NB_LV_BV_tricuspid_stress_x.png
├── src/
│   ├── data_processing.py
│   ├── extract_lv_von_mises.py
│   ├── extract_mitral_stress.py
│   ├── extract_rv_von_mises.py
│   └── extract_tricuspid_stress.py
├── analysis.py
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Reproducibility

The processed simulation datasets are stored as CSV files, while the main comparative figures are stored as PNG files.

The analysis scripts provide a reproducible workflow for processing, analyzing, and visualizing the simulation outputs.

Required Python packages are listed in `requirements.txt`.

## Project Goals

1. Extract simulation data from COMSOL reports.
2. Convert numerical results into structured datasets.
3. Analyze temporal hemodynamic responses.
4. Compare different cardiac compression configurations.
5. Generate publication-quality figures.
6. Demonstrate reproducible computational biomechanics analysis.

## Status

The main COMSOL data extraction, processing, comparative analysis, and visualization stages are complete.

The project is currently organized as a reproducible computational biomechanics portfolio project.

## Status

The main COMSOL data extraction, processing, comparative analysis, and visualization stages are complete.

The project is currently organized as a reproducible computational biomechanics portfolio project.
