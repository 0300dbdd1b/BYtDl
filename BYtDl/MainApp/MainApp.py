from textual.app import App, ComposeResult
import yt_dlp
from textual.widgets import Header, Footer, Input, Button, Static, \
                            Label, LoadingIndicator, SelectionList, ProgressBar, Log, \
                            Collapsible, Select, TabbedContent, TabPane, Tabs, Tab
from textual import events
from textual.color import Color
from textual import work
from textual.binding import Binding
from BYtDl.config.base import *
from BYtDl.Interface.YoutubeInterface import YoutubeInterface


class MainApp(App):

    BINDINGS = [
        Binding("ctrl+d", "download", "Download", show=True, priority=True),
        Binding("ctrl+s", "search", "Search", show=True, priority=False),
        Binding("ctrl+q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tabs(
            Tab("Single Media", id="singleMediaTab"),
            Tab("Playlist", id="playlistTab")
        )
        yield Input(id="searchInput")
        yield SelectionList[str](id="searchResults")
        with TabbedContent(id="downloadFormats", initial="audioFormatTab"):
            with TabPane("audioFormat", id="audioFormatTab"):
                yield Select.from_values(AUDIO_FORMATS, allow_blank=False, id="downloadAudioFormat")
            with TabPane("videoFormat", id="videoFormatTab"):
                yield Select.from_values(VIDEO_FORMATS, allow_blank=False, id="downloadVideoFormat")
        yield Button(label="Search", id="searchButton")
        yield Button(label="Download", id="downloadButton")
        with Collapsible(collapsed=False):
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
            query = self.query_one("#searchInput", Input).value
            resultWidget = self.query_one("#searchResults", SelectionList)
            resultWidget.clear_options()
            self.videos = self.interface.Search(query, 15)
            selections = []
            for idx, video in enumerate(self.videos):
                selections.append((f"{video['title']} ({video['duration']} s)", idx))
            resultWidget.add_options(selections)
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
