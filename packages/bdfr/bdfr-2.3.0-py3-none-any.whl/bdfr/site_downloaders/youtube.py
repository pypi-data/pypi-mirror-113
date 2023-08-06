#!/usr/bin/env python3

import logging
import tempfile
from pathlib import Path
from typing import Optional

import youtube_dl
from praw.models import Submission

from bdfr.exceptions import (NotADownloadableLinkError, SiteDownloaderError)
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class Youtube(BaseDownloader):
    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        ytdl_options = {
            'format': 'best',
            'playlistend': 1,
            'nooverwrites': True,
        }
        out = self._download_video(ytdl_options)
        return [out]

    def _download_video(self, ytdl_options: dict) -> Resource:
        yt_logger = logging.getLogger('youtube-dl')
        yt_logger.setLevel(logging.CRITICAL)
        ytdl_options['quiet'] = True
        ytdl_options['logger'] = yt_logger
        with tempfile.TemporaryDirectory() as temp_dir:
            download_path = Path(temp_dir).resolve()
            ytdl_options['outtmpl'] = str(download_path) + '/' + 'test.%(ext)s'
            try:
                with youtube_dl.YoutubeDL(ytdl_options) as ydl:
                    ydl.download([self.post.url])
            except youtube_dl.DownloadError as e:
                raise SiteDownloaderError(f'Youtube download failed: {e}')

            downloaded_files = list(download_path.iterdir())
            if len(downloaded_files) > 0:
                downloaded_file = downloaded_files[0]
            else:
                raise NotADownloadableLinkError(f"No media exists in the URL {self.post.url}")
            extension = downloaded_file.suffix
            with open(downloaded_file, 'rb') as file:
                content = file.read()
        out = Resource(self.post, self.post.url, extension)
        out.content = content
        out.create_hash()
        return out
