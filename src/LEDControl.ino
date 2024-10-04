// Pin definitions based on your setup
int dataPin = 11;   // DS pin (Data)
int latchPin = 12;  // ST_CP pin (Latch)
int clockPin = 13;  // SH_CP pin (Clock)

void setup() {
  // Set pins as output
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

void loop() {
  // Example usage of set_lights function
  set_lights(0b10101011, 0b11111111); // Call the function with the desired patterns
  delay(2000);  // Wait for 2 seconds before changing the lights
}

// Function to set the lights based on 8-bit binary numbers
void set_lights(uint8_t firstRegister, uint8_t secondRegister) {
  // Invert the registers to correct the LED states

  // Send patterns to the shift registers
  digitalWrite(latchPin, LOW);   // Prepare shift register to receive data
  shiftOut(dataPin, clockPin, MSBFIRST, secondRegister);  // Send pattern to second shift register
  shiftOut(dataPin, clockPin, MSBFIRST, firstRegister); // Send pattern to first shift register
  digitalWrite(latchPin, HIGH);  // Latch the data to output pins
}
