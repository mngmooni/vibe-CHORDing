from src.vibe_chording.engine.harmony_engine import (
    generate_progression_parts,
)
from src.vibe_chording.engine.final_cleanup import (
    remove_consecutive_duplicates,
)
from src.vibe_chording.theory.chord_color import (
    colorize_progression,
)
from src.vibe_chording.theory.key import Key
from src.vibe_chording.theory.secondary_dominant import (
    maybe_insert_secondary_dominants,
)
from src.vibe_chording.theory.modal_interchange import (
    maybe_apply_modal_interchange,
)


presets = [
    {
        "name": "Simple / Stable",
        "complexity": 0.15,
        "chromaticism": 0.05,
        "tension": 0.20,
        "resolution": 0.95,
    },

    {
        "name": "Dreamy / Floating",
        "complexity": 0.85,
        "chromaticism": 0.15,
        "tension": 0.35,
        "resolution": 0.20,
    },

    {
        "name": "Bittersweet",
        "complexity": 0.55,
        "chromaticism": 0.75,
        "tension": 0.55,
        "resolution": 0.65,
    },

    {
        "name": "Dramatic / Tense",
        "complexity": 0.75,
        "chromaticism": 0.85,
        "tension": 0.90,
        "resolution": 0.90,
    },
]


for preset in presets:

    print()
    print("=" * 75)
    print(preset["name"])

    print(
        f"Complexity: {preset['complexity']} | "
        f"Chromaticism: {preset['chromaticism']} | "
        f"Tension: {preset['tension']} | "
        f"Resolution: {preset['resolution']}"
    )

    print("=" * 75)

    for i in range(3):

        key = Key(
            tonic="C",
            mode="major",
        )

        # --------------------------------------------------
        # 1. Generate BODY + protected CADENCE separately
        # --------------------------------------------------

        body, cadence = generate_progression_parts(
            key_name="C",
            length=8,
            tension=preset["tension"],
            resolution=preset["resolution"],
        )

        # --------------------------------------------------
        # 2. Modal interchange ONLY on body
        # --------------------------------------------------

        body = maybe_apply_modal_interchange(
            body,
            key=key,
            chromaticism=preset["chromaticism"],
            max_replacements=2,
        )

        # --------------------------------------------------
        # 3. Secondary dominants ONLY on body
        # --------------------------------------------------

        body = maybe_insert_secondary_dominants(
            body,
            key=key,
            chromaticism=preset["chromaticism"],
            max_insertions=2,
        )

        # --------------------------------------------------
        # 4. Re-attach protected cadence
        # --------------------------------------------------

        progression = (
            body
            + cadence
        )

        # --------------------------------------------------
        # 5. Add chord colors
        # --------------------------------------------------

        progression = colorize_progression(
            progression,
            complexity=preset["complexity"],
        )

        # --------------------------------------------------
        # 6. Remove exact consecutive duplicates
        # --------------------------------------------------

        progression = remove_consecutive_duplicates(
            progression
        )

        # --------------------------------------------------
        # 7. Print
        # --------------------------------------------------

        print(
            " - ".join(
                str(chord)
                for chord in progression
            )
        )