#!/usr/bin/env python3
"""
XY Waveform Generator for Oscilloscope Art
Generates synchronized X,Y coordinate pairs for beautiful oscilloscope patterns.

Usage:
    python xy_waveform_generator.py --bits 8 --size 256 --pattern lissajous --output xy_patterns.h
    python xy_waveform_generator.py --list-patterns
"""

import argparse
import math
import sys
from typing import List, Tuple, Callable
from pathlib import Path

class XYWaveformGenerator:
    def __init__(self, bits: int = 8, array_size: int = 256):
        self.bits = bits
        self.array_size = array_size
        self.max_value = (2 ** bits) - 1
        self.center = self.max_value // 2
        self.data_type = self._get_data_type()
        
    def _get_data_type(self) -> str:
        """Détermine le type de données C approprié"""
        if self.bits <= 8:
            return "uint8_t"
        elif self.bits <= 16:
            return "uint16_t"
        elif self.bits <= 32:
            return "uint32_t"
        else:
            raise ValueError(f"Nombre de bits non supporté: {self.bits}")
    
    def normalize_xy(self, x: float, y: float) -> Tuple[int, int]:
        """Normalise une paire (x,y) de [-1,1] vers [0, max_value]"""
        x_norm = round((x + 1) * self.max_value / 2)
        y_norm = round((y + 1) * self.max_value / 2)
        x_norm = max(0, min(self.max_value, x_norm))
        y_norm = max(0, min(self.max_value, y_norm))
        return x_norm, y_norm
    
    # ========================================================================
    # COURBES CLASSIQUES
    # ========================================================================
    
    def generate_circle(self, radius: float = 0.8, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère un cercle parfait"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            x = radius * math.cos(t)
            y = radius * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_ellipse(self, a: float = 0.8, b: float = 0.6, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère une ellipse"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            x = a * math.cos(t)
            y = b * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    # ========================================================================
    # COURBES DE LISSAJOUS
    # ========================================================================
    
    def generate_lissajous(self, freq_x: int = 3, freq_y: int = 2, phase: float = 0.0, 
                          amplitude: float = 0.8) -> Tuple[List[int], List[int]]:
        """Génère des courbes de Lissajous classiques"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size
            x = amplitude * math.sin(freq_x * t + phase)
            y = amplitude * math.sin(freq_y * t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_lissajous_cos(self, freq_x: int = 3, freq_y: int = 2, phase: float = 0.0,
                              amplitude: float = 0.8) -> Tuple[List[int], List[int]]:
        """Lissajous avec cosinus pour des patterns différents"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size
            x = amplitude * math.cos(freq_x * t + phase)
            y = amplitude * math.sin(freq_y * t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    # ========================================================================
    # COURBES ARTISTIQUES
    # ========================================================================
    
    def generate_heart(self, scale: float = 0.1, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère un cœur mathématique parfait ❤️"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            # Équation paramétrique du cœur
            x = scale * 16 * math.sin(t)**3
            y = scale * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_rose(self, petals: int = 5, scale: float = 0.8, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère une rose à n pétales 🌹"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            # Rose polaire: r = cos(k*θ)
            r = scale * math.cos(petals * t)
            x = r * math.cos(t)
            y = r * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_butterfly(self, scale: float = 0.3, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère un papillon mathématique 🦋"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            # Courbe papillon de Temple Fay
            x = scale * math.sin(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t) - math.sin(t/12)**5)
            y = scale * math.cos(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t) - math.sin(t/12)**5)
            # Clamp pour éviter les valeurs extrêmes
            x = max(-1, min(1, x))
            y = max(-1, min(1, y))
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_infinity(self, scale: float = 0.8, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Génère le symbole infini ∞"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            # Lemniscate de Bernoulli
            denominator = 1 + math.sin(t)**2
            x = scale * math.cos(t) / denominator
            y = scale * math.sin(t) * math.cos(t) / denominator
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    # ========================================================================
    # SPIRALES ET COURBES COMPLEXES
    # ========================================================================
    
    def generate_spiral_archimedes(self, turns: float = 3.0, scale: float = 0.8, 
                                  phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Spirale d'Archimède"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = turns * 2 * math.pi * i / self.array_size + phase
            r = scale * t / (turns * 2 * math.pi)
            x = r * math.cos(t)
            y = r * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_spiral_logarithmic(self, scale: float = 0.1, growth: float = 0.2,
                                   phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Spirale logarithmique (coquille nautile)"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 4 * math.pi * i / self.array_size + phase
            r = scale * math.exp(growth * t)
            r = min(r, 1.0)  # Limiter la croissance
            x = r * math.cos(t)
            y = r * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_hypotrochoid(self, R: float = 5, r: float = 3, d: float = 5,
                             scale: float = 0.15, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Hypotrochoïde (spirographe)"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            # Équations paramétriques de l'hypotrochoïde
            x = scale * ((R - r) * math.cos(t) + d * math.cos((R - r) * t / r))
            y = scale * ((R - r) * math.sin(t) - d * math.sin((R - r) * t / r))
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    # ========================================================================
    # COURBES SCIENTIFIQUES ET TECHNIQUES
    # ========================================================================
    
    def generate_rhodonea(self, k: float = 2.5, scale: float = 0.8, 
                         phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Rhodonéa (courbe rose généralisée)"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            r = scale * math.cos(k * t)
            x = r * math.cos(t)
            y = r * math.sin(t)
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_cycloid(self, radius: float = 0.2, scale: float = 1.0,
                        phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Cycloïde (courbe tracée par un point sur un cercle qui roule)"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 4 * math.pi * i / self.array_size + phase
            x = scale * radius * (t - math.sin(t))
            y = scale * radius * (1 - math.cos(t))
            # Centrer et normaliser
            x = (x / (4 * math.pi * radius)) * 2 - 1
            y = (y / (2 * radius)) - 1
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    def generate_astroid(self, scale: float = 0.8, phase: float = 0.0) -> Tuple[List[int], List[int]]:
        """Astroïde (hypocycloïde à 4 branches)"""
        x_vals, y_vals = [], []
        for i in range(self.array_size):
            t = 2 * math.pi * i / self.array_size + phase
            x = scale * math.cos(t)**3
            y = scale * math.sin(t)**3
            x_norm, y_norm = self.normalize_xy(x, y)
            x_vals.append(x_norm)
            y_vals.append(y_norm)
        return x_vals, y_vals
    
    # ========================================================================
    # PATTERNS ANIMÉS ET DYNAMIQUES
    # ========================================================================
    
    def generate_animated_lissajous(self, frame: int = 0, frames_total: int = 60) -> Tuple[List[int], List[int]]:
        """Lissajous animée avec phase qui change"""
        phase = 2 * math.pi * frame / frames_total
        return self.generate_lissajous(3, 2, phase, 0.8)
    
    def generate_breathing_circle(self, frame: int = 0, frames_total: int = 60) -> Tuple[List[int], List[int]]:
        """Cercle qui respire (rayon variable)"""
        radius = 0.5 + 0.3 * math.sin(2 * math.pi * frame / frames_total)
        return self.generate_circle(radius, 0)
    
    def generate_rotating_rose(self, petals: int = 5, frame: int = 0, 
                              frames_total: int = 60) -> Tuple[List[int], List[int]]:
        """Rose qui tourne"""
        phase = 2 * math.pi * frame / frames_total
        return self.generate_rose(petals, 0.8, phase)

class XYHeaderGenerator:
    def __init__(self, generator: XYWaveformGenerator):
        self.gen = generator
        
    def format_xy_arrays(self, x_data: List[int], y_data: List[int], 
                        name: str, description: str) -> str:
        """Formate les tableaux X,Y en C"""
        lines = [f"/**\n * @brief {description}\n */"]
        
        # Tableau X
        lines.append(f"const {self.gen.data_type} {name}_x[XY_ARRAY_SIZE] = {{")
        for i in range(0, len(x_data), 16):
            line_data = x_data[i:i+16]
            formatted_values = [f"{val:>{len(str(self.gen.max_value))}}" for val in line_data]
            line = "  " + ", ".join(formatted_values)
            if i + 16 < len(x_data):
                line += ","
            lines.append(line)
        lines.append("};")
        lines.append("")
        
        # Tableau Y
        lines.append(f"const {self.gen.data_type} {name}_y[XY_ARRAY_SIZE] = {{")
        for i in range(0, len(y_data), 16):
            line_data = y_data[i:i+16]
            formatted_values = [f"{val:>{len(str(self.gen.max_value))}}" for val in line_data]
            line = "  " + ", ".join(formatted_values)
            if i + 16 < len(y_data):
                line += ","
            lines.append(line)
        lines.append("};")
        
        return "\n".join(lines)
    
    def generate_header(self, patterns: dict, filename: str) -> str:
        """Génère le fichier header XY complet"""
        header_parts = []
        
        # En-tête du fichier
        header_parts.append(f'''/**
 * @file {filename}
 * @brief XY Waveform library for oscilloscope art
 * @author XY Waveform Generator Script
 * @date Generated automatically using Python script from https://github.com/s-celles/waveform-generator/
 * 
 * This file contains {len(patterns)} XY pattern pairs for {self.gen.bits}-bit DACs.
 * Perfect for oscilloscope XY mode, dual DAC output, or vector displays.
 * 
 * Hardware setup:
 * - Connect DAC1 to oscilloscope X input
 * - Connect DAC2 to oscilloscope Y input  
 * - Set oscilloscope to XY mode
 * - Enjoy the patterns!
 * 
 * Usage example:
 *   #include "{filename}"
 *   
 *   for(int i = 0; i < XY_ARRAY_SIZE; i++) {{
 *       dac1_output(heart_x[i]);     // X coordinate
 *       dac2_output(heart_y[i]);     // Y coordinate
 *       delay_us(100);
 *   }}
 */

#ifndef XY_WAVEFORMS_H
#define XY_WAVEFORMS_H

#include <stdint.h>

// Configuration constants
#define XY_ARRAY_SIZE {self.gen.array_size}
#define XY_BITS {self.gen.bits}
#define XY_MAX_VALUE {self.gen.max_value}
#define XY_CENTER {self.gen.center}

typedef enum {
    XY_OK = 0,
    XY_NULL_POINTER_ERROR,
} xy_status_t;

//=============================================================================
// XY PATTERN DATA
//=============================================================================
''')
        
        # Générer chaque pattern XY
        for name, (description, x_data, y_data) in patterns.items():
            header_parts.append(self.format_xy_arrays(x_data, y_data, name, description))
            header_parts.append("")
        
        # Énumération et utilitaires
        pattern_names = list(patterns.keys())
        enum_values = [f"    XY_{name.upper()} = {i}," for i, name in enumerate(pattern_names)]
        enum_values.append(f"    XY_PATTERN_COUNT = {len(pattern_names)}  // Total number of patterns")
        
        header_parts.append(f'''//=============================================================================
// UTILITY ENUMS AND ARRAYS
//=============================================================================

/**
 * @brief XY Pattern type enumeration
 */
typedef enum {{
{chr(10).join(enum_values)}
}} xy_pattern_type_t;

/**
 * @brief XY coordinate structure
 */
typedef struct {{
    {self.gen.data_type} x;
    {self.gen.data_type} y;
}} xy_point_t;

/**
 * @brief Array of X coordinate pointers
 */
const {self.gen.data_type}* const xy_patterns_x[XY_PATTERN_COUNT] = {{
{chr(10).join(f"    {name}_x," for name in pattern_names)}
}};

/**
 * @brief Array of Y coordinate pointers  
 */
const {self.gen.data_type}* const xy_patterns_y[XY_PATTERN_COUNT] = {{
{chr(10).join(f"    {name}_y," for name in pattern_names)}
}};

/**
 * @brief Pattern names for debugging/display
 */
const char* const xy_pattern_names[XY_PATTERN_COUNT] = {{
{chr(10).join(f'    "{name.replace("_", " ").title()}",' for name in pattern_names)}
}};

/**
 * @brief Get XY coordinates at specific index
 * @param pattern Pattern type (0 to XY_PATTERN_COUNT-1)
 * @param index Sample index (0 to XY_ARRAY_SIZE-1)
 * @return XY point structure with coordinates
 */
static inline xy_point_t get_xy_point(xy_pattern_type_t pattern, uint16_t index) {{
    xy_point_t point = {{XY_CENTER, XY_CENTER}};
    if (pattern < XY_PATTERN_COUNT && index < XY_ARRAY_SIZE) {{
        point.x = xy_patterns_x[pattern][index];
        point.y = xy_patterns_y[pattern][index];
    }}
    return point;
}}

/**
 * @brief Output XY pattern to dual DACs
 * @param pattern Pattern to output
 * @param dac_x_func Function pointer for X DAC output
 * @param dac_y_func Function pointer for Y DAC output
 * @param delay_us Delay between samples in microseconds
 */
static inline xy_status_t output_xy_pattern(xy_pattern_type_t pattern,
                                   void (*dac_x_func)({self.gen.data_type}),
                                   void (*dac_y_func)({self.gen.data_type}),
                                   uint16_t delay_us) {{
    if (dac_x_func == NULL || dac_y_func == NULL) {
        return XY_NULL_POINTER_ERROR;
    }
    for (uint16_t i = 0; i < XY_ARRAY_SIZE; i++) {{
        xy_point_t point = get_xy_point(pattern, i);
        dac_x_func(point.x);
        dac_y_func(point.y);
        // delay_microseconds(delay_us);  // Implement your delay function
    }}
    return XY_OK;
}}

#endif // XY_WAVEFORMS_H

/*
 * Generated with XY Waveform Generator:
 * - Bits: {self.gen.bits}
 * - Array size: {self.gen.array_size}
 * - Data type: {self.gen.data_type}
 * - Value range: 0-{self.gen.max_value}
 * - Patterns: {len(patterns)}
 * 
 * Perfect for oscilloscope art and vector displays!
 */''')
        
        return "\n".join(header_parts)

def main():
    parser = argparse.ArgumentParser(description="Generate XY waveform patterns for oscilloscope art")
    parser.add_argument("--bits", type=int, default=8, help="Number of bits for output values")
    parser.add_argument("--size", type=int, default=256, help="Array size (number of samples)")
    parser.add_argument("--output", type=str, default="xy_patterns.h", help="Output filename")
    parser.add_argument("--patterns", type=str, default="all", help="Comma-separated list of patterns to generate")
    parser.add_argument("--list-patterns", action="store_true", help="List available patterns")
    
    args = parser.parse_args()
    
    # Créer le générateur
    try:
        generator = XYWaveformGenerator(args.bits, args.size)
        header_gen = XYHeaderGenerator(generator)
    except ValueError as e:
        print(f"Erreur: {e}")
        return 1
    
    # Définir les patterns disponibles
    available_patterns = {
        # Classiques
        "circle": ("Perfect circle", lambda: generator.generate_circle()),
        "ellipse": ("Ellipse", lambda: generator.generate_ellipse()),
        
        # Lissajous
        "lissajous_3_2": ("Lissajous 3:2", lambda: generator.generate_lissajous(3, 2)),
        "lissajous_5_4": ("Lissajous 5:4", lambda: generator.generate_lissajous(5, 4)),
        "lissajous_7_5": ("Lissajous 7:5", lambda: generator.generate_lissajous(7, 5)),
        "lissajous_cos": ("Lissajous cosine", lambda: generator.generate_lissajous_cos(3, 2)),
        
        # Artistiques
        "heart": ("Mathematical heart ❤️", lambda: generator.generate_heart()),
        "rose_3": ("3-petal rose 🌹", lambda: generator.generate_rose(3)),
        "rose_5": ("5-petal rose 🌹", lambda: generator.generate_rose(5)),
        "rose_8": ("8-petal rose 🌹", lambda: generator.generate_rose(8)),
        "butterfly": ("Butterfly curve 🦋", lambda: generator.generate_butterfly()),
        "infinity": ("Infinity symbol ∞", lambda: generator.generate_infinity()),
        
        # Spirales
        "spiral_archimedes": ("Archimedes spiral", lambda: generator.generate_spiral_archimedes()),
        "spiral_log": ("Logarithmic spiral", lambda: generator.generate_spiral_logarithmic()),
        
        # Techniques
        "hypotrochoid": ("Hypotrochoid (spirograph)", lambda: generator.generate_hypotrochoid()),
        "rhodonea": ("Rhodonea curve", lambda: generator.generate_rhodonea()),
        "cycloid": ("Cycloid curve", lambda: generator.generate_cycloid()),
        "astroid": ("Astroid (4-pointed star)", lambda: generator.generate_astroid()),
    }
    
    if args.list_patterns:
        print("Patterns XY disponibles:")
        for name, (desc, _) in available_patterns.items():
            print(f"  {name:<20} - {desc}")
        return 0
    
    # Sélectionner les patterns à générer
    if args.patterns == "all":
        selected_patterns = available_patterns
    else:
        pattern_list = [p.strip() for p in args.patterns.split(",")]
        selected_patterns = {name: available_patterns[name] for name in pattern_list if name in available_patterns}
        
        invalid = set(pattern_list) - set(available_patterns.keys())
        if invalid:
            print(f"Patterns inconnus: {', '.join(invalid)}")
            print(f"Utilisez --list-patterns pour voir les options disponibles")
            return 1
    
    if not selected_patterns:
        print("Aucun pattern sélectionné")
        return 1
    
    # Générer les données XY
    print(f"Génération de {len(selected_patterns)} patterns XY...")
    print(f"Paramètres: {args.bits} bits, {args.size} échantillons")
    
    patterns = {}
    for name, (description, func) in selected_patterns.items():
        print(f"  Génération: {name}")
        x_data, y_data = func()
        
        # Vérification des valeurs
        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        print(f"    X: {x_min}-{x_max}, Y: {y_min}-{y_max}")
        
        patterns[name] = (description, x_data, y_data)
    
    # Générer le fichier header
    header_content = header_gen.generate_header(patterns, args.output)
    
    # Écrire le fichier
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(header_content)
        print(f"\n✅ Fichier XY généré: {args.output}")
        print(f"📊 Taille: {len(header_content)} caractères")
        
        # Statistiques
        total_points = len(patterns) * args.size * 2  # x2 pour X et Y
        total_bytes = total_points * (args.bits // 8 if args.bits % 8 == 0 else (args.bits // 8) + 1)
        print(f"🔢 Total points XY: {total_points}")
        print(f"💾 Taille mémoire estimée: {total_bytes} bytes ({total_bytes/1024:.1f} KB)")
        
    except IOError as e:
        print(f"Erreur d'écriture: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
