import random

from .chord import Chord
from .key import Key
from .note import transpose_note


def should_prefer_flats(key: Key) -> bool:
    """
    Decide whether chord spelling should prefer flats.
    """

    flat_keys = {
        "F",
        "Bb",
        "Eb",
        "Ab",
        "Db",
        "Gb",
    }

    return key.tonic in flat_keys


def build_minor_dominant(
    key: Key,
) -> Chord:
    """
    Build the major dominant-7 chord of a minor key.

    Examples:
        A minor -> E7
        E minor -> B7
        D minor -> A7
        C minor -> G7
    """

    prefer_flats = should_prefer_flats(
        key
    )

    dominant_root = transpose_note(
        key.tonic,
        7,
        prefer_flats=prefer_flats,
    )

    return Chord(
        root=dominant_root,
        quality="7",
        degree=None,
    )


def strengthen_minor_cadence(
    cadence,
    key: Key,
    tension: float = 0.5,
    resolution: float = 0.8,
):
    """
    In minor keys, optionally replace the diatonic minor v
    with a major dominant-7 chord.

    Example in A minor:

        Dm - Em - Am

    may become:

        Dm - E7 - Am

    Strong resolution and tension increase the chance.
    """

    if key.mode != "minor":
        return cadence

    if not cadence:
        return cadence

    tension = max(
        0.0,
        min(1.0, tension),
    )

    resolution = max(
        0.0,
        min(1.0, resolution),
    )

    dominant = build_minor_dominant(
        key
    )

    result = list(
        cadence
    )

    # Stronger resolved endings should prefer V7 -> i
    probability = (
        0.15
        + 0.45 * resolution
        + 0.25 * tension
    )

    probability = min(
        probability,
        0.95,
    )

    # Replace the penultimate v chord when the cadence
    # actually ends on tonic.
    if len(result) >= 2:

        final_chord = result[-1]
        previous_chord = result[-2]

        if (
            final_chord.degree == 1
            and previous_chord.degree == 5
            and random.random() < probability
        ):
            result[-2] = dominant

    return result


def maybe_strengthen_minor_body(
    progression,
    key: Key,
    tension: float = 0.5,
    resolution: float = 0.5,
    max_replacements: int = 1,
):
    """
    Occasionally replace diatonic minor-v chords in the body
    with dominant-7 chords.

    Example in A minor:

        Am - Em - Am

    may become:

        Am - E7 - Am

    We keep this much more conservative than cadence treatment.
    """

    if key.mode != "minor":
        return progression

    tension = max(
        0.0,
        min(1.0, tension),
    )

    resolution = max(
        0.0,
        min(1.0, resolution),
    )

    dominant = build_minor_dominant(
        key
    )

    probability = (
        0.05
        + 0.20 * tension
        + 0.10 * resolution
    )

    result = []

    replacements = 0

    for index, chord in enumerate(
        progression
    ):

        new_chord = chord

        if (
            chord.degree == 5
            and replacements < max_replacements
        ):

            next_chord = (
                progression[index + 1]
                if index + 1 < len(progression)
                else None
            )

            # Most convincing case:
            # v -> i becomes V7 -> i
            resolves_to_tonic = (
                next_chord is not None
                and next_chord.degree == 1
            )

            local_probability = (
                probability * 1.7
                if resolves_to_tonic
                else probability
            )

            if random.random() < min(
                local_probability,
                0.80,
            ):
                new_chord = dominant
                replacements += 1

        result.append(
            new_chord
        )

    return result