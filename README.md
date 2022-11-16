# vfbLib

Converter and deserializer for VFB files.


## Command Line Scripts

### vfb3ufo

Convert a VFB to one UFO per master. Command line options are compatible to
FontLab’s `vfb2ufo`, but not all of them are implemented yet.

```
vfb3ufo -h
usage: vfb3ufo [-h] [-p PATH] [-fo] [-ttx] [-64] [-s] [-z] [-m] inputpath [outputpath]

VFB3UFO Converter Copyright (c) 2022 by LucasFonts Build 2022-11-08

positional arguments:
  inputpath             input file path (.vfb)
  outputpath            output file path (.ufo[z])

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  output folder
  -fo, --force-overwrite
                        force overwrite

Additional options:

  -m, --minimal         parse only minimal amount of data

Unimplemented options:

  -64, --base64         write GLIF lib 'data' section using base64 (recommended)
  -s, --silent          no display (silent mode)
  -ttx, --ttx           convert binary OpenType Layout data using TTX-like format
  -z, --zip             write UFOZ (compressed UFO)
```


### vfb2json

Generate a representation that closely adheres to the VFB structure.

```bash
$ vfb2json MyFile.vfb
```

will convert the file to `MyFile.json` in the same directory. Existing files will be overwritten.

We expect this to be mostly used for debugging purposes.

```
vfb2json -h
usage: vfb2json [-h] [-m] [-p PATH] inputpath

VFB2JSON Converter Copyright (c) 2022 by LucasFonts Build 2022-11-08

positional arguments:
  inputpath             input file path (.vfb)

options:
  -h, --help            show this help message and exit
  -m, --minimal         parse only minimal amount of data
  -p PATH, --path PATH  output folder
```