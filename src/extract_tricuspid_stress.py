import os
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# Configuration
# ============================================================

SOURCE_FILE = "COMSOL_Complete_Research_Database (2).md"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# Extract COMSOL table from Markdown
# ============================================================

def extract_table(text, heading):
    start = text.find(heading)

    if start == -1:
        raise ValueError(f"Heading not found:\n{heading}")

    section = text[start + len(heading):]
    lines = section.splitlines()

    data = []

    for line in lines:
        line = line.strip()

        if line.startswith("#"):
            break

        if not line:
            if data:
                break
            continue

        if line.startswith("| Time"):
            continue

        if line.startswith("| ---"):
            continue

        if line.startswith("|"):
            parts = [p.strip() for p in line.strip("|").split("|")]

            if len(parts) >= 2:
                try:
                    time = float(parts[0])
                    stress = float(parts[1])

                    data.append({
                        "Time_s": time,
                        "Tricuspid_Total_Stress_X_N_per_m": stress
                    })

                except ValueError:
                    continue

    if not data:
        raise ValueError(f"No numerical data found for:\n{heading}")

    return pd.DataFrame(data)


# ============================================================
# Read COMSOL database
# ============================================================

print("\nReading COMSOL database...")

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    text = f.read()


# ============================================================
# Exact source tables
# ============================================================

NB_HEADING = (
    "### NB Table 7 — Tricuspid total stress, x component "
    "— exact source table NB-T232"
)

LV_HEADING = (
    "### LV Table 15 — Tricuspid total stress, x component, "
    "balloon-assisted case — exact source table LV-T273"
)

BV_HEADING = (
    "### BV Table 15 — Tricuspid total stress, x component, "
    "balloon-assisted case — exact source table BV-T273"
)


# ============================================================
# Extract data
# ============================================================

print("Extracting NB...")
NB = extract_table(text, NB_HEADING)

print("Extracting LV...")
LV = extract_table(text, LV_HEADING)

print("Extracting BV...")
BV = extract_table(text, BV_HEADING)


# ============================================================
# Save individual CSV files
# ============================================================

NB.to_csv(
    os.path.join(DATA_DIR, "NB_tricuspid_stress_x.csv"),
    index=False
)

LV.to_csv(
    os.path.join(DATA_DIR, "LV_tricuspid_stress_x.csv"),
    index=False
)

BV.to_csv(
    os.path.join(DATA_DIR, "BV_tricuspid_stress_x.csv"),
    index=False
)


# ============================================================
# Create comparison CSV
# ============================================================

comparison = pd.DataFrame({
    "Time_s": NB["Time_s"],
    "NB_N_per_m": NB["Tricuspid_Total_Stress_X_N_per_m"],
    "LV_N_per_m": LV["Tricuspid_Total_Stress_X_N_per_m"],
    "BV_N_per_m": BV["Tricuspid_Total_Stress_X_N_per_m"]
})

comparison.to_csv(
    os.path.join(
        DATA_DIR,
        "NB_LV_BV_tricuspid_stress_x_comparison.csv"
    ),
    index=False
)


# ============================================================
# Statistical summary
# ============================================================

def calculate_summary(name, df):

    values = df["Tricuspid_Total_Stress_X_N_per_m"]

    max_idx = values.idxmax()
    min_idx = values.idxmin()
    abs_peak_idx = values.abs().idxmax()

    return {
        "Case": name,
        "N_points": len(df),
        "Mean_N_per_m": values.mean(),
        "Min_N_per_m": values.min(),
        "Min_time_s": df.loc[min_idx, "Time_s"],
        "Max_N_per_m": values.max(),
        "Max_time_s": df.loc[max_idx, "Time_s"],
        "Max_absolute_stress_N_per_m": values.abs().max(),
        "Max_absolute_time_s": df.loc[abs_peak_idx, "Time_s"]
    }


summary = pd.DataFrame([
    calculate_summary("NB", NB),
    calculate_summary("LV", LV),
    calculate_summary("BV", BV)
])


# ============================================================
# Change relative to baseline
# ============================================================

baseline_mean = NB["Tricuspid_Total_Stress_X_N_per_m"].mean()

summary["Mean_difference_vs_NB_N_per_m"] = (
    summary["Mean_N_per_m"] - baseline_mean
)

if abs(baseline_mean) > 1e-12:
    summary["Mean_change_vs_NB_percent"] = (
        (summary["Mean_N_per_m"] - baseline_mean)
        / abs(baseline_mean)
        * 100
    )
else:
    summary["Mean_change_vs_NB_percent"] = float("nan")


summary.to_csv(
    os.path.join(DATA_DIR, "tricuspid_stress_summary.csv"),
    index=False
)


# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(
    NB["Time_s"],
    NB["Tricuspid_Total_Stress_X_N_per_m"],
    label="NB — Baseline",
    linewidth=2
)

plt.plot(
    LV["Time_s"],
    LV["Tricuspid_Total_Stress_X_N_per_m"],
    label="LV — Balloon around LV",
    linewidth=2
)

plt.plot(
    BV["Time_s"],
    BV["Tricuspid_Total_Stress_X_N_per_m"],
    label="BV — Balloon around both ventricles",
    linewidth=2
)

plt.xlabel("Time (s)")
plt.ylabel("Tricuspid Total Stress X (N/m)")
plt.title("Tricuspid Total Stress X — NB vs LV vs BV")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(
        DATA_DIR,
        "NB_LV_BV_tricuspid_stress_x.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# Print results
# ============================================================

print("\n" + "=" * 65)
print("TRICUSPID TOTAL STRESS X ANALYSIS")
print("=" * 65)

print(f"\nNB points: {len(NB)}")
print(f"LV points: {len(LV)}")
print(f"BV points: {len(BV)}")

print("\nSummary:")
print(summary.to_string(index=False))

print("\nFiles created:")
print("  data/NB_tricuspid_stress_x.csv")
print("  data/LV_tricuspid_stress_x.csv")
print("  data/BV_tricuspid_stress_x.csv")
print("  data/NB_LV_BV_tricuspid_stress_x_comparison.csv")
print("  data/tricuspid_stress_summary.csv")
print("  data/NB_LV_BV_tricuspid_stress_x.png")

print("\nDone successfully!")