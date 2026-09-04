import re
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
    """
    Find an exact Graph Data heading and extract the Markdown table
    immediately following it.
    """

    start = text.find(heading)

    if start == -1:
        raise ValueError(f"Heading not found:\n{heading}")

    section = text[start + len(heading):]

    lines = section.splitlines()

    data = []

    for line in lines:
        line = line.strip()

        # Stop when another heading starts
        if line.startswith("#"):
            break

        # Skip empty lines
        if not line:
            if data:
                break
            continue

        # Ignore Markdown table header/separator
        if line.startswith("| Time"):
            continue

        if line.startswith("| ---"):
            continue

        # Extract numerical table rows
        if line.startswith("|"):
            parts = [p.strip() for p in line.strip("|").split("|")]

            if len(parts) >= 2:
                try:
                    time = float(parts[0])
                    stress = float(parts[1])

                    data.append({
                        "Time_s": time,
                        "Mitral_Total_Stress_X_N_per_m": stress
                    })

                except ValueError:
                    continue

    if not data:
        raise ValueError(f"No numerical data found for:\n{heading}")

    return pd.DataFrame(data)


# ============================================================
# Read source file
# ============================================================

print("\nReading COMSOL database...")

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    text = f.read()


# ============================================================
# Exact source tables
# ============================================================

NB_HEADING = (
    "### NB Table 6 — Mitral total stress, x component "
    "— exact source table NB-T231"
)

LV_HEADING = (
    "### LV Table 14 — Mitral total stress, x component, "
    "balloon-assisted case — exact source table LV-T272"
)

BV_HEADING = (
    "### BV Table 14 — Mitral total stress, x component, "
    "balloon-assisted case — exact source table BV-T272"
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
    os.path.join(DATA_DIR, "NB_mitral_stress_x.csv"),
    index=False
)

LV.to_csv(
    os.path.join(DATA_DIR, "LV_mitral_stress_x.csv"),
    index=False
)

BV.to_csv(
    os.path.join(DATA_DIR, "BV_mitral_stress_x.csv"),
    index=False
)


# ============================================================
# Create comparison CSV
# ============================================================

comparison = pd.DataFrame({
    "Time_s": NB["Time_s"],
    "NB_N_per_m": NB["Mitral_Total_Stress_X_N_per_m"],
    "LV_N_per_m": LV["Mitral_Total_Stress_X_N_per_m"],
    "BV_N_per_m": BV["Mitral_Total_Stress_X_N_per_m"]
})

comparison.to_csv(
    os.path.join(
        DATA_DIR,
        "NB_LV_BV_mitral_stress_x_comparison.csv"
    ),
    index=False
)


# ============================================================
# Statistical summary
# ============================================================

def calculate_summary(name, df):

    values = df["Mitral_Total_Stress_X_N_per_m"]

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

summary.to_csv(
    os.path.join(DATA_DIR, "mitral_stress_summary.csv"),
    index=False
)


# ============================================================
# Calculate change relative to baseline
# ============================================================

baseline_mean = NB["Mitral_Total_Stress_X_N_per_m"].mean()

summary["Mean_difference_vs_NB_N_per_m"] = (
    summary["Mean_N_per_m"] - baseline_mean
)

# Percentage change is only informative if baseline mean is
# sufficiently far from zero.
if abs(baseline_mean) > 1e-12:
    summary["Mean_change_vs_NB_percent"] = (
        (summary["Mean_N_per_m"] - baseline_mean)
        / abs(baseline_mean)
        * 100
    )
else:
    summary["Mean_change_vs_NB_percent"] = float("nan")


summary.to_csv(
    os.path.join(DATA_DIR, "mitral_stress_summary.csv"),
    index=False
)


# ============================================================
# Plot
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(
    NB["Time_s"],
    NB["Mitral_Total_Stress_X_N_per_m"],
    label="NB — Baseline",
    linewidth=2
)

plt.plot(
    LV["Time_s"],
    LV["Mitral_Total_Stress_X_N_per_m"],
    label="LV — Balloon around LV",
    linewidth=2
)

plt.plot(
    BV["Time_s"],
    BV["Mitral_Total_Stress_X_N_per_m"],
    label="BV — Balloon around both ventricles",
    linewidth=2
)

plt.xlabel("Time (s)")
plt.ylabel("Mitral Total Stress X (N/m)")
plt.title("Mitral Total Stress X — NB vs LV vs BV")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(
        DATA_DIR,
        "NB_LV_BV_mitral_stress_x.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# Print results
# ============================================================

print("\n" + "=" * 65)
print("MITRAL TOTAL STRESS X ANALYSIS")
print("=" * 65)

print(f"\nNB points: {len(NB)}")
print(f"LV points: {len(LV)}")
print(f"BV points: {len(BV)}")

print("\nSummary:")
print(summary.to_string(index=False))

print("\nFiles created:")
print("  data/NB_mitral_stress_x.csv")
print("  data/LV_mitral_stress_x.csv")
print("  data/BV_mitral_stress_x.csv")
print("  data/NB_LV_BV_mitral_stress_x_comparison.csv")
print("  data/mitral_stress_summary.csv")
print("  data/NB_LV_BV_mitral_stress_x.png")

print("\nDone successfully!")