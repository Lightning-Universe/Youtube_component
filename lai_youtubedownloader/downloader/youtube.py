import logging
import os
from typing import Union

import lightning as L
from lightning.app.storage.drive import Drive
from lightning.app.storage.path import Path
from pytube import YouTube


class VideoDownloader(L.LightningWork):
    """The VideoDownloader Class downloads videos from YouTube.

    Arguments:
        drivename: Optional drive name with protocal. Example, 'lit://drive'.
    """

    def __init__(self, drive_name: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drive_name = drive_name
        self.drive = Drive(drive_name)

    def download_video(
        self,
        link: str,
        filename: Union[str, Path],
        resolution: str = "360p",
        to_drive: bool = False,
    ) -> None:
        """Retrieves video.

        Arguments:
            link: url of the YouTube video.
            filename: name of the file to store the video as.
            resolution: there
        """

        if to_drive is True and self.drive_name is None:
            logging.error(
                "`to_drive` is set to True but not drive_name was provided ",
                "The VideoDownloader can be instantiated with a drive_name ",
                "downloader = VideoDownloader(<YOUR DRIVE NAME>)",
            )

        self.run(
            action="download",
            link=link,
            filename=filename,
            resolution=resolution,
            to_drive=to_drive,
        )

    def _download_video(self, link, filename, resolution, to_drive) -> None:
        try:
            yt = YouTube(link)
        except ConnectionError as e:
            logging.error(e)

        video = yt.streams.filter(res=resolution).first()

        if video is not None:
            video.download(filename=filename)

            if to_drive is True:
                self.drive.put(filename)
                os.remove(filename)

        else:
            logging.warning(
                "Did not find any videos with the criteria set. Either the url"
                " provided doesn't exist or the requested resolutions does not"
                f" exist. These are the available file formats {yt.streams}"
            )

    def run(self, action, *args, **kwargs):
        if action == "download":
            self._download_video(*args, **kwargs)
