Read a lot of pressure sensors using one Particle Photon.

Sensors are in a matrix, with a diode to decould them. See
schematic.jpg for a hardware diagram.

Each row is enabled in turn (using a digital pin pulled to ground),
and then each of the sensors for that row is read (using an analog pin).
Then we advance the row, and when we've read all we store the data in the cloud.
We've seen about 10 sets of 64 readings per second.

sensors2cloud.ino runs on the Photon. Adjust rowPins and
columnPins to the number of sensors.

sensorfromcloud.sh shows how to get the data form the cloud.

You'll need to adapt the device ID and access key.


