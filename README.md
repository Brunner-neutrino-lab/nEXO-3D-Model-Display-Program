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
7. [Data Simulation](#data-simulation)
8. [Usage](#usage)
9. [Acknowledgments](#acknowledgments)

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

- Raspberry Pi (User: pi,  Pass: Element54$)
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
   - Schematics for the Raspberry Pi HAT and inside the model are found in the 'Schematics' folder.


4. **Software Installation**:
  - Assignment of GPIO pins for LEDS:
      - wallGPIO = 17 #physical/board pin 11
      - floorGPIO = 27 #physical/board pin 13
      - redGPIO = 9 #physical/board pin 21
      - greenGPIO = 11 #physical/board pin 23
      - blueGPIO = 25 #physical/board pin 22
  - The program to display the LEDs is found in the file 'LED_program.py'
  - 'Test.py' was only used to store the RGB values for the TPC colours.
      - in the 'Schematic' folder the LED colour assignment to events is found.


## Data Simulation
General approach: calculate the mean/expected time between events (for our time scale of 2 min = 10 years), then randomly sample the time between LED flashes using an exponential distribution (distribution for time between Poisson events). We have the option
 to vary the half-life of 0vbb as well as the LXe volume (inner 2t or inner 1t). 

The TPC will be flashed different colours for 5 different events in the ROI (the ROI is SS events, with energy within 0vbb FHWM): 
  - 0vbb
  - 2vbb
  - solar v
  - Xe-137 activations
  - and the remaining background events. 

0vbb: Mean number of decays per year is calculated based on the mean lifetime (half-life divided by log(2)), assuming 76.1% of events are in the ROI (as FHWM is approximately 76.1% of area under Gaussian distribution). 

  - 3 sigma discovery potential half-life: 7.4 x 10^27 years (https://iopscience.iop.org/article/10.1088/1361-6471/ac3631/pdf)   
  - Half-life sensitivity: 1.35 × 10^28 years
  - Our third option is currently 1 x 10^27 years.

Total background rate (https://arxiv.org/abs/1805.11142v2, table 3.1):  
  - Inner 2 tons: 3.6 × 10^−4 events/(FWHM·kg·yr)  
  - Inner 1 ton: 1.4 × 10^−4 events/(FWHM·kg·yr)  

Events in the background are separated into 2vbb, solar v, Xe-137 and remaining background according to the composition within FWHM for the inner 2t (https://iopscience.iop.org/article/10.1088/1361-6471/ac3631/pdf, estimated from Fig. 8):  
  - 2vbb: 0.8%  
  - Solar v: 2.1%  
  - Xe-137: 2.4%   
  - Rest of background: 94.7%  

The outer detector (walls and floor) will be flashed for muons (these rates may have to be scaled differently as they are very high with our time scale; currently the lights just stay on):  
  - Muons through TPC: about 0.6 per day 
  - Muons through outer cryostat: about 5 per day 

## Usage

1. **Start the Visualization**:
   - Run the main control script: (not finished yet)

2. **Interacting with the Model**:
   - The LEDs will display different data sets including muons, 2vbb, 0vbb, ROI background data, and Xenon 137 data.
   - There will be an option to view the data from the inner 1 tonne as well as the inner 2 tonne of the detector.
   - Observe the visualization of the estimated rate of neutrino-less double beta decay and its half-lives.
3. **Connecting over SSH**
   - pi must be connected to the same network as device (ethernet/internet)
   - type into terminal 'ssh pi@[pi IP address]'
   - if displaying on touchscreeen you have to define the display enviroment (the screen is just DISPLAY=:0) before the command
     - ex. DISPLAY=:0 gui.py
     - ex. sudo DISPLAY=:0 LEDs.py

## Acknowledgments

This project is developed for the nEXO collaboration's Director's Review.
