#include <vector>
#include <string>
#include <iostream>
#include <sstream>

using namespace std;
vector<string> split(const string& str, char delimiter) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(str);
    while (getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

void CallYoutubeDLP(const string& url, const vector<string>& options, const string& output_dir) {
   string command = "yt-dlp ";

    // Add all the options
    for (const auto& option : options) {
        command += option + " ";
    }

    // Add output template
    command += "-o \"" + output_dir + "/%(title)s.%(ext)s\" ";
    command += "\"" + url + "\"";

    cout << "Executing command: " << command << endl;

    int result = system(command.c_str());
    if (result != 0) {
        cerr << "Error downloading the file." << endl;
    } else {
        cout << "Download completed successfully." << endl;
    }
}
#include <iostream>
#include <string>
#include <vector>
#include <curl/curl.h>
#include "includes/YtDownloader.hpp"

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

string search_youtube(const string& query) {
    CURL* curl;
    CURLcode res;
    string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        string url = "https://www.youtube.com/results?search_query=" + string(curl_easy_escape(curl, query.c_str(), query.length()));

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            return "";
        }

        curl_easy_cleanup(curl);
    } else {
        cerr << "Failed to initialize CURL." << endl;
        return "";
    }

    return readBuffer;
}

vector<VideoInfo> extract_video_info(const string& html, size_t n) {
    vector<VideoInfo> videos;
    size_t pos = 0;
    while (videos.size() < n) {
        // Extract video link
        pos = html.find("/watch?v=", pos);
        if (pos == string::npos) break;
        size_t end_pos = html.find("\"", pos);
        string link = "https://www.youtube.com" + html.substr(pos, end_pos - pos);

        // Extract video title
        pos = html.find("title=\"", end_pos);
        if (pos == std::string::npos) break;
        pos += 7;
        end_pos = html.find("\"", pos);
        string title = html.substr(pos, end_pos - pos);

        // Extract author
        pos = html.find("channel-name", end_pos);
        if (pos == string::npos) break;
        pos = html.find(">", pos) + 1;
        end_pos = html.find("<", pos);
        string author = html.substr(pos, end_pos - pos);

        // Extract views
        pos = html.find("view-count", end_pos);
        if (pos == string::npos) break;
        pos = html.find(">", pos) + 1;
        end_pos = html.find("<", pos);
        string views = html.substr(pos, end_pos - pos);

        videos.push_back({title, author, views, link});
        pos = end_pos;
    }
    return videos;
}



