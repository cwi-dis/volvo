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

//
// Power saving features. #undef to disable
//
#define POWERSAVETIMEOUT 10000    // Go to sleep after 10 seconds of no polls received
#define POWERSAVEDURATION 60000   // Go to sleep for 60 seconds
#undef NAP_AFTER_POLL 40  // Nap for 15ms after a poll

#ifdef POWERSAVETIMEOUT 
unsigned long lastReceptionTime;

ISR(WDT_vect) { Sleepy::watchdogEvent(); }

#endif

#define NROW 3
#define NCOLUMN 3
#define NPORT 3 /* max(NROW, NCOLUMN) */
#define NSENSOR (NROW*NCOLUMN)

Port ports[] = {
  Port(1),
  Port(2),
  Port(3)
};

typedef struct {
  byte magic;
  byte node;
  byte lowbat;
  byte data[NSENSOR]; 
} Payload;

Payload payload;

void setup () {
  IFDEBUG Serial.begin(57600);
  IFDEBUG Serial.println("MatrixSender started");
  // use the node ID previously stored in EEPROM by RF12demo
  payload.node = rf12_config();
  payload.magic = MAGIC;
  for (Port *p=ports; p < ports+NPORT; p++) {
  	// Set the digital pin to output, initizalize to HIGH
  	p->mode(OUTPUT);
    p->digiWrite(HIGH);
    // Set the analog pin to input, disable pullup
    p->mode2(INPUT);
    p->digiWrite(LOW);
  }
#ifdef POWERSAVETIMEOUT
  lastReceptionTime = millis();
#endif

}

void loop () {
  // wait for an incoming empty packet for us
  if (rf12_recvDone() && rf12_crc == 0 && rf12_len == 0 && RF12_WANTS_ACK) {
    // read battery status
    payload.lowbat = rf12_lowbat();
    IFDEBUG { if (payload.lowbat) Serial.print("LOWBAT "); }
    // read data from the analog pins and store it into the payload struct
#ifdef POWERSAVETIMEOUT
    lastReceptionTime = millis();
#endif
    IFDEBUG Serial.print("poll ");
    int i = 0;
    for (int row=0; row<NROW; row++) {
      // Enable this row of sensors
      ports[row].digiWrite(LOW);
      // Not needed? delay(10);
      for (int col=0; col < NCOLUMN; col++) {
      	// It is suggested to discard one analog reading to stabilize
      	// the ADC
        uint16_t value; //  = ports[col].anaRead();
        value = ports[col].anaRead();
        payload.data[i++] = (1023-value) >> 2;
        IFDEBUG Serial.print((int)value);
        IFDEBUG Serial.print(' ');
      }
      ports[row].digiWrite(HIGH);
    }
    IFDEBUG Serial.println();
    // start transmission
    rf12_sendStart(RF12_ACK_REPLY, &payload, sizeof payload);
#ifdef NAP_AFTER_POLL
    rf12_sendWait(1);   // Wit for transmission completion with CPU in IDLE mode
    rf12_sleep(RF12_SLEEP);
    Sleepy::loseSomeTime(NAP_AFTER_POLL);
    rf12_sleep(RF12_WAKEUP);
 #endif 
  }
#ifdef POWERSAVETIMEOUT
  else {
    if (millis() > lastReceptionTime + POWERSAVETIMEOUT) {
      IFDEBUG { Serial.println("Sleep"); delay(10); }
      rf12_sleep(RF12_SLEEP);
      Sleepy::loseSomeTime(POWERSAVEDURATION);
      rf12_sleep(RF12_WAKEUP);
      lastReceptionTime = millis();
      IFDEBUG Serial.println("Wakeup");
    }
  }
#endif

}
