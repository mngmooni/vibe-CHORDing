from .chord import Chord
from .key import Key


# --------------------------------------------------
# Diatonic chord qualities
# --------------------------------------------------

MAJOR_QUALITIES = [
    "",       # I
    "m",      # ii
    "m",      # iii
    "",       # IV
    "",       # V
    "m",      # vi
    "dim",    # vii°
]


NATURAL_MINOR_QUALITIES = [
    "m",      # i
    "dim",    # ii°
    "",       # III
    "m",      # iv
    "m",      # v
    "",       # VI
    "",       # VII
]


def diatonic_chords(key: Key):
    """
    Build the diatonic chords for a key.

    Examples:

    C major:
        C Dm Em F G Am Bdim

    A minor:
        Am Bdim C Dm Em F G
    """

    if key.mode == "major":
        qualities = MAJOR_QUALITIES

    elif key.mode == "minor":
        qualities = NATURAL_MINOR_QUALITIES

    else:
        raise ValueError(
            f"Unsupported mode: {key.mode}"
        )

    chords = []

    for degree, (root, quality) in enumerate(
        zip(key.scale, qualities),
        start=1,
    ):

        chord = Chord(
            root=root,
            quality=quality,
            degree=degree,
        )

        chords.append(chord)

    return chords