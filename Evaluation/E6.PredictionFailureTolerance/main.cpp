#include <iostream>
#include <fstream>
#include <ctime>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>

#define FILENAME "testfile.bin"
#define BUFFER_SIZE 1024 * 1024 * 1 // 1MB

// Function to read file using page cache
void readWithPageCache() {
    char *buffer = new char[BUFFER_SIZE];
    std::ifstream file(FILENAME, std::ios::binary);

    if (!file.is_open()) {
        std::cerr << "Unable to open file " << FILENAME << std::endl;
        delete[] buffer;
        exit(1);
    }

    std::clock_t start = std::clock();

    // Read data from file into buffer
    file.read(buffer, BUFFER_SIZE);

    std::clock_t end = std::clock();

    double cpu_time_used = static_cast<double>(end - start) / CLOCKS_PER_SEC * 1000;

    std::cout << "Time taken to read 1MB from disk with page cache: " << cpu_time_used << "ms\n";

    file.close();
    delete[] buffer;
}

int main() {
    // Test with page cache
    readWithPageCache();

    readWithPageCache();

    return 0;
}
