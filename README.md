# 🌊 Waveform Generator

> **Generate C lookup tables for any DAC resolution - from 8-bit Arduino to 64-bit audio processing**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A powerful Python script that generates optimized C header files containing waveform lookup tables for embedded systems, audio processing, and signal generation. Perfect for oscilloscopes, function generators, synthesizers, and any application requiring precise waveforms.

## ✨ Features

- 🎯 **Multi-resolution support**: 8, 10, 12, 16, 32, 64 bits
- 🌊 **13+ waveform types**: Classic (sine, triangle, square) and artistic (heart, butterfly, flower)
- 🔧 **Configurable parameters**: Array size, amplitude, frequency, phase
- 📊 **Memory optimization**: Automatic data type selection (uint8_t to uint64_t)
- ✅ **Validation built-in**: Range checking and error detection
- 📝 **Self-documenting**: Generated headers include full documentation
- 🚀 **Ready-to-use**: Drop-in C headers with utility functions

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/waveform-generator.git
cd waveform-generator

# Generate 8-bit waveforms for Arduino
python waveform_generator.py --bits 8 --size 256 --output arduino_waves.h

# Generate 12-bit waveforms for STM32 DAC
python waveform_generator.py --bits 12 --size 512 --output stm32_waves.h

# Generate only specific waveforms
python waveform_generator.py --bits 16 --waves sine,triangle,heart --output basic_waves.h
```

## 📦 Installation

### Requirements
- Python 3.7+
- No external dependencies required!

### Usage
```bash
python waveform_generator.py [OPTIONS]
```

### Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bits` | Output resolution (8,10,12,16,32,64) | 8 | `--bits 12` |
| `--size` | Array size (samples per waveform) | 256 | `--size 1024` |
| `--output` | Output filename | `waveforms.h` | `--output my_waves.h` |
| `--waves` | Waveforms to generate | `all` | `--waves sine,triangle` |
| `--amplitude` | Global amplitude multiplier | 1.0 | `--amplitude 0.8` |
| `--frequency` | Global frequency multiplier | 1.0 | `--frequency 2.0` |
| `--list` | List available waveforms | - | `--list` |

## 🌊 Available Waveforms

### Classic Waveforms
- **sine** - Perfect sinusoidal wave
- **triangle** - Linear rise and fall
- **square** - Digital high/low signal  
- **sawtooth** - Linear ramp with sharp reset
- **ramp** - Perfect linear 0→max ramp

### Artistic Waveforms
- **heart** ❤️ - Heart-shaped curve
- **flower** 🌸 - Rose petal pattern
- **spiral** - Archimedean spiral
- **butterfly** 🦋 - Mathematical butterfly curve

### Complex Waveforms  
- **lissajous** - Figure-8 Lissajous curves (3:2 ratio)
- **chaos** 🌀 - Deterministic chaotic signal
- **pulse** - Configurable pulse train
- **noise** - Pseudo-random noise

## 📊 Output Examples

### 8-bit (Arduino/AVR)
```c
#define WAVE_ARRAY_SIZE 256
#define WAVE_MAX_VALUE 255

const uint8_t sine_wave[WAVE_ARRAY_SIZE] = {
  128, 131, 134, 137, 140, 143, 146, 149,
  // ... 248 more values
};
```

### 12-bit (STM32 DAC)
```c
#define WAVE_ARRAY_SIZE 512  
#define WAVE_MAX_VALUE 4095

const uint16_t sine_wave[WAVE_ARRAY_SIZE] = {
  2048, 2148, 2248, 2348, 2448, 2548, 2648, 2748,
  // ... 504 more values  
};
```

### 16-bit (Audio Processing)
```c
#define WAVE_ARRAY_SIZE 1024
#define WAVE_MAX_VALUE 65535

const uint16_t sine_wave[WAVE_ARRAY_SIZE] = {
  32768, 32964, 33160, 33356, 33552, 33748, 33944, 34140,
  // ... 1016 more values
};
```

## 🔧 Usage in Your Project

### Basic Usage
```c
#include "waveforms.h"

void play_sine_wave() {
    for(int i = 0; i < WAVE_ARRAY_SIZE; i++) {
        dac_output(sine_wave[i]);
        delay_us(100);  // 10kHz sample rate
    }
}
```

### Using Utility Functions
```c
#include "waveforms.h"

void play_waveform(waveform_type_t type) {
    for(int i = 0; i < WAVE_ARRAY_SIZE; i++) {
        uint16_t sample = get_waveform_sample(type, i);
        dac_output(sample);
        delay_us(50);   // 20kHz sample rate  
    }
}

// Play different waveforms
play_waveform(WAVE_HEART);      // ❤️
play_waveform(WAVE_BUTTERFLY);  // 🦋
play_waveform(WAVE_LISSAJOUS);  // Figure-8
```

### Arduino Example
```c
#include "arduino_waves.h"

void setup() {
    // Initialize DAC (MCP4725, etc.)
    Wire.begin();
}

void loop() {
    // Cycle through all waveforms
    for(int wave = 0; wave < WAVE_COUNT; wave++) {
        for(int i = 0; i < WAVE_ARRAY_SIZE; i++) {
            uint8_t value = get_waveform_sample(wave, i);
            analogWrite(DAC_PIN, value);
            delayMicroseconds(100);
        }
        delay(1000);  // Pause between waveforms
    }
}
```

## 🎯 Use Cases

### 🔬 **Embedded Systems**
- Arduino/ESP32 projects with DACs
- STM32/ARM Cortex-M signal generation  
- Custom function generators
- Oscilloscope calibration

### 🎵 **Audio Processing**
- Synthesizer oscillators
- Audio test signals
- Digital audio workstations
- Effect processing

### 📡 **Signal Processing** 
- Software-defined radio (SDR)
- Digital communications
- Test equipment
- Scientific instruments

### 🎮 **Creative Applications**
- LED matrix animations
- Motor control patterns
- Art installations  
- Educational demonstrations

## 📈 Performance & Memory

| Bits | Data Type | Max Value | Memory per Waveform (256 samples) |
|------|-----------|-----------|-----------------------------------|
| 8    | uint8_t   | 255       | 256 bytes                        |
| 12   | uint16_t  | 4,095     | 512 bytes                        |
| 16   | uint16_t  | 65,535    | 512 bytes                        |
| 32   | uint32_t  | 4.3B      | 1,024 bytes                      |
| 64   | uint64_t  | 1.8×10¹⁹  | 2,048 bytes                      |

### Example: Complete 8-bit library (13 waveforms)
- **Total size**: ~3.3 KB
- **Flash usage**: Stored in program memory (const)
- **RAM usage**: Zero (direct lookup)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🐛 Report bugs** - Open an issue with reproduction steps
2. **✨ Suggest features** - New waveforms, output formats, optimizations  
3. **📖 Improve docs** - Examples, tutorials, hardware guides
4. **🧪 Add tests** - Unit tests, validation scripts
5. **💡 Submit PRs** - Bug fixes, new features, optimizations

### Adding New Waveforms

1. Add your mathematical function to the `WaveformGenerator` class
2. Update the `available_waveforms` dictionary
3. Add documentation and examples
4. Submit a pull request!

```python
def generate_custom(self, amplitude=1.0, frequency=1.0, phase=0.0):
    """Your custom waveform function"""
    return [
        self.normalize(amplitude * your_math_function(i, frequency, phase))
        for i in range(self.array_size)
    ]
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Inspiration**: Oscilloscope art community and embedded audio developers
- **Mathematics**: Classic signal processing and parametric equations
- **Testing**: Arduino, STM32, and ESP32 communities

## 🌟 Star History

If this project helped you, please give it a ⭐! It helps others discover the tool.

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/waveform-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/waveform-generator/discussions)

---

**Made with ❤️ for the embedded and audio communities**

*Generate beautiful waveforms, one lookup table at a time* 🌊
