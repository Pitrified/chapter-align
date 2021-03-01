from pathlib import Path
import logging
import typing as ty

from .utils.load_chapters import load_chapter
from .utils.SentenceList import SentenceList


def align_book(
    book_folder: Path,
    languages: ty.Tuple[str, str],
    chapter_templates: ty.Tuple[str, str],
) -> None:
    r"""Align every chapter in a book

    l1 has to be after l0
    we track tot_len0 and scaled_len1

    if the old tot_len0 is still smaller than scaled_len1
        add the l0 paragraph
    else
        add the l1 paragraph

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
    # logg.setLevel("DEBUG")
    logg.debug("Start align_book")

    chapter_index = 6
    # TODO, the starting index sould be different for the two books

    # skip_interval = 5

    # load the chapter for l0
    lang_folder0 = book_folder / languages[0]
    chapter_name0 = chapter_templates[0].format(chapter_index)
    chapter_path0 = lang_folder0 / chapter_name0
    logg.debug(f"{chapter_path0=}")

    sent0 = load_chapter(chapter_path0)

    recap = f"len(sent0): {len(sent0)}"
    recap += f" sent0.tot_chars: {sent0.tot_chars}"
    logg.debug(recap)

    # load the chapter for l1
    lang_folder1 = book_folder / languages[1]
    chapter_name1 = chapter_templates[1].format(chapter_index)
    chapter_path1 = lang_folder1 / chapter_name1
    logg.debug(f"{chapter_path1=}")

    sent1 = load_chapter(chapter_path1)

    recap = f"len(sent1): {len(sent1)}"
    recap += f" sent1.tot_chars: {sent1.tot_chars}"
    logg.debug(recap)

    tot_len0: int = 0
    tot_len1: int = 0
    tot_scaled_len1: float = 0
    scaling_factor = sent0.tot_chars / sent1.tot_chars
    logg.debug(f"scaling_factor: {scaling_factor}")

    inc_len0: ty.List[int] = []
    inc_sca_len1: ty.List[float] = []

    for i in range(max(len(sent0), len(sent1))):
        len0 = sent0[i].len_norm_tra
        tot_len0 += len0

        len1 = sent1[i].len_norm_tra
        tot_len1 += len1

        scaled_len1 = len1 * scaling_factor
        tot_scaled_len1 += scaled_len1

        inc_len0.append(tot_len0)
        inc_sca_len1.append(tot_scaled_len1)

        recap = f"\n>>>>>> {i}"
        recap += f"\n0 ({len0}): >{sent0[i]}<"
        recap += f"\n1 ({len1}): >{sent1[i]}<"
        recap += f"\nlen0 {len0: 6d} len1 {len1: 6d} sc_len1 {scaled_len1: 10.2f}"
        recap += f"\ntot0 {tot_len0: 6d} tot1 {tot_len1: 6d} t_sc_1  {tot_scaled_len1: 10.2f}"
        logg.debug(recap)

    logg.debug(f"inc_len0: {inc_len0}")
    logg.debug(f"inc_sca_len1: {inc_sca_len1}")

    # the index of the NEXT sentence to add
    added0: int = 1
    added1: int = 0

    composed = SentenceList()

    # the first paragraph is always from l0
    composed.append(sent0[0])

    while added0 < len(sent0) or added1 < len(sent1):
        recap = f">>>>>> {added0} {added1}"
        logg.debug(recap)

        old_tot0 = inc_len0[added0 - 1]
        curr_tot_sca1 = inc_sca_len1[added1]

        if old_tot0 < curr_tot_sca1:
            composed.append(sent0[added0])
            added0 += 1
        else:
            composed.append(sent1[added1])
            added1 += 1

    for i, sent in enumerate(composed):
        recap = f"\n>>>>>> {i}"
        recap += f"\n>{sent}<"
        logg.debug(recap)
