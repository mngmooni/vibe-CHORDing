# --------------------------------------------------
# Pitch-class utilities
# --------------------------------------------------

# Canonical pitch classes
PITCH_CLASS_TO_SHARP = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}

PITCH_CLASS_TO_FLAT = {
    0: "C",
    1: "Db",
    2: "D",
    3: "Eb",
    4: "E",
    5: "F",
    6: "Gb",
    7: "G",
    8: "Ab",
    9: "A",
    10: "Bb",
    11: "B",
}


NOTE_TO_PITCH_CLASS = {
    # Natural notes
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,

    # Sharps
    "C#": 1,
    "D#": 3,
    "E#": 5,
    "F#": 6,
    "G#": 8,
    "A#": 10,
    "B#": 0,

    # Flats
    "Cb": 11,
    "Db": 1,
    "Eb": 3,
    "Fb": 4,
    "Gb": 6,
    "Ab": 8,
    "Bb": 10,
}


def note_to_pitch_class(note: str) -> int:
    """
    Convert a note name to pitch class.

    Examples:
        C  -> 0
        C# -> 1
        Db -> 1
        Bb -> 10
    """

    if note not in NOTE_TO_PITCH_CLASS:
        raise ValueError(
            f"Unsupported note: {note}"
        )

    return NOTE_TO_PITCH_CLASS[note]


def pitch_class_to_note(
    pitch_class: int,
    prefer_flats: bool = False,
) -> str:
    """
    Convert pitch class back to a note name.

    Example:
        1 -> C#   if prefer_flats=False
        1 -> Db   if prefer_flats=True
    """

    pitch_class = pitch_class % 12

    if prefer_flats:
        return PITCH_CLASS_TO_FLAT[pitch_class]

    return PITCH_CLASS_TO_SHARP[pitch_class]


def transpose_note(
    note: str,
    semitones: int,
    prefer_flats: bool = False,
) -> str:
    """
    Transpose a note by semitones.

    Examples:
        C + 7 -> G
        Bb + 7 -> F
        Eb + 7 -> Bb
    """

    pitch_class = note_to_pitch_class(note)

    new_pitch_class = (
        pitch_class + semitones
    ) % 12

    return pitch_class_to_note(
        new_pitch_class,
        prefer_flats=prefer_flats,
    )


def same_pitch(
    note_a: str,
    note_b: str,
) -> bool:
    """
    Check whether two differently spelled notes
    represent the same pitch class.

    Examples:
        C# and Db -> True
        A# and Bb -> True
    """

    return (
        note_to_pitch_class(note_a)
        ==
        note_to_pitch_class(note_b)
    )