# Length of data types used by StreamReader and Stream Writer etc.
uint8 = 1
uint16 = 2
uint32 = 4


def binaryToIntList(value: int, start: int = 0):
    intList = []
    counter = start
    while value:
        if value & 1:
            intList.append(counter)
        value >>= 1
        counter += 1
    return intList
