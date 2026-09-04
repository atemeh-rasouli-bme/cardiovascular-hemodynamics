import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# Cardiovascular Hemodynamics — Summary Dashboard
# NB vs LV vs BV
# ============================================================

DATA_DIR = Path("data/processed")

cases = ["NB", "LV", "BV"]


# ============================================================
# Helper functions
# ============================================================

def load_csv(filename):
    return pd.read_csv(DATA_DIR / filename)


def mean_value(filename, column):
    df = load_csv(filename)
    return df[column].mean()


def max_value(filename, column):
    df = load_csv(filename)
    return df[column].max()


def get_stress_peak(filename):
    df = load_csv(filename)

    column = "von_mises_stress_N_per_m"

    return df[column].max()


def get_absolute_stress_peak(filename):
    df = load_csv(filename)

    column = "stress_N_per_m"

    return df[column].abs().max()


# ============================================================
# Load individual datasets
# ============================================================

print("Loading cardiovascular datasets...")


# ------------------------------------------------------------
# Aortic velocity
# ------------------------------------------------------------

aortic_velocity = {}

for case in cases:
    df = load_csv(f"{case}_aortic_velocity.csv")
    aortic_velocity[case] = df.iloc[:, 1].mean()


# ------------------------------------------------------------
# Pulmonary velocity
# ------------------------------------------------------------

pulmonary_velocity = {}

for case in cases:
    df = load_csv(f"{case}_pulmonary_velocity.csv")
    pulmonary_velocity[case] = df.iloc[:, 1].mean()


# ------------------------------------------------------------
# Aortic pressure
# ------------------------------------------------------------

aortic_pressure = {}

for case in cases:
    df = load_csv(f"{case}_aortic_pressure.csv")
    aortic_pressure[case] = df.iloc[:, 1].mean()


# ------------------------------------------------------------
# Pulmonary pressure
# ------------------------------------------------------------

pulmonary_pressure = {}

for case in cases:
    df = load_csv(f"{case}_pulmonary_pressure.csv")
    pulmonary_pressure[case] = df.iloc[:, 1].mean()


# ------------------------------------------------------------
# LV von Mises stress
# ------------------------------------------------------------

lv_von_mises = {}

for case in cases:
    df = load_csv(f"{case}_lv_von_mises_stress.csv")
    lv_von_mises[case] = df.iloc[:, 1].max()


# ------------------------------------------------------------
# RV von Mises stress
# ------------------------------------------------------------

rv_von_mises = {}

for case in cases:
    df = load_csv(f"{case}_rv_von_mises_stress.csv")
    rv_von_mises[case] = df.iloc[:, 1].max()


# ------------------------------------------------------------
# Mitral stress
# ------------------------------------------------------------

mitral_stress = {}

for case in cases:
    df = load_csv(f"{case}_mitral_stress_x.csv")
    mitral_stress[case] = df.iloc[:, 1].abs().max()


# ------------------------------------------------------------
# Tricuspid stress
# ------------------------------------------------------------

tricuspid_stress = {}

for case in cases:
    df = load_csv(f"{case}_tricuspid_stress_x.csv")
    tricuspid_stress[case] = df.iloc[:, 1].abs().max()


# ============================================================
# Create dashboard
# ============================================================

dashboard = pd.DataFrame({
    "Case": cases,

    "Aortic_velocity_mean_cm_s": [
        aortic_velocity[c] for c in cases
    ],

    "Pulmonary_velocity_mean_cm_s": [
        pulmonary_velocity[c] for c in cases
    ],

    "Aortic_pressure_mean_Pa": [
        aortic_pressure[c] for c in cases
    ],

    "Pulmonary_pressure_mean_Pa": [
        pulmonary_pressure[c] for c in cases
    ],

    "LV_von_Mises_peak_N_m": [
        lv_von_mises[c] for c in cases
    ],

    "RV_von_Mises_peak_N_m": [
        rv_von_mises[c] for c in cases
    ],

    "Mitral_stress_peak_N_m": [
        mitral_stress[c] for c in cases
    ],

    "Tricuspid_stress_peak_N_m": [
        tricuspid_stress[c] for c in cases
    ],
})


# ============================================================
# Save dashboard
# ============================================================

dashboard.to_csv(
    DATA_DIR / "cardiovascular_dashboard_summary.csv",
    index=False
)


# ============================================================
# Print dashboard
# ============================================================

print()
print("=" * 85)
print("CARDIOVASCULAR HEMODYNAMICS — SUMMARY DASHBOARD")
print("=" * 85)

print()
print(dashboard.to_string(index=False))


# ============================================================
# Changes vs NB
# ============================================================

baseline = dashboard.iloc[0]

changes = []

for _, row in dashboard.iloc[1:].iterrows():

    result = {"Case": row["Case"]}

    for column in dashboard.columns[1:]:

        base = baseline[column]
        current = row[column]

        result[column + "_change_percent"] = (
            (current - base) / base * 100
        )

    changes.append(result)


changes_df = pd.DataFrame(changes)

changes_df.to_csv(
    DATA_DIR / "cardiovascular_changes_vs_NB.csv",
    index=False
)


# ============================================================
# Print changes
# ============================================================

print()
print("=" * 85)
print("CHANGES RELATIVE TO BASELINE (NB)")
print("=" * 85)

print()
print(changes_df.to_string(index=False))


# ============================================================
# Figure 1 — Mean Velocity
# ============================================================

plt.figure(figsize=(10, 6))

x = range(len(cases))

plt.plot(
    x,
    dashboard["Aortic_velocity_mean_cm_s"],
    marker="o",
    label="Aortic velocity"
)

plt.plot(
    x,
    dashboard["Pulmonary_velocity_mean_cm_s"],
    marker="o",
    label="Pulmonary velocity"
)

plt.xticks(x, cases)
plt.xlabel("Model")
plt.ylabel("Mean velocity (cm/s)")
plt.title("Mean Cardiovascular Velocity")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    DATA_DIR / "dashboard_mean_velocity.png",
    dpi=300
)

plt.close()


# ============================================================
# Figure 2 — Mean Pressure
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    dashboard["Aortic_pressure_mean_Pa"],
    marker="o",
    label="Aortic pressure"
)

plt.plot(
    x,
    dashboard["Pulmonary_pressure_mean_Pa"],
    marker="o",
    label="Pulmonary pressure"
)

plt.xticks(x, cases)
plt.xlabel("Model")
plt.ylabel("Mean pressure (Pa)")
plt.title("Mean Cardiovascular Pressure")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    DATA_DIR / "dashboard_mean_pressure.png",
    dpi=300
)

plt.close()


# ============================================================
# Figure 3 — Ventricular von Mises Stress
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    dashboard["LV_von_Mises_peak_N_m"],
    marker="o",
    label="LV von Mises"
)

plt.plot(
    x,
    dashboard["RV_von_Mises_peak_N_m"],
    marker="o",
    label="RV von Mises"
)

plt.xticks(x, cases)
plt.xlabel("Model")
plt.ylabel("Peak von Mises stress (N/m)")
plt.title("Peak Ventricular von Mises Stress")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    DATA_DIR / "dashboard_ventricular_stress.png",
    dpi=300
)

plt.close()


# ============================================================
# Figure 4 — Valve Stress
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    dashboard["Mitral_stress_peak_N_m"],
    marker="o",
    label="Mitral stress"
)

plt.plot(
    x,
    dashboard["Tricuspid_stress_peak_N_m"],
    marker="o",
    label="Tricuspid stress"
)

plt.xticks(x, cases)
plt.xlabel("Model")
plt.ylabel("Peak absolute stress (N/m)")
plt.title("Peak Valve Stress")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    DATA_DIR / "dashboard_valve_stress.png",
    dpi=300
)

plt.close()


# ============================================================
# Finished
# ============================================================

print()
print("=" * 85)
print("DASHBOARD CREATED SUCCESSFULLY")
print("=" * 85)

print()
print("Created files:")

print("  data/cardiovascular_dashboard_summary.csv")
print("  data/cardiovascular_changes_vs_NB.csv")
print("  data/dashboard_mean_velocity.png")
print("  data/dashboard_mean_pressure.png")
print("  data/dashboard_ventricular_stress.png")
print("  data/dashboard_valve_stress.png")