import requests
from io import BytesIO
from PIL import Image
from rich_pixels import Pixels
from textual import log
from textual.app import ComposeResult, RenderResult
from textual.containers import Container
from textual.widgets import Static

from BYtDl.config.base import *

class ThumbnailLoader:

    def GetHigherResThumbnail(self, thumbnails):
        higherResThumbnail = {"url": None, "height": 0, "width": 0}
        for thumbnail in thumbnails:
            if thumbnail['height'] > higherResThumbnail['height'] and thumbnail['width'] > higherResThumbnail['width']:
                higherResThumbnail = thumbnail
        return higherResThumbnail


    def GetImageFromThumbnail(self, thumbnail):

        response = requests.get(thumbnail['url'])
        image = Image.open(BytesIO(response.content))
        image.thumbnail((100, 100))
        pixels = Pixels.from_image(image)
        return pixels

    def LoadThumbnailFromThumbnails(self, thumbnails):
        higherResThumbnail = self.GetHigherResThumbnail(thumbnails)
        return self.GetImageFromThumbnail(higherResThumbnail)


class Thumbnail(Static):
    def __init__(self, thumbnails):
        self.thumbnails = thumbnails
        self.img = ThumbnailLoader().LoadThumbnailFromThumbnails(self.thumbnails)


    def render(self) -> RenderResult:
        return self.img
