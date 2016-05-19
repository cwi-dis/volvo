#!/bin/bash
autossh -f -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R 19022:localhost:22  -N dis@flauwte.dis.cwi.nl
