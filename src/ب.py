from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]
file_path = PROJECT_ROOT / "data" / "raw" / "COMSOL_Complete_Research_Database (2).md"
text = file_path.read_text(encoding="utf-8")

keywords = [
    "NB | Table 6 | Mitral total stress",
    "LV | Table 14 | Mitral total stress, x component, balloon-assisted case",
    "BV | Table 14 | Mitral total stress, x component, balloon-assisted case",
]

for keyword in keywords:
    positions = [m.start() for m in re.finditer(re.escape(keyword), text)]

    print("\n" + "=" * 80)
    print(keyword)
    print("Number of occurrences:", len(positions))

    for i, pos in enumerate(positions, 1):
        print(f"\n--- Occurrence {i} ---")
        print(text[pos:pos + 2000])