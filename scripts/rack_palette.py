"""Device colour key for the Nomad rack, shared by the label and schedule builds.

The DK-1221 roll is black thermal on white paper -- the printed labels cannot
carry colour. Colour therefore lives in two places:

  * on screen and on the printed proof / schedule, as a scanning aid;
  * on the rack itself, as the colour of the cable tie the tag folds over,
    which is the physical equivalent and costs nothing since every tag needs
    a tie anyway.

Hexes are the Okabe-Ito qualitative palette, which stays distinguishable under
all common forms of colour blindness -- worth caring about in a dark rack room
where colour discrimination is already degraded. Tie colours are the nearest
match in the colours cable ties are actually manufactured in.
"""

# device -> (hex, emoji swatch for markdown, cable-tie colour)
DEVICE_COLOUR = {
    "Drawmer SP2120": ("#0072B2", "🟦", "blue"),
    "Bias V3 #1":     ("#009E73", "🟩", "green"),
    "Bias Q2 #1":     ("#F0E442", "🟨", "yellow"),
    "Bias Q2 #2":     ("#E69F00", "🟧", "orange"),
    "Bias V3 #2":     ("#D55E00", "🟥", "red"),
    "Bias Q5":        ("#CC79A7", "🟪", "purple"),
    "Tripp Lite PDU": ("#444444", "⬛", "black"),
}

# Anything outside the rack shares one neutral swatch. Giving the switch or the
# venue panel its own colour would imply it is part of the keyed scheme.
OUTSIDE = ("#BBBBBB", "⬜", "—")

# Short forms that fit inside an 11 mm swatch. Colour alone forces a legend
# lookup every time; the name printed on the colour removes that, and leaves
# the colour doing what it is good at -- grouping at a glance.
SHORT = {
    "Drawmer SP2120": "SP2120",
    "Bias V3 #1": "V3 #1",
    "Bias Q2 #1": "Q2 #1",
    "Bias Q2 #2": "Q2 #2",
    "Bias V3 #2": "V3 #2",
    "Bias Q5": "Q5",
    "Tripp Lite PDU": "PDU",
    "Allen & Heath CQ-12T": "CQ-12T",
    "CQ-12T external PSU": "CQ PSU",
    "Pioneer DJM-V10": "DJM-V10",
    "DJM-V10 / Pro DJ Link hub": "DJM/HUB",
    "Pioneer CDJ-3000 #1": "CDJ 1",
    "Pioneer CDJ-3000 #2": "CDJ 2",
    "Pioneer CDJ-3000 #3": "CDJ 3",
    "Pioneer CDJ-3000 #4": "CDJ 4",
    "Network switch": "SWITCH",
    "Separate network / link-local": "LINK-LOCAL",
    "Stasys Xair L-3": "XAIR L-3",
    "Stasys Xair R-3": "XAIR R-3",
    "Stasys Xair L-1 / L-2": "XAIR L-1/2",
    "Stasys Xair R-1 / R-2": "XAIR R-1/2",
    "Air Motion V2 L": "A.MOT L",
    "Air Motion V2 R": "A.MOT R",
    "Airten V3 L": "AIRTEN L",
    "Airten V3 R": "AIRTEN R",
    "Air Vantage L": "VANTAGE L",
    "Air Vantage R": "VANTAGE R",
    "Venu 215 V2 L": "VENU L",
    "Venu 215 V2 R": "VENU R",
    "Turbosound Athens L": "ATHENS L",
    "Turbosound Athens R": "ATHENS R",
    "UNVERIFIED": "?",
    "— none —": "—",
}


def short(device):
    """Short form for a swatch. Venue-panel circuits all collapse to PANEL —
    the breaker rating is on the label text, so repeating it here wastes width."""
    device = (device or "").strip()
    if not device or device == "—":
        return "—"
    if device in SHORT:
        return SHORT[device]
    if device.lower().startswith("venue panel"):
        return "PANEL"
    return device[:10]


# Port names shortened for a label headline. The full text lives in the
# schedule; on a 17 mm line the useful part is which socket, not its prose.
PORT = {
    "Outlet": "OUT",
    "Mains inlet": "MAINS",
    "MAINS inlet": "MAINS",
    "Dedicated breaker": "BREAKER",
    "U5 bay empty": "EMPTY",
    "Output L": "OUT L",
    "Output R": "OUT R",
    "Input L": "IN L",
    "Input R": "IN R",
    "ANALOG CH1 IN": "CH1 IN",
    "ANALOG CH2 IN": "CH2 IN",
    "ANALOG CH1 OUT (pre-DSP)": "CH1 LINE OUT",
    "ANALOG CH2 OUT (pre-DSP)": "CH2 LINE OUT",
    "ANALOG IN 1": "IN 1",
    "LINE input CH1": "LINE CH1",
    "LINE input CH2": "LINE CH2",
    "OUT1 (CH1)": "OUT1",
    "OUT2 (CH2)": "OUT2",
    "OUT1 (CH1+CH2)": "OUT1 CH1-2",
    "OUT2 (CH3+CH4)": "OUT2 CH3-4",
    "OUTPUTS CH1": "CH1",
    "OUTPUTS CH2": "CH2",
    "OUTPUTS CH3": "CH3",
    "OUTPUTS CH4": "CH4",
    "AESOP primary (rear)": "AESOP 1",
    "etherCON ETH1 primary": "ETH1",
    "ETHERNET": "ETH",
    "NETWORK": "NET",
    "Port TBC": "PORT ?",
    "NL4 In": "NL4",
    "NL4 #1 pins 1+/1-": "NL4#1 LF",
    "NL4 #2 pins 2+/2-": "NL4#2 HMF",
    "Phoenix recessed": "PHOENIX",
    "MonOut L (Out 1-6)": "MONOUT L",
    "MonOut R (Out 1-6)": "MONOUT R",
    "BakFil L (Out 1-6)": "BAKFIL L",
    "BakFil R (Out 1-6)": "BAKFIL R",
    "MASTER1 L": "MASTER L",
    "MASTER1 R": "MASTER R",
    "UNVERIFIED": "?",
}


def short_port(port):
    port = (port or "").strip()
    if not port or port == "—":
        return ""
    return PORT.get(port, port)


def ink_on(hex_colour):
    """Black or white, whichever stays legible on the given swatch."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return "#000000" if luminance > 0.4 else "#FFFFFF"


def colour(device):
    """(hex, emoji, tie_colour) for a device; the neutral swatch if off-rack."""
    return DEVICE_COLOUR.get(device, OUTSIDE)


def hex_of(device):
    return colour(device)[0]


def swatch(device):
    return colour(device)[1]


def key_rows():
    """Ordered (device, hex, emoji, tie) for rendering a legend."""
    return [(d, *v) for d, v in DEVICE_COLOUR.items()]


# --- Label text must survive a Windows ANSI reader ---------------------------
# P-touch Editor reads a merge CSV as CP1252, not UTF-8: a middle dot arrives as
# "Â·" and an arrow as "â†'". A BOM usually fixes that, but "usually" is not good
# enough for text that gets stuck on a cable, so anything printed is reduced to
# ASCII as well. The typographic loss at 2.2 mm on a thermal head is nil.
ASCII_MAP = {
    "·": "-",      # middle dot separator
    "→": "->",     # route arrow
    "←": "<-",
    "Ω": "OHM",
    "−": "-",      # U+2212 minus
    "—": "-",      # em dash
    "–": "-",      # en dash
    "’": "'",
    "×": "x",
}


CONN = {
    "Phoenix 12-pin": "PHNX 12P",
    "Phoenix PC 5/8": "PHNX 5/8",
    "Phoenix PC 5/5": "PHNX 5/5",
    "Phoenix": "PHOENIX",
    "etherCON RJ45": "etherCON",
    "speakON NL4": "NL4",
    "NEMA 5-15R": "NEMA 5-15",
}


def short_conn(c):
    """Connector name trimmed to fit the headline slot on the connector face."""
    c = (c or "").strip()
    return CONN.get(c, c) if c and c != "—" else "-"


def ascii_label(s):
    """Reduce a printed label string to ASCII. Non-label columns keep Unicode."""
    for a, b in ASCII_MAP.items():
        s = s.replace(a, b)
    return s.encode("ascii", "replace").decode("ascii")
