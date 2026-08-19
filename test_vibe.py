from src.vibe_chording.vibe.vibe_generator import (
    generate_from_vibe,
)


test_vibes = [
    "dreamy nostalgic",
    "warm emotional nostalgic",
    "bright uplifting energetic",
    "dark mysterious tense",
    "jazzy romantic floating",
]


for vibe in test_vibes:

    print()
    print("=" * 75)
    print(f"VIBE: {vibe}")
    print("=" * 75)

    progression, interpretation = generate_from_vibe(
        vibe_text=vibe,
        key_name="C",
        length=8,
    )

    params = interpretation.parameters

    print(
        "Matched:",
        ", ".join(
            interpretation.matched_words
        )
        or "None"
    )

    print(
        "Unknown:",
        ", ".join(
            interpretation.unknown_words
        )
        or "None"
    )

    print(
        f"complexity={params.complexity:.2f} | "
        f"chromaticism={params.chromaticism:.2f} | "
        f"tension={params.tension:.2f} | "
        f"resolution={params.resolution:.2f}"
    )

    print()

    for i in range(3):

        progression, _ = generate_from_vibe(
            vibe_text=vibe,
            key_name="C",
            length=8,
        )

        print(
            f"{i + 1}. "
            + " - ".join(
                str(chord)
                for chord in progression
            )
        )