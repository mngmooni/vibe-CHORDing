import random

from .chord import Chord


# ============================================================
# Degree-aware color rules
# ============================================================
#
# Key idea:
#
#   1) Preserve the original chord quality
#   2) Use scale degree when it matters
#
# This avoids mistakes such as:
#
#   C major:
#       V = G
#       Gmaj7  ❌
#       G7     ✅
#
# while still supporting:
#
#       I  C  -> C / Cmaj7 / Cadd9
#       IV F  -> F / Fmaj7 / Fadd9
#
# ============================================================


MAJOR_TRIAD_OPTIONS_BY_DEGREE = {
    # I
    1: [
        ("", 0.0),
        ("maj7", 0.5),
        ("add9", 0.8),
    ],

    # IV
    4: [
        ("", 0.0),
        ("maj7", 0.5),
        ("add9", 0.8),
    ],

    # V
    5: [
        ("", 0.0),
        ("7", 0.5),
        ("sus4", 0.7),
        ("9", 0.9),
    ],
}


MINOR_TRIAD_OPTIONS = [
    ("m", 0.0),
    ("m7", 0.5),
    ("m9", 0.9),
]


DIMINISHED_OPTIONS = [
    ("dim", 0.2),
    ("m7b5", 0.7),
]


DOMINANT_OPTIONS = [
    ("7", 0.3),
    ("9", 0.9),
]


# Already-colored chords should stay
# within their harmonic family.
PRECOLORED_OPTIONS = {
    "maj7": [
        ("maj7", 0.5),
        ("add9", 0.8),
    ],

    "m7": [
        ("m7", 0.5),
        ("m9", 0.9),
    ],

    "m7b5": [
        ("m7b5", 0.7),
    ],

    "add9": [
        ("add9", 0.8),
    ],

    "m9": [
        ("m9", 0.9),
    ],

    "9": [
        ("9", 0.9),
    ],

    "sus4": [
        ("sus4", 0.7),
    ],
}


def complexity_weight(
    option_level,
    target_complexity,
):
    """
    Prefer chord colors whose complexity
    is close to the requested value.
    """

    distance = abs(
        option_level
        - target_complexity
    )

    weight = (
        1.0 - distance
    ) ** 4

    return max(
        weight,
        0.001,
    )


def choose_quality(
    options,
    complexity,
):
    qualities = []
    weights = []

    for (
        quality,
        option_level,
    ) in options:

        qualities.append(
            quality
        )

        weights.append(
            complexity_weight(
                option_level=option_level,
                target_complexity=complexity,
            )
        )

    return random.choices(
        qualities,
        weights=weights,
        k=1,
    )[0]


def colorize_chord(
    chord: Chord,
    complexity: float = 0.5,
):
    """
    Add chord color while preserving
    harmonic function.

    Both chord quality AND degree
    are considered.

    Special rule:
        complexity == 0.0
        -> strict simplest-chord mode
    """

    complexity = max(
        0.0,
        min(1.0, complexity),
    )

    quality = chord.quality
    degree = chord.degree


    # ========================================================
    # STRICT SIMPLE MODE
    #
    # complexity == 0.0 means:
    # no 7ths, 9ths, add9, sus4, etc.
    # ========================================================

    if complexity == 0.0:

        # Minor family
        if quality in {
            "m",
            "m7",
            "m9",
        }:
            simple_quality = "m"

        # Diminished family
        elif quality in {
            "dim",
            "m7b5",
        }:
            simple_quality = "dim"

        # Major / dominant / suspended family
        elif quality in {
            "",
            "maj7",
            "add9",
            "7",
            "9",
            "sus4",
        }:
            simple_quality = ""

        # Unknown quality:
        # preserve instead of corrupting it
        else:
            return chord

        return Chord(
            root=chord.root,
            quality=simple_quality,
            degree=degree,
        )


    # ========================================================
    # NORMAL COLOR MODE
    # complexity > 0
    # ========================================================

    # --------------------------------------------------
    # 1. Minor triads
    #
    # Am -> Am / Am7 / Am9
    # --------------------------------------------------

    if quality == "m":

        selected = choose_quality(
            MINOR_TRIAD_OPTIONS,
            complexity,
        )

        return Chord(
            root=chord.root,
            quality=selected,
            degree=degree,
        )


    # --------------------------------------------------
    # 2. Diminished
    #
    # Bdim -> Bdim / Bm7b5
    # --------------------------------------------------

    if quality == "dim":

        selected = choose_quality(
            DIMINISHED_OPTIONS,
            complexity,
        )

        return Chord(
            root=chord.root,
            quality=selected,
            degree=degree,
        )


    # --------------------------------------------------
    # 3. Existing dominant chords
    #
    # A7 -> A7 / A9
    # --------------------------------------------------

    if quality == "7":

        selected = choose_quality(
            DOMINANT_OPTIONS,
            complexity,
        )

        return Chord(
            root=chord.root,
            quality=selected,
            degree=degree,
        )


    # --------------------------------------------------
    # 4. Plain major triads
    #
    # Degree matters:
    #
    # I  -> maj7 / add9 allowed
    # IV -> maj7 / add9 allowed
    # V  -> 7 / sus4 / 9
    # --------------------------------------------------

    if quality == "":

        if (
            degree
            in MAJOR_TRIAD_OPTIONS_BY_DEGREE
        ):

            options = (
                MAJOR_TRIAD_OPTIONS_BY_DEGREE[
                    degree
                ]
            )

        else:
            # Other major/chromatic triads:
            # keep conservative.
            options = [
                ("", 0.0),
                ("add9", 0.8),
            ]

        selected = choose_quality(
            options,
            complexity,
        )

        return Chord(
            root=chord.root,
            quality=selected,
            degree=degree,
        )


    # --------------------------------------------------
    # 5. Already-colored chords
    # --------------------------------------------------

    if (
        quality
        in PRECOLORED_OPTIONS
    ):

        selected = choose_quality(
            PRECOLORED_OPTIONS[
                quality
            ],
            complexity,
        )

        return Chord(
            root=chord.root,
            quality=selected,
            degree=degree,
        )


    # --------------------------------------------------
    # 6. Unknown quality
    #
    # Never destroy information.
    # --------------------------------------------------

    return chord


def colorize_progression(
    progression,
    complexity: float = 0.5,
):
    return [
        colorize_chord(
            chord,
            complexity=complexity,
        )
        for chord
        in progression
    ]