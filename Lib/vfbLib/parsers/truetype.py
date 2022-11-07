from io import BytesIO
from vfbLib.parsers import BaseParser, read_encoded_value


class TrueTypeStemsParser(BaseParser):
    @classmethod
    def parse(cls, data: bytes):
        stream = BytesIO(data)
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = read_encoded_value(stream)
            for _ in range(num_stems):
                width = read_encoded_value(stream)
                stem_name_length = cls.read_uint8(stream)
                stem_name = stream.read(stem_name_length).decode("cp1252")
                ppm6 = read_encoded_value(stream)

                direction.append(
                    {
                        "value": width,
                        "name": stem_name,
                        "round": {"6": ppm6},
                    }
                )
            result[names[i]] = direction

        return result


class TrueTypeStemPpemsParser(BaseParser):
    @classmethod
    def parse(cls, data: bytes):
        stream = BytesIO(data)
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = read_encoded_value(stream)
            d = {}
            for j in range(num_stems):
                for k in range(2, 6):
                    ppm = read_encoded_value(stream)
                    d[str(k)] = ppm

                direction.append(
                    {
                        "stem": j,
                        "round": d.copy(),
                    }
                )
            result[names[i]] = direction
        return result
