# Length of data types used by StreamReader and Stream Writer etc.
int8_size = 1
int16_size = 2
int32_size = 4
double_size = 8


def binaryToIntList(value: int, start: int = 0) -> list[int]:
    intList = []
    counter = start
    while value:
        if value & 1:
            intList.append(counter)
        value >>= 1
        counter += 1
    return intList


def deHexStr(hexstr: str) -> bytes:
    return bytes.fromhex(hexstr)


def hexStr(b: bytes) -> str:
    return bytes.hex(b)
