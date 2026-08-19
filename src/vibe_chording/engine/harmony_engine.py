import random

from ..theory.key import Key
from ..theory.progression import diatonic_chords


# --------------------------------------------------
# Functional-harmony transition graph
#
# Degree-based, so it can be shared by
# major and minor keys.
# --------------------------------------------------

TRANSITIONS = {
    1: [(4, 0.30), (5, 0.30), (6, 0.40)],
    2: [(5, 0.80), (7, 0.20)],
    3: [(6, 0.70), (4, 0.30)],
    4: [(1, 0.20), (2, 0.20), (5, 0.60)],
    5: [(1, 0.75), (6, 0.25)],
    6: [(2, 0.45), (4, 0.40), (5, 0.15)],
    7: [(1, 0.90), (3, 0.10)],
}


# --------------------------------------------------
# Rough harmonic tension by degree
# --------------------------------------------------

DEGREE_TENSION = {
    1: 0.05,
    2: 0.45,
    3: 0.25,
    4: 0.40,
    5: 0.85,
    6: 0.35,
    7: 1.00,
}


def clamp(value):
    return max(
        0.0,
        min(1.0, value),
    )


def tension_weight(
    degree: int,
    tension: float,
) -> float:

    target = clamp(
        tension
    )

    degree_tension = (
        DEGREE_TENSION[degree]
    )

    distance = abs(
        degree_tension
        - target
    )

    return max(
        (1.0 - distance) ** 2,
        0.05,
    )


def choose_next_degree(
    current_degree,
    history,
    tension=0.5,
):
    """
    Choose the next scale degree using:
        - functional transition weight
        - requested tension
        - repetition penalties
    """

    candidates = (
        TRANSITIONS[current_degree]
    )

    degrees = []
    weights = []

    for degree, base_weight in candidates:

        weight = base_weight

        weight *= tension_weight(
            degree,
            tension,
        )

        # Avoid exact repetition
        if degree == current_degree:
            weight *= 0.05

        # Avoid strong ABAB pattern
        if len(history) >= 3:

            if (
                degree == history[-2]
                and current_degree
                == history[-3]
            ):
                weight *= 0.05

        degrees.append(
            degree
        )

        weights.append(
            weight
        )

    return random.choices(
        degrees,
        weights=weights,
        k=1,
    )[0]


def choose_cadence(
    resolution: float,
    mode: str = "major",
):
    """
    Select an ending pattern according to resolution.

    Degree numbers work for both modes.

    Major:
        ii - V - I
        IV - V - I

    Minor:
        ii° - v - i
        iv - v - i

    Harmonic-minor dominant V7 will be added later
    as a separate minor-harmony color.
    """

    resolution = clamp(
        resolution
    )

    if resolution >= 0.7:

        return random.choices(
            population=[
                [2, 5, 1],
                [4, 5, 1],
            ],
            weights=[
                0.6,
                0.4,
            ],
            k=1,
        )[0]

    elif resolution >= 0.35:

        return random.choices(
            population=[
                [5, 6],
                [4, 1],
                [2, 5, 1],
            ],
            weights=[
                0.40,
                0.35,
                0.25,
            ],
            k=1,
        )[0]

    else:

        return random.choices(
            population=[
                [2, 5],
                [4, 5],
                [6, 4],
            ],
            weights=[
                0.40,
                0.35,
                0.25,
            ],
            k=1,
        )[0]


def generate_progression_parts(
    key_name: str = "C",
    mode: str = "major",
    length: int = 8,
    tension: float = 0.5,
    resolution: float = 0.8,
):
    """
    Generate:

        BODY + protected CADENCE

    Supports:
        major
        minor
    """

    key = Key(
        tonic=key_name,
        mode=mode,
    )

    chords = {
        chord.degree: chord
        for chord in diatonic_chords(
            key
        )
    }

    cadence_degrees = choose_cadence(
        resolution=resolution,
        mode=mode,
    )

    body_length = max(
        length
        - len(cadence_degrees),
        1,
    )

    current_degree = 1

    body_degrees = [
        current_degree
    ]

    while (
        len(body_degrees)
        < body_length
    ):

        next_degree = choose_next_degree(
            current_degree=
                current_degree,

            history=
                body_degrees,

            tension=
                tension,
        )

        body_degrees.append(
            next_degree
        )

        current_degree = (
            next_degree
        )

    # --------------------------------------------------
    # Avoid exact duplicate at body/cadence boundary
    # --------------------------------------------------

    if (
        body_degrees
        and cadence_degrees
        and body_degrees[-1]
        == cadence_degrees[0]
    ):

        if len(body_degrees) >= 2:

            previous_degree = (
                body_degrees[-2]
            )

            replacement = (
                choose_next_degree(
                    current_degree=
                        previous_degree,

                    history=
                        body_degrees[:-1],

                    tension=
                        tension,
                )
            )

            body_degrees[-1] = (
                replacement
            )

    body = [
        chords[degree]
        for degree
        in body_degrees
    ]

    cadence = [
        chords[degree]
        for degree
        in cadence_degrees
    ]

    return (
        body,
        cadence,
    )


def generate_progression(
    key_name: str = "C",
    mode: str = "major",
    length: int = 8,
    tension: float = 0.5,
    resolution: float = 0.8,
):
    """
    Backwards-compatible complete progression.
    """

    body, cadence = (
        generate_progression_parts(
            key_name=key_name,
            mode=mode,
            length=length,
            tension=tension,
            resolution=resolution,
        )
    )

    return (
        body
        + cadence
    )