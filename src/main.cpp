#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include <chrono>
#include <omp.h>
#include "mandelbrot.h"

// Sequential baseline (single core, no OpenMP pragmas)
double run_sequential(const Config& cfg, std::vector<int>& img) {
    auto t0 = std::chrono::high_resolution_clock::now();

    for (int y = 0; y < cfg.height; ++y) {
        double ci = cfg.y_min + y * (cfg.y_max - cfg.y_min) / (cfg.height - 1);
        for (int x = 0; x < cfg.width; ++x) {
            double cr = cfg.x_min + x * (cfg.x_max - cfg.x_min) / (cfg.width - 1);
            img[y * cfg.width + x] = compute_pixel(cr, ci, cfg.max_iter);
        }
    }

    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// OpenMP with Static Scheduling
double run_static(const Config& cfg, int threads, std::vector<int>& img) {
    omp_set_num_threads(threads);
    auto t0 = std::chrono::high_resolution_clock::now();

    #pragma omp parallel for schedule(static)
    for (int y = 0; y < cfg.height; ++y) {
        double ci = cfg.y_min + y * (cfg.y_max - cfg.y_min) / (cfg.height - 1);
        for (int x = 0; x < cfg.width; ++x) {
            double cr = cfg.x_min + x * (cfg.x_max - cfg.x_min) / (cfg.width - 1);
            img[y * cfg.width + x] = compute_pixel(cr, ci, cfg.max_iter);
        }
    }

    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// OpenMP with Dynamic Scheduling (chunk size in rows)
double run_dynamic(const Config& cfg, int threads, int chunk_size, std::vector<int>& img) {
    omp_set_num_threads(threads);
    auto t0 = std::chrono::high_resolution_clock::now();

    #pragma omp parallel for schedule(dynamic, chunk_size)
    for (int y = 0; y < cfg.height; ++y) {
        double ci = cfg.y_min + y * (cfg.y_max - cfg.y_min) / (cfg.height - 1);
        for (int x = 0; x < cfg.width; ++x) {
            double cr = cfg.x_min + x * (cfg.x_max - cfg.x_min) / (cfg.width - 1);
            img[y * cfg.width + x] = compute_pixel(cr, ci, cfg.max_iter);
        }
    }

    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main() {
    Config cfg;
    std::vector<int> img(cfg.width * cfg.height);
    std::vector<int> thread_counts = {1, 2, 4, 8, 12};
    int chunk_size = 4;

    std::cout << "========================================================\n";
    std::cout << "    Parallel Mandelbrot Benchmark (OpenMP vs Static)    \n";
    std::cout << "    Resolution: " << cfg.width << "x" << cfg.height << " | Max Iter: " << cfg.max_iter << "\n";
    std::cout << "========================================================\n";

    // 1. Measure pure sequential baseline
    std::cout << "Running sequential baseline (1 thread, no OpenMP)... " << std::flush;
    double t_seq = run_sequential(cfg, img);
    std::cout << std::fixed << std::setprecision(2) << t_seq << " ms\n\n";

    // 2. Benchmark thread scaling
    std::cout << "Threads | Static (ms) | Dynamic (ms) | Static Spd | Dynamic Spd | Dynamic Eff\n";
    std::cout << "-------------------------------------------------------------------------\n";

    std::ofstream csv("output/benchmark_results.csv");
    csv << "threads,static_time_ms,dynamic_time_ms,static_speedup,dynamic_speedup,static_efficiency,dynamic_efficiency\n";

    for (int t : thread_counts) {
        double t_stat = run_static(cfg, t, img);
        double t_dyn = run_dynamic(cfg, t, chunk_size, img);

        double spd_stat = t_seq / t_stat;
        double spd_dyn = t_seq / t_dyn;
        double eff_stat = (spd_stat / t) * 100.0;
        double eff_dyn = (spd_dyn / t) * 100.0;

        std::cout << std::setw(7) << t << " | "
                  << std::setw(11) << std::fixed << std::setprecision(2) << t_stat << " | "
                  << std::setw(12) << t_dyn << " | "
                  << std::setw(9) << spd_stat << "x | "
                  << std::setw(10) << spd_dyn << "x | "
                  << std::setw(9) << eff_dyn << "%\n";

        csv << t << "," << t_stat << "," << t_dyn << ","
            << spd_stat << "," << spd_dyn << "," << eff_stat << "," << eff_dyn << "\n";
    }

    // Save final image rendered with all available threads
    run_dynamic(cfg, 12, chunk_size, img);
    save_ppm("output/mandelbrot.ppm", cfg.width, cfg.height, img, cfg.max_iter);
    std::cout << "\n[Done] Output saved to output/mandelbrot.ppm and output/benchmark_results.csv\n";

    return 0;
}
