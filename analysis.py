import csv
import matplotlib.pyplot as plt

times = []
probe_1 = []
probe_2 = []

with open("data/processed/LV_T258.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        times.append(float(row["time_s"]))
        probe_1.append(float(row["probe_1_m2_s"]))
        probe_2.append(float(row["probe_2_m2_s"]))

print("Data loaded successfully.")
print(f"Number of data points: {len(times)}")

plt.plot(times, probe_1, label="Probe 1")
plt.plot(times, probe_2, label="Probe 2")

plt.xlabel("Time (s)")
plt.ylabel("Integrated Velocity (m²/s)")
plt.title("LV Cardiac Assist Balloon - COMSOL Simulation")

plt.legend()
plt.grid(True)
plt.show()