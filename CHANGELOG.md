# Change Log

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
