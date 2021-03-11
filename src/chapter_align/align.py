import logging
from pathlib import Path
import typing as ty

# import prettierfier  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import pycountry  # type: ignore
from termcolor import colored

# from .utils.customhtmlparser import MyHTMLParser
from .utils.Sentence import Sentence
from .utils.SentenceList import SentenceList
from .utils.load_chapters import load_chapter
from .utils.misc import get_package_folders


def color_in_dict(
    color_sent: Sentence, match_sentences: ty.List[Sentence], color: str = "yellow"
) -> str:
    r"""MAKEDOC: what is color_in_dict doing?"""
    logg = logging.getLogger(f"c.{__name__}.color_in_dict")
    # logg.setLevel("DEBUG")
    logg.debug("Start color_in_dict")

    # build set of words in match_sent
    words_seen = set()
    for match_sent in match_sentences:
        for word in match_sent.norm_tra.split(" "):
            # keep vaguely interesting words
            if len(word) < 4:
                continue
            words_seen.add(word)

    logg.debug(f"words_seen: {words_seen}")

    color_str = ""
    for word in color_sent.norm_tra.split(" "):
        matched = False
        for match_word in words_seen:
            frac_match = int(len(match_word) * 0.6)

            # keep vaguely interesting matches
            if frac_match < 3:
                continue

            match_word = match_word.lower()
            word = word.lower()

            if word.startswith(match_word[:frac_match]):
                logg.debug(f"word: {word} matches {match_word}")
                matched = True

        # if the beginning of a seen word is in the current word, color it
        # if match_word[:frac_match] in word:
        if matched:
            color_str += colored(f"{word} ", color)
        else:
            color_str += f"{word} "

    return color_str


def align_chapter_basic(
    sent0: SentenceList,
    sent1: SentenceList,
    inc_len0: ty.List[int],
    inc_sca_len1: ty.List[float],
) -> ty.Tuple[SentenceList, ty.List[ty.Tuple[int, int]]]:
    r"""MAKEDOC: what is align_chapter_basic doing?

    l1 paragraphs have to be after l0
    we track the current len for l0 and the scaled len for l1

    if the old tot_len0 is smaller than scaled_len1
        add the l0 paragraph
        (we want to read the l0 paragraph before the l1)
    else
        add the l1 paragraph
    finally
        add the remaining paragraphs

             p0       p1        link
           len0     len1     sc_len1
           tot0     tot1      t_sc_1
         ----------------------------
    >  0      a        A           0
             46  |    47  |    43.08
             46  |    47  |    43.08
    >  1      -        B           0
              1  |   306  |   280.47
             47  |   353  |   323.55
    >  2     bc        C           1
            857  |   551  |   505.03
            904  |   904  |   828.57
    >  3    def        D           3
           1289  |   147  |   134.73
           2193  |  1051  |   963.31
    >  4      g        E           6
            723  |   774  |   709.42
           2916  |  1825  |  1672.72
    >  5      h        F           7
             95  |   582  |   533.44
           3011  |  2407  |  2206.16
    >  6      i        G           8
            406  |   664  |   608.60
           3417  |  3071  |  2814.76
    >  7    jkl        H           9
            768  |    76  |    69.66
           4185  |  3147  |  2884.42
    >  8      -        I           -
            916  |   388  |   355.63
           5101  |  3535  |  3240.04
    >  9      -        J           -
           1520  |   305  |   279.55
           6621  |  3840  |  3519.60
    > 10      -        K           -
            820  |   337  |   308.88
           7441  |  4177  |  3828.48
    > 11      -        L           -
            532  |   152  |   139.32
           7973  |  4329  |  3967.79
    """
    logg = logging.getLogger(f"c.{__name__}.align_chapter_basic")
    # logg.setLevel("DEBUG")
    logg.debug("Start align_chapter_basic")

    # the first paragraph is always from l0: if in l1 the first paragraph is split in
    # smaller sentences, those are not added before the long single paragraph from l0

    # the index of the NEXT sentence to add
    next0: int = 1
    next1: int = 0

    # the aligned list of sentences
    composed = SentenceList()
    composed.append(sent0[0])

    # the aligned list of indexes
    composed_indexes: ty.List[ty.Tuple[int, int]] = [(0, 0)]

    # while there are sentences left on either list
    while next0 < len(sent0) and next1 < len(sent1):
        recap = f"> next {next0: 3d} {next1: 3d}"
        recap += f" curr {next0-1: 3d} {next1-1: 3d}"
        logg.debug(recap)

        # we know that there are more sentences on BOTH

        # the total length if the next was added
        curr_tot0 = inc_len0[next0 - 1]
        next_tot0 = inc_len0[next0]
        next_tot_sca1 = inc_sca_len1[next1]
        recap = f" curr_tot0: {curr_tot0}"
        recap += f"  next_tot0: {next_tot0}"
        recap += f"  next_tot_sca1: {next_tot_sca1:.2f}"
        logg.debug(recap)

        # different approach
        # if the end of the next l0 is lower than the next l1
        # if next_tot0 <= next_tot_sca1 :

        # if the current 0 is still lower than the next 1
        # you need to add p0
        # add the sentence 0
        if curr_tot0 <= next_tot_sca1:
            composed.append(sent0[next0])
            logg.debug(f"  add 0: {next0}")
            composed_indexes.append((0, next0))
            next0 += 1

        # add the sentence 1
        else:
            composed.append(sent1[next1])
            logg.debug(f"            add 1: {next1}")
            composed_indexes.append((1, next1))
            next1 += 1

    # we check if there are more sentences on l0
    if next0 < len(sent0):
        logg.debug("  finish 0")
        while next0 < len(sent0):
            composed.append(sent0[next0])
            logg.debug(f"  add 0: {next0}")
            composed_indexes.append((0, next0))
            next0 += 1

    # we check if there are more sentences on l1
    if next1 < len(sent1):
        logg.debug("  finish 1")
        while next1 < len(sent1):
            composed.append(sent1[next1])
            logg.debug(f"  add 1: {next1}")
            composed_indexes.append((1, next1))
            next1 += 1

    return composed, composed_indexes


def compute_incremental_len(
    sent0: SentenceList, sent1: SentenceList
) -> ty.Tuple[float, ty.List[int], ty.List[float]]:
    r"""MAKEDOC: what is compute_incremental_len doing?"""
    logg = logging.getLogger(f"c.{__name__}.compute_incremental_len")
    # logg.setLevel("DEBUG")
    logg.debug("Start compute_incremental_len")

    tot_len0: int = 0
    tot_len1: int = 0
    tot_scaled_len1: float = 0
    scaling_factor = sent0.tot_chars / sent1.tot_chars
    logg.debug(f"scaling_factor: {scaling_factor}")

    logg.debug(f"len(sent0): {len(sent0)}")
    logg.debug(f"len(sent1): {len(sent1)}")

    inc_len0: ty.List[int] = []
    inc_sca_len1: ty.List[float] = []

    # for i in range(len(sent0), len(sent1)):
    for i in range(len(sent0)):
        len0 = sent0[i].len_norm_tra
        tot_len0 += len0

        inc_len0.append(tot_len0)

    for i in range(len(sent1)):
        len1 = sent1[i].len_norm_tra
        tot_len1 += len1

        scaled_len1 = len1 * scaling_factor
        tot_scaled_len1 += scaled_len1

        inc_sca_len1.append(tot_scaled_len1)

    # this fancy log is done by iterating over both lists at once
    # recap = f"\n>>>>>> {i}"
    # recap += f"\n0 ({len0}): >{sent0[i]}<"
    # recap += f"\n1 ({len1}): >{sent1[i]}<"
    # recap += f"\nlen0 {len0: 6d}"
    # recap += f"  |  len1 {len1: 6d}"
    # recap += f"  |  sc_len1 {scaled_len1: 10.2f}"
    # recap += f"\ntot0 {tot_len0: 6d}"
    # recap += f"  |  tot1 {tot_len1: 6d}"
    # recap += f"  |  t_sc_1  {tot_scaled_len1: 10.2f}"
    # logg.debug(recap)

    return scaling_factor, inc_len0, inc_sca_len1


def interactive_hints(  # noqa: C901 very COMPLEX sorry
    sent0: SentenceList,
    sent1: SentenceList,
    composed_indexes: ty.List[ty.Tuple[int, int]],
    hint_dist: int = -1,
) -> ty.List[ty.Tuple[int, int]]:
    r"""MAKEDOC: what is interactive_hints doing?"""
    logg = logging.getLogger(f"c.{__name__}.interactive_hints")
    logg.setLevel("DEBUG")
    logg.debug("Start interactive_hints")

    for ci in composed_indexes:
        logg.debug(f"{'    ' if ci[0] == 1 else ''}{ci[1]: 3d}")

    # build the links from s0 to s1, to provide a better prompt
    curr_i1: int = len(sent1) - 1
    link0to1: ty.List[int] = []
    for ci in composed_indexes[::-1]:
        if ci[0] == 0:
            link0to1.insert(0, curr_i1)
        else:
            curr_i1 = ci[1]

    for i in range(len(link0to1)):
        logg.debug(f"i: {i} -> {link0to1[i]}")

    hint_indexes0 = list(range(3, len(sent0), hint_dist))
    logg.debug(f"hint_indexes0: {hint_indexes0}")

    logg.debug(f"len(sent0): {len(sent0)}")
    logg.debug(f"len(sent1): {len(sent1)}")

    # a visible tag
    vt = ">>>>>> "
    tv = " <<<<<<"

    # the hint will link a sentence from l0 to l1
    hints: ty.List[ty.Tuple[int, int]] = []

    window_size0 = 1
    window_size1 = 4

    for hi0 in hint_indexes0:

        done = False
        curr_hi0 = hi0
        curr_window_size0 = window_size0
        curr_window_size1 = window_size1

        while not done:

            # extract the central index for l1
            i1 = link0to1[curr_hi0]

            # line to split the flow
            recap = f"\n{vt*3}"
            recap += colored(f"curr_hi0: {curr_hi0} -> {i1}", "cyan")
            recap += f"{tv*3}"
            logg.debug(recap)

            # the l0 sentence to align
            # logg.debug(f"sent0[{curr_hi0}]:\n{sent0[curr_hi0]}")
            i0_min = max(curr_hi0 - curr_window_size0, 0)
            i0_max = min(curr_hi0 + curr_window_size0, len(sent0) - 1)
            # logg.debug(f"i0_min: {i0_min} i0_max: {i0_max} cws {curr_window_size0}")
            for hi0_show in range(i0_min, i0_max + 1):
                recap = f"\n{vt}"
                if hi0_show == curr_hi0:
                    recap += colored(f"sent0[{hi0_show}]:", "green", attrs=["bold"])
                    recap += f"{tv}"
                else:
                    recap += f"sent0[{hi0_show}]:"
                # recap += f"\n{sent0[hi0_show]}"
                recap += f"\n{color_in_dict(sent0[hi0_show], [sent1[i1]])}"
                logg.debug(recap)

            # line to split the flow
            recap = f"\n{vt*3}"
            recap += colored(f"{vt}{tv}", "cyan")
            recap += f"{tv*3}"
            logg.debug(recap)

            # the range of l1 sentences to pick from
            i1_min = max(i1 - curr_window_size1, 0)
            i1_max = min(i1 + curr_window_size1, len(sent1) - 1)
            for hi1 in range(i1_min, i1_max + 1):
                recap = f"\n{vt}"
                if hi1 == i1:
                    recap += colored(
                        f"sent1[{hi1-i1}] ({hi1}):", "green", attrs=["bold"]
                    )
                    recap += f"{tv}"
                else:
                    recap += f"sent1[{hi1-i1}] ({hi1}):"
                # recap += f"\n{sent1[hi1]}"
                recap += f"\n{color_in_dict(sent1[hi1], [sent0[curr_hi0]])}"
                logg.debug(recap)

            prompt = "Change the l0 sentence: s0[NUM]."
            prompt += "\tChange the window size: w{0|1}[NUM]."
            prompt += "\tInsert the correct l1 sentence: [NUM]: "
            ri = input(prompt)

            # change the l0 sentence
            if ri.startswith("s0"):
                ri_cmd = ri[2:]
                recap = f"Change l0: parsing {ri}"
                recap += f" ri_cmd {ri_cmd}"
                logg.debug(recap)

                try:
                    delta_hi0 = int(ri_cmd)
                except ValueError:
                    logg.warning(f"{ri_cmd} is not a valid integer.")
                    delta_hi0 = 0
                curr_hi0 += delta_hi0

                # validate the value for hi0
                curr_hi0 = max(curr_hi0, 0)
                curr_hi0 = min(curr_hi0, len(sent0) - 1)
                logg.debug(f"Using delta_hi0: {delta_hi0} curr_hi0: {curr_hi0}")

            # change the window size
            elif ri.startswith("w0") or ri.startswith("w1"):
                ri_type = ri[:2]
                ri_cmd = ri[2:]
                recap = f"Window size: parsing {ri}"
                recap += f" ri_type {ri_type} ri_cmd {ri_cmd}"
                logg.debug(recap)

                try:
                    delta_winsize = int(ri_cmd)
                except ValueError:
                    logg.warning(f"{ri_cmd} is not a valid integer.")
                    delta_winsize = 0

                if ri_type == "w0":
                    curr_window_size0 += delta_winsize
                    # validate win size, must be at least 0 for l0
                    curr_window_size0 = max(curr_window_size0, 0)

                elif ri_type == "w1":
                    curr_window_size1 += delta_winsize
                    # validate win size, must be at least 2 for l1
                    curr_window_size1 = max(curr_window_size1, 2)

            # select which sentence to align
            else:
                ri_cmd = ri
                try:
                    delta_hi1 = int(ri_cmd)
                    good_hi1 = i1 + delta_hi1
                    # validate the result, within the list
                    good_hi1 = max(good_hi1, 0)
                    good_hi1 = min(good_hi1, len(sent1) - 1)
                    done = True
                except ValueError:
                    logg.warning(f"{ri_cmd} is not a valid integer.")

        logg.debug(f"\n{vt}Adding curr_hi0: {curr_hi0} good_hi1: {good_hi1}")
        hints.append((curr_hi0, good_hi1))

    # sanity check
    for hint in hints:
        logg.debug(f"\n{vt*3}{hint}")
        logg.debug(f"{vt}sent0[{hint[0]}]:\n{sent0[hint[0]]}")
        logg.debug(f"{vt}sent1[{hint[1]}]:\n{sent1[hint[1]]}")

    return hints


def align_with_hints(
    sent0: SentenceList,
    sent1: SentenceList,
    inc_len0: ty.List[int],
    inc_sca_len1: ty.List[float],
    hints: ty.List[ty.Tuple[int, int]],
) -> SentenceList:
    r"""MAKEDOC: what is align_with_hints doing?

    We basically copy align_chapter_basic but fancier.
    """
    logg = logging.getLogger(f"c.{__name__}.align_with_hints")
    logg.setLevel("DEBUG")
    logg.debug("Start align_with_hints")

    # the aligned list of sentences
    composed = SentenceList()

    # the aligned list of indexes
    composed_indexes: ty.List[ty.Tuple[int, int]] = []

    # a visible tag
    vt = ">>>>>> "

    logg.debug(f"len(sent0): {len(sent0)}")
    logg.debug(f"len(sent1): {len(sent1)}")

    # add artificial first and last hint
    hints.insert(0, (0, 0))
    hints.append((len(sent0), len(sent1)))

    for ih, hint in enumerate(hints[:-1]):

        next_hint = hints[ih + 1]
        logg.debug(f"\n{vt*3}{hint} - {next_hint}{vt*3}\n")

        # how many sentences in each list to use
        chunk_len0 = next_hint[0] - hint[0]
        chunk_len1 = next_hint[1] - hint[1]

        # the index of the NEXT sentence to add, relative to the hint
        rel_next0: int = 1
        rel_next1: int = 0

        # add a Sentence to debug things
        # sentence_soup = BeautifulSoup("<p>New hint.</p>", "html.parser")
        # sentence_tag = sentence_soup.find_all("p")[0]
        # composed.append(Sentence(sentence_tag))

        # add the first sentence from l0
        composed.append(sent0[hint[0]])
        composed_indexes.append((0, hint[0]))
        logg.debug(f"  add 0 manual: {hint[0]}")

        # track the amount of chars in each side relative to the start of the hint
        start_curr_tot0 = inc_len0[hint[0]]
        start_next_tot_sca1 = inc_sca_len1[hint[1]]

        while rel_next0 < chunk_len0 and rel_next1 < chunk_len1:
            # the absolute position in the SentenceList
            next0 = hint[0] + rel_next0
            next1 = hint[1] + rel_next1

            recap = f"> rel_next {rel_next0: 2d} {rel_next1: 2d}"
            recap += f"  -  curr {rel_next0-1: 2d} {rel_next1-1: 2d}"
            recap += f"  -  next {next0: 2d} {next1: 2d}"
            logg.debug(recap)

            # the relative amount of chars in each side
            curr_tot0 = inc_len0[next0 - 0] - start_curr_tot0
            next_tot_sca1 = inc_sca_len1[next1] - start_next_tot_sca1
            recap = f"  curr_tot0: {curr_tot0}"
            recap += f"  next_tot_sca1: {next_tot_sca1:.2f}"
            logg.debug(recap)

            # if the current 0 is still lower than the next 1
            # you need to add p0
            # add the sentence 0
            if curr_tot0 <= next_tot_sca1:
                composed.append(sent0[next0])
                logg.debug(f"  add 0: {next0}")
                composed_indexes.append((0, next0))
                rel_next0 += 1

            # add the sentence 1
            else:
                composed.append(sent1[next1])
                logg.debug(f"            add 1: {next1}")
                composed_indexes.append((1, next1))
                rel_next1 += 1

        recap = f"> rel_next0 {rel_next0: 2d} chunk_len0 {chunk_len0: 2d}"
        logg.debug(recap)
        if rel_next0 < chunk_len0:
            logg.debug("  finish 0")
            while rel_next0 < chunk_len0:
                next0 = hint[0] + rel_next0
                composed.append(sent0[next0])
                logg.debug(f"  add 0: {next0}")
                composed_indexes.append((0, next0))
                rel_next0 += 1

        recap = f"> rel_next1 {rel_next1: 2d} chunk_len1 {chunk_len1: 2d}"
        logg.debug(recap)
        if rel_next1 < chunk_len1:
            logg.debug("  finish 1")
            while rel_next1 < chunk_len1:
                next1 = hint[1] + rel_next1
                composed.append(sent1[next1])
                logg.debug(f"  add 1: {next1}")
                composed_indexes.append((1, next1))
                rel_next1 += 1

    # sanity check
    for ci in composed_indexes:
        logg.debug(f"{'    ' if ci[0] == 1 else ''}{ci[1]: 3d}")

    return composed


def align_chapter(sent0: SentenceList, sent1: SentenceList) -> SentenceList:
    r"""MAKEDOC: what is align_chapter doing?"""
    logg = logging.getLogger(f"c.{__name__}.align_chapter")
    logg.setLevel("DEBUG")
    logg.debug("Start align_chapter")

    #############################################################
    # compute the incremental lengths
    #############################################################

    scaling_factor, inc_len0, inc_sca_len1 = compute_incremental_len(sent0, sent1)

    #############################################################
    # align the paragraphs with basic method
    #############################################################

    composed, composed_indexes = align_chapter_basic(
        sent0, sent1, inc_len0, inc_sca_len1
    )

    #############################################################
    # use the basic alignment to prompt for hints
    #############################################################

    do_interactive = True
    hint_dist = 5

    if do_interactive:
        hints = interactive_hints(sent0, sent1, composed_indexes, hint_dist)
        composed = align_with_hints(sent0, sent1, inc_len0, inc_sca_len1, hints)

    return composed


def align_book(
    book_folder: Path,
    languages: ty.Tuple[str, str],
    chapter_templates: ty.Tuple[str, str],
    chapter_start_indexes: ty.Tuple[int, int],
    tot_chapter_num: int,
    author_name_full: str,
    book_name_full: str,
) -> None:
    r"""Align every chapter in a book"""
    logg = logging.getLogger(f"c.{__name__}.align_book")
    logg.setLevel("DEBUG")
    logg.info("\nStart align_book")

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

        # get the chapter output path
        composed_chapter_name = f"ch_{chapter_index+1:04d}.xhtml"
        composed_chapter_path = composed_folder / composed_chapter_name

        if composed_chapter_path.exists():
            logg.info(f"Skipping: {composed_chapter_path}, already processed.")
            continue

        #############################################################
        # load the chapter for l0
        #############################################################

        lang_folder0 = book_folder / languages[0]
        chapter_name0 = chapter_templates[0].format(chapter_index0)
        chapter_path0 = lang_folder0 / chapter_name0
        lang0 = pycountry.languages.get(name=languages[0])
        logg.debug(f"lang0: {lang0}")
        lang_alpha2_tag0 = lang0.alpha_2
        sent0 = load_chapter(chapter_path0, lang_alpha2_tag0)

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
        lang1 = pycountry.languages.get(name=languages[1])
        logg.debug(f"lang1: {lang1}")
        lang_alpha2_tag1 = lang1.alpha_2
        sent1 = load_chapter(chapter_path1, lang_alpha2_tag1)

        recap = f"{chapter_path1=}"
        recap += f" len(sent1): {len(sent1)}"
        recap += f" sent1.tot_chars: {sent1.tot_chars}"
        logg.info(recap)

        #############################################################
        # align the two SentenceList
        #############################################################

        composed = align_chapter(sent0, sent1)

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

        # composed_chapter_path.write_text(full_ch_text)

        # full_ch_text = full_ch_text.replace("\n", " ")
        # parser = MyHTMLParser()
        # parser.feed(full_ch_text)
        # parsed_text = parser.get_parsed_string()
        # composed_chapter_path.write_text(parsed_text)

        # build a soup for the chapter
        parsed_text = BeautifulSoup(full_ch_text, features="html.parser")
        # write the prettified text
        composed_chapter_path.write_text(parsed_text.prettify())

        # prettierfier!
        # pretty_text = prettierfier.prettify_html(parsed_text)
        # composed_chapter_path.write_text(pretty_text)
