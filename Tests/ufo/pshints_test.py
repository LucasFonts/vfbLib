from unittest import TestCase

from vfbLib.ufo.pshints import update_adobe_hinting

ps_hints_empty = """  <hintSetList>
  </hintSetList>"""

ps_hints = """  <hintSetList>
    <hintset pointTag="at01">
      <hstem pos="0" width="50" />
      <hstem pos="358" width="54" />
      <hstem pos="648" width="50" />
      <vstem pos="8" width="123" />
      <vstem pos="227" width="64" />
      <vstem pos="460" width="101" />
      <vstem pos="803" width="106" />
    </hintset>
    <hintset pointTag="sv03">
      <hstem pos="-12" width="51" />
      <hstem pos="-12" width="51" />
      <hstem pos="0" width="50" />
      <hstem pos="358" width="54" />
      <hstem pos="358" width="54" />
      <hstem pos="358" width="54" />
      <hstem pos="648" width="50" />
      <hstem pos="648" width="50" />
      <hstem pos="648" width="50" />
      <vstem pos="8" width="123" />
      <vstem pos="8" width="123" />
      <vstem pos="8" width="123" />
      <vstem pos="227" width="64" />
      <vstem pos="227" width="64" />
      <vstem pos="227" width="64" />
      <vstem pos="460" width="101" />
      <vstem pos="460" width="101" />
      <vstem pos="460" width="101" />
      <vstem pos="803" width="106" />
      <vstem pos="803" width="106" />
      <vstem pos="803" width="106" />
    </hintset>
  </hintSetList>"""

expected_2_hintsets = {
    "hintSetList": [
        {
            "pointTag": "at01",
            "stems": [
                "hstem 0 50",
                "hstem 358 54",
                "hstem 648 50",
                "vstem 8 123",
                "vstem 227 64",
                "vstem 460 101",
                "vstem 803 106",
            ],
        },
        {
            "pointTag": "sv03",
            "stems": [
                "hstem -12 51",
                "hstem -12 51",
                "hstem 0 50",
                "hstem 358 54",
                "hstem 358 54",
                "hstem 358 54",
                "hstem 648 50",
                "hstem 648 50",
                "hstem 648 50",
                "vstem 8 123",
                "vstem 8 123",
                "vstem 8 123",
                "vstem 227 64",
                "vstem 227 64",
                "vstem 227 64",
                "vstem 460 101",
                "vstem 460 101",
                "vstem 460 101",
                "vstem 803 106",
                "vstem 803 106",
                "vstem 803 106",
            ],
        },
    ]
}


class PshintsTest(TestCase):
    def test_empty(self):
        r = update_adobe_hinting(ps_hints_empty)
        assert r == {}

    def test_2_hintsets(self):
        r = update_adobe_hinting(ps_hints)
        assert r == expected_2_hintsets
