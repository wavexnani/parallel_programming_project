#pragma once

#include <vector>
#include <string>
#include <fstream>
#include <cmath>

struct Config {
    int width = 1920;
    int height = 1080;
    int max_iter = 1000;
    double x_min = -2.0;
    double x_max = 0.5;
    double y_min = -1.25;
    double y_max = 1.25;
};

// Computes the escape iteration count for point (cr, ci)
inline int compute_pixel(double cr, double ci, int max_iter) {
    double zr = 0.0, zi = 0.0;
    int iter = 0;
    while (zr * zr + zi * zi <= 4.0 && iter < max_iter) {
        double tmp = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci;
        zr = tmp;
        iter++;
    }
    return iter;
}

// Writes image buffer to binary PPM (P6 format) using standard sine palette matching presentation slide 6
inline bool save_ppm(const std::string& filename, int width, int height, const std::vector<int>& buffer, int max_iter) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) return false;

    file << "P6\n" << width << " " << height << "\n255\n";
    for (int iter : buffer) {
        unsigned char r = 0, g = 0, b = 0;
        if (iter < max_iter) {
            double t = (double)iter / 40.0;
            r = (unsigned char)(128 + 127 * std::sin(t));
            g = (unsigned char)(128 + 127 * std::sin(t + 2.094));
            b = (unsigned char)(128 + 127 * std::sin(t + 4.188));
        }
        file.put(r).put(g).put(b);
    }
    return true;
}
