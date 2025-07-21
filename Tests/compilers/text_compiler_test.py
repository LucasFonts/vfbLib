from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.compilers.text import NameRecordsCompiler, StringCompiler
from vfbLib.parsers.text import StringParser

decompiled_ibm_serif_text = [
    [0, 1, 0, 0, "Copyright 2020 IBM Corp. All rights reserved."],
    [0, 3, 1, 1033, "Copyright 2020 IBM Corp. All rights reserved."],
    [1, 1, 0, 0, "IBM Plex Serif Text"],
    [1, 3, 1, 1033, "IBM Plex Serif Text"],
    [2, 1, 0, 0, "Regular"],
    [2, 3, 1, 1033, "Regular"],
    [3, 1, 0, 0, "IBM;IBMPlexSerif-Text;2.006;2020"],
    [3, 3, 1, 1033, "IBM;IBMPlexSerif-Text;2.006;2020"],
    [4, 1, 0, 0, "IBM Plex Serif Text"],
    [4, 3, 1, 1033, "IBM Plex Serif Text"],
    [5, 1, 0, 0, "Version 2.006 2020"],
    [5, 3, 1, 1033, "Version 2.006 2020"],
    [6, 1, 0, 0, "IBMPlexSerif-Text"],
    [6, 3, 1, 1033, "IBMPlexSerif-Text"],
    [
        7,
        1,
        0,
        0,
        "IBM Plex® is a trademark of IBM Corp, registered in many jurisdictions worldwide.",
    ],
    [
        7,
        3,
        1,
        1033,
        "IBM Plex® is a trademark of IBM Corp, registered in many jurisdictions worldwide.",
    ],
    [8, 1, 0, 0, "Bold Monday"],
    [8, 3, 1, 1033, "Bold Monday"],
    [9, 1, 0, 0, "Mike Abbink, Paul van der Laan, Pieter van Rosmalen"],
    [9, 3, 1, 1033, "Mike Abbink, Paul van der Laan, Pieter van Rosmalen"],
    [11, 1, 0, 0, "http://www.boldmonday.com"],
    [11, 3, 1, 1033, "http://www.boldmonday.com"],
    [12, 1, 0, 0, "http://www.ibm.com"],
    [12, 3, 1, 1033, "http://www.ibm.com"],
    [
        13,
        1,
        0,
        0,
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL",
    ],
    [
        13,
        3,
        1,
        1033,
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL",
    ],
    [14, 1, 0, 0, "http://scripts.sil.org/OFL"],
    [14, 3, 1, 1033, "http://scripts.sil.org/OFL"],
    [16, 1, 0, 0, "IBM Plex Serif"],
    [16, 3, 1, 1033, "IBM Plex Serif"],
    [17, 1, 0, 0, "Text"],
    [17, 3, 1, 1033, "Text"],
    [19, 1, 0, 0, "How razorback-jumping frogs can level six piqued gymnasts!"],
    [19, 3, 1, 1033, "How razorback-jumping frogs can level six piqued gymnasts!"],
]
expected_ibm_serif_text = (
    "ad"  # 34
    # 0
    "8b8c8b8bb8cef703f704f70df706f4f2f3f708abbdbbbdbbabd4cdd8abcef703f706f704b9abccf700f700abf706f4f2f3f708f707abf706f0f707f0f706f70af0efb9"
    "8b8e8cfa9db8cef703f704f70df706f4f2f3f708abbdbbbdbbabd4cdd8abcef703f706f704b9abccf700f700abf706f4f2f3f708f707abf706f0f707f0f706f70af0efb9"
    # 1
    "8c8c8b8b9ed4cdd8abdbf700f0f70cabdef0f706f4f1abdff0f70cf708"
    "8c8e8cfa9d9ed4cdd8abdbf700f0f70cabdef0f706f4f1abdff0f70cf708"
    # 2
    "8d8c8b8b92ddf0f2f709f700ecf706"
    "8d8e8cfa9d92ddf0f2f709f700ecf706"
    # 3
    "8e8c8b8babd4cdd8c6d4cdd8dbf700f0f70cdef0f706f4f1b8dff0f70cf708c6bdb9bbbbc1c6bdbbbdbb"
    "8e8e8cfa9dabd4cdd8c6d4cdd8dbf700f0f70cdef0f706f4f1b8dff0f70cf708c6bdb9bbbbc1c6bdbbbdbb"
    # 4
    "8f8c8b8b9ed4cdd8abdbf700f0f70cabdef0f706f4f1abdff0f70cf708"
    "8f8e8cfa9d9ed4cdd8abdbf700f0f70cabdef0f706f4f1abdff0f70cf708"
    # 5
    "908c8b8b9de1f0f706f707f4f703f702abbdb9bbbbc1abbdbbbdbb"
    "908e8cfa9d9de1f0f706f707f4f703f702abbdb9bbbbc1abbdbbbdbb"
    # 6
    "918c8b8b9cd4cdd8dbf700f0f70cdef0f706f4f1b8dff0f70cf708"
    "918e8cfa9d9cd4cdd8dbf700f0f70cdef0f706f4f1b8dff0f70cf708"
    # 7
    "928c8b8bdcd4cdd8abdbf700f0f70cf73cabf4f707abecabf708f706eceff0f701ecf706f6abf703f1abd4cdd8abcef703f706f704b7abf706f0f2f4f707f708f0f706f0efabf4f702abf701ecf702f70dabf5f709f706f4f707eff4eef708f4f703f702f707abf70bf703f706f700eff70bf4eff0b9"
    "928e8cfa9ddcd4cdd8abdbf700f0f70cf742abf4f707abecabf708f706eceff0f701ecf706f6abf703f1abd4cdd8abcef703f706f704b7abf706f0f2f4f707f708f0f706f0efabf4f702abf701ecf702f70dabf5f709f706f4f707eff4eef708f4f703f702f707abf70bf703f706f700eff70bf4eff0b9"
    # 8
    "938c8b8b96cdf703f700efabd8f703f702efecf70d"
    "938e8cfa9d96cdf703f700efabd8f703f702efecf70d"
    # 9
    "948c8b8bbed8f4f6f0abccededf4f702f6b7abdbecf709f700abf70aecf702abeff0f706abd7ececf702b7abdbf4f0f708f0f706abf70aecf702abddf703f707f701ecf700f0f702"
    "948e8cfa9dbed8f4f6f0abccededf4f702f6b7abdbecf709f700abf70aecf702abeff0f706abd7ececf702b7abdbf4f0f708f0f706abf70aecf702abddf703f707f701ecf700f0f702"
    # 11
    "968c8b8ba4f3f708f708f704c5babaf70bf70bf70bb9edf703f700eff701f703f702efecf70db9eef703f701"
    "968e8cfa9da4f3f708f708f704c5babaf70bf70bf70bb9edf703f700eff701f703f702efecf70db9eef703f701"
    # 12
    "978c8b8b9df3f708f708f704c5babaf70bf70bf70bb9f4edf701b9eef703f701"
    "978e8cfa9d9df3f708f708f704c5babaf70bf70bf70bb9f4edf701b9eef703f701"
    # 13
    "988c8b8bf724dff3f4f707abd1f703f702f708abdef703f1f708f70becf706f0abf4f707abf700f4eef0f702f707f0efabf709f702eff0f706abf708f3f0abded4d7abdaf704f0f702abd1f703f702f708abd7f4eef0f702f707f0b7abe1f0f706f707f4f703f702abbcb9bcb9abdff3f4f707abf700f4eef0f702f707f0abf4f707abecf70aecf4f700ecedf700f0abf70bf4f708f3abecabd1ccdcabecf708c5abf3f708f708f704c5babaf707eef706f4f704f708f707b9f707f4f700b9f703f706f2badad1d7"
    "988e8cfa9df724dff3f4f707abd1f703f702f708abdef703f1f708f70becf706f0abf4f707abf700f4eef0f702f707f0efabf709f702eff0f706abf708f3f0abded4d7abdaf704f0f702abd1f703f702f708abd7f4eef0f702f707f0b7abe1f0f706f707f4f703f702abbcb9bcb9abdff3f4f707abf700f4eef0f702f707f0abf4f707abecf70aecf4f700ecedf700f0abf70bf4f708f3abecabd1ccdcabecf708c5abf3f708f708f704c5babaf707eef706f4f704f708f707b9f707f4f700b9f703f706f2badad1d7"
    # 14
    "998c8b8ba5f3f708f708f704c5babaf707eef706f4f704f708f707b9f707f4f700b9f703f706f2badad1d7"
    "998e8cfa9da5f3f708f708f704c5babaf707eef706f4f704f708f707b9f707f4f700b9f703f706f2badad1d7"
    # 16
    "9b8c8b8b99d4cdd8abdbf700f0f70cabdef0f706f4f1"
    "9b8e8cfa9d99d4cdd8abdbf700f0f70cabdef0f706f4f1"
    # 17
    "9c8c8b8b8fdff0f70cf708"
    "9c8e8cfa9d8fdff0f70cf708"
    # 19
    "9e8c8b8bc5d3f703f70babf706ecf70ef703f706edeceef6b8f5f709f701f704f4f702f2abf1f706f703f2f707abeeecf702abf700f0f70af0f700abf707f4f70cabf704f4f705f709f0efabf2f70df701f702ecf707f708f707ac"
    "9e8e8cfa9dc5d3f703f70babf706ecf70ef703f706edeceef6b8f5f709f701f704f4f702f2abf1f706f703f2f707abeeecf702abf700f0f70af0f700abf707f4f70cabf704f4f705f709f0efabf2f70df701f702ecf707f708f707ac"
)

raw_short = [
    [
        7,
        1,
        0,
        0,
        "IBM Plex® is a trademark of IBM Corp, registered in many jurisdictions worldwide.",
    ],
    [
        7,
        3,
        1,
        1033,
        "IBM Plex® is a trademark of IBM Corp, registered in many jurisdictions worldwide.",
    ],
]

expected_short = (
    "8d"  # 2
    # 7
    "928c8b8bdcd4cdd8abdbf700f0f70cf73cabf4f707abecabf708f706eceff0f701ecf706f6abf703f1abd4cdd8abcef703f706f704b7abf706f0f2f4f707f708f0f706f0efabf4f702abf701ecf702f70dabf5f709f706f4f707eff4eef708f4f703f702f707abf70bf703f706f700eff70bf4eff0b9"
    "928e8cfa9ddcd4cdd8abdbf700f0f70cf742abf4f707abecabf708f706eceff0f701ecf706f6abf703f1abd4cdd8abcef703f706f704b7abf706f0f2f4f707f708f0f706f0efabf4f702abf701ecf702f70dabf5f709f706f4f707eff4eef708f4f703f702f707abf70bf703f706f700eff70bf4eff0b9"
)


class NameRecordsCompilerTest(TestCase):
    def test_empty(self) -> None:
        result = NameRecordsCompiler().compile_hex([])
        assert result == "8b"

    def test_mac(self) -> None:
        result = NameRecordsCompiler().compile_hex([[0, 1, 0, 0, "Hällo"]])
        assert result == hexStr(deHexStr("8c 8b 8c 8b 8b 90 d3 f71e f700 f700 f703"))

    def test_unicode(self) -> None:
        result = NameRecordsCompiler().compile_hex([[0, 3, 1, 1033, "Hällo"]])
        assert result == hexStr(deHexStr("8c 8b 8e 8c fa9d 90 d3 f778 f700 f700 f703"))

    def test_ibm_serif_text(self) -> None:
        result = NameRecordsCompiler().compile_hex(decompiled_ibm_serif_text)
        assert result == expected_ibm_serif_text

    def test_mac_utf_encodings(self) -> None:
        result = NameRecordsCompiler().compile_hex(raw_short)
        assert result == expected_short


expected_regular = hexStr(deHexStr("52 65 67 75 6C 61 72"))
expected_space = hexStr(deHexStr("57 74 30 20 57 64 31 20"))


class StringCompilerTest(TestCase):
    def test_regular(self):
        result = StringCompiler().compile_hex("Regular")
        assert result == expected_regular

    def test_space(self):
        result = StringCompiler().compile_hex("Wt0 Wd1 ")  # Trailing space is compiled
        assert result == expected_space

    def test_space_roundtrip(self):
        dec = StringParser().parse_hex(expected_space)
        assert dec == "Wt0 Wd1 "  # Trailing space does not get stripped
        cde = StringCompiler().compile_hex(dec)
        assert cde == expected_space
