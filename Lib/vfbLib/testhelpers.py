from fontTools.misc.textTools import deHexStr
from io import BytesIO


def expect(parser, encoded, decoded):
    data = deHexStr(encoded)
    assert parser().parse(BytesIO(data), len(data)) == decoded
