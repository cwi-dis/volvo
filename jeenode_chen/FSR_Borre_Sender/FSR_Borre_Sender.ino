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

#define MAGIC 43
#define IFDEBUG if(1)
Port ports[] = {
  Port(3),
  Port(4),
  Port(1),
  Port(2)
};

#define NPORT (sizeof(ports) / sizeof(ports[0]))
#define NSENSOR NPORT

typedef struct {
  byte magic;
  byte node;
  byte lowbat;
  
  byte data[NSENSOR]; 
} Payload;

Payload payload;

void setup () {
  IFDEBUG Serial.begin(57600);
  // use the node ID previously stored in EEPROM by RF12demo
  payload.node = rf12_config();
  payload.magic = MAGIC;
  for (Port *p=ports; p < ports+NPORT; p++) {
    // Set the digital pin to output, initizalize to HIGH
    // (only needed for debugging, if this jeenode happens to
    // have a matrix circuit attached)
    p->mode(OUTPUT);
    p->digiWrite(HIGH);
    // Set the analog pin to input, disable pullup
    p->mode2(INPUT);
    p->digiWrite(LOW);
  }
}

void loop () {
  // wait for an incoming empty packet for us
  if (rf12_recvDone() && rf12_crc == 0 && rf12_len == 0 && RF12_WANTS_ACK) {
    // read battery status
    payload.lowbat = rf12_lowbat();
    IFDEBUG { if (payload.lowbat) Serial.print("LOWBAT "); }
    // read data from the analog pins and store it into the payload struct
    IFDEBUG Serial.print("poll ");
    for (int i=0; i<NPORT; i++) {
       uint16_t value = ports[i].anaRead();
       payload.data[i] = value >> 2;
       IFDEBUG Serial.print((int)value);
       IFDEBUG Serial.print(' ');
    }
    IFDEBUG Serial.println();
    // start transmission
    rf12_sendStart(RF12_ACK_REPLY, &payload, sizeof payload);  
  }
}
