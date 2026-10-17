#!/usr/bin/env python3
import csv
import os
import matplotlib.pyplot as plt
from PIL import Image

def main():
    csv_path = "output/benchmark_results.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    threads = []
    static_time = []
    dynamic_time = []
    static_spd = []
    dynamic_spd = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            threads.append(int(row["threads"]))
            static_time.append(float(row["static_time_ms"]))
            dynamic_time.append(float(row["dynamic_time_ms"]))
            static_spd.append(float(row["static_speedup"]))
            dynamic_spd.append(float(row["dynamic_speedup"]))

    # Create 2 subplots: Speedup and Execution Time
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Speedup
    ax1.plot(threads, threads, "k--", label="Ideal Linear Speedup")
    ax1.plot(threads, dynamic_spd, "o-", color="blue", label="Dynamic Scheduling")
    ax1.plot(threads, static_spd, "s-", color="red", label="Static Scheduling")
    ax1.set_title("Speedup vs. Threads")
    ax1.set_xlabel("Number of Threads")
    ax1.set_ylabel("Speedup (T_seq / T_par)")
    ax1.set_xticks(threads)
    ax1.grid(True)
    ax1.legend()

    # Plot 2: Execution Time
    ax2.plot(threads, static_time, "s-", color="red", label="Static Scheduling")
    ax2.plot(threads, dynamic_time, "o-", color="blue", label="Dynamic Scheduling")
    ax2.set_title("Execution Time vs. Threads")
    ax2.set_xlabel("Number of Threads")
    ax2.set_ylabel("Execution Time (ms)")
    ax2.set_xticks(threads)
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    chart_path = "output/benchmark_comparison.png"
    plt.savefig(chart_path, dpi=150)
    print(f"Saved benchmark plot to {chart_path}")

    # Convert PPM image to PNG for easy viewing
    ppm_path = "output/mandelbrot.ppm"
    png_path = "output/mandelbrot.png"
    if os.path.exists(ppm_path):
        Image.open(ppm_path).save(png_path)
        print(f"Converted {ppm_path} to {png_path}")

if __name__ == "__main__":
    main()
