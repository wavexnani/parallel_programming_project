# Parallel Mandelbrot Set Computation (OpenMP)

A high-performance C++ project benchmarking **Static Loop Scheduling** versus **Dynamic Load Balancing** using **OpenMP** on multi-core CPU architectures.

The project evaluates how to eliminate severe spatial load imbalance when rendering the Mandelbrot fractal ($z_{n+1} = z_n^2 + c$) by dynamically distributing computation across worker threads.

---

## 1. Requirements & Prerequisites

To build and run this project, ensure your environment meets the following requirements:

### Hardware Requirements
- **Processor**: Multi-core x86_64 CPU (tested on 13th Gen Intel Core i5-13420H, 8 physical cores / 12 hardware threads).
- **Architecture**: Symmetric Multiprocessing (SMP) with Uniform Memory Access (UMA).

### Software & Toolchain Dependencies
- **Operating System**: Linux (Ubuntu 20.04+, Debian, Arch, or similar POSIX OS).
- **C++ Compiler**: GCC `g++` (version 9.0 or newer) or Clang with **OpenMP** support (`-fopenmp`).
- **Build System**: GNU `make`.
- **Python**: Python 3.8+ with:
  - `matplotlib` (for generating speedup and execution time plots)
  - `Pillow` (PIL) (for converting Netpbm PPM buffers to PNG)
- **Web Browser**: Any modern web browser (Chrome, Firefox, Edge) to run the interactive multi-core visualizer.

---

## 2. Installation & Setup

Clone or download the project folder, then install the required dependencies:

### Step 1: Install Compiler and Dependencies (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y build-essential python3 python3-pip python3-matplotlib python3-pil
```

### Step 2: Navigate to Project Directory
```bash
cd PP_ProjectWork
```

### Step 3: Compile the C++ Engine
Compile the optimized binary using `make` (enables `-O3 -fopenmp -std=c++17`):
```bash
make clean && make
```
This produces the executable `mandelbrot_bench`.

---

## 3. Usage

The project provides simple commands to run benchmarks, plot performance charts, and launch the interactive visualizer.

### 1. Run the Multi-Threaded Benchmark
Execute the C++ benchmark across 1, 2, 4, 8, and 12 threads:
```bash
./mandelbrot_bench
```
- Measures the pure sequential baseline (single-thread, no OpenMP).
- Executes both **Static Scheduling** and **Dynamic Scheduling** across all thread counts.
- Displays a formatted console summary table of execution times, speedups, and efficiency.
- Exports raw timings to `output/benchmark_results.csv` and renders `output/mandelbrot.ppm`.

### 2. Generate Benchmark Performance Charts
Generate the speedup and execution time comparison graphs:
```bash
make plot
# Or directly: python3 scripts/plot_results.py
```
Outputs:
- `output/benchmark_comparison.png`: Dual-panel speedup ($S_p$) and execution time ($T_p$) plots.
- `output/mandelbrot.png`: 1080p visualization converted directly from PPM.

### 3. Open the Interactive Multi-Core Web Visualizer
Launch the interactive web visualizer in your browser:
```bash
make view
# Or directly: xdg-open viewer/index.html
# Or via HTTP server: python3 -m http.server --directory viewer 8080
```

---

## 4. Key Features

- **Compiler-Directed OpenMP Parallelism**: Clean, idiomatic parallel loops using `#pragma omp parallel for` without manual thread pool boilerplate.
- **Static vs. Dynamic Scheduling Comparison**: Direct head-to-head comparison between:
  - `schedule(static)`: Deterministic block row allocation.
  - `schedule(dynamic, 4)`: On-demand work-stealing from a shared queue in 4-row chunks.
- **Lock-Free Disjoint Writes**: Zero lock contention; worker threads write directly into independent rows of a contiguous 1D frame buffer.
- **Automated CSV & Metric Telemetry**: Exports wall-clock times, self-relative speedups ($S_p = T_1 / T_p$), and parallel efficiency ($E_p$).
- **Interactive Multi-Core Web Visualizer**:
  - **Live Calculation Animation**: Watch simulated worker threads calculate rows in real-time.
  - **Core Count Selection**: Dynamically test with 1, 2, 4, 8, 12, or 16 cores.
  - **🧵 Core Allocation Map**: Color-codes every row by the core that computed it, visually demonstrating why static chunking suffers from the straggler problem.
  - **Multiple Color Themes**: Royal Amethyst, Quanta Cyan, Classic Electric, Sunset, and Emerald.
  - **Real-Time Hover Inspector**: Read exact HEX/RGB codes, iteration counts, complex coordinates, and assigned core IDs.

---

## 5. Parallel Computing Environment

- **Host Machine**: 13th Gen Intel(R) Core(TM) i5-13420H (x86_64).
- **Core Topology**: 8 physical cores (4 Performance cores with Hyper-Threading + 4 Efficient cores = 12 hardware threads).
- **Cache Architecture**:
  - **L1 Data Cache**: 320 KB total
  - **L2 Cache**: 7 MB total
  - **L3 Shared Cache**: 12 MB shared across all cores
- **Spatial Cache Locality**: Frame buffer stored row-major, maximizing L1/L2 cache line hits and avoiding false sharing between cores.

---

## 6. Benchmark Results (1920x1080, Max Iter 1000)

Measured on: **Intel Core i5-13420H (12 Hardware Threads)**

| Threads ($p$) | Static Time (ms) | Dynamic Time (ms) | Static Speedup ($S_p$) | Dynamic Speedup ($S_p$) | Dynamic Efficiency ($E_p$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 1345.43 ms | 1338.51 ms | 1.00x | 1.01x | 100.9% |
| **2** | 679.81 ms | 670.41 ms | 1.99x | 2.02x | 100.8% |
| **4** | 638.49 ms | 338.92 ms | **2.11x** | **3.95x** | **98.7%** |
| **8** | 416.64 ms | 207.43 ms | **3.23x** | **6.45x** | **80.7%** |
| **12** | 339.12 ms | 157.33 ms | **3.97x** | **8.51x** | **70.9%** |

### Key Performance Findings:
1. **The Straggler Effect**: Under static scheduling on 4 threads, the middle threads handle the dense cardioid (taking 1000 iterations/pixel) while outer threads finish early and sit idle, capping speedup at **2.11x** (51% efficiency).
2. **Dynamic Load Balancing**: `schedule(dynamic, 4)` dispatches work on-demand, achieving **3.95x speedup (98.7% efficiency)** on 4 threads and **8.51x** on 12 threads.
3. **Hybrid CPU Scaling**: Efficiency tapers after 8 threads because threads 9–12 run on Intel's Efficient cores (E-cores) and Hyper-Threading shares pipelines on P-cores.

---

## 7. Project Structure

```
PP_ProjectWork/
├── Parallel_Mandelbrot_OpenMP.pptx   # 15-slide PowerPoint presentation
├── Makefile                           # Build configuration (make, make plot, make view)
├── README.md                          # Comprehensive project documentation
├── src/
│   ├── main.cpp                       # OpenMP benchmark runner (1, 2, 4, 8, 12 threads)
│   └── mandelbrot.h                   # Escape-time math & PPM image writer
├── viewer/
│   ├── index.html                     # Interactive multi-core calculation visualizer
│   ├── styles.css                     # Dark glassmorphism HUD styling
│   └── app.js                         # Real-time multi-core calculation simulation
├── scripts/
│   ├── plot_results.py                # Speedup & execution time plotting script
│   └── generate_pptx.py               # Script generating the 16:9 presentation deck
└── output/
    ├── benchmark_results.csv          # Actual measured execution timings
    ├── benchmark_comparison.png       # Generated speedup and time charts
    ├── mandelbrot.ppm                 # 1080p binary PPM image
    └── mandelbrot.png                 # Rendered PNG fractal image
```

---

## 8. References

1. OpenMP Architecture Review Board, *OpenMP Application Programming Interface Specification (Version 5.2)*, 2021.
2. R. Chandra, L. Dagum, D. Kohr, D. Maydan, J. McDonald, and R. Menon, *Parallel Programming in OpenMP*, Morgan Kaufmann Publishers, 2001.
3. P. Pacheco, *An Introduction to Parallel Programming*, Morgan Kaufmann / Elsevier, 2011.
4. B. B. Mandelbrot, *The Fractal Geometry of Nature*, W. H. Freeman and Company, 1982.
5. Intel Corporation, *13th Gen Intel Core Processor Datasheet, Volume 1: Architecture and Hybrid Multiprocessing*, 2023.
