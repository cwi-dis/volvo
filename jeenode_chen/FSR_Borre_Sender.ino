/// @dir pollee
  //This the software we used to upload to the pollee. Each second 5 packets/per second, so that each poller has 5*25*2=250 packets/per second, and this is good for sink node to work.
/// This can run on several nodes, and get data to the central "poller" node.
// 2011-11-23 <jc@wippler.nl> http://opensource.org/licenses/mit-license.php
//
// Warning: this test will flood the radio band so nothing else gets through!
//
// To prepare for this test, you need to upload RF12demo to each pollee first,
// and set its node ID, group (77) and band (868 MHz). Node IDs must be in the 
// range 1 .. NUM_NODES, as defined in poller.ino (all nodes must be present).

#include <JeeLib.h>
#include <Ports.h>
#include <RF12.h>

Port ldr_3 (3);//setup Jeenode V6 using Port3 
Port ldr_4 (4);//setup Jeenode V6 using Port4
Port ldr_1 (1);//setup Jeenode V6 using Port1 
Port ldr_2 (2);//setup Jeenode V6 using Port2

typedef struct {
  byte node;
 byte data_1; 
 byte data_2;
  byte data_3; 
  byte data_4; 
} Payload;

Payload payload;

void setup () {
  Serial.begin(57600);
  Serial.print("\n[pollee]");
  // use the node ID previously stored in EEPROM by RF12demo
  payload.node = rf12_config();
}

void loop () {
  // wait for an incoming empty packet for us
  if (rf12_recvDone() && rf12_crc == 0 && rf12_len == 0 && RF12_WANTS_ACK) 
  {
    // invent some data to send back
    //payload.time = millis();
   payload.data_1 = ldr_1.anaRead();
   payload.data_2 = ldr_2.anaRead();
    payload.data_3 = ldr_3.anaRead();
   payload.data_4 = ldr_4.anaRead();
    // start transmission
    rf12_sendStart(RF12_ACK_REPLY, &payload, sizeof payload);
    
  }
}
