def remove_consecutive_duplicates(
    progression,
):
    """
    Remove consecutive duplicate chords.

    Example:

        Cmaj7 - Dm7 - Dm7 - G7

    becomes:

        Cmaj7 - Dm7 - G7
    """

    if not progression:
        return []

    cleaned = [
        progression[0]
    ]

    for chord in progression[1:]:

        previous = cleaned[-1]

        if str(chord) == str(previous):
            continue

        cleaned.append(chord)

    return cleaned