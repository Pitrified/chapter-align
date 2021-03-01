from pathlib import Path
import logging
import typing as ty

from bs4 import BeautifulSoup  # type: ignore

from .Sentence import Sentence


def load_chapter(
    lang_folder: Path, chapter_template: str, chapter_index: int
) -> ty.List[Sentence]:
    r"""Load a chapter and split it in Sentences"""
    logg = logging.getLogger(f"c.{__name__}.load_chapter")
    # logg.setLevel("DEBUG")
    logg.debug("Start load_chapter")

    chapter_path = lang_folder / chapter_template.format(chapter_index)
    logg.debug(f"{chapter_path=}")

    if not chapter_path.exists():
        raise FileNotFoundError(f"Chapter not found at {chapter_path}")

    parsed_html = BeautifulSoup(chapter_path.read_text(), features="html.parser")

    parsed_body = parsed_html.body
    if parsed_body is None:
        raise RuntimeError("Body not found in the chapter text")

    sentences: ty.List[Sentence] = []

    for i, par in enumerate(parsed_body.find_all("p")):
        logg.debug(f"\n>>>>>> par {i}\n{par}")
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
