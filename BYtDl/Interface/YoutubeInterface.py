from BYtDl.config.base import *
from BYtDl.Interface.YoutubeDownloadLogger import YtDlLogger
import yt_dlp

class YoutubeInterface():
    def Download(self, url, output_path='.', is_playlist=False, format='mp3', quality='192'):
        if format.lower() in ['mp3', 'aac', 'aiff', 'alac', 'flac', 'm4a', 'mka', 'ogg', 'opus', 'vorbis', 'wav']:
            # Audio formats: extract audio only
            postprocessors = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': quality
            }]
            format_selection = 'bestaudio/best'
        elif format.lower() in ['mp4', 'mkv', 'flv', 'mov', 'avi', 'webm']:
            # Video formats: download best video and best audio
            postprocessors = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': format  # Correct spelling mistake to 'preferredformat'
            }]
            format_selection = 'bestvideo+bestaudio/best'
        elif format.lower() == 'gif':
            # Special case for GIF (needs conversion from video)
            postprocessors = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'gif'
            }]
            format_selection = 'bestvideo/best'
        else:
            raise ValueError("Unsupported format specified")

        ydl_opts = {
            'format': format_selection,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': postprocessors,
            'noplaylist': not is_playlist,
            'quiet': True,
            'no_warnings': True,
            'logger': YtDlLogger()
        }

        # Execute download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download complete. Files saved to {output_path}")

    def Search(self, query, n=1):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'force_generic_extractor': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{SEARCH_RESULTS}:{query}", download=False)

        videos = []
        if 'entries' in result:
            for entry in result['entries']:
                if len(videos) >= n:
                    break
                if entry.get('duration'):
                    videos.append({
                        'author': entry.get('uploader'),
                        'title': entry.get('title'),
                        'duration': entry.get('duration'),
                        'views': entry.get('view_count'),
                        'url': entry.get('url')
                    })

        return videos

