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
- Supports more UFO font info attributes


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
usage: vfb3ufo [-h] [-p PATH] [-fo] [-g] [-j] [-k] [-ttx] [-64] [-s] [-n] [-nops] [-v] [-z] [-m] [-u] inputpath [outputpath]

vfb3ufo Converter Copyright (c) 2024 by LucasFonts

positional arguments:
  inputpath             input file path (.vfb)
  outputpath            output file path (.ufo[z])

options:
  -h, --help            show this help message and exit
  -p, --path PATH       output folder
  -fo, --force-overwrite
                        force overwrite
  -64, --base64         write GLIF lib 'data' section using base64
  -s, --silent          no display (silent mode)
  -v, --verbose         Print debugging output
  -z, --zip             write UFOZ (compressed UFO)

Additional options not present in vfb2ufo:

  -g, --keep-groups     don't move non-kerning groups from groups.plist to feature code
  -j, --json            serialize UFO as JSON; combine with -z to write JSON without line breaks/indentation
  -k, --add-kerning-groups
                        add kerning groups to feature code
  -m, --minimal         parse only minimal amount of data, drop missing glyphs from groups, etc.
  -n, --no-normalize    don't normalize the UFOs (faster)
  -nops, --no-postscript-hints
                        Don't output PostScript hinting
  -u, --unicode-strings
                        interpret strings as Unicode instead of Windows-1252

Options not implemented here, but present in the original vfb2ufo:

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
usage: vfb2json [-h] [-d] [--header] [-m] [-p PATH] [-r] [-u] inputpath

vfb2json Converter Copyright (c) 2024 by LucasFonts

positional arguments:
  inputpath             input file path (.vfb)

options:
  -h, --help            show this help message and exit
  -d, --no-decompile    don't decompile data, output binary in JSON
  --header              only read the VFB header, not the actual data
  -m, --minimal         parse only minimal amount of data
  -p, --path PATH       output folder
  -r, --roundtrip       roundtrip data by decompiling and compiling again before saving
  -u, --unicode-strings
                        interpret name table strings as Unicode instead of Windows-1252
```


### vfb2tth

Export the TrueType hinting from a VFB in a custom format, either as JSON (default), TOML, or YAML.

```bash
$ vfb2tth MyFile.vfb
```

To make the TOML and YAML output options available, you must install with extras
`vfblib[toml]` or `vfblib[yaml]`, respectively.

```
usage: vfb2tth [-h] [-f FORMAT] [-p PATH] inputpath

vfb2tth Converter Copyright (c) 2024 by LucasFonts

positional arguments:
  inputpath            input file path (.vfb)

options:
  -h, --help           show this help message and exit
  -f, --format FORMAT  The output format: json (default), toml, or yaml
  -p, --path PATH      output folder
```


### vfbcu2qu

Convert a VFB file to quadratic using the `cu2qu` library.

```bash
$ vfbcu2qu MyFile.vfb
```

will convert the file and save it with the suffix `.qu.vfb` in the same directory.

```
vfbcu2qu -h
usage: vfbcu2qu [-h] [-p PATH] [-fo] [-m MAX_ERR_EM] inputpath [outputpath]

VFB Cubic to Quadratic Converter Copyright (c) 2023 by LucasFonts

positional arguments:
  inputpath             input file path (.vfb)
  outputpath            output file path (.vfb)

options:
  -h, --help            show this help message and exit
  -p, --path PATH       output folder
  -fo, --force-overwrite
                        force overwrite
  -m, --max-err-em MAX_ERR_EM
                        Maximum allowed error, relative to the font's units per em. Default is 0.001.
```


### vfbdiff

Generate a diff of two VFB files, either in unified diff or HTML format.

```
vfbdiff -h
usage: vfbdiff [-h] [--html HTML] file1 file2

vfbdiff Copyright (c) 2024 by LucasFonts

positional arguments:
  file1        First input file path (.vfb)
  file2        Second input file path (.vfb)

options:
  -h, --help   show this help message and exit
  --html HTML  Output diff in HTML format to file path
```

## Copyright

© 2022–2025 by [LucasFonts GmbH](https://www.lucasfonts.com/), Berlin
