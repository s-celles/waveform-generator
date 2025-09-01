#include <Arduino.h>
#include <TFT_eSPI.h>
#include <SPI.h>

#include "xy_waveforms.h"
#include "driver/dac.h"

// --- Boutons T-Display classique ---
#define BTN_A 35   // bouton haut (GPIO35, input-only, pull-up externe)
#define BTN_B 0    // bouton bas (GPIO0/BOOT, avec pull-up interne)

// --- Écran TFT ---
TFT_eSPI tft = TFT_eSPI();

// Pattern management
typedef struct {
  const uint8_t* x_data;
  const uint8_t* y_data;
  const char* name;
} Pattern;

const Pattern patterns[] = {
  {circle_x, circle_y, "Circle"},
  {ellipse_x, ellipse_y, "Ellipse"},
  {lissajous_3_2_x, lissajous_3_2_y, "Lissajous 3:2"},
  {lissajous_5_4_x, lissajous_5_4_y, "Lissajous 5:4"},
  {lissajous_7_5_x, lissajous_7_5_y, "Lissajous 7:5"},
  {lissajous_cos_x, lissajous_cos_y, "Lissajous Cos"},
  {heart_x, heart_y, "Heart"},
  {rose_3_x, rose_3_y, "Rose 3"},
  {rose_5_x, rose_5_y, "Rose 5"},
  {rose_8_x, rose_8_y, "Rose 8"},
  {butterfly_x, butterfly_y, "Butterfly"},
  {infinity_x, infinity_y, "Infinity"},
  {spiral_archimedes_x, spiral_archimedes_y, "Spiral Archimedes"},
  {spiral_log_x, spiral_log_y, "Spiral Log"},
  {hypotrochoid_x, hypotrochoid_y, "Hypotrochoid"},
  {rhodonea_x, rhodonea_y, "Rhodonea"},
  {cycloid_x, cycloid_y, "Cycloid"},
  {astroid_x, astroid_y, "Astroid"}
};

const int NUM_PATTERNS = sizeof(patterns) / sizeof(patterns[0]);
int current_pattern = 8; // Start with Rose 5

// Button state management
bool button_a_pressed = false;
bool button_b_pressed = false;

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(115200);
  Serial.println("ESP32 XY DAC Display Starting...");

  // Initialize buttons
  pinMode(BTN_A, INPUT_PULLUP);  // Button A (GPIO35)
  pinMode(BTN_B, INPUT_PULLUP);  // Button B (GPIO0)
  
  // Init écran
  tft.init();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  tft.drawString("Hello, T-Display!", 10, 10, 2);

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
  Serial.println("- Button A: Next pattern");
  Serial.println("- Button B: Previous pattern");
}

static bool pattern_drawn = false;

void checkButtons() {
  // Check Button A (next pattern)
  if (digitalRead(BTN_A) == LOW && !button_a_pressed) {
    button_a_pressed = true;
    current_pattern = (current_pattern + 1) % NUM_PATTERNS;
    pattern_drawn = false; // Force redraw
    Serial.print("Next pattern: ");
    Serial.println(patterns[current_pattern].name);
  } else if (digitalRead(BTN_A) == HIGH) {
    button_a_pressed = false;
  }
  
  // Check Button B (previous pattern)
  if (digitalRead(BTN_B) == LOW && !button_b_pressed) {
    button_b_pressed = true;
    current_pattern = (current_pattern - 1 + NUM_PATTERNS) % NUM_PATTERNS;
    pattern_drawn = false; // Force redraw
    Serial.print("Previous pattern: ");
    Serial.println(patterns[current_pattern].name);
  } else if (digitalRead(BTN_B) == HIGH) {
    button_b_pressed = false;
  }
}

void drawPatternOnDisplay() {
  // Clear screen for new pattern
  tft.fillScreen(TFT_BLACK);
  
  // Display pattern info
  tft.setTextColor(TFT_CYAN, TFT_BLACK);
  tft.drawString(patterns[current_pattern].name, 10, 10, 2);
  tft.setTextColor(TFT_YELLOW, TFT_BLACK);
  tft.drawString("DAC: GPIO25(X), GPIO26(Y)", 10, 30, 1);
  
  // Display pattern navigation info
  tft.setTextColor(TFT_MAGENTA, TFT_BLACK);
  String pattern_info = String(current_pattern + 1) + "/" + String(NUM_PATTERNS) + " A:Next B:Prev";
  tft.drawString(pattern_info, 10, 45, 1);
  
  // Calculate display scaling and offset
  int16_t display_center_x = tft.width() / 2;
  int16_t display_center_y = tft.height() / 2;
  
  // Use same scale for both axes to maintain proportions
  float max_scale_x = (tft.width() - 40) / 255.0;   // Leave 20px margin on each side
  float max_scale_y = (tft.height() - 100) / 255.0;  // Leave more margin for text
  float scale = min(max_scale_x, max_scale_y);       // Use the smaller scale to fit both dimensions

  // Draw the complete pattern at once
  for (uint16_t i = 0; i < XY_ARRAY_SIZE; i++) {
    // Convert to display coordinates
    int16_t display_x = display_center_x + (patterns[current_pattern].x_data[i] - XY_CENTER) * scale;
    int16_t display_y = display_center_y - (patterns[current_pattern].y_data[i] - XY_CENTER) * scale; // Invert Y for proper orientation
    
    // Draw connected lines
    if (i > 0) {
      int16_t prev_display_x = display_center_x + (patterns[current_pattern].x_data[i-1] - XY_CENTER) * scale;
      int16_t prev_display_y = display_center_y - (patterns[current_pattern].y_data[i-1] - XY_CENTER) * scale;
      tft.drawLine(prev_display_x, prev_display_y, display_x, display_y, TFT_GREEN);
    }
    
    // Draw current point
    tft.drawPixel(display_x, display_y, TFT_RED);
  }
  
  // Show completion info
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.drawString("Pattern drawn - DAC running", 10, tft.height() - 20, 1);
}

void loop() {
  // Check for button presses
  checkButtons();
  
  // Draw pattern on screen when needed
  if (!pattern_drawn) {
    drawPatternOnDisplay();
    pattern_drawn = true;
  }

  // Run DAC output at full speed
  for (uint16_t i = 0; i < XY_ARRAY_SIZE; i++) {
    // Output current pattern to DAC channels at maximum speed
    dac_output_voltage(DAC_CHANNEL_1, patterns[current_pattern].x_data[i]);  // X coordinate to DAC1 (GPIO25)
    dac_output_voltage(DAC_CHANNEL_2, patterns[current_pattern].y_data[i]);  // Y coordinate to DAC2 (GPIO26)
    
    // Minimal delay for DAC stability (can be reduced or removed)
    delayMicroseconds(10);
  }
}
