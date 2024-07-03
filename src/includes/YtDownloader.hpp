#pragma once

#include <vector>
#include <string>
#include <iostream>
#include <sstream>

using namespace std;

struct VideoInfo
{
	string title;
	string author;
	string views;
	string link;
};

vector<string> split(const string& str, char delimiter);
void CallYoutubeDLP(const string& url, const vector<string>& options, const string& output_dir);
string search_youtube(const string& query);
vector<VideoInfo> extract_video_info(const string& html, size_t n);
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp);
