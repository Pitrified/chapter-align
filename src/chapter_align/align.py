from pathlib import Path
import logging
import typing as ty

from .utils.load_chapters import load_chapter
from .utils.SentenceList import SentenceList
from .utils.misc import get_package_folders


def align_book(
    book_folder: Path,
    languages: ty.Tuple[str, str],
    chapter_templates: ty.Tuple[str, str],
    chapter_start_indexes: ty.Tuple[int, int],
    tot_chapter_num: int,
    author_name_full: str,
    book_name_full: str,
) -> None:
    r"""Align every chapter in a book

    l1 paragraphs have to be after l0
    we track tot_len0 and scaled_len1

    if the old tot_len0 is smaller than scaled_len1
        add the l0 paragraph
        (we want to read the l0 paragraph before the l1)
    else
        add the l1 paragraph

            l0    l1
           ----------
    >  0:    a     a
    >  1:          b
    >  2:    bc    c
    >  3:    def   d
    >  4:    g     e
    >  5:    h     f
    >  6:    i     g
    >  7:    jkl   h
    >  8:    _     i
    >  9:    _     j
    > 10:    _     k
    > 11:    _     l
    """
    logg = logging.getLogger(f"c.{__name__}.align_book")
    # logg.setLevel("DEBUG")
    logg.debug("Start align_book")

    #############################################################
    # build the input/output paths
    #############################################################

    # get the chapter output folder
    composed_folder = book_folder / "composed"
    if not composed_folder.exists():  # pragma: nocover
        composed_folder.mkdir(parents=True, exist_ok=True)

    # get the template path
    template_epub_folder = get_package_folders("template_epub")
    tmpl_ch_path = template_epub_folder / "tmpl_ch.xhtml"
    # load the template
    tmpl_ch = tmpl_ch_path.read_text()

    # build the composed tag
    composed_tag = f"{languages[0]}/{languages[1]}"

    # for chapter_index in list(range(tot_chapter_num))[10:11]:
    for chapter_index in list(range(tot_chapter_num))[:]:
        chapter_index0 = chapter_index + chapter_start_indexes[0]
        chapter_index1 = chapter_index + chapter_start_indexes[1]
        recap = f"\nchapter_index0: {chapter_index0}"
        recap += f" chapter_index1: {chapter_index1}"
        logg.info(recap)

        #############################################################
        # load the chapter for l0
        #############################################################

        lang_folder0 = book_folder / languages[0]
        chapter_name0 = chapter_templates[0].format(chapter_index0)
        chapter_path0 = lang_folder0 / chapter_name0
        sent0 = load_chapter(chapter_path0)

        recap = f"{chapter_path0=}"
        recap += f" len(sent0): {len(sent0)}"
        recap += f" sent0.tot_chars: {sent0.tot_chars}"
        logg.info(recap)

        #############################################################
        # load the chapter for l1
        #############################################################

        lang_folder1 = book_folder / languages[1]
        chapter_name1 = chapter_templates[1].format(chapter_index1)
        chapter_path1 = lang_folder1 / chapter_name1
        sent1 = load_chapter(chapter_path1)

        recap = f"{chapter_path1=}"
        recap += f" len(sent1): {len(sent1)}"
        recap += f" sent1.tot_chars: {sent1.tot_chars}"
        logg.info(recap)

        #############################################################
        # compute the incremental lengths
        #############################################################

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

        #############################################################
        # align the paragraphs
        #############################################################

        # the index of the NEXT sentence to add
        added0: int = 1
        added1: int = 0

        composed = SentenceList()

        # the first paragraph is always from l0
        composed.append(sent0[0])

        # the state of the two lists
        available0 = True
        available1 = True

        while available0 or available1:
            recap = f">>>>>> {added0} {added1}"

            old_tot0 = inc_len0[added0 - 1]
            curr_tot_sca1 = inc_sca_len1[added1]

            if old_tot0 < curr_tot_sca1 and available0:
                composed.append(sent0[added0])
                recap += f" - added0 {added0}"
                added0 += 1
                recap += f" - incremented to {added0}"
                if added0 >= len(sent0):
                    available0 = False
            else:
                # this seems really shaky but it sould never try to access a sentence
                # out of bounds: this side is only called when curr_tot_sca1 is smaller
                # than old_tot0, and the last inc_sca_len1 is exactly equal to the last
                # inc_len0 (it is rescaled), so if the last inc_sca_len1 is added all
                # the inc_len0 have already been added and available0 is False and the
                # loop happily quits
                # or maybe it's 2am and I should check again

                if available1 is False:  # pragma: nocover - this should not happen
                    recap = f">>>>>> {added0} {added1}"
                    recap += " Something strange happened while composing"
                    recap += " {chapter_path0=}"
                    recap += " {chapter_path1=}"
                    recap += " {chapter_index=}"
                    logg.warning(recap)
                    break

                composed.append(sent1[added1])
                recap += f" - added1 {added1}"
                added1 += 1
                recap += f" - incremented to {added1}"
                if added1 >= len(sent1):
                    available1 = False

            logg.debug(recap)

        # both lists must be depleted
        assert added0 == len(sent0) and added1 == len(sent1)

        #############################################################
        # save the composed chapter
        #############################################################

        # build the chapter content
        composed_chapter_text = ""
        for i, sent in enumerate(composed):
            composed_chapter_text += f"{sent.orig_str}\n"
            recap = f"\n>>>>>> {i}"
            recap += f"\n>{sent}<"
            logg.debug(recap)

        # get the chapter output path
        composed_chapter_name = f"ch_{chapter_index+1:04d}.xhtml"
        composed_chapter_path = composed_folder / composed_chapter_name

        # build a vague chapter title
        chapter_title = f"Chapter {chapter_index+1}"

        # create the full chapter text
        full_ch_text = tmpl_ch.format(
            book_title=book_name_full,
            book_author=author_name_full,
            composed_tag=composed_tag,
            chapter_title=chapter_title,
            chapter_content=composed_chapter_text,
        )

        composed_chapter_path.write_text(full_ch_text)
