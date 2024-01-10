from __future__ import annotations

from regex import search
from typing import List


def rename_kern_classes_in_feature_code(data: List[str]) -> List[str]:
    """
    Convert references to kerning classes in the feature code to current UFO naming
    standards (public.kern1, public.kern2).
    """
    features = []
    in_kern = False
    for line in data:
        if "#" in line:
            code, comment = line.split("#", 1)
            print(f"'{code}' '{comment}'")
        else:
            code = line
            comment = None

        if code.startswith("feature kern {"):
            in_kern = True
        elif in_kern:
            if code.startswith("} kern;"):
                in_kern = False
            else:
                parts = code.split()
                if parts:
                    first = parts[0]
                    if first == "enum":
                        if parts[1] == "pos":
                            L = parts[2]
                            R = parts[3]
                            if L.startswith("@_"):
                                parts[2] = f"@public.kern1.{L[1:]}"
                            if R.startswith("@_"):
                                parts[3] = f"@public.kern2.{R[1:]}"
                            code = "   " + " ".join(parts)
                        else:
                            print("Could not parse kerning line:")
                            print(line)
                            raise ValueError
                    elif first == "pos":
                        L = parts[1]
                        R = parts[2]
                        if L.startswith("@_"):
                            parts[1] = f"@public.kern1.{L[1:]}"
                        if R.startswith("@_"):
                            parts[2] = f"@public.kern2.{R[1:]}"
                        line = "   " + " ".join(parts)
                    elif first == "subtable;":
                        pass
                    else:
                        print("Could not parse kerning line:")
                        print(line)
                        raise ValueError
                else:
                    pass
        if comment:
            features.append(f"{code}#{comment}")
        else:
            features.append(code)
    return features
