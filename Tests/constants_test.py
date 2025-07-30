from unittest import TestCase

from vfbLib.constants import parser_classes


class ConstantsTest(TestCase):
    def test_uniqueness(self):
        # Make sure the human-readable keys are unique
        all_classes = [key for key, _, _ in parser_classes.values()]
        assert len(set(all_classes)) == len(all_classes), (
            f"Duplicate keys in classes: {sorted(all_classes)}"
        )
