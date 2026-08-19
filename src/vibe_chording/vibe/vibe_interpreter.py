from dataclasses import dataclass
import re


@dataclass
class VibeParameters:
    complexity: float
    chromaticism: float
    tension: float
    resolution: float


@dataclass
class VibeInterpretation:
    parameters: VibeParameters
    matched_words: list[str]
    unknown_words: list[str]


BASE_PARAMETERS = VibeParameters(
    complexity=0.45,
    chromaticism=0.20,
    tension=0.45,
    resolution=0.65,
)


VIBE_RULES = {
    "dreamy": {
        "complexity": +0.22,
        "chromaticism": +0.05,
        "tension": -0.10,
        "resolution": -0.22,
    },

    "nostalgic": {
        "complexity": +0.08,
        "chromaticism": +0.18,
        "tension": -0.05,
        "resolution": -0.14,
    },

    "floating": {
        "complexity": +0.12,
        "chromaticism": +0.03,
        "tension": -0.10,
        "resolution": -0.30,
    },

    "bittersweet": {
        "complexity": +0.08,
        "chromaticism": +0.28,
        "tension": +0.08,
        "resolution": -0.10,
    },

    "emotional": {
        "complexity": +0.08,
        "chromaticism": +0.12,
        "tension": +0.05,
        "resolution": -0.08,
    },

    "melancholic": {
        "complexity": +0.10,
        "chromaticism": +0.20,
        "tension": +0.02,
        "resolution": -0.18,
    },

    "sad": {
        "complexity": +0.02,
        "chromaticism": +0.12,
        "tension": -0.02,
        "resolution": -0.15,
    },

    "warm": {
        "complexity": +0.06,
        "chromaticism": -0.05,
        "tension": -0.12,
        "resolution": +0.05,
    },

    "romantic": {
        "complexity": +0.12,
        "chromaticism": +0.10,
        "tension": -0.05,
        "resolution": -0.05,
    },

    "hopeful": {
        "complexity": -0.02,
        "chromaticism": -0.05,
        "tension": +0.05,
        "resolution": +0.18,
    },

    "bright": {
        "complexity": -0.10,
        "chromaticism": -0.15,
        "tension": -0.05,
        "resolution": +0.18,
    },

    "uplifting": {
        "complexity": -0.05,
        "chromaticism": -0.10,
        "tension": +0.10,
        "resolution": +0.22,
    },

    "energetic": {
        "complexity": -0.05,
        "chromaticism": -0.05,
        "tension": +0.22,
        "resolution": +0.10,
    },

    "dramatic": {
        "complexity": +0.12,
        "chromaticism": +0.25,
        "tension": +0.30,
        "resolution": +0.08,
    },

    "dark": {
        "complexity": +0.05,
        "chromaticism": +0.22,
        "tension": +0.22,
        "resolution": -0.10,
    },

    "mysterious": {
        "complexity": +0.15,
        "chromaticism": +0.20,
        "tension": +0.18,
        "resolution": -0.20,
    },

    "jazzy": {
        "complexity": +0.35,
        "chromaticism": +0.22,
        "tension": +0.10,
        "resolution": -0.05,
    },

    "simple": {
        "complexity": -0.32,
        "chromaticism": -0.15,
        "tension": -0.05,
        "resolution": +0.10,
    },

    "stable": {
        "complexity": -0.10,
        "chromaticism": -0.15,
        "tension": -0.22,
        "resolution": +0.28,
    },

    "tense": {
        "complexity": +0.05,
        "chromaticism": +0.15,
        "tension": +0.35,
        "resolution": -0.10,
    },

    "unresolved": {
        "complexity": +0.05,
        "chromaticism": +0.05,
        "tension": +0.10,
        "resolution": -0.40,
    },

    "soft": {
        "complexity": +0.03,
        "chromaticism": -0.08,
        "tension": -0.18,
        "resolution": -0.02,
    },

    "gentle": {
        "complexity": +0.02,
        "chromaticism": -0.08,
        "tension": -0.20,
        "resolution": +0.03,
    },

    "epic": {
        "complexity": +0.10,
        "chromaticism": +0.12,
        "tension": +0.28,
        "resolution": +0.18,
    },
}


STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "with",
    "without",
    "very",
    "really",
    "slightly",
    "somewhat",
    "feeling",
    "feel",
    "feels",
    "vibe",
    "song",
    "music",
    "like",
}


def clamp(value: float) -> float:
    return max(
        0.0,
        min(1.0, value),
    )


def tokenize(text: str) -> list[str]:
    """
    Very simple English tokenizer for v0.2.
    """

    return re.findall(
        r"[a-zA-Z]+",
        text.lower(),
    )


def interpret_vibe(
    text: str,
) -> VibeInterpretation:
    """
    Convert vibe keywords into harmony parameters
    and report which words were understood.
    """

    tokens = tokenize(text)

    complexity = BASE_PARAMETERS.complexity
    chromaticism = BASE_PARAMETERS.chromaticism
    tension = BASE_PARAMETERS.tension
    resolution = BASE_PARAMETERS.resolution

    matched_words = []
    unknown_words = []

    for token in tokens:

        if token in VIBE_RULES:

            matched_words.append(token)

            effects = VIBE_RULES[token]

            complexity += effects.get(
                "complexity",
                0.0,
            )

            chromaticism += effects.get(
                "chromaticism",
                0.0,
            )

            tension += effects.get(
                "tension",
                0.0,
            )

            resolution += effects.get(
                "resolution",
                0.0,
            )

        elif token not in STOPWORDS:

            unknown_words.append(token)

    parameters = VibeParameters(
        complexity=clamp(complexity),
        chromaticism=clamp(chromaticism),
        tension=clamp(tension),
        resolution=clamp(resolution),
    )

    return VibeInterpretation(
        parameters=parameters,
        matched_words=list(dict.fromkeys(matched_words)),
        unknown_words=list(dict.fromkeys(unknown_words)),
    )