"""Sentence class"""

import logging

from bs4.element import Tag  # type: ignore


class Sentence:
    def __init__(self, orig_tag: Tag) -> None:
        r"""Build a Sentence

        Mostly a thin wrapper around a BeautifulSoup Tag
        """
        logg = logging.getLogger(f"c.{__name__}.__init__")
        # logg.setLevel("DEBUG")
        logg.debug("Start __init__")

        self.orig_tag = orig_tag
        self.orig_str = str(self.orig_tag)
        self.norm_tra = self.orig_tag.string
