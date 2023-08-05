from typing import Optional


class Song:
    def __init__(
        self,
        track: str,
        artist: str,
        source: Optional[str],
        url: Optional[str],
        kwargs,
    ):
        self.track = track
        self.artist = artist
        self.source = source
        self.url = url
        self.kwargs = kwargs
