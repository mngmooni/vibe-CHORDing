from src.vibe_chording.theory.chord import Chord


chord = Chord(
    root="C",
    quality="maj7",
    degree=1
)

print(chord)
print(chord.root)
print(chord.quality)
print(chord.degree)