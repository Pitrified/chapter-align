from click.testing import CliRunner
import pytest

from chapter_align.__main__ import main  # type: ignore


@pytest.fixture
def runner():
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main)
    assert result.exit_code == 0
