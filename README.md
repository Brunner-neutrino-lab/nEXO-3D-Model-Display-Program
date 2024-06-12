# nEXO 3D Model and Display

## Overview

This project showcases a scaled-down, 3D-printed model of the nEXO detector, designed to visualize various data related to muon interactions and double beta decay events. The model is created using SolidWorks and powered by a Raspberry Pi, enabling interactive LED displays and simulated data visualization. This project aims to present condensed data from ten years of observation, highlighting the rarity of neutrino-less double beta decay.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Features](#project-features)
3. [Responsabilities](#responsabilities)
4. [Hardware Components](#hardware-components)
5. [Software Components](#software-components)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Acknowledgments](#acknowledgments)

## Introduction

The nEXO detector is part of an experiment projected to detect neutrino-less double beta decay. Our project involves creating a scaled-down 3D model of the detector to visualize simulated muon data and rare decay events in an engaging and informative manner.

## Project Features

- **True-to-Scale 3D Model**: Created in SolidWorks, scaled down by a factor of 100, and optimized for 3D printing.
- **Simulated Data Visualization**:
  - Muons passing through the TPC (Time Projection Chamber).
  - Muons passing through the outer detector.
  - Coincident muons passing through both the TPC and outer detector.
  - Background Region of Interest (ROI) data.
  - Xenon 137 data.
  - Estimated rate of neutrino-less double beta decay.
- **Interactive LED Display**: Powered by a Raspberry Pi, the LED display will showcase multiple half-lives of the decay to highlight its rarity.
- **Condensed Time Frame**: Displaying ten years of data in a two-minute visualization.

## Responsabilities

1. 3D model and printing
- Grace,Felix, Eliot
2. Hardware
- Tania, Julien, Felix 
3. Programming
- Sophie, Emilio, Kavin

Brian is advising the programming and hardware

## Hardware Components

- Raspberry Pi (User: pi  Pass: Element54$)
- 3D-printed model of the nEXO detector
- LEDs (Blue for walls, RGB for TPC)
- Power supply
- Current-limiting resistors
- Transistors

## Software Components

- SolidWorks for 3D modeling
- Python for controlling the Raspberry Pi and LEDs
- Data from previous simulation scripts for muon and decay events

## Setup and Installation

1. **3D Printing**:
   - Use the SolidWorks files provided in the [sharepoint](https://mcgill.sharepoint.com/:f:/s/BrunnerNeutrinoLabModels_Group/EvGFXZofQUZPt6qD_oMlr6YBIfcuM76ZlL9AQwnTyHu-Tg?e=94aHd1) to print the scaled-down model of the nEXO detector.
   
2. **Hardware Assembly**:


3. **Software Installation**:


4. **Data Simulation**:

## Usage

1. **Start the Visualization**:
   - Run the main control script: (not finished yet)

2. **Interacting with the Model**:
   - The LEDs will display different data sets including muons, ROI background data, and Xenon 137 data.
   - Observe the visualization of the estimated rate of neutrino-less double beta decay and its half-lives.

## Acknowledgments

This project is developed for the nEXO collaboration's Director's Review.
