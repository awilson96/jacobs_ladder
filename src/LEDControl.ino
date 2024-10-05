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
  set_lights(0b00000000, 0b00000000, 0b00000000, 0b00000000);
  delay(animation_speed); // Delay to see all LEDs off
  
  // Loop through each LED in the first shift register (LEDs 1-8)
  for (int i = 0; i < 8; i++) {
    // Light up each LED in the first shift register
    set_lights(1 << i, 0b00000000, 0b00000000, 0b00000000); // Shift left to set the appropriate bit
    delay(animation_speed); // Wait before lighting up the next LED
  }

  // Loop through each LED in the second shift register (LEDs 9-16)
  for (int i = 0; i < 8; i++) {
    // Light up each LED in the second shift register
    set_lights(0b00000000, 1 << i, 0b00000000, 0b00000000); // Shift left to set the appropriate bit
    delay(animation_speed); // Wait before lighting up the next LED
  }

  // Loop through each LED in the third shift register (LEDs 17-24)
  for (int i = 0; i < 8; i++) {
    // Light up each LED in the third shift register
    set_lights(0b00000000, 0b00000000, 1 << i, 0b00000000); // Shift left to set the appropriate bit
    delay(animation_speed); // Wait before lighting up the next LED
  }

  // Loop through each LED in the fourth shift register (LEDs 25-32)
  for (int i = 0; i < 8; i++) {
    // Light up each LED in the fourth shift register
    set_lights(0b00000000, 0b00000000, 0b00000000, 1 << i); // Shift left to set the appropriate bit
    delay(animation_speed); // Wait before lighting up the next LED
  }
}

// Function to set the lights based on 32-bit binary numbers
void set_lights(uint8_t firstRegister, uint8_t secondRegister, uint8_t thirdRegister, uint8_t fourthRegister) {
  // Invert the registers to correct the LED states

  // Send patterns to the shift registers
  digitalWrite(latchPin, LOW);   // Prepare shift register to receive data
  shiftOut(dataPin, clockPin, MSBFIRST, fourthRegister);  // Send pattern to fourth shift register
  shiftOut(dataPin, clockPin, MSBFIRST, thirdRegister); // Send pattern to third shift register
  shiftOut(dataPin, clockPin, MSBFIRST, secondRegister); // Send pattern to second shift register
  shiftOut(dataPin, clockPin, MSBFIRST, firstRegister); // Send pattern to first shift register
  digitalWrite(latchPin, HIGH);  // Latch the data to output pins
}
