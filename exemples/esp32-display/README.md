# 📺 ESP32 T-Display Oscilloscope Art Generator

> **Interactive oscilloscope art with live pattern preview on TFT display + dual DAC output**

This advanced example combines the power of ESP32's dual DACs with a TFT display for the ultimate oscilloscope art experience. See patterns on the built-in screen while simultaneously outputting to your oscilloscope. Navigate through 18+ mathematical art patterns using physical buttons!

## 🎬 **See It In Action!**

[![ESP32 T-Display Oscilloscope Art Demo](https://img.youtube.com/vi/mfS9IEM6bus/maxresdefault.jpg)](https://www.youtube.com/watch?v=mfS9IEM6bus)

**▶️ [Watch the full demonstration on YouTube](https://www.youtube.com/watch?v=mfS9IEM6bus)**

*Click the image above to see all patterns in action with live display preview and oscilloscope output!*

## ✨ **Advanced Features**

### 📱 **Interactive Display**
- 🖥️ **1.14" TFT Color Display** - Real-time pattern preview
- 🎮 **Physical Button Control** - Navigate patterns instantly
- 📊 **Live Pattern Info** - Shows current pattern name and DAC pins
- 🎨 **Visual Feedback** - See exactly what your oscilloscope will display

### 🎯 **Dual Output System**
- 📺 **TFT Preview** - See patterns on built-in 135x240 color display
- 🔬 **Oscilloscope Output** - Simultaneous DAC output to oscilloscope
- ⚡ **Real-time Sync** - Both displays update together
- 🎛️ **Interactive Control** - Switch patterns with physical buttons

### 🌟 **18+ Art Patterns**
- 🔵 **Geometric:** Circle, Ellipse, Infinity
- 🌹 **Floral:** Rose (3, 5, 8 petals), Rhodonea
- ❤️ **Organic:** Heart, Butterfly
- 🔄 **Lissajous:** 3:2, 5:4, 7:5, Cosine variants
- 🌀 **Spirals:** Archimedes, Logarithmic
- ⭐ **Mathematical:** Hypotrochoid, Cycloid, Astroid

## 🔌 **Hardware Requirements**

### **LILYGO T-Display ESP32**
- ✅ **ESP32-WROVER-B** with integrated TFT display
- ✅ **1.14" IPS Display** (135x240 pixels, ST7789 driver)
- ✅ **Two Physical Buttons** (GPIO35 and GPIO0)
- ✅ **Built-in USB-C** programming interface
- ✅ **Dual DAC Pins** (GPIO25, GPIO26) exposed

### **Oscilloscope Setup**
- 🔬 Any oscilloscope with **XY mode** capability
- 📡 **2x BNC cables** or probe wires
- ⚡ **Bandwidth:** 10MHz+ recommended for smooth patterns

## 🔧 **Hardware Connections**

```
LILYGO T-Display → Oscilloscope
├── GPIO25 (DAC1) → Channel 1 (X-axis)
├── GPIO26 (DAC2) → Channel 2 (Y-axis)  
└── GND           → Oscilloscope Ground

Built-in Controls:
├── Button A (GPIO35) → Next Pattern
├── Button B (GPIO0)  → Previous Pattern
└── TFT Display       → Live Preview
```

## 🚀 **Quick Start Guide**

### **1. Hardware Setup**
```bash
# Get a LILYGO T-Display ESP32 board
# Available from: AliExpress, Amazon, or official LILYGO store
# Search for: "LILYGO TTGO T-Display ESP32"
```

### **2. Flash the Firmware**
```bash
# Clone the repository
git clone https://github.com/s-celles/waveform-generator.git
cd waveform-generator/exemples/esp32-display

# Install PlatformIO and flash
pio run --target upload

# Or use Arduino IDE with TFT_eSPI library
```

### **3. Connect to Oscilloscope**
- Connect **GPIO25** to oscilloscope **Channel 1** (X-axis)
- Connect **GPIO26** to oscilloscope **Channel 2** (Y-axis)
- Connect **GND** to oscilloscope ground

### **4. Configure Oscilloscope**
- Set to **XY mode** (not normal timebase mode)
- Voltage scale: **1V/div** on both channels
- **Center** the display using position controls
- **Adjust intensity** for best visibility

### **5. Start Creating Art!**
- Power on the T-Display
- Use **Button A** to go to next pattern
- Use **Button B** to go to previous pattern  
- Watch the magic happen on both displays!

## 🎮 **Interactive Controls**

### **Button Functions**
| Button | GPIO | Function |
|--------|------|----------|
| **A** (Top) | GPIO35 | Next Pattern → |
| **B** (Bottom) | GPIO0 | ← Previous Pattern |

### **Display Information**
The TFT screen shows:
- 🏷️ **Pattern Name** - Current mathematical pattern
- 📍 **DAC Pin Info** - GPIO25(X), GPIO26(Y)  
- 📊 **Pattern Counter** - "5/18 A:Next B:Prev"
- ✅ **Status** - "Pattern drawn - DAC running"

## 🎨 **Available Art Patterns**

| # | Pattern | Description | Mathematical Basis |
|---|---------|-------------|-------------------|
| 1 | **Circle** | Perfect circle | x=cos(t), y=sin(t) |
| 2 | **Ellipse** | Oval shape | x=a×cos(t), y=b×sin(t) |
| 3 | **Lissajous 3:2** | Classic figure-8 | x=sin(3t), y=sin(2t) |
| 4 | **Lissajous 5:4** | Complex knot | x=sin(5t), y=sin(4t) |
| 5 | **Lissajous 7:5** | Intricate pattern | x=sin(7t), y=sin(5t) |
| 6 | **Lissajous Cos** | Cosine variant | x=cos(3t), y=cos(2t) |
| 7 | **Heart** ❤️ | Romantic curve | Heart equation |
| 8 | **Rose 3** 🌹 | 3-petal rose | Polar rose curve |
| 9 | **Rose 5** 🌹 | 5-petal rose | r=cos(5θ) |
| 10 | **Rose 8** 🌹 | 8-petal rose | Complex polar rose |
| 11 | **Butterfly** 🦋 | Butterfly curve | Butterfly equation |
| 12 | **Infinity** ∞ | Infinity symbol | Lemniscate |
| 13 | **Spiral Archimedes** | Linear spiral | r=aθ |
| 14 | **Spiral Log** | Logarithmic spiral | r=ae^(bθ) |
| 15 | **Hypotrochoid** | Wheel curve | Roulette curve |
| 16 | **Rhodonea** | Rose variant | Rhodonea curve |
| 17 | **Cycloid** | Wheel trace | Cycloid curve |
| 18 | **Astroid** ⭐ | 4-pointed star | Star-shaped curve |

## 🛠️ **Advanced Customization**

### **Adjust Pattern Speed**
```cpp
// In main.cpp loop()
delayMicroseconds(10);  // Default speed

delayMicroseconds(5);   // Faster (smooth for simple patterns)
delayMicroseconds(20);  // Slower (better for complex patterns)
delayMicroseconds(1);   // Maximum speed (may cause flicker)
```

### **Add New Patterns**
```cpp
// Add to patterns array in main.cpp
const Pattern patterns[] = {
  // ...existing patterns...
  {your_pattern_x, your_pattern_y, "Your Pattern"},
};
```

### **Customize Display Colors**
```cpp
// Change pattern colors in drawPatternOnDisplay()
tft.drawLine(prev_x, prev_y, x, y, TFT_BLUE);    // Line color
tft.drawPixel(x, y, TFT_WHITE);                  // Point color
tft.setTextColor(TFT_YELLOW, TFT_BLACK);         // Text color
```

### **Auto-Cycling Mode**
```cpp
// Add automatic pattern cycling
void loop() {
  static unsigned long lastChange = 0;
  
  if (millis() - lastChange > 5000) {  // Change every 5 seconds
    current_pattern = (current_pattern + 1) % NUM_PATTERNS;
    pattern_drawn = false;
    lastChange = millis();
  }
  
  // ... rest of loop
}
```

## 📊 **Technical Specifications**

### **T-Display Specs**
- **MCU:** ESP32-WROVER-B (240MHz dual-core)
- **Display:** 1.14" IPS TFT, 135×240 pixels, ST7789V
- **RAM:** 520KB SRAM + 8MB PSRAM
- **Flash:** 4MB
- **DAC:** 8-bit, 0-3.3V output range
- **Buttons:** 2× physical buttons with debouncing

### **Performance Metrics**
- **Pattern Update Rate:** ~100Hz (10μs delay)
- **Display Refresh:** Real-time preview
- **Pattern Switching:** Instant with button press
- **Memory Usage:** <50KB including all 18 patterns
- **Power Consumption:** ~150mA during operation

## 🎓 **Educational Applications**

### **STEM Learning**
- 📐 **Mathematics Visualization** - See parametric equations live
- ⚡ **Electronics Concepts** - DACs, analog output, displays
- 💻 **Programming Skills** - Embedded C++, real-time systems
- 🔬 **Instrumentation** - Oscilloscope operation and XY mode

### **Classroom Demonstrations**
- 🎪 **Interactive Math** - Students control pattern selection
- 🎨 **Art + Science** - Combine mathematics with visual art
- 🔧 **Hands-on Learning** - Build, program, and experiment
- 📊 **Real-time Feedback** - See changes immediately

## 🔍 **Troubleshooting**

### **Display Issues**
- ❌ **Blank Screen:** Check TFT_eSPI library installation
- 🔄 **Wrong Orientation:** Verify `tft.setRotation(1)` setting
- 🎨 **Color Issues:** Check display initialization in setup()

### **Button Problems**
- 🔘 **Not Responsive:** Verify GPIO35 and GPIO0 connections
- ⚡ **Multiple Triggers:** Button debouncing working correctly
- 🔄 **Stuck Pattern:** Reset device if buttons become unresponsive

### **Oscilloscope Output**
- 📺 **No Pattern:** Check DAC connections (GPIO25, GPIO26)
- 🌀 **Distorted Shape:** Verify ground connection and oscilloscope settings
- ⚡ **Too Fast/Slow:** Adjust `delayMicroseconds()` value in code

### **Serial Monitor Debug**
Connect at 115200 baud to see:
```
ESP32 XY DAC Display Starting...
DAC channels initialized
Connect oscilloscope:
- X channel (DAC1): GPIO25
- Y channel (DAC2): GPIO26  
- Set oscilloscope to XY mode
- Button A: Next pattern
- Button B: Previous pattern
Next pattern: Rose 5
```

## 🛒 **Shopping List**

### **Essential Hardware**
- 🛒 **LILYGO T-Display ESP32** (~$15-25)
  - Search: "LILYGO TTGO T-Display ESP32 1.14 inch"
  - Sources: AliExpress, Amazon, Adafruit
- 📡 **BNC Cables** (2×) or oscilloscope probes
- 🔌 **USB-C Cable** for programming

### **Optional Additions**
- 📦 **Breadboard** for external connections
- 🔌 **Jumper Wires** for easy connections
- 📱 **Phone Stand** to hold T-Display for better viewing
- 🎧 **External DAC** for higher resolution (16-bit)

## 🎨 **Creative Projects**

### **Art Installations**
- 🖼️ **Gallery Displays** - Interactive math art for museums
- 🎪 **Maker Faire Demos** - Engaging STEM demonstrations
- 🏫 **School Projects** - Visual mathematics education

### **Technical Applications**
- 🔧 **Oscilloscope Calibration** - Known reference patterns
- 📊 **Signal Generator** - Precise test waveforms  
- 🎵 **Audio Visualization** - Connect to audio systems
- 🤖 **Robot Navigation** - XY coordinate generation

### **Educational Extensions**
- 📱 **Mobile App Control** - Bluetooth pattern selection
- 🌐 **Web Interface** - WiFi-based remote control
- 📊 **Data Logging** - Record pattern parameters
- 🎮 **Game Integration** - Interactive pattern challenges

## 🔗 **Related Resources**

### **Project Links**
- 🏠 **[Main Repository](../../)** - Core waveform generator
- 🔧 **[Basic ESP32 Example](../esp32/)** - Simple oscilloscope art
- 📚 **[Arduino Examples](../arduino/)** - Arduino-compatible versions
- 🎯 **[STM32 Examples](../stm32/)** - 12-bit DAC implementations

### **Documentation**
- 📖 **[TFT_eSPI Library](https://github.com/Bodmer/TFT_eSPI)** - Display library
- 🔧 **[LILYGO T-Display](https://github.com/Xinyuan-LilyGO/TTGO-T-Display)** - Hardware docs
- 📊 **[ESP32 DAC Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/dac.html)**
- 🎨 **[Mathematical Curves](https://mathworld.wolfram.com/topics/PlaneCurves.html)**

## 💝 **Support the Project**

- ⭐ **Star this repository** if it helped you create amazing art!
- 🍴 **Fork and contribute** new patterns or improvements
- 📢 **Share your creations** - tag us in your oscilloscope art photos
- 🐛 **Report issues** to help make this project better

## 📄 **License**

This project is licensed under the MIT License - feel free to use it for educational, personal, or commercial projects!

---

**🎨 Transform mathematics into interactive visual art with ESP32 T-Display and oscilloscopes!** ✨

*The perfect blend of embedded programming, mathematics, and visual art* 🌟