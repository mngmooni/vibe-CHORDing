from dataclasses import dataclass


@dataclass
class Chord:
    root: str
    quality: str
    degree: int | None = None

    def __str__(self):
        return f"{self.root}{self.quality}"