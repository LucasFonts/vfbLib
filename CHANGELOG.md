# Change Log

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
