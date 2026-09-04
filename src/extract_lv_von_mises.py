import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# Left Ventricular von Mises Stress Analysis
# NB vs LV vs BV
# ============================================================

SOURCE = Path("COMSOL_Complete_Research_Database (2).md")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

print("Reading COMSOL database...")

text = SOURCE.read_text(encoding="utf-8")

# ------------------------------------------------------------
# Exact table headings
# ------------------------------------------------------------

tables = {
    "NB": "### NB Table 8 — Left-ventricular von Mises stress",
    "LV": "### LV Table 16 — Left-ventricular von Mises stress, balloon-assisted case",
    "BV": "### BV Table 16 — Left-ventricular von Mises stress, balloon-assisted case",
}

def extract_table(text, heading):
    start = text.find(heading)

    if start == -1:
        raise ValueError(f"Could not find table heading:\n{heading}")

    section = text[start:]

    # Stop at the next markdown heading
    next_heading = re.search(r"\n### ", section[len(heading):])

    if next_heading:
        section = section[:len(heading) + next_heading.start()]

    # Extract rows containing time and value
    rows = []

    for line in section.splitlines():
        line = line.strip()

        # Match markdown table rows
        if "|" not in line:
            continue

        cells = [c.strip() for c in line.strip("|").split("|")]

        if len(cells) < 2:
            continue

        try:
            time = float(cells[0])
            stress = float(cells[1])
            rows.append((time, stress))
        except ValueError:
            continue

    if not rows:
        raise ValueError(f"No numerical data found for:\n{heading}")

    df = pd.DataFrame(rows, columns=["time_s", "von_mises_stress_N_per_m"])

    return df


# ------------------------------------------------------------
# Extract NB / LV / BV
# ------------------------------------------------------------

print("Extracting NB...")
NB = extract_table(text, tables["NB"])

print("Extracting LV...")
LV = extract_table(text, tables["LV"])

print("Extracting BV...")
BV = extract_table(text, tables["BV"])


# ------------------------------------------------------------
# Save individual CSV files
# ------------------------------------------------------------

NB.to_csv(DATA_DIR / "NB_lv_von_mises_stress.csv", index=False)
LV.to_csv(DATA_DIR / "LV_lv_von_mises_stress.csv", index=False)
BV.to_csv(DATA_DIR / "BV_lv_von_mises_stress.csv", index=False)


# ------------------------------------------------------------
# Combined comparison
# ------------------------------------------------------------

comparison = pd.DataFrame({
    "time_s": NB["time_s"],
    "NB_stress_N_per_m": NB["von_mises_stress_N_per_m"],
    "LV_stress_N_per_m": LV["von_mises_stress_N_per_m"],
    "BV_stress_N_per_m": BV["von_mises_stress_N_per_m"],
})

comparison.to_csv(
    DATA_DIR / "NB_LV_BV_lv_von_mises_comparison.csv",
    index=False
)


# ------------------------------------------------------------
# Summary statistics
# ------------------------------------------------------------

def summarize(name, df, baseline_max=None):

    values = df["von_mises_stress_N_per_m"]

    max_idx = values.idxmax()
    min_idx = values.idxmin()

    maximum = values.max()
    minimum = values.min()
    mean = values.mean()

    max_time = df.loc[max_idx, "time_s"]
    min_time = df.loc[min_idx, "time_s"]

    result = {
        "Case": name,
        "N_points": len(df),
        "Mean_N_per_m": mean,
        "Min_N_per_m": minimum,
        "Min_time_s": min_time,
        "Max_N_per_m": maximum,
        "Max_time_s": max_time,
    }

    if baseline_max is not None:
        result["Peak_change_vs_NB_percent"] = (
            (maximum - baseline_max) / baseline_max * 100
        )
        result["Peak_ratio_vs_NB"] = maximum / baseline_max

    return result


NB_max = NB["von_mises_stress_N_per_m"].max()

summary = pd.DataFrame([
    summarize("NB", NB),
    summarize("LV", LV, NB_max),
    summarize("BV", BV, NB_max),
])

summary.to_csv(
    DATA_DIR / "lv_von_mises_summary.csv",
    index=False
)


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print()
print("=" * 65)
print("LEFT VENTRICULAR VON MISES STRESS ANALYSIS")
print("=" * 65)

print()
print("NB points:", len(NB))
print("LV points:", len(LV))
print("BV points:", len(BV))

print()
print("Summary:")
print(summary.to_string(index=False))

print()
print("Peak stress comparison:")
print(f"NB peak = {NB_max:.4f} N/m")
print(
    f"LV peak = {LV['von_mises_stress_N_per_m'].max():.4f} N/m "
    f"({LV['von_mises_stress_N_per_m'].max()/NB_max:.2f}x NB)"
)
print(
    f"BV peak = {BV['von_mises_stress_N_per_m'].max():.4f} N/m "
    f"({BV['von_mises_stress_N_per_m'].max()/NB_max:.2f}x NB)"
)


# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    NB["time_s"],
    NB["von_mises_stress_N_per_m"],
    label="NB — Baseline"
)

plt.plot(
    LV["time_s"],
    LV["von_mises_stress_N_per_m"],
    label="LV — LV balloon"
)

plt.plot(
    BV["time_s"],
    BV["von_mises_stress_N_per_m"],
    label="BV — Biventricular balloon"
)

plt.xlabel("Time (s)")
plt.ylabel("Left Ventricular von Mises Stress (N/m)")
plt.title("Left Ventricular von Mises Stress: NB vs LV vs BV")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    DATA_DIR / "NB_LV_BV_lv_von_mises_stress.png",
    dpi=300
)

plt.show()


print()
print("Files created:")
print("  data/NB_lv_von_mises_stress.csv")
print("  data/LV_lv_von_mises_stress.csv")
print("  data/BV_lv_von_mises_stress.csv")
print("  data/NB_LV_BV_lv_von_mises_comparison.csv")
print("  data/lv_von_mises_summary.csv")
print("  data/NB_LV_BV_lv_von_mises_stress.png")
print()
print("Done successfully!")