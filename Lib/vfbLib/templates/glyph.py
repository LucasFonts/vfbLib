from vfbLib import GLYPH_CONSTANT


def get_empty_glyph(num_masters: int):
    return {
        "constants": GLYPH_CONSTANT,
        "metrics": [(0, 0) for _ in range(num_masters)],
        "name": "",
        "nodes": [],
        "num_masters": num_masters,
        "num_node_values": 0,
    }
