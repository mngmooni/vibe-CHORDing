from src.vibe_chording.theory.key import Key
from src.vibe_chording.theory.progression import diatonic_chords


key = Key("C")

chords = diatonic_chords(key)

for chord in chords:
    print(chord.degree, chord)