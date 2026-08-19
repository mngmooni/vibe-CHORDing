from pathlib import Path

from src.vibe_chording.audio.midi_renderer import (
    render_progression_to_midi,
)
from src.vibe_chording.vibe.vibe_generator import (
    generate_from_vibe,
)


def progression_to_text(
    progression,
):
    return " - ".join(
        str(chord)
        for chord in progression
    )


def print_parameters(
    interpretation,
):
    params = interpretation.parameters

    print()
    print("Detected vibe:")

    print(
        "  "
        + (
            ", ".join(
                interpretation.matched_words
            )
            or "No known vibe words"
        )
    )

    if interpretation.unknown_words:

        print()
        print("Unknown words:")

        print(
            "  "
            + ", ".join(
                interpretation.unknown_words
            )
        )

    print()
    print("Harmony parameters:")

    print(
        f"  Complexity   : "
        f"{params.complexity:.2f}"
    )

    print(
        f"  Chromaticism : "
        f"{params.chromaticism:.2f}"
    )

    print(
        f"  Tension      : "
        f"{params.tension:.2f}"
    )

    print(
        f"  Resolution   : "
        f"{params.resolution:.2f}"
    )


def main():

    print()
    print("=" * 60)
    print("                 VIBE CHORDING")
    print("=" * 60)

    print()
    print("Describe your vibe.")
    print(
        "Example: dreamy nostalgic floating"
    )
    print()

    vibe_text = input(
        "Your vibe > "
    ).strip()

    if not vibe_text:
        print("Please enter a vibe.")
        return

    key_name = input(
        "Key [C] > "
    ).strip()

    if not key_name:
        key_name = "C"

    # --------------------------------------------------
    # Generate first progression + interpretation
    # --------------------------------------------------

    first_progression, interpretation = (
        generate_from_vibe(
            vibe_text=vibe_text,
            key_name=key_name,
            length=8,
        )
    )

    print_parameters(
        interpretation
    )

    # --------------------------------------------------
    # Generate three candidates
    # --------------------------------------------------

    progressions = [
        first_progression
    ]

    for _ in range(2):

        progression, _ = generate_from_vibe(
            vibe_text=vibe_text,
            key_name=key_name,
            length=8,
        )

        progressions.append(
            progression
        )

    print()
    print("Generated progressions:")
    print()

    for index, progression in enumerate(
        progressions,
        start=1,
    ):

        print(
            f"{index}. "
            f"{progression_to_text(progression)}"
        )

    # --------------------------------------------------
    # MIDI selection
    # --------------------------------------------------

    print()
    print("-" * 60)

    choice = input(
        "Which progression should I export? "
        "[1/2/3, Enter=1] > "
    ).strip()

    if not choice:
        choice = "1"

    if choice not in {
        "1",
        "2",
        "3",
    }:
        print(
            "Invalid selection. Using progression 1."
        )

        choice = "1"

    selected_index = (
        int(choice) - 1
    )

    selected_progression = (
        progressions[selected_index]
    )

    # --------------------------------------------------
    # BPM
    # --------------------------------------------------

    bpm_text = input(
        "BPM [90] > "
    ).strip()

    if bpm_text:

        try:
            bpm = int(
                bpm_text
            )

        except ValueError:
            print(
                "Invalid BPM. Using 90."
            )

            bpm = 90

    else:
        bpm = 90

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    output_path = Path(
        "outputs"
    ) / "vibe_progression.mid"

    render_progression_to_midi(
        progression=selected_progression,
        output_path=output_path,
        bpm=bpm,
        beats_per_chord=4,
        velocity=70,
    )

    print()
    print(
        f"MIDI exported successfully:"
    )

    print(
        f"  {output_path.resolve()}"
    )

    print()
    print(
        f"Progression:"
    )

    print(
        f"  {progression_to_text(selected_progression)}"
    )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()