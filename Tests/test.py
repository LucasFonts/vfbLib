from pprint import pprint

from fontTools.misc.textTools import deHexStr

from vfbLib.parsers.truetype import TrueTypeZoneDeltasParser

data = deHexStr("958fa9838fa7838e9a838ea5838da7938da8838daa938eab838dae838eb883")

result = TrueTypeZoneDeltasParser.parse(data)

pprint(result)

print(
    "\u0043\\u006f\\u0070\\u0079\\u0072\\u0069\\u0067\\u0068\\u0074\\u0020\\u0032\\u0030\\u0031\\u0038\\u0020\\u0049\\u0042\\u004d\\u0020\\u0043\\u006f\\u0072\\u0070\\u002e\\u0020\\u0041\\u006c\\u006c\\u0020\\u0072\\u0069\\u0067\\u0068\\u0074\\u0073\\u0020\\u0072\\u0065\\u0073\\u0065\\u0072\\u0076\\u0065\\u0064\\u002e"
)
