from unittest import TestCase

from vfbLib.tth import (
    extract_tt_stems,
    extract_tt_zones,
)


class TTHExportTest(TestCase):
    def test_extract_tt_stems(self):
        data = {
            "ttStemsV": [
                {"value": 77, "name": "currency_stroke", "round": {"6": 72}},
                {"value": 84, "name": "currency_white", "round": {"6": 66}},
            ],
            "ttStemsH": [
                {"value": 109, "name": "X: 109", "round": {"6": 51}},
                {"value": 91, "name": "X: 91", "round": {"6": 61}},
            ],
        }
        target = {}
        extract_tt_stems(data, target)
        assert target["stems"] == {
            "ttStemsV": [
                {
                    "width": 77,
                    "name": "currency_stroke",
                    "round": {"6": 72},
                    "horizontal": True,
                },
                {
                    "width": 84,
                    "name": "currency_white",
                    "round": {"6": 66},
                    "horizontal": True,
                },
            ],
            "ttStemsH": [
                {
                    "width": 109,
                    "name": "X: 109",
                    "round": {"6": 51},
                    "horizontal": False,
                },
                {
                    "width": 91,
                    "name": "X: 91",
                    "round": {"6": 61},
                    "horizontal": False,
                },
            ],
        }

    def test_extract_tt_stems_duplicate_names(self):
        data = {
            "ttStemsV": [
                {"value": 77, "name": "currency", "round": {"6": 72}},
                {"value": 84, "name": "currency", "round": {"6": 66}},
            ],
            "ttStemsH": [
                {"value": 72, "name": "currency", "round": {"6": 74}},
            ],
        }
        target = {}
        extract_tt_stems(data, target)
        assert target["stems"]["ttStemsV"] == [
            {
                "width": 77,
                "name": "currency",
                "round": {"6": 72},
                "horizontal": True,
            },
            {
                "width": 84,
                "name": "currency#1",
                "round": {"6": 66},
                "horizontal": True,
            },
        ]
        assert target["stems"]["ttStemsH"] == [
            {
                "width": 72,
                "name": "currency#2",
                "round": {"6": 74},
                "horizontal": False,
            },
        ]

    def test_extract_tt_zones(self):
        data = {
            "ttZonesT": [
                {"position": 520, "value": 12, "name": "xheight"},
            ],
            "ttZonesB": [
                {"position": 0, "value": 12, "name": "baseline"},
            ],
        }
        target = {}
        zone_names = {"ttZonesT": {}, "ttZonesB": {}}
        extract_tt_zones(data, target, zone_names)
        assert zone_names["ttZonesT"] == {0: "xheight"}
        assert zone_names["ttZonesB"] == {0: "baseline"}

    def test_extract_tt_zones_duplicate_names(self):
        data = {
            "ttZonesT": [
                {"position": 520, "value": 12, "name": "xheight"},
                {"position": 530, "value": 12, "name": "xheight"},
            ],
            "ttZonesB": [
                {"position": 0, "value": 12, "name": "xheight"},
            ],
        }
        target = {}
        zone_names = {"ttZonesT": {}, "ttZonesB": {}}
        extract_tt_zones(data, target, zone_names)
        assert zone_names["ttZonesT"] == {0: "xheight", 1: "xheight#1"}
        assert zone_names["ttZonesB"] == {0: "xheight#2"}
