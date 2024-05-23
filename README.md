README
======
`pyfcf` is a package to create standardized, publication quality matplotlib figures. It is partcularly useful for creating figures where the axis are a specfic size, allowing standardization between figures in e.g., papers, charts, or posters.

# Installation

Requirements:

- maptlotlib

To install:

```
  pip install pyfcf
```

# Examples

Initialize basic `matplotlib` settings:

```
pyfcf.setup_matplotlib()
```

See `examples/` folder.

# Development

## Tests

```
python -m unittest discover -s tests
```

## Build

You need additional package `build` `wheel` and `twine`. Make sure that everything is up to date and then

```
  pip install --upgrade build wheel twine
  python3 -m build
  python3 -m twine upload --repository testpypi dist/*
```


