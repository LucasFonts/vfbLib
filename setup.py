from setuptools import setup
# from mypyc.build import mypycify
from setuptools_rust import Binding, RustExtension


if __name__ == "__main__":
    setup(
        # ext_modules=mypycify([
        #     "Lib/vfbLib/tools/helpers.py",
        # ]),
        rust_extensions=[
            RustExtension(
                "vfbLib.reader",
                binding=Binding.PyO3
            )
        ],
    )
