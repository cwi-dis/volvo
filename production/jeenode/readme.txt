FSR_Borre_Reveiver is the software that runs in the jeenode with USB that is connected to the computer.
FSR_Borre_Sender runs on the 3- or 2-sensor tiles.
FSR_Borre_MatrixSender runs on the 9-sensor tile.

For each jeenode, first flash RF12Demo and set node-ID and group-ID, which are kept in EEPROM (and used by our programs).
The receiver should have id 31, the MtrixSender should have a higher ID than all other senders
(because board N transmits is sensors as numbers 4(N-1), 4(N-1)+1, 4(N-1)+2).
All nodes should be set to group 80.

After setting id/group flash the correct software and probably label the jeenode.

The normal senders use analog inputs on ports 1, 2 and 3, sensor to Vcc and a 1Kohm pulldown to ground.
The matrix sender uses the hardware described in ../hardware.