# Chapter align TODOs

## Misc

* Colors for the prompt.
* Merge CSS from the two originals, keep the `l1` in conflicts (and warn the user).

## NMT

### Model

* Package in the contents of this tutorial:
    [Neural machine translation with attention](https://www.tensorflow.org/tutorials/text/nmt_with_attention)
* Fix this `KeyError`, use `UNK` or a similar fallback:

```python
Traceback (most recent call last):
  File "nmt_with_attention.py", line 712, in <module>
    translate("trata de averiguarlo.")
  File "nmt_with_attention.py", line 670, in translate
    result, sentence, attention_plot = evaluate(sentence)
  File "nmt_with_attention.py", line 610, in evaluate
    inputs = [inp_lang.word_index[i] for i in sentence.split(" ")]
  File "nmt_with_attention.py", line 610, in <listcomp>
    inputs = [inp_lang.word_index[i] for i in sentence.split(" ")]
KeyError: 'trata'
```

### Install

* Optional install of `tensorflow`:
    [Poetry](https://python-poetry.org/docs/pyproject/#extras),
    [SO](https://stackoverflow.com/a/60990574/2237151).

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
* Also flags for training the model.
* Indexes for first/last chapter to analyze.
* Single option for `l01`, pass a list.

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
