from pathlib import Path
import logging

# import typing as ty

from bs4 import BeautifulSoup  # type: ignore

from .Sentence import Sentence
from .SentenceList import SentenceList


def load_chapter(chapter_path: Path, lang_alpha2_tag: str) -> SentenceList:
    r"""Load a chapter and split it in Sentences"""
    logg = logging.getLogger(f"c.{__name__}.load_chapter")
    logg.setLevel("DEBUG")
    logg.debug("Start load_chapter")

    if not chapter_path.exists():
        raise FileNotFoundError(f"Chapter not found at {chapter_path}")

    parsed_html = BeautifulSoup(chapter_path.read_text(), features="html.parser")

    parsed_body = parsed_html.body
    if parsed_body is None:
        raise RuntimeError(f"Body not found in the chapter text {chapter_path}")

    sentences = SentenceList()

    for i, par in enumerate(parsed_body.find_all("p")):

        # add lang info in the tag
        par["lang"] = lang_alpha2_tag
        par["class"] = par.get("class", []) + [f"lang_{lang_alpha2_tag}"]

        # logg.debug(f"\n>>>>>> par {i}\n{par}")
        # logg.debug(f"{type(par)=}")
        # logg.debug(f"{par.contents=}")
        # logg.debug(f"str(par): >{str(par)}<")
        # logg.debug(f"par.string: >{par.string}<")
        # logg.debug(f"par.strings: >{list(par.strings)}<")
        sentence = Sentence(par)
        # logg.debug(f"\n>>>>> sentence {i}:\n{sentence}")
        logg.debug(f"\n>>>>> sentence {i}:\n{sentence!r}")
        # break

        sentences.append(sentence)

    return sentences
