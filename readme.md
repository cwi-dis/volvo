# Volvo Design Challenge 

This repository contains software and instructions for the exhibit entered into the Volvo Design Challenge 2015 by ByBorre, with help from the CWI DIS group.

As of this writing (May 2017) the exhibit is on display in the Atrium at CWI.

Contents:

- **production** contains the hardware and software as currently in use:
	- [production/readme.txt](production/readme.txt) has terse instructions on putting everything together.
	- **production/hardware** has the schematics for the matrix touch sensor (for the volume-like pad).
	- **production/jeenode** has software for the three types of JeeNode boards: the receiver, the 4-pad sender and the matrix sender.
	- **production/receiver** has the Python script that communicates with the jeenode receiver.
	- **production/server** has the web server that connects the receiver and the visualisation.
	- There are various scripts here to run everything.
- **artwork** contains the artwork for the visualisation, see [artwork/readme.txt](artwork/readme.txt) for details.
- **jeenode_test** is an Arduino program to test the matrix-style touch interface.
- **photon_experiment** is an earlier touch experiment using a Particle Photon.
