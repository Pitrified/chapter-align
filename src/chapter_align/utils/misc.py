from pathlib import Path
import logging


def setup_logger(
    logLevel: str = "DEBUG", msg_type: str = "m"
) -> None:  # pragma: no cover
    r"""Setup logger that outputs to console for the module"""
    logroot = logging.getLogger("c")
    logroot.propagate = False
    logroot.setLevel(logLevel)

    module_console_handler = logging.StreamHandler()

    if msg_type == "anlm":
        log_format_module = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
        package_tests_folder = package_root_folder / "tests"
        return package_tests_folder

    else:
        raise KeyError(f"Not recognized {which_folder}")
