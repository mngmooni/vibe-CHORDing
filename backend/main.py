from fastapi import (
    FastAPI,
    HTTPException,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from pydantic import BaseModel

from src.vibe_chording.vibe.vibe_generator import (
    generate_from_vibe,
    resolve_harmony_parameters,
)


app = FastAPI(
    title="Vibe CHORDing API",
    version="0.5.0",
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(
    BaseModel
):
    vibe: str

    key: str = "C Major"

    section: str = "Chorus"

    complexity: float = 0.5

    bpm: int = 80


def parse_key(
    key_text: str,
):
    parts = (
        key_text
        .strip()
        .split()
    )

    if len(parts) != 2:

        raise ValueError(
            f"Invalid key format: "
            f"{key_text}"
        )

    tonic = parts[0]

    mode = (
        parts[1]
        .lower()
    )

    if mode not in {
        "major",
        "minor",
    }:

        raise ValueError(
            f"Unsupported mode: "
            f"{mode}"
        )

    return (
        tonic,
        mode,
    )


@app.get("/")
def root():
    return {
        "message":
            "Vibe CHORDing backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/generate")
def generate(
    request: GenerateRequest,
):
    try:

        tonic, mode = parse_key(
            request.key
        )

        generated = []

        first_interpretation = None

        # --------------------------------------------------
        # Generate 3 alternatives
        # --------------------------------------------------

        for _ in range(3):

            (
                slots,
                interpretation,
            ) = generate_from_vibe(

                vibe_text=
                    request.vibe,

                key_name=
                    tonic,

                mode=
                    mode,

                length=
                    8,

                complexity_override=
                    request.complexity,

                section=
                    request.section,
            )

            if (
                first_interpretation
                is None
            ):
                first_interpretation = (
                    interpretation
                )

            serialized_slots = [

                [
                    str(chord)

                    for chord
                    in slot.chords
                ]

                for slot
                in slots
            ]

            generated.append(
                serialized_slots
            )

        # --------------------------------------------------
        # Return the ACTUAL parameters used
        # by the harmony engine.
        # --------------------------------------------------

        effective_params = (
            resolve_harmony_parameters(

                interpretation=
                    first_interpretation,

                complexity_override=
                    request.complexity,

                section=
                    request.section,
            )
        )

        return {

            "vibe":
                request.vibe,

            "key":
                request.key,

            "tonic":
                tonic,

            "mode":
                mode,

            "section":
                request.section,

            "bpm":
                request.bpm,

            "slot_count":
                8,

            "parameters": {

                "complexity":
                    round(
                        effective_params[
                            "complexity"
                        ],
                        2,
                    ),

                "chromaticism":
                    round(
                        effective_params[
                            "chromaticism"
                        ],
                        2,
                    ),

                "tension":
                    round(
                        effective_params[
                            "tension"
                        ],
                        2,
                    ),

                "resolution":
                    round(
                        effective_params[
                            "resolution"
                        ],
                        2,
                    ),
            },

            "matched_words":
                first_interpretation
                .matched_words,

            "unknown_words":
                first_interpretation
                .unknown_words,

            "progressions":
                generated,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )