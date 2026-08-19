from src.vibe_chording.theory.key import Key


keys = [
    "C",
    "Db",
    "D",
    "Eb",
    "E",
    "F",
    "F#",
    "G",
    "Ab",
    "A",
    "Bb",
    "B",
]


for tonic in keys:

    key = Key(
        tonic=tonic,
        mode="major",
    )

    print(
        f"{tonic} major:",
        key.scale,
    )