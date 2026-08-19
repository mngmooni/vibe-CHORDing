from pathlib import Path

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

from ..theory.note import note_to_pitch_class


# --------------------------------------------------
# Chord intervals
# --------------------------------------------------

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


def chord_to_midi_notes(
    chord,
    root_octave: int = 4,
):
    """
    Convert a Chord object into MIDI note numbers.

    C4 = MIDI 60

    Example:
        Cmaj7 -> [60, 64, 67, 71]
        Am7   -> [69, 72, 76, 79]
    """

    if chord.quality not in CHORD_INTERVALS:
        raise ValueError(
            f"Unsupported chord quality for MIDI: "
            f"{chord.quality}"
        )

    pitch_class = note_to_pitch_class(
        chord.root
    )

    root_note = (
        12 * (root_octave + 1)
        + pitch_class
    )

    intervals = CHORD_INTERVALS[
        chord.quality
    ]

    return [
        root_note + interval
        for interval in intervals
    ]


def render_progression_to_midi(
    progression,
    output_path="vibe_progression.mid",
    bpm: int = 90,
    beats_per_chord: int = 4,
    velocity: int = 70,
):
    """
    Render a chord progression to a MIDI file.

    Each chord currently lasts the same number of beats.
    Harmonic rhythm will be added later.
    """

    midi = MidiFile(
        ticks_per_beat=480
    )

    track = MidiTrack()
    midi.tracks.append(track)

    # ----------------------------------------------
    # Tempo
    # ----------------------------------------------

    track.append(
        MetaMessage(
            "set_tempo",
            tempo=bpm2tempo(bpm),
            time=0,
        )
    )

    # Acoustic Grand Piano
    track.append(
        Message(
            "program_change",
            program=0,
            time=0,
        )
    )

    chord_duration = (
        midi.ticks_per_beat
        * beats_per_chord
    )

    # ----------------------------------------------
    # Chords
    # ----------------------------------------------

    for chord in progression:

        notes = chord_to_midi_notes(
            chord
        )

        # Start all notes simultaneously
        for note in notes:
            track.append(
                Message(
                    "note_on",
                    note=note,
                    velocity=velocity,
                    time=0,
                )
            )

        # Stop notes.
        #
        # MIDI time is delta-time, so only the first
        # note_off carries the duration.
        for index, note in enumerate(notes):
            track.append(
                Message(
                    "note_off",
                    note=note,
                    velocity=0,
                    time=(
                        chord_duration
                        if index == 0
                        else 0
                    ),
                )
            )

    track.append(
        MetaMessage(
            "end_of_track",
            time=0,
        )
    )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    midi.save(
        output_path
    )

    return output_path