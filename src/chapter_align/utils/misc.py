import json
import logging
from pathlib import Path
import pycountry  # type: ignore
from string import ascii_lowercase
import typing as ty


def setup_logger(
    logLevel: str = "DEBUG", msg_type: str = "m"
) -> None:  # pragma: no cover
    r"""Setup logger that outputs to console for the module"""
    logroot = logging.getLogger("c")
    logroot.propagate = False
    logroot.setLevel(logLevel)

    module_console_handler = logging.StreamHandler()

    if msg_type == "anlm":
        log_format_module = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    elif msg_type == "nlm":
        log_format_module = "%(name)s - %(levelname)s: %(message)s"
    elif msg_type == "lm":
        log_format_module = "%(levelname)s: %(message)s"
    elif msg_type == "nm":
        log_format_module = "%(name)s: %(message)s"
    else:
        log_format_module = "%(message)s"

    formatter = logging.Formatter(log_format_module)
    module_console_handler.setFormatter(formatter)

    logroot.addHandler(module_console_handler)


def get_package_folders(which_folder: str = "root") -> Path:
    r"""Gets the relevant folders of the project"""
    logg = logging.getLogger(f"c.{__name__}.get_package_folders")
    # logg.setLevel("INFO")
    logg.debug("Start get_package_folders")

    this_file_folder = Path(__file__).absolute().parent
    logg.debug(f"{this_file_folder=}")

    package_root_folder = this_file_folder.parent.parent.parent

    if which_folder == "root":
        return package_root_folder

    elif which_folder == "tests":
        tests_folder = package_root_folder / "tests"
        return tests_folder

    elif which_folder == "template_epub":
        template_epub_folder = package_root_folder / "assets" / "template_epub"
        return template_epub_folder

    elif which_folder == "word_pairs":
        word_pairs_folder = package_root_folder / "assets" / "word_pairs"
        return word_pairs_folder

    elif which_folder == "common_words":
        common_words_folder = package_root_folder / "assets" / "common_words"
        return common_words_folder

    else:
        raise KeyError(f"Not recognized {which_folder}")


def load_word_pairs(languages: ty.Tuple[str, str]) -> ty.Dict[str, ty.List[str]]:
    r"""Load a dictionary of words.

    No filtering is done except for multi word entries.
    """
    logg = logging.getLogger(f"c.{__name__}.load_word_pairs")
    # logg.setLevel("DEBUG")
    logg.debug("Start load_word_pairs")

    lang0 = pycountry.languages.get(name=languages[0])
    lang_alpha2_tag0 = lang0.alpha_2
    lang1 = pycountry.languages.get(name=languages[1])
    lang_alpha2_tag1 = lang1.alpha_2

    word_pairs_folder = get_package_folders("word_pairs")
    lang_pairs_folder = word_pairs_folder / f"{lang_alpha2_tag0}_{lang_alpha2_tag1}"

    word_pairs_name_template = f"{lang_alpha2_tag0}_{lang_alpha2_tag1}_{{}}.json"

    all_word_pairs: ty.Dict[str, ty.List[str]] = {}

    for letter in ascii_lowercase:
        word_pairs_name = word_pairs_name_template.format(letter)
        word_pairs_path = lang_pairs_folder / word_pairs_name
        logg.debug(f"word_pairs_path: {word_pairs_path}")

        word_pairs_letter = json.loads(word_pairs_path.read_text(encoding="utf-8"))

        for word0 in word_pairs_letter:

            # filter entries with more than one word
            if " " in word0:
                continue

            # add the whole list to the known dict
            all_word_pairs[word0] = word_pairs_letter[word0]

    logg.info(f"len(all_word_pairs): {len(all_word_pairs)}")

    return all_word_pairs


def load_common_words(language: str, tot_num: int) -> ty.Set[str]:
    r"""Load a list of common words for a language."""
    logg = logging.getLogger(f"c.{__name__}.load_common_words")
    logg.setLevel("DEBUG")
    logg.debug("Start load_common_words")

    lang = pycountry.languages.get(name=language)
    lang_alpha2_tag = lang.alpha_2

    common_words_folder = get_package_folders("common_words")
    common_words_path = common_words_folder / f"{lang_alpha2_tag}.txt"

    common_words = set()
    with common_words_path.open() as common_words_file:
        for line in common_words_file:
            common_words.add(line.strip())
            if len(common_words) == tot_num:
                break

    logg.debug(f"common_words: {common_words}")

    return common_words
