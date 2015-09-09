/// @dir poller
/// Polls a number of "pollee" nodes as fast as possible to get data from them.
// 2011-11-23 <jc@wippler.nl> http://opensource.org/licenses/mit-license.php
//
// Warning: this test will flood the radio band so nothing else gets through!
//
// Maximum rates will only be achieved if all nodes 1 .. NUM_NODES are powered
// up, properly configured, and pre-loaded with the pollee.ino sketch.

#include <JeeLib.h>

const byte NUM_NODES = 2; // poll using node ID from 1 to NUM_NODES 

typedef struct {
  byte node;
  
  byte data_1; 
  byte data_2; 
  byte data_3;
  byte data_4; 
} Payload;

byte nextId;
MilliTimer timer;

void setup () {
  Serial.begin(57600);
  rf12_initialize(31, RF12_868MHZ, 80);
}

void loop () {
  // switch to next node
  if (++nextId > NUM_NODES) {
    nextId = 1;
  }
    
  // send an empty packet to one specific pollee
  rf12_sendNow(RF12_HDR_ACK | RF12_HDR_DST | nextId, 0, 0);
  // wait up to 10 milliseconds for a reply
  timer.set(10);
  
  while (!timer.poll())
    if (rf12_recvDone() && rf12_crc == 0 && rf12_len == sizeof (Payload)) {
      // got a good ACK packet, print out its contents
      const Payload* p = (const Payload*) rf12_data;

      // remap all the values into a range from 0 to 1000
      int value1 = map(p->data_1, 0, 255, 0, 1000);
      int value2 = map(p->data_2, 0, 255, 0, 1000);
      int value3 = map(p->data_3, 0, 255, 0, 1000);
      int value4 = map(p->data_4, 0, 255, 0, 1000);

      // calculate base ID
      int base_id = (((int)p->node) - 1) * 4;

      // send data out over the serial interface encoded as JSON
      Serial.print("{");
      Serial.print("\""); Serial.print(base_id + 1); Serial.print("\": "); Serial.print(value1);  Serial.print(", ");
      Serial.print("\""); Serial.print(base_id + 2); Serial.print("\": "); Serial.print(value2);  Serial.print(", ");
      Serial.print("\""); Serial.print(base_id + 3); Serial.print("\": "); Serial.print(value3);  Serial.print(", ");
      Serial.print("\""); Serial.print(base_id + 4); Serial.print("\": "); Serial.print(value4);  Serial.print(" ");
      Serial.println("}");
      
      break;
    }
}
