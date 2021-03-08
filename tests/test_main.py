from click.testing import CliRunner
import pytest

from chapter_align.__main__ import main  # type: ignore


@pytest.fixture
def runner():
    return CliRunner()


def test_main_succeeds_default_args(runner: CliRunner) -> None:
    """It exits with a status code of zero, using the default args."""
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_main_succeeds_with_args(runner: CliRunner) -> None:
    """It exits with a status code of zero, using CLI args."""
    result = runner.invoke(
        main,
        [
            "--book_base_folder",
            "data/leroux/yellow_room",
            "--language0",
            "english",
            "--language1",
            "french",
            "--ch_template0",
            "ch_{:04d}.xhtml",
            "--ch_template1",
            "main{}.xml",
            "--ch_start_index0",
            "10",
            "--ch_start_index1",
            "9",
            "--tot_chapter_num",
            "6",
            "--author_name",
            "Author",
            "--book_title",
            "Title",
        ],
    )
    assert result.exit_code == 0
