#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include "includes/YtDownloader.hpp"
#include <curl/curl.h>




int main() {
    std::string query;
    int n;
    std::cout << "Enter the title to search on YouTube: ";
    std::getline(std::cin, query);
    std::cout << "Enter the number of results to retrieve: ";
    std::cin >> n;

    std::string html = search_youtube(query);
    if (html.empty()) {
        std::cerr << "Failed to retrieve search results." << std::endl;
        return 1;
    }

    std::vector<VideoInfo> videos = extract_video_info(html, n);
    if (videos.empty()) {
        std::cerr << "Failed to extract video information." << std::endl;
        return 1;
    }

    for (const auto& video : videos) {
        std::cout << "Title: " << video.title << std::endl;
        std::cout << "Author: " << video.author << std::endl;
        std::cout << "Views: " << video.views << std::endl;
        std::cout << "Link: " << video.link << std::endl;
        std::cout << std::endl;
    }

    return 0;
}

