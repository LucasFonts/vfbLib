from pathlib import Path

from vfbLib.vfb.vfb import Vfb

size(1000, 1000)

vfb_path = Path(__file__).parent.parent / "Tests" / "Data" / "ComicJensPro-Regular.vfb"

vfb = Vfb(vfb_path)
g = vfb["Adieresis"]
bez = BezierPath()
g.drawPoints(bez)
drawPath(bez)
