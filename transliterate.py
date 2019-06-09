#!/mingw64/bin/python3

import sys


transliterations = {
    "u0410": "A",
    "u0411": "B",
    "u0412": "V",
    "u0413": "G",
    "u0414": "D",
    "u0402": "Dy",
    "u0415": "E",
    "u0416": "Zx",
    "u0417": "Z",
    "u0418": "I",
    "u0408": "J",
    "u041a": "K",
    "u041b": "L",
    "u0409": "Ly",
    "u041c": "M",
    "u041d": "N",
    "u040a": "Ny",
    "u041e": "O",
    "u041f": "P",
    "u0420": "R",
    "u0421": "S",
    "u0422": "T",
    "u040b": "Ch",
    "u0423": "U",
    "u0424": "F",
    "u0425": "H",
    "u0426": "C",
    "u0427": "Cx",
    "u040f": "Dx",
    "u0428": "Sx",
    "u0430": "a",
    "u0431": "b",
    "u0432": "v",
    "u0433": "g",
    "u0434": "d",
    "u0452": "dy",
    "u0435": "e",
    "u0436": "zx",
    "u0437": "z",
    "u0438": "i",
    "u0458": "j",
    "u043a": "k",
    "u043b": "l",
    "u0459": "ly",
    "u043c": "m",
    "u043d": "n",
    "u045a": "ny",
    "u043e": "o",
    "u043f": "p",
    "u0440": "r",
    "u0441": "s",
    "u0442": "t",
    "u045b": "ch",
    "u0443": "u",
    "u0444": "f",
    "u0445": "h",
    "u0446": "c",
    "u0447": "cx",
    "u045f": "dx",
    "u0448": "sx"
}


def transliterate(original):
    transliterated = ""
    enc = sys.stdout.encoding
    for c in original:
        t = c
        u = str(c).encode(enc, errors='backslashreplace').decode(enc)
        if len(u) > 1:
            t = transliterations[u[1::]]
        transliterated += t
    return transliterated
