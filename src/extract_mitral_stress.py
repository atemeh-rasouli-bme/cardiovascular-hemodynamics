from pathlib import Path
import re

file_path = Path(
    r"C:\Users\novin.toos\Desktop\cardiovascular-hemodynamics"
    r"\COMSOL_Complete_Research_Database (2).md"
)

text = file_path.read_text(encoding="utf-8")

patterns = [
    "Mitral total stress",
    "Mitral total stress, x component",
    "NB-T232",
    "LV-T",
    "BV-T"
]

for pattern in patterns:
    print("\n" + "=" * 80)
    print("SEARCH:", pattern)

    matches = list(re.finditer(re.escape(pattern), text, re.IGNORECASE))
    print("Occurrences:", len(matches))

    for i, match in enumerate(matches[:10], 1):
        start = max(0, match.start() - 300)
        end = min(len(text), match.start() + 1200)

        print(f"\n--- Match {i} ---")
        print(text[start:end])