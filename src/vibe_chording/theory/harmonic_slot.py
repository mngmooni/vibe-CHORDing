from dataclasses import dataclass, field

from .chord import Chord


@dataclass
class HarmonicSlot:
    chords: list[Chord] = field(
        default_factory=list
    )

    def __post_init__(self):
        if not self.chords:
            raise ValueError(
                "HarmonicSlot must contain "
                "at least one chord."
            )

        if len(self.chords) > 2:
            raise ValueError(
                "HarmonicSlot currently supports "
                "at most two chords."
            )

    def __str__(self):
        return " → ".join(
            str(chord)
            for chord in self.chords
        )

    @property
    def target(self):
        return self.chords[-1]

    @property
    def is_split(self):
        return len(self.chords) == 2


def chords_to_slots(
    progression,
):
    return [
        HarmonicSlot(
            chords=[chord]
        )
        for chord in progression
    ]