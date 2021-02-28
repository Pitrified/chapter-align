import logging

import click

from . import __version__
from .utils.misc import setup_logger


@click.command()
@click.option(
    "-lld",
    "--log_level_debug",
    type=click.Choice(
        ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="DEBUG",
    help="Level for the debugging logger",
    show_default=True,
)
@click.option(
    "-llt",
    "--log_level_type",
    type=click.Choice(["anlm", "nlm", "lm", "nm", "m"], case_sensitive=False),
    default="m",
    help="Message format for the debugging logger",
    show_default=True,
)
@click.version_option(version=__version__)
def main(log_level_debug: str, log_level_type: str) -> None:
    r"""MAKEDOC: What is main doing?"""
    setup_logger(log_level_debug, log_level_type)
    logg = logging.getLogger(f"c.{__name__}.main")
    logg.debug("Starting main")


if __name__ == "__main__":  # pragma: no cover
    main()
