from unittest import TestCase

from vfbLib.helpers import binaryToIntList, intListToBinary


class HelpersTest(TestCase):
    def test_binaryToIntList0(self):
        assert binaryToIntList(0) == []

    def test_binaryToIntList1(self):
        assert binaryToIntList(1) == [0]

    def test_binaryToIntList2(self):
        assert binaryToIntList(2) == [1]

    def test_binaryToIntList3(self):
        assert binaryToIntList(3) == [0, 1]

    def test_intListToBinary0(self):
        assert intListToBinary([]) == 0

    def test_intListToBinary1(self):
        assert intListToBinary([0]) == 1

    def test_intListToBinary2(self):
        assert intListToBinary([1]) == 2

    def test_intListToBinary3(self):
        assert intListToBinary([0, 1]) == 3
