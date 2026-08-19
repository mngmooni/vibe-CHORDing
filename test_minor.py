from src.vibe_chording.theory.key import Key
from src.vibe_chording.theory.progression import diatonic_chords


test_keys = [
    Key("A", mode="minor"),
    Key("C", mode="minor"),
    Key("E", mode="minor"),
    Key("F", mode="minor"),
]


for key in test_keys:

    print()
    print("=" * 50)
    print(f"Key: {key.tonic} {key.mode}")
    print("=" * 50)

    print(
        "Scale:",
        " ".join(key.scale),
    )

    chords = diatonic_chords(key)

    print(
        "Chords:",
        " - ".join(
            str(chord)
            for chord in chords
        )
    )