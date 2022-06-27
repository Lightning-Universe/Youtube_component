"""Integration tests."""
import os
import pathlib

import lightning as L
from lightning.app.runners import MultiProcessRuntime
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
        assert not self.destination.exists()

        self.downloader.download_video(
            link=VIDEO_URL,
            filename="should_not_exist.mp4",
            resolution="10p",
            to_drive=True,
        )

        assert not pathlib.Path("should_not_exist.mp4").exists()

        self.run_after()
        self._exit()

    def run_after(self):
        os.remove("localfoo.mp4")


def test_download_data_from_app():
    """Test that VideoDownloader work runs end-to-end in an appflow."""
    app = L.LightningApp(LitApp(), debug=True)
    MultiProcessRuntime(app, start_server=False).dispatch()
