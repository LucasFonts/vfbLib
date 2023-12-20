# vfbLib

Converter and deserializer for FontLab Studio 5 VFB files.

FontLab’s own `vfb2ufo` converter is from 2015, only outputs UFO v2, and
contains serious bugs that are never going to be fixed. Its support on macOS is
subject to Apple’s mercy (no native support for Apple Silicon).

That’s why a single determined programmer with a hex editor set out to rectify
this situation.


## Improvements Over vfb2ufo

- Outputs normalized UFO v3
- Outputs FontLab user data (font and glyph level)
- Mark colors are written to the official UFO v3 lib key
- Guideline data is written to the official UFO v3 elements
- Anchors are preserved in composite glyphs
- PostScript hinting is written correctly, but to the Adobe lib key
- TrueType hinting is supported in composite glyphs
- Supports more UFO font info attributes:
  - `openTypeGaspRangeRecords`
  - `openTypeHeadLowestRecPPEM`
  - `openTypeNameRecords`
  - `openTypeOS2WeightClass` is written correctly


## Command Line Script Usage

### vfb3ufo

Convert a VFB to one UFO per master. Command line options are compatible to
FontLab’s `vfb2ufo`, but not all of them are implemented yet.

```bash
$ vfb3ufo MyFile.vfb
```

will convert the file to `MyFile.ufo` in the same directory. Existing files will
not be overwritten unless you specify the `-fo` option.

```
vfb3ufo -h
usage: vfb3ufo [-h] [-p PATH] [-fo] [-ttx] [-64] [-s] [-nops] [-z] [-m] [-u] inputpath [outputpath]

VFB3UFO Converter Copyright (c) 2023 by LucasFonts Build 2023-07-19

positional arguments:
  inputpath             input file path (.vfb)
  outputpath            output file path (.ufo[z])

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  output folder
  -fo, --force-overwrite
                        force overwrite
  -64, --base64         write GLIF lib 'data' section using base64 (recommended)
  -s, --silent          no display (silent mode)
  -nops, --no-postscript-hints
                        Don't output PostScript hinting
  -z, --zip             write UFOZ (compressed UFO)
  -m, --minimal         parse only minimal amount of data, drop missing glyphs from groups, etc.
  -u, --unicode-strings
                        interpret name table strings as Unicode instead of Windows-1252

Not yet implemented options:

  -ttx, --ttx           convert binary OpenType Layout data using TTX-like format
```


### vfb2json

Generate a representation that closely adheres to the VFB structure.

```bash
$ vfb2json MyFile.vfb
```

will convert the file to `MyFile.vfb.json` in the same directory. Existing files will be overwritten.

We expect this to be mostly used for debugging purposes.

```
vfb2json -h
usage: vfb2json [-h] [-d] [--header] [-m] [-p PATH] inputpath

VFB2JSON Converter Copyright (c) 2023 by LucasFonts Build 2023-07-18

positional arguments:
  inputpath             input file path (.vfb)

options:
  -h, --help            show this help message and exit
  -d, --no-decompile    don't decompile data, output binary in JSON
  --header              only read the VFB header, not the actual data
  -m, --minimal         parse only minimal amount of data
  -p PATH, --path PATH  output folder
```


### vfbcu2qu

Convert a VFB file to quadratic using the `cu2qu` library.

```bash
$ vfbcu2qu MyFile.vfb
```

will convert the file and save it with the suffix `.qu.vfb` in the same directory.

```
usage: vfbcu2qu [-h] [-p PATH] [-fo] [-m MAX_ERR_EM] inputpath [outputpath]

VFB Cubic to Quadratic Converter Copyright (c) 2023 by LucasFonts Build 2023-07-18

positional arguments:
  inputpath             input file path (.vfb)
  outputpath            output file path (.vfb)

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  output folder
  -fo, --force-overwrite
                        force overwrite
  -m MAX_ERR_EM, --max-err-em MAX_ERR_EM
                        Maximum allowed error, relative to the font's units per em. Default is 0.001.
```


### diffvfb

Generate a diff of two VFB files, either in unified diff or HTML format.

```
usage: diffvfb [-h] [--html HTML] file1 file2

diffvfb Copyright (c) 2023 by LucasFonts Build 2023-07-18

positional arguments:
  file1        First input file path (.vfb)
  file2        Second input file path (.vfb)

options:
  -h, --help   show this help message and exit
  --html HTML  Output diff in HTML format to file path
```

## Copyright

© 2022–2023 by [LucasFonts GmbH](https://www.lucasfonts.com/), Berlin
