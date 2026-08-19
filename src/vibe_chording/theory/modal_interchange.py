import random

from .chord import Chord
from .key import Key


# ============================================================
# Practical modal-interchange vocabulary for major keys
#
# Borrowed from the parallel minor:
#
#   IV  -> iv
#   vi  -> bVI
#   V   -> bVII
#
# We use practical enharmonic spellings where theoretical
# spelling would require double flats.
#
# Examples:
#
#   Db major:
#       iv   = Gbm
#       bVI  = A     (theoretical Bbb)
#       bVII = B     (theoretical Cb)
#
#   Ab major:
#       iv   = Dbm
#       bVI  = E     (theoretical Fb)
#       bVII = Gb
#
# This keeps the UI readable while preserving the sound.
# ============================================================

BORROWED_CHORDS = {

    "C": {
        "iv": ("F", "m"),
        "bVI": ("Ab", ""),
        "bVII": ("Bb", ""),
    },

    "Db": {
        "iv": ("Gb", "m"),
        "bVI": ("A", ""),
        "bVII": ("B", ""),
    },

    "D": {
        "iv": ("G", "m"),
        "bVI": ("Bb", ""),
        "bVII": ("C", ""),
    },

    "Eb": {
        "iv": ("Ab", "m"),
        "bVI": ("B", ""),
        "bVII": ("Db", ""),
    },

    "E": {
        "iv": ("A", "m"),
        "bVI": ("C", ""),
        "bVII": ("D", ""),
    },

    "F": {
        "iv": ("Bb", "m"),
        "bVI": ("Db", ""),
        "bVII": ("Eb", ""),
    },

    "F#": {
        "iv": ("B", "m"),
        "bVI": ("D", ""),
        "bVII": ("E", ""),
    },

    "G": {
        "iv": ("C", "m"),
        "bVI": ("Eb", ""),
        "bVII": ("F", ""),
    },

    "Ab": {
        "iv": ("Db", "m"),
        "bVI": ("E", ""),
        "bVII": ("Gb", ""),
    },

    "A": {
        "iv": ("D", "m"),
        "bVI": ("F", ""),
        "bVII": ("G", ""),
    },

    "Bb": {
        "iv": ("Eb", "m"),
        "bVI": ("Gb", ""),
        "bVII": ("Ab", ""),
    },

    "B": {
        "iv": ("E", "m"),
        "bVI": ("G", ""),
        "bVII": ("A", ""),
    },
}


def get_parallel_minor_borrowed_chords(
    key: Key,
):
    """
    Return practical borrowed chords from the
    parallel minor of a major key.

    Supported borrowed functions:

        iv
        bVI
        bVII
    """

    if key.mode != "major":
        raise ValueError(
            "Modal interchange currently supports "
            "major keys only."
        )

    if key.tonic not in BORROWED_CHORDS:
        raise ValueError(
            f"Unsupported major key for modal interchange: "
            f"{key.tonic}"
        )

    definitions = BORROWED_CHORDS[
        key.tonic
    ]

    borrowed = {}

    for name, (
        root,
        quality,
    ) in definitions.items():

        borrowed[name] = Chord(
            root=root,
            quality=quality,
            degree=None,
        )

    return borrowed


def copy_as_borrowed(
    chord: Chord,
) -> Chord:
    """
    Return an independent borrowed chord.

    Borrowed chords intentionally have no
    diatonic scale degree.
    """

    return Chord(
        root=chord.root,
        quality=chord.quality,
        degree=None,
    )


def maybe_apply_modal_interchange(
    progression,
    key: Key,
    chromaticism: float = 0.5,
    max_replacements: int = 2,
):
    """
    Apply modal interchange to the BODY
    of a major-key progression.

    Possible substitutions:

        IV -> iv
        vi -> bVI
        V  -> bVII

    Higher chromaticism increases the probability
    of borrowed harmony.

    Cadence should normally be passed separately
    and protected from this transformation.
    """

    chromaticism = max(
        0.0,
        min(1.0, chromaticism),
    )

    borrowed = (
        get_parallel_minor_borrowed_chords(
            key
        )
    )

    result = []

    replacements = 0

    for chord in progression:

        new_chord = chord

        if (
            replacements
            >= max_replacements
        ):
            result.append(
                new_chord
            )

            continue


        # --------------------------------------------------
        # IV -> iv
        #
        # C major:
        # F -> Fm
        # --------------------------------------------------

        if chord.degree == 4:

            probability = (
                0.50
                * (
                    chromaticism
                    ** 2
                )
            )

            if (
                random.random()
                < probability
            ):

                new_chord = (
                    copy_as_borrowed(
                        borrowed["iv"]
                    )
                )

                replacements += 1


        # --------------------------------------------------
        # vi -> bVI
        #
        # C major:
        # Am -> Ab
        # --------------------------------------------------

        elif chord.degree == 6:

            probability = (
                0.28
                * (
                    chromaticism
                    ** 2
                )
            )

            if (
                random.random()
                < probability
            ):

                new_chord = (
                    copy_as_borrowed(
                        borrowed["bVI"]
                    )
                )

                replacements += 1


        # --------------------------------------------------
        # V -> bVII
        #
        # C major:
        # G -> Bb
        # --------------------------------------------------

        elif chord.degree == 5:

            probability = (
                0.15
                * (
                    chromaticism
                    ** 2
                )
            )

            if (
                random.random()
                < probability
            ):

                new_chord = (
                    copy_as_borrowed(
                        borrowed["bVII"]
                    )
                )

                replacements += 1


        result.append(
            new_chord
        )

    return result