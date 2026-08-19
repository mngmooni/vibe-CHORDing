from src.vibe_chording.vibe.vibe_generator import (
    generate_from_vibe,
)
from src.vibe_chording.audio.voice_leading import (
    voice_lead_progression,
)


vibe = "dreamy nostalgic floating"

progression, interpretation = generate_from_vibe(
    vibe_text=vibe,
    key_name="C",
    length=8,
)

voicings = voice_lead_progression(
    progression
)


print()
print("=" * 70)
print("VIBE CHORDING — VOICE LEADING TEST")
print("=" * 70)

print()
print(f"Vibe: {vibe}")

print()
print(
    "Progression:"
)

print(
    " - ".join(
        str(chord)
        for chord in progression
    )
)

print()
print("Voicings:")
print()

for chord, voicing in zip(
    progression,
    voicings,
):

    print(
        f"{str(chord):8} -> {voicing}"
    )

print()
print("=" * 70)