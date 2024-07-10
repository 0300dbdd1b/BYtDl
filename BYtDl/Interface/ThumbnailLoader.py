import requests
from io import BytesIO
from PIL import Image
from rich_pixels import Pixels
from textual import log

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
        image.thumbnail((thumbnail['height'], thumbnail['width']))
        pixels = Pixels.from_image(image)
        return pixels

    def LoadThumbnailFromThumbnails(self, thumbnails):
        higherResThumbnail = self.GetHigherResThumbnail(thumbnails)
        return self.GetImageFromThumbnail(higherResThumbnail)
