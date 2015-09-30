/// @dir poller
/// Polls a number of "pollee" nodes as fast as possible to get data from them.
// 2011-11-23 <jc@wippler.nl> http://opensource.org/licenses/mit-license.php
//
// Warning: this test will flood the radio band so nothing else gets through!
//
// Maximum rates will only be achieved if all nodes 1 .. NUM_NODES are powered
// up, properly configured, and pre-loaded with the pollee.ino sketch.

#include <JeeLib.h>

const byte NUM_NODES = 9; // poll using node ID from 1 to NUM_NODES 

#define MAGIC 43  // Magic number that signals an ACK comes from our sensors

#define POLL_TIMEOUT 20  // How many milliseconds to wait for poll reply
#define MAX_POLL_FREQ 10  // Poll sensors at most 25 times per second
#ifdef MAX_POLL_FREQ
// If the poll frequency is maximised the sensors can powerdown
// after a poll, because they know they will not be polled again for a
// certain time
#define MIN_POLL_INTERVAL (1000/MAX_POLL_FREQ)
uint32_t nextPollCycleTime;
#endif // MAX_POLL_FREQ

#define IFDEBUG if(0)

typedef struct {
  byte magic;
  byte node;
  byte lowbat;
  
  byte data[0]; 
} Payload;

byte nextId;
MilliTimer timer;

void setup () {
  Serial.begin(57600);
  //rf12_initialize(31, RF12_868MHZ, 80);
  rf12_config();
}

void loop () {
  // switch to next node
  if (++nextId > NUM_NODES) {
    nextId = 1;
#ifdef MAX_POLL_FREQ
    // Go to sleep until the next poll cycle can be started
    uint64_t now = millis();
    if (now < nextPollCycleTime) {
      delay(nextPollCycleTime - now);
      now = millis();
    }
    nextPollCycleTime = now+MIN_POLL_INTERVAL;
#endif
  }
    
  // send an empty packet to one specific pollee
  rf12_sendNow(RF12_HDR_ACK | RF12_HDR_DST | nextId, 0, 0);
  // wait up to 10 milliseconds for a reply
  timer.set(POLL_TIMEOUT);
  
  while (!timer.poll()) {
    if (rf12_recvDone() && rf12_crc == 0 && rf12_len > 2) {
      // got a good ACK packet, print out its contents
      const Payload* p = (const Payload*) rf12_data;
      
      Serial.print("{\"n\":"); 
      Serial.print(nextId);
      Serial.print(",");
      if (p->magic != MAGIC || p->node != nextId) {
        Serial.println("\"error\":\"badResponse\"}");
        return;
      }
      int count = rf12_len - sizeof(Payload);
      // calculate base ID

      if (p->lowbat) {
        // Low-battery indicator for this sensor
        Serial.print("\"error\":\"lowBattery\",");
      }
      for(int i=0; i<count; i++) {
        int value = p->data[i];
        Serial.print("\""); Serial.print(i+1); Serial.print("\":"); Serial.print(value);  
        if (i < count-1) Serial.print(",");            
      }
      Serial.println("}");    
      return;
    }
  }
  Serial.print("{\"n\":"); 
  Serial.print(nextId);
  Serial.print(",");
  Serial.println("\"error\":\"noResponse\"}");
 }
