#include <Arduino.h>
#include "xy_waveforms.h"
#include "driver/dac.h"

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(115200);
  Serial.println("ESP32 XY DAC Display Starting...");
  
  // Configure DAC channels
  dac_output_enable(DAC_CHANNEL_1);  // GPIO25 - X channel
  dac_output_enable(DAC_CHANNEL_2);  // GPIO26 - Y channel
  
  // Set initial DAC values to center
  dac_output_voltage(DAC_CHANNEL_1, XY_CENTER);  // X center
  dac_output_voltage(DAC_CHANNEL_2, XY_CENTER);  // Y center
  
  Serial.println("DAC channels initialized");
  Serial.println("Connect oscilloscope:");
  Serial.println("- X channel (DAC1): GPIO25");
  Serial.println("- Y channel (DAC2): GPIO26");
  Serial.println("- Set oscilloscope to XY mode");
}

void loop() {
  // Display circle pattern
  for (uint16_t i = 0; i < XY_ARRAY_SIZE; i++) {
    // Output X and Y coordinates to DAC channels
    //dac_output_voltage(DAC_CHANNEL_1, circle_x[i]);  // X coordinate to DAC1 (GPIO25)
    //dac_output_voltage(DAC_CHANNEL_2, circle_y[i]);  // Y coordinate to DAC2 (GPIO26)

    dac_output_voltage(DAC_CHANNEL_1, rose_5_x[i]);  // X coordinate to DAC1 (GPIO25)
    dac_output_voltage(DAC_CHANNEL_2, rose_5_y[i]);  // Y coordinate to DAC2 (GPIO26)

    // Small delay to control drawing speed
    delayMicroseconds(10);
  }
  
  // Optional: pause between pattern repeats
  delay(10);
}
