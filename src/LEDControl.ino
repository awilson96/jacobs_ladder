// Pin definitions based on your setup
int dataPin = 11;   // Input (Pin 14 on 74HC595)
int latchPin = 12;  // Output Register Clock (Pin 12 on 74HC595)
int clockPin = 13;  // Shift Register Clock (Pin 11 on 74HC595)

void setup() {
  // Set pins as output
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

void loop() {
  // Pattern to light up LEDs 1, 3, 5, and 7 (odd LEDs)
  int oddPattern = 0b10101010; // Binary pattern for odd LEDs on
  // Pattern to light up LEDs 2, 4, 6, and 8 (even LEDs)
  int evenPattern = 0b01010101; // Binary pattern for even LEDs on

  // Send odd pattern to shift register (LEDs 1, 3, 5, and 7 ON)
  digitalWrite(latchPin, LOW);   // Prepare shift register to receive data
  shiftOut(dataPin, clockPin, MSBFIRST, oddPattern); // Send odd pattern
  digitalWrite(latchPin, HIGH);  // Latch the data to output pins
  delay(3000);  // Wait for 400 milliseconds

  // Send even pattern to shift register (LEDs 2, 4, 6, and 8 ON)
  digitalWrite(latchPin, LOW);   // Prepare shift register to receive data
  shiftOut(dataPin, clockPin, MSBFIRST, evenPattern); // Send even pattern
  digitalWrite(latchPin, HIGH);  // Latch the data to output pins
  delay(3000);  // Wait for 400 milliseconds
}
