def get_master_guides(mm_guides, master_index):
    # Concatenate guidlines for both directions and extract coords for master_index
    guides = []
    for d in "hv":
        for master_guide in mm_guides[d][master_index]:
            coord = "y" if d == "h" else "x"
            guide = {coord: master_guide["pos"]}
            angle = master_guide["angle"]
            if angle:
                guide["angle"] = angle
            guides.append(guide)
    return guides
