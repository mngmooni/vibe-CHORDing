import random

from .chord import Chord
from .key import Key
from .note import transpose_note
from .harmonic_slot import HarmonicSlot


def should_prefer_flats(
    key: Key,
) -> bool:
    flat_keys = {
        "F",
        "Bb",
        "Eb",
        "Ab",
        "Db",
        "Gb",
    }

    return key.tonic in flat_keys


def secondary_dominant_for_target(
    target_chord: Chord,
    key: Key,
) -> Chord:
    prefer_flats = should_prefer_flats(
        key
    )

    dominant_root = transpose_note(
        target_chord.root,
        7,
        prefer_flats=prefer_flats,
    )

    return Chord(
        root=dominant_root,
        quality="7",
        degree=None,
    )


def maybe_apply_secondary_dominants_to_slots(
    slots,
    key: Key,
    chromaticism: float = 0.5,
    max_insertions: int = 2,
):
    """
    Add secondary dominants inside harmonic slots
    without increasing the number of slots.

    Example:

        [C], [Dm], [G]

    may become:

        [C], [A7 -> Dm], [G]
    """

    chromaticism = max(
        0.0,
        min(1.0, chromaticism),
    )

    insertion_probability = (
        0.55 * (chromaticism ** 2)
    )

    eligible_degrees = {
        2,
        3,
        4,
        5,
        6,
    }

    result = []

    insertions = 0

    for index, slot in enumerate(
        slots
    ):
        target = slot.target

        new_slot = slot

        if (
            index > 0
            and target.degree in eligible_degrees
            and target.quality not in {"dim", "m7b5"}
            and insertions < max_insertions
            and len(slot.chords) == 1
        ):
            if (
                random.random()
                < insertion_probability
            ):
                secondary = (
                    secondary_dominant_for_target(
                        target_chord=target,
                        key=key,
                    )
                )

                if (
                    str(secondary)
                    != str(target)
                ):
                    new_slot = HarmonicSlot(
                        chords=[
                            secondary,
                            target,
                        ]
                    )

                    insertions += 1

        result.append(
            new_slot
        )

    return result