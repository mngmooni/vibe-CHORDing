from ..engine.harmony_engine import (
    generate_progression_parts,
)


from ..theory.chord_color import (
    colorize_progression,
)

from ..theory.key import Key

from ..theory.modal_interchange import (
    maybe_apply_modal_interchange,
)

from ..theory.secondary_dominant import (
    maybe_apply_secondary_dominants_to_slots,
)

from ..theory.minor_harmony import (
    maybe_strengthen_minor_body,
    strengthen_minor_cadence,
)

from ..theory.harmonic_slot import (
    HarmonicSlot,
    chords_to_slots,
)

from .vibe_interpreter import (
    interpret_vibe,
)


# ============================================================
# Helpers
# ============================================================

def clamp(value: float) -> float:
    return max(
        0.0,
        min(1.0, value),
    )


# ------------------------------------------------------------
# SECTION PROFILES
#
# These modify the vibe-derived harmony parameters.
#
# Complexity is NOT modified here because the UI slider
# should behave as a direct user control.
# ------------------------------------------------------------

SECTION_PROFILES = {

    "Verse": {
        "chromaticism": -0.08,
        "tension": -0.10,
        "resolution": -0.10,
    },

    "Pre-Chorus": {
        "chromaticism": 0.05,
        "tension": 0.22,
        "resolution": -0.12,
    },

    "Chorus": {
        "chromaticism": 0.03,
        "tension": 0.05,
        "resolution": 0.20,
    },

    "Bridge": {
        "chromaticism": 0.20,
        "tension": 0.10,
        "resolution": -0.15,
    },
}


def resolve_harmony_parameters(
    interpretation,
    complexity_override=None,
    section: str = "Chorus",
):
    """
    Combine:

        vibe interpretation
        +
        user complexity slider
        +
        song-section behavior

    into the final parameters used by the harmony engine.
    """

    base = interpretation.parameters

    # --------------------------------------------------
    # Complexity
    #
    # If frontend supplies a slider value,
    # use it directly.
    # --------------------------------------------------

    if complexity_override is None:
        complexity = base.complexity
    else:
        complexity = complexity_override

    complexity = clamp(
        complexity
    )

    # --------------------------------------------------
    # Section profile
    # --------------------------------------------------

    profile = SECTION_PROFILES.get(
        section,
        SECTION_PROFILES["Chorus"],
    )

    chromaticism = clamp(
        base.chromaticism
        + profile["chromaticism"]
    )

    tension = clamp(
        base.tension
        + profile["tension"]
    )

    resolution = clamp(
        base.resolution
        + profile["resolution"]
    )

    return {
        "complexity": complexity,
        "chromaticism": chromaticism,
        "tension": tension,
        "resolution": resolution,
    }


def colorize_slot(
    slot: HarmonicSlot,
    complexity: float,
):
    """
    Apply chord coloring to every chord
    contained inside one harmonic slot.
    """

    colored_chords = colorize_progression(
        slot.chords,
        complexity=complexity,
    )

    return HarmonicSlot(
        chords=colored_chords
    )


# ============================================================
# Main generator
# ============================================================

def generate_from_vibe(
    vibe_text: str,
    key_name: str = "C",
    mode: str = "major",
    length: int = 8,
    complexity_override=None,
    section: str = "Chorus",
):
    """
    Generate fixed harmonic slots from natural-language vibe.

    Parameters
    ----------
    vibe_text:
        Natural-language mood description.

    key_name:
        Tonic, e.g. C / A / Bb.

    mode:
        major or minor.

    length:
        Number of harmonic slots.

    complexity_override:
        If supplied by the frontend,
        directly controls chord-color complexity.

    section:
        Verse / Pre-Chorus / Chorus / Bridge.
    """

    # --------------------------------------------------
    # 1. Interpret vibe
    # --------------------------------------------------

    interpretation = interpret_vibe(
        vibe_text
    )

    params = resolve_harmony_parameters(
        interpretation=interpretation,
        complexity_override=complexity_override,
        section=section,
    )

    complexity = params[
        "complexity"
    ]

    chromaticism = params[
        "chromaticism"
    ]

    tension = params[
        "tension"
    ]

    resolution = params[
        "resolution"
    ]

    key = Key(
        tonic=key_name,
        mode=mode,
    )

    # --------------------------------------------------
    # 2. Harmonic skeleton
    # --------------------------------------------------

    body, cadence = generate_progression_parts(
        key_name=key_name,
        mode=mode,
        length=length,
        tension=tension,
        resolution=resolution,
    )

    # --------------------------------------------------
    # 3. Major modal interchange
    # --------------------------------------------------

    if mode == "major":

        body = maybe_apply_modal_interchange(
            body,
            key=key,
            chromaticism=chromaticism,
            max_replacements=2,
        )

    # --------------------------------------------------
    # 4. Minor dominant treatment
    # --------------------------------------------------

    if mode == "minor":

        body = maybe_strengthen_minor_body(
            body,
            key=key,
            tension=tension,
            resolution=resolution,
            max_replacements=1,
        )

        cadence = strengthen_minor_cadence(
            cadence,
            key=key,
            tension=tension,
            resolution=resolution,
        )

    # --------------------------------------------------
    # 5. Reassemble
    # --------------------------------------------------

    progression = (
        body
        + cadence
    )

    

    # --------------------------------------------------
    # 6. Convert to harmonic slots
    # --------------------------------------------------

    slots = chords_to_slots(
        progression
    )

    # --------------------------------------------------
    # 7. Secondary dominants
    #
    # They live INSIDE slots, so they do not
    # increase the number of harmonic slots.
    # --------------------------------------------------

    slots = maybe_apply_secondary_dominants_to_slots(
        slots,
        key=key,
        chromaticism=chromaticism,
        max_insertions=2,
    )

    # --------------------------------------------------
    # 8. Chord extensions / color
    # --------------------------------------------------

    slots = [
        colorize_slot(
            slot,
            complexity=complexity,
        )
        for slot in slots
    ]

    return (
        slots,
        interpretation,
    )