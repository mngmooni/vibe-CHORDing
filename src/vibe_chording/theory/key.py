from dataclasses import dataclass


# --------------------------------------------------
# Correctly spelled major scales
# --------------------------------------------------

MAJOR_SCALES = {
    "C":  ["C", "D", "E", "F", "G", "A", "B"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "D":  ["D", "E", "F#", "G", "A", "B", "C#"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E":  ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "F":  ["F", "G", "A", "Bb", "C", "D", "E"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "G":  ["G", "A", "B", "C", "D", "E", "F#"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "A":  ["A", "B", "C#", "D", "E", "F#", "G#"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "B":  ["B", "C#", "D#", "E", "F#", "G#", "A#"],
}


# --------------------------------------------------
# Correctly spelled natural minor scales
# --------------------------------------------------

MINOR_SCALES = {
    "C":  ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "C#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "D":  ["D", "E", "F", "G", "A", "Bb", "C"],
    "Eb": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
    "E":  ["E", "F#", "G", "A", "B", "C", "D"],
    "F":  ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "F#": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "G":  ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "G#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "A":  ["A", "B", "C", "D", "E", "F", "G"],
    "Bb": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
    "B":  ["B", "C#", "D", "E", "F#", "G", "A"],
}


SUPPORTED_MAJOR_KEYS = list(MAJOR_SCALES.keys())
SUPPORTED_MINOR_KEYS = list(MINOR_SCALES.keys())


@dataclass
class Key:
    tonic: str
    mode: str = "major"

    @property
    def scale(self):

        if self.mode == "major":

            if self.tonic not in MAJOR_SCALES:
                raise ValueError(
                    f"Unsupported major key: {self.tonic}. "
                    f"Supported keys: {SUPPORTED_MAJOR_KEYS}"
                )

            return MAJOR_SCALES[self.tonic]

        if self.mode == "minor":

            if self.tonic not in MINOR_SCALES:
                raise ValueError(
                    f"Unsupported minor key: {self.tonic}. "
                    f"Supported keys: {SUPPORTED_MINOR_KEYS}"
                )

            return MINOR_SCALES[self.tonic]

        raise ValueError(
            f"Unsupported mode: {self.mode}. "
            f"Use 'major' or 'minor'."
        )