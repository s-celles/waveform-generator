#!/usr/bin/env python3
"""
Waveform Generator for C Arrays (Template Version)
Generates C header files with waveform lookup tables for any bit depth.

Usage:
    python waveform_generator.py --bits 12 --size 256 --output waveforms_12bit.h
    python waveform_generator.py --bits 8 --size 1024 --waves sine,triangle,heart
    
Requirements:
    pip install jinja2
    
Project structure:
    waveform_generator.py       # Main script
    templates/
        waveforms.h.j2          # Main C header template
        waveforms_simple.h.j2   # Simple template
        waveforms_arduino.h.j2  # Arduino template
    output/
        waveforms.h             # Generated C header
"""

import argparse
import math
import sys
from typing import List, Callable, Tuple
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template


class WaveformData:
    """Data structure for waveform information"""

    def __init__(self, description: str, data: List[int]):
        self.description = description
        self.data = data


class WaveformGenerator:
    def __init__(self, bits: int = 8, array_size: int = 256):
        self.bits = bits
        self.array_size = array_size
        self.max_value = (2**bits) - 1
        self.center = self.max_value // 2
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

    def generate_sine(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une onde sinusoïdale"""
        return [
            self.normalize(
                amplitude
                * math.sin(2 * math.pi * frequency * i / self.array_size + phase)
            )
            for i in range(self.array_size)
        ]

    def generate_triangle(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une onde triangulaire"""
        return [
            self.normalize(
                amplitude
                * (2 / math.pi)
                * math.asin(
                    math.sin(2 * math.pi * frequency * i / self.array_size + phase)
                )
            )
            for i in range(self.array_size)
        ]

    def generate_square(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une onde carrée"""
        return [
            self.normalize(
                amplitude
                * (
                    1
                    if math.sin(2 * math.pi * frequency * i / self.array_size + phase)
                    >= 0
                    else -1
                )
            )
            for i in range(self.array_size)
        ]

    def generate_sawtooth(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une onde en dent de scie"""
        return [
            self.normalize(
                amplitude
                * (
                    2 * ((frequency * i / self.array_size + phase / (2 * math.pi)) % 1)
                    - 1
                )
            )
            for i in range(self.array_size)
        ]

    def generate_linear_ramp(self) -> List[int]:
        """Génère une rampe linéaire parfaite de 0 à max_value"""
        return [
            round(i * self.max_value / (self.array_size - 1))
            for i in range(self.array_size)
        ]

    def generate_heart(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une courbe en forme de cœur"""
        result = []
        for i in range(self.array_size):
            t = 2 * math.pi * frequency * i / self.array_size + phase
            try:
                value = (
                    amplitude
                    * math.cos(t)
                    * (math.sin(t) * math.sqrt(abs(math.cos(t))))
                    / (math.sin(t) + 1.4)
                )
                if not math.isfinite(value):
                    value = 0
            except:
                value = 0
            result.append(self.normalize(value))
        return result

    def generate_flower(
        self,
        amplitude: float = 1.0,
        frequency: float = 1.0,
        phase: float = 0.0,
        petals: int = 5,
    ) -> List[int]:
        """Génère une courbe en forme de fleur"""
        return [
            self.normalize(
                amplitude
                * math.sin(
                    petals * (2 * math.pi * frequency * i / self.array_size + phase)
                )
                * math.cos(2 * math.pi * frequency * i / self.array_size + phase)
            )
            for i in range(self.array_size)
        ]

    def generate_spiral(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une spirale d'Archimède"""
        return [
            self.normalize(
                amplitude
                * (2 * math.pi * frequency * i / self.array_size + phase)
                / (2 * math.pi)
                * math.sin((2 * math.pi * frequency * i / self.array_size + phase) * 3)
            )
            for i in range(self.array_size)
        ]

    def generate_butterfly(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère une courbe papillon"""
        result = []
        for i in range(self.array_size):
            t = 2 * math.pi * frequency * i / self.array_size + phase
            try:
                value = (
                    amplitude
                    * math.sin(t)
                    * (
                        math.exp(math.cos(t))
                        - 2 * math.cos(4 * t)
                        - math.pow(math.sin(t / 12), 5)
                    )
                    / 3
                )
                if not math.isfinite(value):
                    value = 0
                value = max(-2, min(2, value))  # Clamp avant normalisation
            except:
                value = 0
            result.append(self.normalize(value))
        return result

    def generate_lissajous(
        self,
        amplitude: float = 1.0,
        frequency: float = 1.0,
        phase: float = 0.0,
        ratio_a: int = 3,
        ratio_b: int = 2,
    ) -> List[int]:
        """Génère une courbe de Lissajous"""
        return [
            self.normalize(
                amplitude
                * math.sin(
                    ratio_a * (2 * math.pi * frequency * i / self.array_size + phase)
                )
                * math.cos(
                    ratio_b * (2 * math.pi * frequency * i / self.array_size + phase)
                )
            )
            for i in range(self.array_size)
        ]

    def generate_chaos(
        self, amplitude: float = 1.0, frequency: float = 1.0, phase: float = 0.0
    ) -> List[int]:
        """Génère un signal chaotique"""
        return [
            self.normalize(
                amplitude
                * math.sin(2 * math.pi * frequency * i / self.array_size + phase)
                * math.sin(
                    math.sqrt(2)
                    * (2 * math.pi * frequency * i / self.array_size + phase)
                )
                * math.sin(
                    math.sqrt(3)
                    * (2 * math.pi * frequency * i / self.array_size + phase)
                )
            )
            for i in range(self.array_size)
        ]

    def generate_pulse(
        self,
        amplitude: float = 1.0,
        frequency: float = 1.0,
        phase: float = 0.0,
        duty_cycle: float = 0.1,
    ) -> List[int]:
        """Génère un train d'impulsions"""
        return [
            self.normalize(
                amplitude
                if ((frequency * i / self.array_size + phase / (2 * math.pi)) % 1)
                < duty_cycle
                else -amplitude
            )
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

    def generate_exponential(
        self, amplitude: float = 1.0, rate: float = 2.0
    ) -> List[int]:
        """Génère une décroissance exponentielle"""
        return [
            self.normalize(amplitude * math.exp(-rate * i / self.array_size))
            for i in range(self.array_size)
        ]

    def generate_logarithmic(
        self, amplitude: float = 1.0, base: float = 10.0
    ) -> List[int]:
        """Génère une courbe logarithmique"""
        return [
            self.normalize(
                amplitude
                * math.log(1 + base * i / self.array_size)
                / math.log(1 + base)
            )
            for i in range(self.array_size)
        ]

    def generate_gaussian(
        self, amplitude: float = 1.0, center: float = 0.5, sigma: float = 0.2
    ) -> List[int]:
        """Génère une courbe gaussienne"""
        return [
            self.normalize(
                amplitude
                * math.exp(-0.5 * ((i / self.array_size - center) / sigma) ** 2)
            )
            for i in range(self.array_size)
        ]


class HeaderGenerator:
    def __init__(self, generator: WaveformGenerator, template_dir: str = "templates"):
        self.gen = generator
        self.template_dir = Path(template_dir)

        # Créer l'environnement Jinja2
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Ajouter les filtres personnalisés
        self.env.filters["batch"] = self._batch_filter

        # Vérifier si le dossier templates existe
        if not self.template_dir.exists():
            print(f"⚠️  Dossier templates manquant: {self.template_dir}")
            print(f"   Création du dossier...")
            self.template_dir.mkdir(parents=True, exist_ok=True)

    def _batch_filter(self, iterable, n, fill_with=None):
        """Jinja2 filter to batch items into chunks of n"""
        result = []
        for i in range(0, len(iterable), n):
            chunk = iterable[i : i + n]
            if fill_with is not None and len(chunk) < n:
                chunk.extend([fill_with] * (n - len(chunk)))
            result.append(chunk)
        return result

    def list_templates(self) -> List[str]:
        """Liste tous les templates disponibles"""
        if not self.template_dir.exists():
            return []

        templates = []
        for template_file in self.template_dir.glob("*.j2"):
            templates.append(template_file.name)
        return templates

    def load_template(self, template_name: str) -> Template:
        """Charge un template depuis le fichier"""
        try:
            return self.env.get_template(template_name)
        except TemplateNotFound:
            available = self.list_templates()
            if available:
                print(f"❌ Template '{template_name}' non trouvé.")
                print(f"   Templates disponibles: {', '.join(available)}")
            else:
                print(f"❌ Aucun template trouvé dans {self.template_dir}")
                print(f"   Créez un fichier template (ex: waveforms.h.j2)")
            raise

    def generate_header(
        self, waveforms: dict, filename: str, template_name: str = "waveforms.h.j2"
    ) -> str:
        """Génère le fichier header complet using Jinja2 template"""

        # Charger le template
        template = self.load_template(template_name)

        # Convert waveforms to WaveformData objects
        waveform_data = {}
        for name, (description, data) in waveforms.items():
            waveform_data[name] = WaveformData(description, data)

        # Render template with all needed variables
        return template.render(
            filename=filename,
            bits=self.gen.bits,
            array_size=self.gen.array_size,
            max_value=self.gen.max_value,
            center=self.gen.center,
            data_type=self.gen.data_type,
            waveforms=waveform_data,
        )


def setup_project_structure():
    """Crée la structure de projet recommandée"""
    directories = ["templates", "output", "examples"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    print("📁 Structure de projet créée:")
    print("   templates/     - Templates Jinja2 (.j2)")
    print("   output/        - Fichiers C générés (.h)")
    print("   examples/      - Exemples d'utilisation")


def main():
    parser = argparse.ArgumentParser(description="Generate C waveform lookup tables")
    parser.add_argument(
        "--bits",
        type=int,
        default=8,
        help="Number of bits for output values (8, 10, 12, 16)",
    )
    parser.add_argument(
        "--size", type=int, default=256, help="Array size (number of samples)"
    )
    parser.add_argument(
        "--output", type=str, default="output/waveforms.h", help="Output filename"
    )
    parser.add_argument(
        "--template", type=str, default="waveforms.h.j2", help="Template filename"
    )
    parser.add_argument(
        "--template-dir", type=str, default="templates", help="Templates directory"
    )
    parser.add_argument(
        "--waves",
        type=str,
        default="all",
        help="Comma-separated list of waveforms to generate",
    )
    parser.add_argument(
        "--amplitude", type=float, default=1.0, help="Global amplitude multiplier"
    )
    parser.add_argument(
        "--frequency", type=float, default=1.0, help="Global frequency multiplier"
    )
    parser.add_argument(
        "--list-waves", action="store_true", help="List available waveforms"
    )
    parser.add_argument(
        "--list-templates", action="store_true", help="List available templates"
    )
    parser.add_argument("--setup", action="store_true", help="Setup project structure")

    args = parser.parse_args()

    # Configuration du projet
    if args.setup:
        setup_project_structure()
        print("✅ Structure de projet créée avec succès!")
        return 0

    # Check if Jinja2 is available
    try:
        from jinja2 import Environment, FileSystemLoader, TemplateNotFound
    except ImportError:
        print("❌ Erreur: Jinja2 n'est pas installé. Utilisez: pip install jinja2")
        return 1

    # Créer le générateur
    try:
        generator = WaveformGenerator(args.bits, args.size)
        header_gen = HeaderGenerator(generator, args.template_dir)
    except ValueError as e:
        print(f"❌ Erreur: {e}")
        return 1

    # Lister les templates
    if args.list_templates:
        templates = header_gen.list_templates()
        if templates:
            print("📋 Templates disponibles:")
            for template in templates:
                print(f"   {template}")
        else:
            print(f"❌ Aucun template trouvé dans {args.template_dir}")
            print(f"   Utilisez --setup pour créer la structure de projet")
        return 0

    # Définir les waveforms disponibles
    available_waveforms = {
        # Formes d'onde classiques
        "sine": (
            "Classic sine wave",
            lambda: generator.generate_sine(args.amplitude, args.frequency),
        ),
        "triangle": (
            "Triangle wave",
            lambda: generator.generate_triangle(args.amplitude, args.frequency),
        ),
        "square": (
            "Square wave",
            lambda: generator.generate_square(args.amplitude, args.frequency),
        ),
        "sawtooth": (
            "Sawtooth wave",
            lambda: generator.generate_sawtooth(args.amplitude, args.frequency),
        ),
        "ramp": ("Linear ramp 0→max", lambda: generator.generate_linear_ramp()),
        # Formes d'onde artistiques
        "heart": (
            "Heart-shaped curve ❤️",
            lambda: generator.generate_heart(args.amplitude, args.frequency),
        ),
        "flower": (
            "Flower pattern 🌸",
            lambda: generator.generate_flower(args.amplitude, args.frequency),
        ),
        "spiral": (
            "Archimedean spiral",
            lambda: generator.generate_spiral(args.amplitude, args.frequency),
        ),
        "butterfly": (
            "Butterfly curve 🦋",
            lambda: generator.generate_butterfly(args.amplitude, args.frequency),
        ),
        "lissajous": (
            "Lissajous curve (3:2)",
            lambda: generator.generate_lissajous(args.amplitude, args.frequency),
        ),
        # Formes d'onde techniques
        "chaos": (
            "Chaotic signal 🌀",
            lambda: generator.generate_chaos(args.amplitude, args.frequency),
        ),
        "pulse": (
            "Pulse train",
            lambda: generator.generate_pulse(args.amplitude, args.frequency),
        ),
        "noise": (
            "Pseudo-random noise",
            lambda: generator.generate_noise(args.amplitude),
        ),
        "exponential": (
            "Exponential decay",
            lambda: generator.generate_exponential(args.amplitude),
        ),
        "logarithmic": (
            "Logarithmic curve",
            lambda: generator.generate_logarithmic(args.amplitude),
        ),
        "gaussian": (
            "Gaussian bell curve",
            lambda: generator.generate_gaussian(args.amplitude),
        ),
    }

    if args.list_waves:
        print("📋 Waveforms disponibles:")
        for name, (desc, _) in available_waveforms.items():
            print(f"   {name:<12} - {desc}")
        return 0

    # Sélectionner les waveforms à générer
    if args.waves == "all":
        selected_waves = available_waveforms
    else:
        wave_list = [w.strip() for w in args.waves.split(",")]
        selected_waves = {
            name: available_waveforms[name]
            for name in wave_list
            if name in available_waveforms
        }

        # Vérifier les waveforms invalides
        invalid = set(wave_list) - set(available_waveforms.keys())
        if invalid:
            print(f"❌ Waveforms inconnues: {', '.join(invalid)}")
            print(f"   Utilisez --list-waves pour voir les options disponibles")
            return 1

    if not selected_waves:
        print("❌ Aucune waveform sélectionnée")
        return 1

    # Générer les données
    print(f"🔄 Génération de {len(selected_waves)} waveforms...")
    print(
        f"   Paramètres: {args.bits} bits, {args.size} échantillons, plage 0-{generator.max_value}"
    )
    print(f"   Template: {args.template}")
    print(f"   Amplitude: {args.amplitude}, Fréquence: {args.frequency}")

    waveforms = {}
    for name, (description, func) in selected_waves.items():
        print(f"   Génération: {name}")
        data = func()

        # Vérification des valeurs
        min_val, max_val = min(data), max(data)
        if min_val < 0 or max_val > generator.max_value:
            print(
                f"     ⚠️  Attention: plage {min_val}-{max_val} (attendu: 0-{generator.max_value})"
            )
        else:
            print(f"     ✅ Plage: {min_val}-{max_val}")

        waveforms[name] = (description, data)

    # Générer le fichier header
    try:
        header_content = header_gen.generate_header(
            waveforms, Path(args.output).name, args.template
        )
    except TemplateNotFound:
        return 1
    except Exception as e:
        print(f"❌ Erreur lors de la génération du template: {e}")
        return 1

    # Créer le dossier de sortie si nécessaire
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Écrire le fichier
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header_content)
        print(f"\n✅ Fichier généré: {output_path}")
        print(f"📊 Taille: {len(header_content)} caractères")

        # Statistiques
        total_samples = len(waveforms) * args.size
        total_bytes = total_samples * (
            args.bits // 8 if args.bits % 8 == 0 else (args.bits // 8) + 1
        )
        print(f"🔢 Total échantillons: {total_samples}")
        print(
            f"💾 Taille mémoire estimée: {total_bytes} bytes ({total_bytes/1024:.1f} KB)"
        )

    except IOError as e:
        print(f"❌ Erreur d'écriture: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
