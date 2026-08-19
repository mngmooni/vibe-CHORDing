from src.vibe_chording.theory.note import (
    note_to_pitch_class,
    transpose_note,
    same_pitch,
)


print(
    "C# == Db:",
    same_pitch("C#", "Db"),
)

print(
    "A# == Bb:",
    same_pitch("A#", "Bb"),
)

print(
    "Bb + 7 semitones:",
    transpose_note(
        "Bb",
        7,
        prefer_flats=True,
    ),
)

print(
    "Eb + 7 semitones:",
    transpose_note(
        "Eb",
        7,
        prefer_flats=True,
    ),
)

print(
    "F# pitch class:",
    note_to_pitch_class("F#"),
)

print(
    "Gb pitch class:",
    note_to_pitch_class("Gb"),
)