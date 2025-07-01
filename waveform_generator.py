#!/usr/bin/env python3
"""
Waveform Generator for C Arrays
Generates C header files with waveform lookup tables for any bit depth.

Usage:
    python waveform_generator.py --bits 12 --size 256 --output waveforms_12bit.h
    python waveform_generator.py --bits 8 --size 1024 --waves sine,triangle,heart
"""

import argparse
import math
import sys
from typing import List, Callable, Tuple
from pathlib import Path

class WaveformGenerator:
    def __init__(self, bits: int = 8, array_size: int = 256):
        self.bits = bits
        self.array_size = array_size
        self.max_value = (2 ** bits) - 1
        self.data_type = self._get_data_type()
        
    def _get_data_type(self) -> str:
        """Détermine le type de données C approprié selon le nombre de bits"""
        if self.bits <= 8:
            return "uint8_t"
        elif self.bits <= 16:
            return "uint16_t"
        elif self.bits <= 32:
            return "uint32_t"
        else:
            raise ValueError(f"Nombre de bits non supporté: {self.bits}")
    
    def normalize(self, value: float) -> int:
        """Normalise une valeur [-1, 1] vers [0, max_value]"""
        normalized = round((value + 1) * self.max_value / 2)
        return max(0, min(self.max_value, normalized))
    
    def generate_sine(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une onde sinusoïdale"""
        return [
            self.normalize(amplitude * math.sin(2 * math.pi * frequency * i / self.array_size + phase))
            for i in range(self.array_size)
        ]
    
    def generate_triangle(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une onde triangulaire"""
        return [
            self.normalize(amplitude * (2 / math.pi) * math.asin(math.sin(2 * math.pi * frequency * i / self.array_size + phase)))
            for i in range(self.array_size)
        ]
    
    def generate_square(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une onde carrée"""
        return [
            self.normalize(amplitude * (1 if math.sin(2 * math.pi * frequency * i / self.array_size + phase) >= 0 else -1))
            for i in range(self.array_size)
        ]
    
    def generate_sawtooth(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une onde en dent de scie"""
        return [
            self.normalize(amplitude * (2 * ((frequency * i / self.array_size + phase / (2 * math.pi)) % 1) - 1))
            for i in range(self.array_size)
        ]
    
    def generate_linear_ramp(self) -> List[int]:
        """Génère une rampe linéaire parfaite de 0 à max_value"""
        return [round(i * self.max_value / (self.array_size - 1)) for i in range(self.array_size)]
    
    def generate_heart(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une courbe en forme de cœur"""
        result = []
        for i in range(self.array_size):
            t = 2 * math.pi * frequency * i / self.array_size + phase
            try:
                value = amplitude * math.cos(t) * (math.sin(t) * math.sqrt(abs(math.cos(t)))) / (math.sin(t) + 1.4)
                if not math.isfinite(value):
                    value = 0
            except:
                value = 0
            result.append(self.normalize(value))
        return result
    
    def generate_flower(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0, petals: int = 5) -> List[int]:
        """Génère une courbe en forme de fleur"""
        return [
            self.normalize(amplitude * math.sin(petals * (2 * math.pi * frequency * i / self.array_size + phase)) * 
                         math.cos(2 * math.pi * frequency * i / self.array_size + phase))
            for i in range(self.array_size)
        ]
    
    def generate_spiral(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une spirale d'Archimède"""
        return [
            self.normalize(amplitude * (2 * math.pi * frequency * i / self.array_size + phase) / (2 * math.pi) * 
                         math.sin((2 * math.pi * frequency * i / self.array_size + phase) * 3))
            for i in range(self.array_size)
        ]
    
    def generate_butterfly(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère une courbe papillon"""
        result = []
        for i in range(self.array_size):
            t = 2 * math.pi * frequency * i / self.array_size + phase
            try:
                value = amplitude * math.sin(t) * (math.exp(math.cos(t)) - 2 * math.cos(4 * t) - math.pow(math.sin(t / 12), 5)) / 3
                if not math.isfinite(value):
                    value = 0
                value = max(-2, min(2, value))  # Clamp avant normalisation
            except:
                value = 0
            result.append(self.normalize(value))
        return result
    
    def generate_lissajous(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0, ratio_a: int = 3, ratio_b: int = 2) -> List[int]:
        """Génère une courbe de Lissajous"""
        return [
            self.normalize(amplitude * math.sin(ratio_a * (2 * math.pi * frequency * i / self.array_size + phase)) * 
                         math.cos(ratio_b * (2 * math.pi * frequency * i / self.array_size + phase)))
            for i in range(self.array_size)
        ]
    
    def generate_chaos(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0) -> List[int]:
        """Génère un signal chaotique"""
        return [
            self.normalize(amplitude * math.sin(2 * math.pi * frequency * i / self.array_size + phase) * 
                         math.sin(math.sqrt(2) * (2 * math.pi * frequency * i / self.array_size + phase)) * 
                         math.sin(math.sqrt(3) * (2 * math.pi * frequency * i / self.array_size + phase)))
            for i in range(self.array_size)
        ]
    
    def generate_pulse(self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0, duty_cycle: float = 0.1) -> List[int]:
        """Génère un train d'impulsions"""
        return [
            self.normalize(amplitude if ((frequency * i / self.array_size + phase / (2 * math.pi)) % 1) < duty_cycle else -amplitude)
            for i in range(self.array_size)
        ]
    
    def generate_noise(self, amplitude: float = 1.0, seed: int = 12345) -> List[int]:
        """Génère du bruit pseudo-aléatoire"""
        import random
        random.seed(seed)
        return [
            self.normalize(amplitude * (2 * random.random() - 1))
            for _ in range(self.array_size)
        ]

class HeaderGenerator:
    def __init__(self, generator: WaveformGenerator):
        self.gen = generator
        
    def format_array(self, data: List[int], name: str, description: str) -> str:
        """Formate un tableau en C"""
        lines = [f"/**\n * @brief {description}\n */"]
        
        # En-tête du tableau
        lines.append(f"const {self.gen.data_type} {name}[WAVE_ARRAY_SIZE] = {{")
        
        # Données formatées par lignes de 16
        for i in range(0, len(data), 16):
            line_data = data[i:i+16]
            formatted_values = [f"{val:>{len(str(self.gen.max_value))}}" for val in line_data]
            line = "  " + ", ".join(formatted_values)
            if i + 16 < len(data):
                line += ","
            lines.append(line)
        
        lines.append("};")
        return "\n".join(lines)
    
    def generate_header(self, waveforms: dict, filename: str) -> str:
        """Génère le fichier header complet"""
        header_parts = []
        
        # En-tête du fichier
        header_parts.append(f'''/**
 * @file {filename}
 * @brief Waveform library for {self.gen.bits}-bit DACs
 * @author Waveform Generator Script
 * @date Generated automatically using https://github.com/s-celles/waveform-generator/
 * 
 * This file contains {len(waveforms)} waveforms with {self.gen.array_size} {self.gen.bits}-bit values each.
 * Value range: 0 to {self.gen.max_value}
 * 
 * Usage example:
 *   #include "{filename}"
 *   
 *   for(int i = 0; i < WAVE_ARRAY_SIZE; i++) {{
 *       dac_output(sine_wave[i]);
 *       delay_us(100);
 *   }}
 */

#ifndef WAVEFORMS_H
#define WAVEFORMS_H

#include <stdint.h>

// Configuration constants
#define WAVE_ARRAY_SIZE {self.gen.array_size}
#define WAVE_BITS {self.gen.bits}
#define WAVE_MAX_VALUE {self.gen.max_value}

//=============================================================================
// WAVEFORM DATA
//=============================================================================
''')
        
        # Générer chaque waveform
        for name, (description, data) in waveforms.items():
            header_parts.append(self.format_array(data, f"{name}_wave", description))
            header_parts.append("")  # Ligne vide
        
        # Énumération et utilitaires
        wave_names = list(waveforms.keys())
        enum_values = [f"    WAVE_{name.upper()} = {i}," for i, name in enumerate(wave_names)]
        enum_values.append(f"    WAVE_COUNT = {len(wave_names)}  // Total number of waveforms")
        
        header_parts.append(f'''//=============================================================================
// UTILITY ENUMS AND ARRAYS
//=============================================================================

/**
 * @brief Waveform type enumeration
 */
typedef enum {{
{chr(10).join(enum_values)}
}} waveform_type_t;

/**
 * @brief Array of waveform pointers for easy access
 */
const {self.gen.data_type}* const waveforms[WAVE_COUNT] = {{
{chr(10).join(f"    {name}_wave," for name in wave_names)}
}};

/**
 * @brief Waveform names for debugging/display
 */
const char* const waveform_names[WAVE_COUNT] = {{
{chr(10).join(f'    "{name.replace("_", " ").title()} Wave",' for name in wave_names)}
}};

/**
 * @brief Get waveform value at specific index
 * @param type Waveform type (0 to WAVE_COUNT-1)
 * @param index Sample index (0 to WAVE_ARRAY_SIZE-1)
 * @return {self.gen.bits}-bit sample value (0-{self.gen.max_value})
 */
static inline {self.gen.data_type} get_waveform_sample(waveform_type_t type, uint16_t index) {{
    if (type >= WAVE_COUNT || index >= WAVE_ARRAY_SIZE) return {self.gen.max_value // 2}; // Return center value for invalid params
    return waveforms[type][index];
}}

#endif // WAVEFORMS_H

/*
 * Generated with:
 * - Bits: {self.gen.bits}
 * - Array size: {self.gen.array_size}
 * - Data type: {self.gen.data_type}
 * - Value range: 0-{self.gen.max_value}
 * - Waveforms: {len(waveforms)}
 */''')
        
        return "\n".join(header_parts)

def main():
    parser = argparse.ArgumentParser(description="Generate C waveform lookup tables")
    parser.add_argument("--bits", type=int, default=8, help="Number of bits for output values (8, 10, 12, 16)")
    parser.add_argument("--size", type=int, default=256, help="Array size (number of samples)")
    parser.add_argument("--output", type=str, default="waveforms.h", help="Output filename")
    parser.add_argument("--waves", type=str, default="all", help="Comma-separated list of waveforms to generate")
    parser.add_argument("--amplitude", type=float, default=1.0, help="Global amplitude multiplier")
    parser.add_argument("--frequency", type=float, default=1.0, help="Global frequency multiplier")
    parser.add_argument("--list", action="store_true", help="List available waveforms")
    
    args = parser.parse_args()
    
    # Créer le générateur
    try:
        generator = WaveformGenerator(args.bits, args.size)
        header_gen = HeaderGenerator(generator)
    except ValueError as e:
        print(f"Erreur: {e}")
        return 1
    
    # Définir les waveforms disponibles
    available_waveforms = {
        "sine": ("Classic sine wave", lambda: generator.generate_sine(args.amplitude, args.frequency)),
        "triangle": ("Triangle wave", lambda: generator.generate_triangle(args.amplitude, args.frequency)),
        "square": ("Square wave", lambda: generator.generate_square(args.amplitude, args.frequency)),
        "sawtooth": ("Sawtooth wave", lambda: generator.generate_sawtooth(args.amplitude, args.frequency)),
        "ramp": ("Linear ramp 0→max", lambda: generator.generate_linear_ramp()),
        "heart": ("Heart-shaped curve ❤️", lambda: generator.generate_heart(args.amplitude, args.frequency)),
        "flower": ("Flower pattern 🌸", lambda: generator.generate_flower(args.amplitude, args.frequency)),
        "spiral": ("Archimedean spiral", lambda: generator.generate_spiral(args.amplitude, args.frequency)),
        "butterfly": ("Butterfly curve 🦋", lambda: generator.generate_butterfly(args.amplitude, args.frequency)),
        "lissajous": ("Lissajous curve (3:2)", lambda: generator.generate_lissajous(args.amplitude, args.frequency)),
        "chaos": ("Chaotic signal 🌀", lambda: generator.generate_chaos(args.amplitude, args.frequency)),
        "pulse": ("Pulse train", lambda: generator.generate_pulse(args.amplitude, args.frequency)),
        "noise": ("Pseudo-random noise", lambda: generator.generate_noise(args.amplitude))
    }
    
    if args.list:
        print("Waveforms disponibles:")
        for name, (desc, _) in available_waveforms.items():
            print(f"  {name:<12} - {desc}")
        return 0
    
    # Sélectionner les waveforms à générer
    if args.waves == "all":
        selected_waves = available_waveforms
    else:
        wave_list = [w.strip() for w in args.waves.split(",")]
        selected_waves = {name: available_waveforms[name] for name in wave_list if name in available_waveforms}
        
        # Vérifier les waveforms invalides
        invalid = set(wave_list) - set(available_waveforms.keys())
        if invalid:
            print(f"Waveforms inconnues: {', '.join(invalid)}")
            print(f"Utilisez --list pour voir les options disponibles")
            return 1
    
    if not selected_waves:
        print("Aucune waveform sélectionnée")
        return 1
    
    # Générer les données
    print(f"Génération de {len(selected_waves)} waveforms...")
    print(f"Paramètres: {args.bits} bits, {args.size} échantillons, plage 0-{generator.max_value}")
    
    waveforms = {}
    for name, (description, func) in selected_waves.items():
        print(f"  Génération: {name}")
        data = func()
        
        # Vérification des valeurs
        min_val, max_val = min(data), max(data)
        if min_val < 0 or max_val > generator.max_value:
            print(f"    ⚠️  Attention: plage {min_val}-{max_val} (attendu: 0-{generator.max_value})")
        else:
            print(f"    ✅ Plage: {min_val}-{max_val}")
        
        waveforms[name] = (description, data)
    
    # Générer le fichier header
    header_content = header_gen.generate_header(waveforms, args.output)
    
    # Écrire le fichier
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(header_content)
        print(f"\n✅ Fichier généré: {args.output}")
        print(f"📊 Taille: {len(header_content)} caractères")
        
        # Statistiques
        total_samples = len(waveforms) * args.size
        total_bytes = total_samples * (args.bits // 8 if args.bits % 8 == 0 else (args.bits // 8) + 1)
        print(f"🔢 Total échantillons: {total_samples}")
        print(f"💾 Taille mémoire estimée: {total_bytes} bytes ({total_bytes/1024:.1f} KB)")
        
    except IOError as e:
        print(f"Erreur d'écriture: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
