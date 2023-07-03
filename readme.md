# Volvo Design Challenge 

This repository contains software and instructions for the exhibit entered into the Volvo Design Challenge 2015 by ByBorre, with help from the CWI DIS group.

Here is a video of Borre Akkersdijk explaining the vision behind it:

[Sublime News - Volvo Design Challenge - ByBorre (YouTube)](https://youtu.be/kw6YL740Hyo)

From May 2017 until June 2023 the exhibit wass on display in the Atrium at CWI. It was dismantled and put into storage, some instructions on re-assembling it if you happen to have the hardware are in [hwsetup/readme.md](hwsetup/readme.md).

Here is an image of the exhibit on display at CWI:

![volvo-exhibit-cwi](https://www.cwi.nl/images/14228/spring_school_dis_4.width-768.jpg)

Contents:

- **hwsetup** contains minimal instructions to revive the piece. See [hwsetup/readme.md](hwsetup/readme.md).

- **production** contains the hardware and software as originall built in 2017:
	- [production/readme.txt](production/readme.txt) has terse instructions on putting everything together.
	- **production/hardware** has the schematics for the matrix touch sensor (for the volume-like pad).
	- **production/jeenode** has software for the three types of JeeNode boards: the receiver, the 4-pad sender and the matrix sender.
	- **production/receiver** has the Python script that communicates with the jeenode receiver.
	- **production/server** has the web server that connects the receiver and the visualisation.
	- There are various scripts here to run everything.
- **artwork** contains the artwork for the visualisation, see [artwork/readme.txt](artwork/readme.txt) for details.
- **jeenode_test** is an Arduino program to test the matrix-style touch interface.
- **photon_experiment** is an earlier touch experiment using a Particle Photon.
