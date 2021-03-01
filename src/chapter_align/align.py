from pathlib import Path
import logging
import typing as ty

from .utils.load_chapters import load_chapter


def align_book(
    book_folder: Path,
    languages: ty.Tuple[str, str],
    chapter_templates: ty.Tuple[str, str],
) -> None:
    r"""Align every chapter in a book

            l0    l1    di
           ----------------
    >  0:    a     a     0
    >  1:          b    -1
    >  2:    bc    c    -1
    >  3:    def   d     0
    >  4:    g     e     2
    >  5:    h     f     2
    >  6:    i     g     2
    >  7:    jkl   h     2
    >  8:    _     i     -
    >  9:    _     j     -
    > 10:    _     k     -
    > 11:    _     l     -

    > 12:    A     _
    > 16:    _     A

    > 17:    B     _
    > 18:    C     _
    > 20:    _     BC

    > 28:    D     _
    > 31:    _     D

    """
    logg = logging.getLogger(f"c.{__name__}.align_book")
    logg.setLevel("DEBUG")
    logg.debug("Start align_book")

    chapter_index = 1
    # TODO, the starting index sould be different for the two books

    # skip_interval = 5

    lang_folder0 = book_folder / languages[0]
    sent0 = load_chapter(lang_folder0, chapter_templates[0], chapter_index)
    recap = f"len(sent0): {len(sent0)}"
    recap += f" sent0.tot_chars: {sent0.tot_chars}"
    logg.debug(recap)

    lang_folder1 = book_folder / languages[1]
    sent1 = load_chapter(lang_folder1, chapter_templates[1], chapter_index)
    recap = f"len(sent1): {len(sent1)}"
    recap += f" sent1.tot_chars: {sent1.tot_chars}"
    logg.debug(recap)

    tot_len0: int = 0
    tot_len1: int = 0
    tot_scaled_len1: float = 0
    scaling_factor = sent0.tot_chars / sent1.tot_chars
    logg.debug(f"scaling_factor: {scaling_factor}")

    for i in range(max(len(sent0), len(sent1))):
        len0 = sent0[i].len_norm_tra
        tot_len0 += len0

        len1 = sent1[i].len_norm_tra
        tot_len1 += len1

        scaled_len1 = len1 * scaling_factor
        tot_scaled_len1 += scaled_len1

        recap = f"\n>>>>>> {i}"
        recap += f"\n0 ({len0}): >{sent0[i]}<"
        recap += f"\n1 ({len1}): >{sent1[i]}<"
        recap += f"\nlen0 {len0: 6d} len1 {len1: 6d} sc_len1 {scaled_len1: 8.2f}"
        recap += f"\ntot0 {tot_len0: 6d} tot1 {tot_len1: 6d} t_sc_1 {tot_scaled_len1: 8.2f}"
        logg.debug(recap)
