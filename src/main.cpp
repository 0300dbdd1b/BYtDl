#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "includes/YtDownloader.hpp"





int main() {
    std::string url;
    std::string options_input;
    std::string output_dir;

    std::cout << "Enter the URL of the YouTube video: ";
    std::cin >> url;
    std::cin.ignore(); // Ignore the newline character left in the input buffer
    std::cout << "Enter the yt-dlp options separated by space: ";
    std::getline(std::cin, options_input);
    std::cout << "Enter the output directory: ";
    std::cin >> output_dir;

    std::vector<std::string> options = split(options_input, ' ');

    CallYoutubeDLP(url, options, output_dir);

    return 0;
}
