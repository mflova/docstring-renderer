# docstring-renderer

Wrapper around `docrepr` to get the rendered docstring of any given function from a Python file.

## Developper

### Testing

For testing, install the package with:

```bash
pip install .[dev]
```

Then, you can run all tests with:

```bash
pytest .
```

### Contributions

This repo makes use of different tools to ensure the code quality. These are:

  - pytest: To ensure that all unit tests are passing.
  - flake8: For code linting.
  - Black: To auto-format the code.
  - Mypy (strict): To ensure type hints are properly enforced.

A pre-push hook can be set up to ensure that all these tools are passing before pushing to the online repo. For it, you only need to:

```
# Rename the pre-push.sample to pre-push
mv pre-push.sample pre-push
```

And paste this content inside:

```bash
#!/bin/sh
git_root=$(git rev-parse --show-toplevel)

echo "Running black"
black --check ${git_root}
if [ $? != 0 ]; then
    exit 1
else
    echo "OK"
fi

echo "Running flake8"
flake8 ${git_root}
if [ $? != 0 ]; then
    exit 1
else
    echo "OK"
fi

echo "Running mypy"
mypy --exclude="build" ${git_root}
if [ $? != 0 ]; then
    exit 1
else
    echo "OK"
fi

echo "Running pytest"
pytest -m "not slow_test and not debugging_test" ${git_root}
if [ $? != 0 ]; then
    exit 1
else
    echo "OK"
fi

exit 0
```
