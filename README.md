# vfbLib

Converter and deserializer for FontLab Studio 5 VFB files.

FontLab’s own `vfb2ufo` converter is from 2015, only outputs UFO v2, and
contains serious bugs that are never going to be fixed. Its support on macOS is
subject to Apple’s mercy (no native support for Apple Silicon).

That’s why in 2022 a single determined programmer, me, Jens Kutílek, armed with nothing
but a hex editor set out to rectify this situation. In late 2025, Yuri Yarmola let me
have a look at the original VFB code from FontLab. I am very grateful for his kindness.
Without Yuri’s help, I would probably never have figured out some parts of the format.

The VFB file format is described in the
[vfbLib-rust](https://github.com/jenskutilek/vfbLib-rust/blob/main/FILEFORMAT.md) repo,
a work-in-progress implementation of vfbLib in rust.

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

© 2022-2026 by [LucasFonts GmbH](https://www.lucasfonts.com/), Berlin
