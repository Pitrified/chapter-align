# Chapter align TODOs

## Misc

* Colors for the prompt.

## Test

* Test the interactive prompt with a
  [context manager](https://stackoverflow.com/a/36491341/2237151).

```python
import sys
from contextlib import contextmanager

@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig

    # use it with
with replace_stdin(StringIO("some preprogrammed input")):
    module.call_function()
```

## Align

* Do not generate `hint_indexes0` but add 5 to wherever you end up to.
* Show only beginning and end of the sentences, option to show all.
* The prompts to the user should not be on the debug logger,
  but on a separate one.
* Shift all subsequent links using the acquired hints.

##### Done

* Split in separate function the analysis of a single chapter.
* Option to make hint window bigger (`w+1`).
* Check if the combined chapter exists already.

## CLI

* Flags to do only align/build epub.
* Indexes for first/last chapter to analyze.

##### Done

* Finish a usable cli.

## Docs

* Add docs with nox + sphinx.

## Nox

* Add a lot more checks (eg on the docstrings, flake-*).

## Epub

* Somewhere there is a metadata regarding the language that must be set
  so that the correct dictionary is used by the Kindle.
  It should be line 5 in `tmpl_content.opf`:
  `<dc:language>en</dc:language>`
  Set it based on l1.
  Also somewhere else, look for `en`.
* There is a mysterious lang attribute that can be put in `<p>` tags, maybe two
  dictionaries can be used?
* In the original chapters a lot of classes are used,
  the styles should be copied.
