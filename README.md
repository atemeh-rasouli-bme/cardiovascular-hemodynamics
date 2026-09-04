# Python-based Cardiovascular Hemodynamics Analysis of a Cardiac Assist Balloon

## Overview

This project presents a Python-based analysis pipeline for cardiovascular hemodynamics obtained from COMSOL Multiphysics simulations.

The project investigates the effect of an external cardiac assist balloon on ventricular hemodynamics using a coupled fluid–structure interaction (FSI) model.

## Simulation Cases

* **NB** — Healthy biventricular model without balloon
* **LV** — External compression of the left ventricle
* **BV** — External compression of both ventricles

## Main Outputs

The analysis focuses on:

* Outlet velocity
* Outlet pressure
* Myocardial von Mises stress
* Comparison between NB, LV, and BV configurations

## Tools

* COMSOL Multiphysics
* Python
* NumPy
* Pandas
* Matplotlib
* CSV-based data processing

## Research Context

The underlying computational model was developed as part of cardiovascular biomechanics research investigating a blood-contact-free cardiac assist concept.

The Python pipeline is used to organize, process, visualize, and compare the numerical simulation results.

## Project Goals

1. Extract simulation data from COMSOL reports.
2. Convert raw numerical results into structured datasets.
3. Analyze temporal hemodynamic responses.
4. Compare different cardiac compression strategies.
5. Generate publication-quality figures.
6. Demonstrate reproducible computational biomechanics analysis.

## Status

Data collection from the COMSOL simulations is complete.

The next stage is automated data processing and generation of comparative figures for the NB, LV, and BV cases.
