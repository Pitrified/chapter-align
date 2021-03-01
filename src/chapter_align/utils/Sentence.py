"""Sentence class"""

import logging
import re


class Sentence:
    def __init__(self, orig_tra: str) -> None:
        r"""Build a Sentence"""
        logg = logging.getLogger(f"c.{__name__}.__init__")
        # logg.setLevel("INFO")
        logg.debug("Start __init__")

        self.orig_tra = orig_tra

        self.normalize_sentence()

    def normalize_sentence(self) -> None:
        r"""Normalize a sentence by removing all tags"""
        logg = logging.getLogger(f"c.{__name__}.normalize_sentence")
        # logg.setLevel("INFO")
        logg.debug("Start normalize_sentence")

        re_tag = re.compile("<.*?>")
        self.norm_tra = re_tag.sub("", self.orig_tra)
