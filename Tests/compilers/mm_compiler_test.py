from unittest import TestCase

from vfbLib.compilers.mm import (
    AnisotropicInterpolationsCompiler,
    AxisMappingsCompiler,
    AxisMappingsCountCompiler,
    MasterLocationCompiler,
    PrimaryInstancesCompiler,
)

ani_bin = "8d8b8bfa7cfa7c"
ani_raw = [[[0, 0], [1000, 1000]]]

axis_mappings_count_bin = "08000000000000000000000000000000"
axis_mappings_count_raw = [8, 0, 0, 0]

axis_mappings_bin = (
    "0000000000006940"
    "0000000000000000"
    "0000000000c07240"
    "83c0caa145b6b33f"
    "0000000000007940"
    "6f1283c0caa1c53f"
    "0000000000407f40"
    "3d0ad7a3703dd23f"
    "0000000000c08240"
    "8fc2f5285c8fda3f"
    "0000000000e08540"
    "105839b4c876e23f"
    "0000000000008940"
    "cff753e3a59be83f"
    "0000000000208c40"
    "000000000000f03f"
    "0000000000208c40"
    "000000000000f03f"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
    "0000000000000000"
)
axis_mappings_raw = [
    [200.0, 0.0],
    [300.0, 0.077],
    [400.0, 0.169],
    [500.0, 0.285],
    [600.0, 0.415],
    [700.0, 0.577],
    [800.0, 0.769],
    [900.0, 1.0],
    [900.0, 1.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
    [0.0, 0.0],
]


master_location_bin = (
    "02000000000000000000f03f000000000000000000000000000000000000000000000000"
)
master_location_raw = [2, [1.0, 0.0, 0.0, 0.0]]

primary_instances_raw = [
    {"name": "Plain 500 wt", "values": [500.0, 0.0, 0.0, 0.0]},
    {"name": "ExtraLight 200 wt", "values": [200.0, 0.0, 0.0, 0.0]},
    {"name": "Light 300 wt", "values": [300.0, 0.0, 0.0, 0.0]},
    {"name": "SemiLight 400 wt", "values": [400.0, 0.0, 0.0, 0.0]},
    {"name": "SemiBold 600 wt", "values": [600.0, 0.0, 0.0, 0.0]},
    {"name": "Bold 700 wt", "values": [700.0, 0.0, 0.0, 0.0]},
    {"name": "ExtraBold 800 wt", "values": [800.0, 0.0, 0.0, 0.0]},
    {"name": "Black 900 wt", "values": [900.0, 0.0, 0.0, 0.0]},
    {"name": "Office 469 wt", "values": [469.0, 0.0, 0.0, 0.0]},
    {"name": "Office 737 wt", "values": [737.0, 0.0, 0.0, 0.0]},
]

primary_instances_bin = (
    "95"  # 10 = Number of locations
    "97"  # 12 = name length
    "506c61696e20353030207774"  # name
    "ff004c4b40"  # location on axis 1
    "8b"  # location on axis 2
    "8b"  # location on axis 3
    "8b"  # location on axis 4
    "9c45787472614c6967687420323030207774ff001e84808b8b8b974c6967687420333030207774ff002dc6c08b8b8b9b53656d694c6967687420343030207774ff003d09008b8b8b9a53656d69426f6c6420363030207774ff005b8d808b8b8b96426f6c6420373030207774ff006acfc08b8b8b9b4578747261426f6c6420383030207774ff007a12008b8b8b97426c61636b20393030207774ff008954408b8b8b984f666669636520343639207774ff004790508b8b8b984f666669636520373337207774ff007075108b8b8b"
)


class AnisotropicInterpolationsCompilerTest(TestCase):
    def test(self) -> None:
        result = AnisotropicInterpolationsCompiler().compile_hex(ani_raw)
        assert result == ani_bin


class AxisMappingsCountCompilerTest(TestCase):
    def test(self) -> None:
        result = AxisMappingsCountCompiler().compile_hex(axis_mappings_count_raw)
        assert result == axis_mappings_count_bin


class AxisMappingsCompilerTest(TestCase):
    def test(self) -> None:
        result = AxisMappingsCompiler().compile_hex(axis_mappings_raw)
        assert result == axis_mappings_bin


class MasterLocationCompilerTest(TestCase):
    def test(self) -> None:
        result = MasterLocationCompiler().compile_hex(master_location_raw)
        assert result == master_location_bin


class PrimaryInstancesCompilerTest(TestCase):
    def test(self) -> None:
        result = PrimaryInstancesCompiler().compile_hex(primary_instances_raw)
        assert result == primary_instances_bin
