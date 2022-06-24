"""Example app to download videos."""

import pathlib

import lightning as L
from lightning.app.storage.path import Path

from lai_youtubedownloader import VideoDownloader

VIDEO_URL = "https://www.youtube.com/watch?v=mndB6zHmU3k"


class LitApp(L.LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.downloader = VideoDownloader(drive_name="lit://drive")
        self.destination = Path("foo.mp4")

    def run(self):
        # Download data to filesystem
        self.downloader.download_video(link=VIDEO_URL, filename="localfoo.mp4")
        assert pathlib.Path("localfoo.mp4").is_file()

        # Load data to the drive
        self.downloader.download_video(
            link=VIDEO_URL,
            filename=self.destination,
            to_drive=True,
        )

        self._exit()


app = L.LightningApp(LitApp())
