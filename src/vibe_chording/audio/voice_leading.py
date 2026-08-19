from itertools import product

from ..theory.note import note_to_pitch_class


CHORD_INTERVALS = {
    "": [0, 4, 7],
    "m": [0, 3, 7],
    "dim": [0, 3, 6],

    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10],
    "m7b5": [0, 3, 6, 10],

    "add9": [0, 4, 7, 14],
    "m9": [0, 3, 7, 10, 14],
    "9": [0, 4, 7, 10, 14],

    "sus4": [0, 5, 7],
}


def chord_pitch_classes(chord):
    """
    Convert a chord into pitch classes.

    Example:
        Cmaj7 -> [0, 4, 7, 11]
    """

    if chord.quality not in CHORD_INTERVALS:
        raise ValueError(
            f"Unsupported chord quality: {chord.quality}"
        )

    root_pc = note_to_pitch_class(
        chord.root
    )

    return [
        (root_pc + interval) % 12
        for interval in CHORD_INTERVALS[chord.quality]
    ]


def generate_voicing_candidates(
    chord,
    min_note=48,
    max_note=76,
):
    """
    Generate possible voicings for a chord
    inside a practical keyboard register.

    Default:
        C3 (48) -> E5 (76)
    """

    pitch_classes = chord_pitch_classes(
        chord
    )

    note_options = []

    for pitch_class in pitch_classes:

        options = []

        for midi_note in range(
            min_note,
            max_note + 1,
        ):

            if midi_note % 12 == pitch_class:
                options.append(midi_note)

        note_options.append(options)

    candidates = []

    for combination in product(
        *note_options
    ):

        notes = sorted(
            combination
        )

        # No duplicated exact MIDI notes
        if len(set(notes)) != len(notes):
            continue

        # Keep voicing reasonably compact
        span = (
            notes[-1]
            - notes[0]
        )

        if span > 24:
            continue

        candidates.append(
            notes
        )

    return candidates


def voice_leading_cost(
    previous_voicing,
    candidate_voicing,
):
    """
    Calculate a simple movement cost.

    Lower = smoother voice leading.
    """

    previous = sorted(
        previous_voicing
    )

    candidate = sorted(
        candidate_voicing
    )

    # ------------------------------------------
    # Compare closest voices
    # ------------------------------------------

    count = min(
        len(previous),
        len(candidate),
    )

    movement_cost = sum(
        abs(
            candidate[i]
            - previous[i]
        )
        for i in range(count)
    )

    # ------------------------------------------
    # Penalize large jumps
    # ------------------------------------------

    jump_penalty = 0

    for i in range(count):

        movement = abs(
            candidate[i]
            - previous[i]
        )

        if movement > 7:
            jump_penalty += (
                movement - 7
            ) * 2

    # ------------------------------------------
    # Slight penalty for extremely wide voicings
    # ------------------------------------------

    span = (
        candidate[-1]
        - candidate[0]
    )

    span_penalty = max(
        0,
        span - 16,
    ) * 0.5

    # ------------------------------------------
    # Slight penalty for very high / low center
    # ------------------------------------------

    center = sum(
        candidate
    ) / len(candidate)

    preferred_center = 60

    register_penalty = (
        abs(
            center - preferred_center
        )
        * 0.15
    )

    return (
        movement_cost
        + jump_penalty
        + span_penalty
        + register_penalty
    )


def choose_first_voicing(
    chord,
):
    """
    Pick a balanced first voicing around middle C.
    """

    candidates = generate_voicing_candidates(
        chord
    )

    if not candidates:
        raise ValueError(
            f"No voicing candidates found for {chord}"
        )

    def first_voicing_cost(
        voicing,
    ):

        center = sum(
            voicing
        ) / len(voicing)

        span = (
            voicing[-1]
            - voicing[0]
        )

        return (
            abs(center - 60)
            + 0.25 * span
        )

    return min(
        candidates,
        key=first_voicing_cost,
    )


def choose_next_voicing(
    chord,
    previous_voicing,
):
    """
    Find the voicing with minimum movement
    from the previous chord.
    """

    candidates = generate_voicing_candidates(
        chord
    )

    if not candidates:
        raise ValueError(
            f"No voicing candidates found for {chord}"
        )

    return min(
        candidates,
        key=lambda candidate: voice_leading_cost(
            previous_voicing,
            candidate,
        ),
    )


def voice_lead_progression(
    progression,
):
    """
    Convert an entire chord progression into
    smooth MIDI-note voicings.
    """

    if not progression:
        return []

    voicings = []

    first = choose_first_voicing(
        progression[0]
    )

    voicings.append(
        first
    )

    previous = first

    for chord in progression[1:]:

        current = choose_next_voicing(
            chord=chord,
            previous_voicing=previous,
        )

        voicings.append(
            current
        )

        previous = current

    return voicings