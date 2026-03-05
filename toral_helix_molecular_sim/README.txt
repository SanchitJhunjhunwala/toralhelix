
Toral Helix Molecular Simulation Package
========================================

Contents
--------
helix_molecular_sim.py

Description
-----------
Simulates two molecular strands modeled as toral helices undergoing
Brownian motion and weak Lennard-Jones interactions.

Goal:
Estimate how geometric proximity increases residence time and
binding probability for enzyme-like locking events.

Usage
-----
1. Install dependencies:

   pip install numpy matplotlib

2. Run:

   python helix_molecular_sim.py

Output
------
- Prints number of detected binding events
- Displays a plot of minimum distance between strands over time

Extension Ideas
---------------
- Add enzyme particles diffusing in the field
- Produce catalytic probability phase diagrams
- Extend to three interacting helices
- Add spectral resonance analysis
