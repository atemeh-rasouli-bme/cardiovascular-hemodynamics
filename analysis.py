import csv
import matplotlib.pyplot as plt

# Load COMSOL simulation data
file_path = "data/processed/LV_T258.csv"

times = []
probe_1 = []
probe_2 = []

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        times.append(float(row["time_s"]))
        probe_1.append(float(row["probe_1_m2_s"]))
        probe_2.append(float(row["probe_2_m2_s"]))

# Basic data summary
print("=== COMSOL Cardiovascular Analysis ===")
print(f"Data points: {len(times)}")
print(f"Time range: {min(times):.3f} - {max(times):.3f} s")

# Calculate mean values
mean_probe_1 = sum(probe_1) / len(probe_1)
mean_probe_2 = sum(probe_2) / len(probe_2)

print(f"Probe 1 mean: {mean_probe_1:.4f} m²/s")
print(f"Probe 2 mean: {mean_probe_2:.4f} m²/s")

# Plot simulation results
plt.figure(figsize=(8, 5))

plt.plot(times, probe_1, label="Probe 1")
plt.plot(times, probe_2, label="Probe 2")

plt.xlabel("Time (s)")
plt.ylabel("Integrated Velocity (m²/s)")
plt.title("LV Cardiac Assist Balloon - COMSOL Simulation")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("data/processed/LV_T258_analysis.png", dpi=300, bbox_inches="tight")

plt.show()