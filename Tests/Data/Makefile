.PHONY: all
all: json ufo


.PHONY: json
json: ComicJensPro-Regular.vfb.json IBMPlexSans-Medium.vfb.json IBMPlexSerif-TextItalic.vfb.json IBMPlexSerif-Text.vfb.json closepath.vfb.json hintrep.vfb.json masters.vfb.json test.vfb.json truetype_stems.vfb.json


%.vfb.json: %.vfb
	vfb2json $<


.PHONY: ufo
ufo: ComicJensPro-Regular.ufo IBMPlexSans-Medium.ufo IBMPlexSerif-TextItalic.ufo IBMPlexSerif-Text.ufo closepath.ufo hintrep.ufo masters.ufo test.ufo truetype_stems.ufo


%.ufo: %.vfb
	vfb3ufo -fo $<
