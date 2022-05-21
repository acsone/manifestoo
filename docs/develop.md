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

- Run `towncrier build --version {version}` to update `HISTORY.rst`.
- Run `tox -e docs` to update `docs/cli.md` and verify that the documentation builds
  correctly.
- Commit and push.
- Make sure the tests pass on GitHub.
- Create a tag and release on GitHub and let the CI publish to PyPI
