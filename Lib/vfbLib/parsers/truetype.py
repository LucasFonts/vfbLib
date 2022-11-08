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

        assert stream.read() == b""
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

        assert stream.read() == b""
        return result


class TrueTypeZoneDeltasParser(BaseParser):
    @classmethod
    def parse(cls, data: bytes):
        stream = BytesIO(data)
        num_deltas = read_encoded_value(stream)
        # print(num_deltas, "Zone deltas follow")
        result = {}
        for _ in range(num_deltas):
            # Index into Bottom + Top Zones
            index = read_encoded_value(stream)
            ppm = read_encoded_value(stream)
            shift = read_encoded_value(stream)
            if index in result:
                result[index][ppm] = shift
            else:
                result[index] = {ppm: shift}

        assert stream.read() == b""
        return result


class TrueTypeZonesParser(BaseParser):
    @classmethod
    def parse(cls, data: bytes):
        stream = BytesIO(data)
        names = ("ttZonesT", "ttZonesB")
        result = {}
        for i in range(2):
            side = []
            num_zones = read_encoded_value(stream)
            # print(num_zones)
            for _ in range(num_zones):
                position = read_encoded_value(stream)
                width = read_encoded_value(stream)
                # print(position, width)
                name_length = read_encoded_value(stream)
                # print("Name of length", name_length, "follows")
                zone_name = stream.read(name_length).decode("cp1252")
                side.append({
                    "position": position,
                    "value": width,
                    "name": zone_name,
                })
            result[names[i]] = side

        assert stream.read() == b""
        return result
