// Test program for jeenode: dump 4 sensor values (matrix-style)
// to the serial port.

#include <JeeLib.h>

Port p1(1);
Port p2(2);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  p1.mode(OUTPUT);
  p2.mode(OUTPUT);
  p1.mode2(INPUT);
  p2.mode2(INPUT);
  p1.digiWrite(HIGH);
  p2.digiWrite(HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  p1.digiWrite(LOW);
  delay(100);
  int v1 = p1.anaRead();
  int v2 = p2.anaRead();
  Serial.print(v1); Serial.print(" ");
  Serial.print(v2); Serial.print(" ");
  p1.digiWrite(HIGH);
  
  p2.digiWrite(LOW);
  delay(100);
  v1 = p1.anaRead();
  v2 = p2.anaRead();
  Serial.print(v1); Serial.print(" ");
  Serial.print(v2); Serial.print(" ");
  p2.digiWrite(HIGH);
  Serial.println();
  delay(200);

}
