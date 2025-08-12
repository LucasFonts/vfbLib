# Change Log

## 0.10.4

Breaking changes

- Change `EncodedValueListWithCount` format from `{"values: []}` to `list[int]`

Command line changes:

- Add `vfb3ufo` option `--json/-j` to save UFOs as "JSON-UFO" as written by ufoLib2. `-jz` combined option writes JSON without line breaks and indentation.


## 0.10.3

Breaking changes

- Some internal dict keys are ints now, but they are still written as str when dumping to JSON.

Compiler changes

- Allow un-decompiled `VfbEntry`s to be written back to VFB. They are identified by `VfbEntry.data` being an instance of `bytes`.


## 0.10.2

Breaking changes

- Fix `num_contours` check when compiling imported binary glyph data (follows OT spec; num_contours == -1 means composite glyph)
- Fix `GuidesCompiler` and guides parser
- Fix name of `F.PostScriptHintingOptions` (was `F.PostScript`)
- Change guides format
- Use IntEnum for VFB entry keys in all places
- Use `match...case` in some places
- Remove caching of original data from `VfbEntry`
- Deprecate `VfbEntry.decompiled`, use `VfbEntry.data` which now holds the binary or structured data depending on de-/compilation state
- Rework `ttinfo.head_creation`


## 0.10.1

UFO changes:

- Add `vfb3ufo` option `-n` to not normalize the UFO(s), which is much faster

Compiler changes:

- Fix `MaskMetricsMMCompiler`
- Fix `PrimaryInstanceLocationsCompiler`
- Support entry 1295 (Global Mask)
- Support entry 1410 (FL3 info)
- Support entry 2007 (image)
- Support entry 2013 (Glyph Bitmaps)
- Support entry 2019 (Glyph Sketch)
- Support compiling imported binary data in glyphs

Parser changes:

- Move `GaspParser` from `base` to `truetype`

Breaking changes:

- Change bitmap format


## 0.10.0

Compiler changes:

- Support entry 1093 (PostScript Hinting Options)
- Support entry 1136 (PCLT Table)
- Support entry 1138 (fontnames)
- Support entry 1141 (Custom CMAPs)
- Support entry 1250 (unicodes)
- Support entry 1253 (Glyph Unicode Non-BMP)
- Support entry 1254 (Primary Instances)
- Support entry 1264 (ttinfo)
- Support entry 1265 (gasp)
- Support entry 1266 (TrueType Stem PPEMs 2 And 3)
- Support entry 1268 (TrueType Stem PPEMs)
- Support entry 1269 (TrueType Stems)
- Support entry 1271 (vdmx)
- Support entry 1294 (Global Guides)
- Support entry 1296 (Global Guide Properties)
- Support entry 1505 (Master Location)
- Support entry 1515 (Axis Mappings Count)
- Support entry 1516 (Axis Mappings)
- Support entry 1523 (Anisotropic Interpolation Mappings)
- Support entry 1524 (TrueType Stem PPEMs 1)
- Support entry 1536 (PostScript Info)
- Support entry 1742 (Mapping Mode)
- Support entry 1743 (OpenType Export Options)
- Support entry 1744 (Export Options)
- Support entry 2008 (Links)
- Support entry 2009 (mask)
- Support entry 2010 (Glyph Hinting Options)
- Support entry 2011 (mask.metrics)
- Support entry 2018 (Glyph GDEF Data)
- Support entry 2020 (Glyph Anchors Supplemental)
- Support entry 2023 (unknown)
- Support entry 2024 (OpenType Metrics Class Flags)
- Support entry 2026 (OpenType Kerning Class Flags)
- Support entry 2027 (Glyph Origin)
- Support entry 2028 (mask.metrics_mm)
- Support entry 2029 (Glyph Anchors MM)
- Support entry 2031 (Glyph Guide Properties)
- Compile "marker" entries (271, 513, 527) with HexStringCompiler
- Compile 1121 (vendor) padded to 4 characters
- Add option to pad a written string with null bytes
- Support writing unsigned encoded values
- Don't write empty glyph fields

Parser changes:

- Add `read_str_with_len` method
- Don't strip spaces from strings

Breaking changes:

- Rename entries `"Binary cvt Table"` to `cvt`, `Binary prep Table` to `prep`, `Binary fpgm Table` to `fpgm` to match FLS5 Python API
- Change decompiled format of `Custom CMAPs` from `dict` to `list`
- Fix guide properties parsing (separate lists for h/v directions)


## 0.9.6

Compiler changes:

- Support entry 1255 (TrueType Zones)
- Support entry 1273 (TrueType Zone Deltas)

## 0.9.5

Parser changes:

- Add entry 1093 (global PostScript Hinting Options)
- Add entry 2010 (Glyph Hinting Options)

UFO:

- Store `postscriptDefaultWidthX` and `postscriptNominalWidthX`
- Warn about duplicate hint sets per point

Other:

- Store "links" in `VfbGlyph`
- Store global/glyph PS hinting options when decompiling glyphs
- Use separate `HintSet` and `UfoHintSet` types
- Add methods to handle hints and hint sets, links to hints to `VfbGlyph`
- Improve `VfbGlyph.draw()` (don't go through UFO conversion)


## 0.9.4

Parser changes:

- Add entry 1266 (TrueType Stem PPMs 2 and 3)
- Add entry 1295 (Global Mask)
- Add entry 2011, 2028 (Mask Metrics)

UFO:

- Export FL mask layer as background layer in UFO
- Add verbose output option (`-v/--verbose`) to vfb3ufo
- Fix export of head flags
- Improve logging, throw an error if no UFO could be extracted
- Synthesize master names if they are not present in the VFB


## 0.9.3

Parser changes:

- Add new entry `pcl_chars_set` (1059)
- Add entry 2034, String
- Remove unused read_float
- Handle read_double right in StreamReader
- Rename and use size constants (6502088)
- Use our own hexStr/deHexStr

Compiler changes:

- Implement writing double-precision floats
- Support compiling entries without data
- Add HexStringCompiler for fallbacks
- Add more numeric compilers
- Add compiler for UnicodeRanges
- Improve hash update error
- Handle json export in a separate file
- Write kerning gid as int (comes in as str from json)
- Use HexStringCompiler for binary tables
- Remove write_float(s) from compiler
- Use our own hexStr/deHexStr


## 0.9.2

- Update dependencies
- Fix duplicate UFO info key mapping for `styleMapFamilyName`
- Fix deprecated entry in `pyproject.toml`
- Remove debug logging for glyph names
- Improve error message for entries with no compiler
- VfbEntry: Improve init and id setter logic
- Better message if an entry could not be decompiled

Breaking changes:

- Rename entries `x_u_id` to `xuid`, `x_u_id_num` to `xuid_num` to match FLS5 Python API


## 0.9.1

- Fix error in `vfbcu2qu` introduced in the previous release.

## v0.9.0

Parser changes:

- Change the internal `VfbHeader` format

Compiler changes:

- Support the new internal `VfbHeader` format

Breaking changes:

- Modify many `VfbEntry` names to better match the FLS5 Python API attribute names

## v0.8.3

- HTML-escape XML attributes in glyph program
- Use `orjson` for faster JSON export
- Move to modern Python packaging (`pyproject.toml`)

## v0.8.2

- Fix hintmask conversion in UFO builder (broken since v0.8.0)

## v0.8.1

- Add vfb2tth command for TrueType hinting export
- Don't read VFB if no path has been passed
- Add Python 3.13 support
- Drop Python 3.9 support
- Update dependencies
- Remove deprecated/obsolete setup options

Parser changes:

- Add "Glyph Sketch" entry
- Add a few IDs found in FL3
- Improve PCLT table parsing
- Add specialised parsers for various int types
- Improve error message when parser did not consume all bytes
- Support header compilation
- Decode mapping mode
- Fix: Kerning and metrics class flags are stored slightly differently
- Store header reserved field as hexStr
- Change name of IntParser to Int16Parser, add compiler
- Add Binary table parser

Compiler changes:

- Make compiler structure similar to parser structure
- Improve compiler class inheritance
- Differentiate string parsers
- Introduce StringCompiler
- Add GlyphEncodingCompiler
- Fix modification detection
- Init glyph with empty structure
- Implement compiling hint masks
- Compile binary table
- Compile OpenType features

Breaking changes:

- Store OpenType classes as strings
- Store hintmasks as tuples
