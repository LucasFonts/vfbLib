```
8B        0     EV      x0 (pos x in font units)
49      -66     EV      y0 (pos y in font units)
F8 A4   528     EV      x1 (width in font units)
F8 E6   594     EV      y1 (height in font units)
93        8     EV      w (width in pixels)
95       10     EV      h (width in pixels)
9F       20     EV      image data size (in bytes)
10       16     int8    16 + 1 values follow
00 00           -------- --------
3E 00           --11111- --------
63 00           -11---11 --------
63 00           -11---11 --------
7F 00           -1111111 --------
60 00           -11----- --------
60 00           -11----- --------
63 00           -11---11 --------
3E              --11111-
FE       -2     int8     -(-2) + 1 values are repetitions of the following uint8
00                       --------
               (-------- --------)
```

Glyph bitmaps:

```
93        8     EV      number of bitmaps

9a       15     EV      ppm of next bitmap
8b        0     EV      x position
8a       -1     EV      y position
93        8     EV      x advance
8b        0     EV      y advance
94        9     EV      w (width in pixels)
95       10     EV      h (width in pixels)
9f       20     EV      image data size (in bytes)
10       16     int8    16 + 1 values follow
00 00 3b 00 66 00 66 00 3e 00 06 00 66 00 66 00 3c
fe       -2     int8    -(-2) + 1 values are repetitions of the following uint8
00

99       14     EV      ppm of next bitmap
8b        0     EV      x position
8a       -1     EV      y position
93
8b
93
94
9d
0e       14     int8    14 + 1 values follow
00 00 3b 00 66 00 66 00 3e 00 06 00 66 00 3c
fe
00
98
8b
8a928b93948def009b8b8a948b9495a013fe80fe80fe80fe80fe80fe80fe80aa8055000080958a8a908b9292990a0000340048003800080070fe00968a8a918b93939b0c000036004c0044003c00040038fe00938a8a8f8b91919708000068005800080070fe00948a8a908b9292990a0000340048003800080070fe00
```
