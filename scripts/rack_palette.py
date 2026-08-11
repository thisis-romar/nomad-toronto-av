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
