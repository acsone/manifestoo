# Development workflow

## Linters

This project uses [pre-commit](https://pre-commit.com/) to check and apply various
linters.

Run `pre-commit install` in your local git clone to be sure to apply them locally before
pushing to GitHub.

## Running tests

To debug tests, install the project in a virtual environment using
`pip install -e .[test]`. You can then run tests using `pytest`.

You can also run all tests using `tox`.

## Creating a release

- Update the version in `pyproject.toml`.
- Run `towncrier` to update `HISTORY.rst`.
- Run `tox docs` to update `docs/cli.md` and verify that the documentation builds
  correctly.
- Publish using `flit publish`. Do *not* use `python -m build` to create the sdist,
  because it would be [incomplete](https://github.com/pypa/flit/issues/540).
