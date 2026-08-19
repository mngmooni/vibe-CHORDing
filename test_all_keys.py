from src.vibe_chording.vibe.vibe_generator import (
    generate_from_vibe,
)


TEST_KEYS = [
    ("C", "major"),
    ("Db", "major"),
    ("D", "major"),
    ("Eb", "major"),
    ("E", "major"),
    ("F", "major"),
    ("F#", "major"),
    ("G", "major"),
    ("Ab", "major"),
    ("A", "major"),
    ("Bb", "major"),
    ("B", "major"),

    ("C", "minor"),
    ("C#", "minor"),
    ("D", "minor"),
    ("Eb", "minor"),
    ("E", "minor"),
    ("F", "minor"),
    ("F#", "minor"),
    ("G", "minor"),
    ("G#", "minor"),
    ("A", "minor"),
    ("Bb", "minor"),
    ("B", "minor"),
]


TEST_VIBE = "dreamy nostalgic floating"


def test_key(
    tonic,
    mode,
):
    slots, interpretation = (
        generate_from_vibe(
            vibe_text=TEST_VIBE,
            key_name=tonic,
            mode=mode,
            length=8,
            complexity_override=0.65,
            section="Chorus",
        )
    )

    # --------------------------------------------------
    # 1. Slot count
    # --------------------------------------------------

    if len(slots) != 8:
        raise AssertionError(
            f"Expected 8 slots, got {len(slots)}"
        )

    # --------------------------------------------------
    # 2. Every slot must have 1 or 2 chords
    # --------------------------------------------------

    for index, slot in enumerate(
        slots
    ):
        if len(slot.chords) not in {
            1,
            2,
        }:
            raise AssertionError(
                f"Slot {index + 1} has "
                f"{len(slot.chords)} chords."
            )

    # --------------------------------------------------
    # 3. Every chord must stringify
    # --------------------------------------------------

    serialized = [
        [
            str(chord)
            for chord
            in slot.chords
        ]
        for slot
        in slots
    ]

    return serialized


def main():
    passed = 0
    failed = 0

    failures = []

    print()
    print("=" * 70)
    print("Vibe CHORDing — 24-Key Smoke Test")
    print("=" * 70)
    print()

    for tonic, mode in TEST_KEYS:

        label = (
            f"{tonic} "
            f"{mode.capitalize()}"
        )

        try:

            progression = test_key(
                tonic,
                mode,
            )

            print(
                f"[PASS] {label}"
            )

            print(
                "       "
                + " | ".join(
                    " → ".join(slot)
                    for slot
                    in progression
                )
            )

            passed += 1

        except Exception as error:

            print(
                f"[FAIL] {label}"
            )

            print(
                f"       {error}"
            )

            failures.append(
                (
                    label,
                    str(error),
                )
            )

            failed += 1

        print()

    print("=" * 70)
    print(
        f"RESULT: "
        f"{passed}/24 PASS "
        f"| {failed}/24 FAIL"
    )
    print("=" * 70)

    if failures:

        print()
        print("FAILED KEYS")
        print("-" * 70)

        for (
            label,
            error,
        ) in failures:

            print(
                f"{label}: {error}"
            )

        raise SystemExit(1)

    print()
    print(
        "All supported keys passed."
    )


if __name__ == "__main__":
    main()