import logging
import typing as ty

from bs4 import BeautifulSoup  # type: ignore

from .Sentence import Sentence


class SentenceList:
    r"""A Sentence list

    If a sentence index beyond the end is requested, return a "_" Sentence
    """

    def __init__(self) -> None:
        r"""Initialize a SentenceList"""
        logg = logging.getLogger(f"c.{__name__}.__init__")
        # logg.setLevel("DEBUG")
        logg.debug("Start __init__")

        self._inner_list: ty.List[Sentence] = []
        self.tot_chars = 0

        placeholder_soup = BeautifulSoup("<p>_</p>", "html.parser")
        placeholder_tag = placeholder_soup.find_all("p")[0]
        self.placeholder_sentence = Sentence(placeholder_tag)

    def __len__(self) -> int:
        r"""Return the length of the inner list, or the number of Sentences"""
        # logg = logging.getLogger(f"c.{__name__}.__len__")
        # logg.setLevel("DEBUG")
        # logg.debug("Start __len__")

        return len(self._inner_list)

    def append(self, sent: Sentence) -> None:
        r"""Append a Sentence on the SentenceList"""
        # logg = logging.getLogger(f"c.{__name__}.append")
        # logg.setLevel("DEBUG")
        # logg.debug("Start append")

        self._inner_list.append(sent)
        self.tot_chars += len(sent.norm_tra)

    def __getitem__(self, index: int) -> Sentence:
        r"""Get an item safely, return a placeholder sentence for invalid indexes"""
        # logg = logging.getLogger(f"c.{__name__}.__getitem__")
        # logg.setLevel("DEBUG")
        # logg.debug("Start __getitem__")

        if not -len(self._inner_list) <= index < len(self._inner_list):
            return self.placeholder_sentence
        return self._inner_list[index]

    def __iter__(self) -> ty.Iterator[Sentence]:
        r"""Iterate over the inner sentence list"""
        # https://stackoverflow.com/a/37349475
        # logg = logging.getLogger(f"c.{__name__}.__iter__")
        # logg.setLevel("DEBUG")
        # logg.debug("Start __iter__")
        for sent in self._inner_list:
            yield sent
