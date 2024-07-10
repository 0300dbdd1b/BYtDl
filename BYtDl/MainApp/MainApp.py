import yt_dlp
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Input, Button, Static, \
                            Label, LoadingIndicator, SelectionList, ProgressBar, Log, \
                            Collapsible, Select, TabbedContent, TabPane, Tabs, Tab
from textual import events, work, log
from textual.color import Color
from textual.binding import Binding


from rich.text import Text
from rich.columns import Columns
from rich.panel import Panel
from rich_pixels import Pixels
from rich.console import Console


from BYtDl.config.base import *
from BYtDl.Interface.YoutubeInterface import YoutubeInterface
from BYtDl.Interface.ThumbnailLoader import ThumbnailLoader

import time

class MainApp(App):

    CSS_PATH = "styles.css"
    BINDINGS = [
        Binding("ctrl+d", "download", "Download", show=True, priority=True),
        Binding("ctrl+s", "search", "Search", show=True, priority=False),
        Binding("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:

        # yield Header()
        yield Tabs(
            Tab("Single Media", id="singleMediaTab"),
            Tab("Playlist", id="playlistTab")
        )
        with Container(id="appGrid"):
            with Vertical(id="leftPane"):
                yield Input(id="searchInput", classes="box")
                yield SelectionList[str](id="searchResults", classes="box")
            with Vertical(id="topRight"):
                with TabbedContent(id="downloadFormats", initial="audioFormatTab", classes="box"):
                    with TabPane("audioFormat", id="audioFormatTab"):
                        yield Select.from_values(AUDIO_FORMATS, allow_blank=False, id="downloadAudioFormat")
                    with TabPane("videoFormat", id="videoFormatTab"):
                        yield Select.from_values(VIDEO_FORMATS, allow_blank=False, id="downloadVideoFormat")
                with Horizontal(id="buttonContainer"):
                    yield Button(label="Search", id="searchButton", classes="box")
                    yield Button(label="Download", id="downloadButton", classes="box")
            with Container(id="bottomRight"):
                with Collapsible(collapsed=False, classes="box"):
                    yield Log(id="logs", max_lines=10, auto_scroll=True)
        yield Footer()

    def on_mount(self):
        self.interface = YoutubeInterface()
        self.screen.styles.background = Color(40, 40, 40)

    @work(thread=True)
    async def on_button_pressed(self, event):
        if event.button.id == "searchButton":
            self.action_search()
        if event.button.id == "downloadButton":
            self.action_download()

    @work(thread=True)
    async def action_search(self):
        try:
            console = Console()
            query = self.query_one("#searchInput", Input).value
            resultWidget = self.query_one("#searchResults", SelectionList)
            resultWidget.clear_options()
            self.videos = self.interface.Search(query, 15)
            for idx, video in enumerate(self.videos):
                thumbnailPixels = ThumbnailLoader().LoadThumbnailFromThumbnails(video['thumbnails'])
                musicInfo = Text(f"{video['title']} ({video['duration']})")
                resultWidget.add_option((musicInfo, idx))
                log("PANNEL CREE")
            resultWidget.refresh()
        except Exception as e:
            logsWidget = self.query_one("#logs", Log)
            logsWidget.clear()
            logsWidget.write_line(f"Error Searching : {e}")

    @work(thread=True)
    async def action_download(self):
        try:
            resultWidget = self.query_one("#searchResults", SelectionList)
            logsWidget = self.query_one("#logs", Log)
            formatTab = self.query_one("#downloadFormats", TabbedContent).active
            if formatTab == "videoFormatTab":
                format = self.query_one("#downloadVideoFormat", Select).value
            else:
                format = self.query_one("#downloadAudioFormat", Select).value
            logsWidget.clear()
            selected_indices = resultWidget.selected
            printedLines = []
            for index in selected_indices:
                video = self.videos[index]
                logsWidget.write_line(f"Downloading {video['title']} ...")
                self.interface.Download(url=video['url'], format=format)
                printedLines.append(f"{video['title']} Downloaded !")
                logsWidget.clear()
                logsWidget.write_lines(printedLines)
                logsWidget.refresh()
        except Exception as e:
            logsWidget = self.query_one("#logs", Log)
            logsWidget.clear()
            logsWidget.write_line(f"Error Downloading : {e}")

    async def action_quit(self):
        self.app.exit()
