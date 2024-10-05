// Pin definitions based on your setup
int dataPin = 11;   // DS pin (Data)
int latchPin = 12;  // ST_CP pin (Latch)
int clockPin = 13;  // SH_CP pin (Clock)

int animation_speed = 250;

void setup() {
  // Set pins as output
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

void loop() {
  // Animate lighting up LEDs individually
  animateLEDs();
}

// Function to animate LEDs lighting up individually
void animateLEDs() {
  // Turn off all LEDs first
  set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
             0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
  delay(animation_speed); // Delay to see all LEDs off
  
  // Loop through each LED in the first shift register (LEDs 1-8)
  for (int i = 0; i < 8; i++) {
    set_lights(1 << i, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Loop through each LED in the second shift register (LEDs 9-16)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 1 << i, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Continue for registers 3-11...
  // Third shift register (LEDs 17-24)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 1 << i, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Fourth shift register (LEDs 25-32)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 1 << i, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Fifth shift register (LEDs 33-40)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 1 << i, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Sixth shift register (LEDs 41-48)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 1 << i,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Seventh shift register (LEDs 49-56)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               1 << i, 0b00000000, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Eighth shift register (LEDs 57-64)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 1 << i, 0b00000000, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Ninth shift register (LEDs 65-72)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 1 << i, 0b00000000, 0b00000000);
    delay(animation_speed);
  }

  // Tenth shift register (LEDs 73-80)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 1 << i, 0b00000000);
    delay(animation_speed);
  }

  // Eleventh shift register (LEDs 81-88)
  for (int i = 0; i < 8; i++) {
    set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
               0b00000000, 0b00000000, 0b00000000, 0b00000000, 1 << i);
    delay(animation_speed);
  }
}

// Function to set the lights based on 88-bit binary numbers
void set_lights(uint8_t firstRegister, uint8_t secondRegister, uint8_t thirdRegister, uint8_t fourthRegister, uint8_t fifthRegister, uint8_t sixthRegister,
                uint8_t seventhRegister, uint8_t eighthRegister, uint8_t ninthRegister, uint8_t tenthRegister, uint8_t eleventhRegister) {

  digitalWrite(latchPin, LOW);   // Prepare shift register to receive data
  shiftOut(dataPin, clockPin, MSBFIRST, eleventhRegister); // Send pattern to eleventh shift register (LEDs 81-88)
  shiftOut(dataPin, clockPin, MSBFIRST, tenthRegister);    // Send pattern to tenth shift register (LEDs 73-80)
  shiftOut(dataPin, clockPin, MSBFIRST, ninthRegister);    // Send pattern to ninth shift register (LEDs 65-72)
  shiftOut(dataPin, clockPin, MSBFIRST, eighthRegister);   // Send pattern to eighth shift register (LEDs 57-64)
  shiftOut(dataPin, clockPin, MSBFIRST, seventhRegister);  // Send pattern to seventh shift register (LEDs 49-56)
  shiftOut(dataPin, clockPin, MSBFIRST, sixthRegister);    // Send pattern to sixth shift register (LEDs 41-48)
  shiftOut(dataPin, clockPin, MSBFIRST, fifthRegister);    // Send pattern to fifth shift register (LEDs 33-40)
  shiftOut(dataPin, clockPin, MSBFIRST, fourthRegister);   // Send pattern to fourth shift register (LEDs 25-32)
  shiftOut(dataPin, clockPin, MSBFIRST, thirdRegister);    // Send pattern to third shift register (LEDs 17-24)
  shiftOut(dataPin, clockPin, MSBFIRST, secondRegister);   // Send pattern to second shift register (LEDs 9-16)
  shiftOut(dataPin, clockPin, MSBFIRST, firstRegister);    // Send pattern to first shift register (LEDs 1-8)
  digitalWrite(latchPin, HIGH);  // Latch the data, updating the LEDs
}
