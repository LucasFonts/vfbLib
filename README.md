# vfbLib

Converter and deserializer for FontLab Studio 5 VFB files.

FontLab’s own `vfb2ufo` converter is from 2015, only outputs UFO v2, and
contains serious bugs that are never going to be fixed. Its support on macOS is
subject to Apple’s mercy (no native support for Apple Silicon).

That’s why a single determined programmer with a hex editor set out to rectify
this situation.


## Installation

### Development Installation

To install from source in editable mode:

```bash
git clone git@github.com:LucasFonts/vfbLib.git
cd vfbLib
pip install -e .
```

### End-User Installation

`vfbLib` is on the Python Package Index. Install via pip:

```bash
pip install vfblib
```


## Usage

See the [description](DESCRIPTION.md) of the command line scripts.


## Copyright

© 2022-2024 by [LucasFonts GmbH](https://www.lucasfonts.com/), Berlin
