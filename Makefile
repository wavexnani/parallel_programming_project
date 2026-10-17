CXX = g++
CXXFLAGS = -O3 -fopenmp -Wall -std=c++17

SRC = src/main.cpp
TARGET = mandelbrot_bench

all: $(TARGET)

$(TARGET): $(SRC) src/mandelbrot.h
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

plot:
	python3 scripts/plot_results.py

view:
	@which xdg-open > /dev/null && xdg-open viewer/index.html || echo "Open viewer/index.html in your web browser."

clean:
	rm -f $(TARGET) output/mandelbrot.ppm output/*.png output/*.csv
	rm -rf build

.PHONY: all plot view clean
