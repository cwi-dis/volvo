bool ledStatus;
int ledPin = D7;

int rowPins[] = { D0, D1 /*, D2, D3, D4, D5 */ };
int columnPins[] = {A0, A1 /*, A2, A3, A4, A5 */};
int rowIndex = 0;

#define N(x) (sizeof(x)/sizeof(x[0]))
String pressures;
#define STRSIZE 400
char pressureCloud[STRSIZE];
int timestamp;
int seqno;

void setup()
{
  // variable name max length is 12 characters long
  pressureCloud[0] = '\0';
  Particle.variable("pressures", pressureCloud, STRING);
  Particle.variable("timestamp", &timestamp, INT);
  Particle.variable("seqno", &seqno, INT);
  pinMode(ledPin, OUTPUT);
  // Initialize all output (row) pins
  unsigned int i;
  for (i=0; i<N(rowPins); i++) {
      pinMode(rowPins[i], OUTPUT);
      digitalWrite(rowPins[i], HIGH);
  }
  // Initialize all input (column) pins
  for (i=0; i<N(columnPins); i++) {
      pinMode(columnPins[i], INPUT);
  }
}

void loop()
{
  // Enable current row of sensors
  digitalWrite(rowPins[rowIndex], LOW);
  // Read the analog values of the current row, append to string
  for (unsigned int i=0; i<N(columnPins); i++) {
      int analogvalue = analogRead(columnPins[i]);
      if (i!=0 || rowIndex!=0) pressures += ",";
      pressures += String(analogvalue);
  }
  // Disable the row again
  digitalWrite(rowPins[rowIndex], HIGH);
  // Transmit, if we have read the complete matrix
  rowIndex++;
  if (rowIndex >= N(rowPins)) {
      strncpy(pressureCloud, pressures.c_str(), STRSIZE);
      pressures = "";
      seqno++;
      timestamp = millis();
      rowIndex = 0;
      ledStatus = !ledStatus;
      digitalWrite(ledPin, ledStatus?HIGH:LOW);
      delay(100);
    
  }
}

