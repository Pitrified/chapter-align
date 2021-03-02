# Chapter align TODOs

### CLI

##### Done

* Finish a usable cli

### Docs

* Add docs with nox + sphinx

### Nox

* Add a lot more checks (eg on the docstrings, flake-*)

### Epub

* Somewhere there is a metadata regarding the language that must be set
  so that the correct dictionary is used by the Kindle.
  It should be line 5 in `tmpl_content.opf`:
  `<dc:language>en</dc:language>`
* In the original chapters a lot of classes are used,
  the styles should be copied.
