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










