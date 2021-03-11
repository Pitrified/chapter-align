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
        # logg.debug("Start __init__")

        self.orig_tag = orig_tag

        # TODO add lang='' to the tag

        self.orig_str = str(self.orig_tag)

        # if there is only one component, just get the string
        self.norm_tra: str = self.orig_tag.string
        if self.norm_tra is None:
            logg.debug(".string was empty")
            strings = self.orig_tag.strings
            self.norm_tra = "".join(strings)
            logg.debug(f"self.norm_tra: {self.norm_tra}")

        # normalize further by removing \n
        self.norm_tra = self.norm_tra.replace("\n", " ")

        self.len_norm_tra = len(self.norm_tra)

        if self.len_norm_tra < 5:
            logg.debug(f"Very short sentence found:\n{self!r}")

    def __str__(self) -> str:
        r"""Return the readable string for the sentence"""
        # logg = logging.getLogger(f"c.{__name__}.__str__")
        # logg.setLevel("DEBUG")
        # logg.debug("Start __str__")

        return self.norm_tra

    def __repr__(self) -> str:
        r"""Return more informations on the sentence"""
        # logg = logging.getLogger(f"c.{__name__}.__repr__")
        # logg.setLevel("DEBUG")
        # logg.debug("Start __repr__")

        repr_str = ""
        repr_str += f"OT: {self.orig_tag}"
        repr_str += "\nNT"
        repr_str += f" ({self.len_norm_tra}):"
        repr_str += f" >{self.norm_tra}<"

        return repr_str
