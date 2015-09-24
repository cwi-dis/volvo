FSR_Borre_Reveiver is the software that runs in the jeenode with USB that is connected to the computer.
FSR_Borre_Sender runs on the 3- or 2-sensor tiles.
FSR_Borre_MatrixSender runs on the 9-sensor tile.

For each jeenode, first flash RF12Demo and set node-ID and group-ID, which are kept in EEPROM (and used by our programs).
The receiver should have id 31.

All nodes should be set to group 80. Double-check this, Jack used group 81 for debugging.

After setting id/group flash the correct software and probably label the jeenode.

The normal senders use GND (black) and Vcc (red) on Port 1,
analog inputs on ports 1 (blue), 2 (orange) and 3 (yellow) to the resistor-board.
The resistor board connects to the FSR sensors with color codes blue (1), red (2)
and yellow (3), so using a red wire in stead of the orange (don't ask:-)

The matrix sender uses the resistor/diode board described in ../hardware.
