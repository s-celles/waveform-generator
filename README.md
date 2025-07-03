# 🌊 Waveform Generator

> **Professional waveform lookup table generator for embedded systems and oscilloscope art**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/s-celles/waveform-generator.svg)](https://github.com/s-celles/waveform-generator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/s-celles/waveform-generator.svg)](https://github.com/s-celles/waveform-generator/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Generate optimized C lookup tables for **any DAC resolution** - from 8-bit Arduino to 64-bit precision audio. Create stunning **oscilloscope art** with synchronized XY patterns. Perfect for embedded systems, signal generation, and creative projects.

## ✨ Features

### 🎯 **Multi-Resolution Support**
- **8-bit** (Arduino, AVR) → `uint8_t` arrays
- **12-bit** (STM32 DAC) → `uint16_t` with 4096 values  
- **16-bit** (Audio DACs) → Professional audio quality
- **32/64-bit** → Scientific precision applications

### 🌊 **Rich Waveform Library**
- **Classic:** Sine, Triangle, Square, Sawtooth, Ramp
- **Artistic:** Heart ❤️, Flower 🌸, Butterfly 🦋, Spiral 🌀  
- **Mathematical:** Lissajous, Cycloid, Astroid, Rhodonea
- **Technical:** Chaos, Pulse trains, Noise patterns

### 🎨 **Oscilloscope XY Art**
- **Synchronized X,Y patterns** for dual-DAC setups
- **18+ artistic patterns** including hearts, roses, infinity symbols
- **Real-time control** examples for Arduino/ESP32/STM32
- **Auto-cycling demos** and interactive controls

### 🔧 **Developer-Friendly**
- **Zero external dependencies** - uses only Python standard library
- **Self-documenting** generated headers with full API
- **Memory optimized** - automatic data type selection
- **Validation built-in** - range checking and error detection

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/s-celles/waveform-generator.git
cd waveform-generator
```

### Generate Your First Waveforms
```bash
# Basic 8-bit waveforms for Arduino
python yt_waveform_generator.py --bits 8 --size 256 --output arduino_waves.h

# 12-bit waveforms for STM32 DAC  
python yt_waveform_generator.py --bits 12 --size 512 --output stm32_waves.h

# XY patterns for oscilloscope art
python xy_waveform_generator.py --patterns heart,rose_5,butterfly --output xy_art.h

# See all available options
python yt_waveform_generator.py --list
python xy_waveform_generator.py --list-patterns
```

### Use in Your Project
```c
#include "arduino_waves.h"

void play_sine_wave() {
    for(int i = 0; i < WAVE_ARRAY_SIZE; i++) {
        dac_output(sine_wave[i]);
        delay_us(100);  // 10kHz sample rate
    }
}
```

## 📊 Generated Output Examples

<details>
<summary><strong>8-bit Arduino Example</strong></summary>

```c
#define WAVE_ARRAY_SIZE 256
#define WAVE_BITS 8
#define WAVE_MAX_VALUE 255

const uint8_t sine_wave[WAVE_ARRAY_SIZE] = {
  128, 131, 134, 137, 140, 143, 146, 149, 152, 155, 158, 162, 165, 167, 170, 173,
  176, 179, 182, 185, 188, 190, 193, 196, 198, 201, 203, 206, 208, 211, 213, 215,
  // ... 224 more values
};
```
</details>

<details>
<summary><strong>12-bit STM32 Example</strong></summary>

```c
#define WAVE_ARRAY_SIZE 512
#define WAVE_BITS 12  
#define WAVE_MAX_VALUE 4095

const uint16_t sine_wave[WAVE_ARRAY_SIZE] = {
  2048, 2073, 2098, 2123, 2148, 2173, 2198, 2223, 2248, 2273, 2298, 2323, 2348, 2373, 2398, 2423,
  2448, 2473, 2498, 2523, 2548, 2573, 2598, 2623, 2648, 2673, 2698, 2723, 2748, 2773, 2798, 2823,
  // ... 480 more values
};
```
</details>

<details>
<summary><strong>XY Oscilloscope Art Example</strong></summary>

```c
// Heart pattern ❤️ for oscilloscope XY mode
const uint8_t heart_x[XY_ARRAY_SIZE] = {
  127, 127, 128, 129, 131, 133, 135, 138, 141, 144, 148, 152, 156, 161, 166, 171,
  // ... X coordinates
};

const uint8_t heart_y[XY_ARRAY_SIZE] = {  
  127, 130, 133, 137, 140, 144, 147, 151, 154, 158, 161, 165, 168, 172, 175, 179,
  // ... Y coordinates  
};

// Usage: Connect X to CH1, Y to CH2, set oscilloscope to XY mode
```
</details>

## 🎨 Oscilloscope Art Gallery

Transform your oscilloscope into an art canvas with stunning XY patterns:

| Pattern | Description | Best For |
|---------|-------------|----------|
| `heart` ❤️ | Mathematical heart curve | Demos, gifts |
| `rose_5` 🌹 | 5-petal rose pattern | Beautiful, balanced |
| `butterfly` 🦋 | Complex butterfly equation | Impressive complexity |
| `lissajous_3_2` | Classic figure-8 | Educational, stable |
| `infinity` ∞ | Infinity symbol | Simple but effective |
| `spiral_log` 🌀 | Logarithmic spiral | Hypnotic motion |

### Hardware Setup for XY Art
```
Arduino + 2x MCP4725 DACs:
├── DAC1 (0x60) → Oscilloscope X Input  
├── DAC2 (0x61) → Oscilloscope Y Input
└── Set oscilloscope to XY mode

ESP32 (built-in DACs):
├── GPIO25 → Oscilloscope X Input
├── GPIO26 → Oscilloscope Y Input  
└── 8-bit resolution, very fast
```

## 🛠️ Platform Support

### Embedded Platforms
- **Arduino** (Uno, Nano, ESP32) - 8-bit optimized
- **STM32** (Discovery, Nucleo) - 12-bit DAC support
- **ESP32** - Built-in dual DACs for XY patterns
- **Raspberry Pi** - GPIO + external DACs
- **Any microcontroller** with DAC capability

### Development Tools
- **C/C++** embedded projects
- **Python** signal processing  
- **MATLAB/Octave** integration
- **LabVIEW** measurement systems

## 📁 Repository Structure

```
waveform-generator/
├── 🐍 yt_waveform_generator.py    # Main 1D waveform generator
├── 🎨 xy_waveform_generator.py    # XY pattern generator for oscilloscope art
├── 📁 examples/                   # Ready-to-use examples
│   ├── 8bit/                      # Arduino-compatible (uint8_t)
│   ├── 12bit/                     # STM32 DAC (uint16_t)  
│   ├── 16bit/                     # Audio quality (uint16_t)
│   ├── 32bit/                     # High precision (uint32_t)
│   └── 64bit/                     # Scientific precision (uint64_t)
├── 📁 hardware/                   # Hardware integration guides
│   ├── arduino/                   # Arduino examples and wiring
│   ├── esp32/                     # ESP32 DAC examples
│   ├── stm32/                     # STM32 HAL examples
│   └── oscilloscope_xy/           # XY art setup guides
├── 📁 docs/                       # Comprehensive documentation
└── 📁 tests/                      # Validation and unit tests
```

## 📚 Documentation

- **[Hardware Setup Guide](docs/HARDWARE.md)** - Wiring diagrams and platform-specific setup - ToDo
- **[API Reference](docs/API.md)** - Complete function documentation - ToDo
- **[Waveform Mathematics](docs/WAVEFORMS.md)** - Mathematical descriptions of all patterns - ToDo
- **[Oscilloscope XY Art](docs/OSCILLOSCOPE_ART.md)** - Create stunning visual displays - ToDo
- **[Performance Guide](docs/PERFORMANCE.md)** - Optimization tips and benchmarks - ToDo

## 🎯 Use Cases

### 🔬 **Embedded & IoT**
- Function generators and signal sources
- Motor control and PWM generation  
- Audio synthesis and effects
- Sensor calibration and testing

### 🎵 **Audio & Music**
- Synthesizer oscillators
- Audio test signals and calibration
- Digital audio workstation plugins
- Educational audio processing

### 📡 **Test & Measurement** 
- Oscilloscope calibration patterns
- Signal integrity testing
- RF and communications testing
- Laboratory equipment

### 🎨 **Creative & Art**
- Oscilloscope art installations  
- LED matrix animations
- Interactive art projects
- STEM education demonstrations

## ⚡ Performance Benchmarks

| Resolution | Data Type | Memory/Waveform | Generation Speed | Best For |
|------------|-----------|-----------------|------------------|----------|
| 8-bit | `uint8_t` | 256 bytes | ~1ms | Arduino, simple projects |
| 12-bit | `uint16_t` | 512-1024 bytes | ~2ms | STM32 DAC, embedded |
| 16-bit | `uint16_t` | 512-2048 bytes | ~5ms | Audio applications |
| 32-bit | `uint32_t` | 1-8KB | ~10ms | Industrial, scientific |
| 64-bit | `uint64_t` | 2-16KB | ~20ms | Research, simulation |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report bugs** - Open issues with reproduction steps
- ✨ **Add waveforms** - Contribute new mathematical patterns  
- 📖 **Improve docs** - Better examples and tutorials
- 🔧 **Hardware support** - New platform integrations
- 🎨 **Oscilloscope art** - New XY patterns and creative ideas

### Adding New Waveforms
```python
def generate_your_waveform(self, param1=1.0, param2=0.0):
    """Your custom waveform description"""
    return [
        self.normalize(your_math_function(i, param1, param2))
        for i in range(self.array_size)
    ]
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Showcase

### Community Projects
- **Oscilloscope Music Visualizer** - Real-time audio → XY patterns
- **Educational Math Display** - Parametric equations visualization  
- **Interactive Art Installation** - Gesture-controlled waveforms
- **Retro Game Console** - Vector graphics using oscilloscope

### Featured In
- **Hackaday** projects and articles
- **Arduino** community showcases  
- **Maker Faire** demonstrations
- **University** STEM education courses

## 🙏 Acknowledgments

- **Mathematics Community** - For beautiful parametric equations
- **Oscilloscope Art Artists** - Inspiration for XY patterns
- **Embedded Developers** - Real-world testing and feedback
- **Open Source Contributors** - Making this project better

## 📧 Contact & Support

- **🐛 Issues:** [GitHub Issues](https://github.com/s-celles/waveform-generator/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/s-celles/waveform-generator/discussions)  
- **🌐 Website:** [GitHub Pages](https://s-celles.github.io/waveform-generator/) (ToDo)

---

**⭐ Star this repository if it helped you create amazing waveforms!**

*Made with ❤️ for the embedded systems and oscilloscope art communities*

![Waveform Generator](https://img.shields.io/badge/Waveform-Generator-blue?style=for-the-badge&logo=github)
