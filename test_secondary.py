from src.vibe_chording.theory.key import Key
from src.vibe_chording.theory.progression import diatonic_chords
from src.vibe_chording.theory.secondary_dominant import (
    secondary_dominant_for_target,
)


keys = [
    "C",
    "D",
    "E",
    "F",
    "G",
    "Bb",
    "Eb",
]


for key_name in keys:

    key = Key(key_name)

    print()
    print("=" * 50)
    print(f"Key: {key_name} major")
    print("=" * 50)

    chords = diatonic_chords(key)

    for chord in chords:

        if chord.degree in {
            2,
            3,
            4,
            5,
            6,
        }:

            secondary = secondary_dominant_for_target(
                target_chord=chord,
                key=key,
            )

            print(
                f"V/{chord.degree}: "
                f"{secondary} -> {chord}"
            )