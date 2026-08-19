import { useRef, useState } from "react";
import * as Tone from "tone";
import "./App.css";


const FALLBACK_PROGRESSIONS = [
  {
    id: 1,
    title: "Vibe Match",
    slots: [
      ["Cadd9"],
      ["Am9"],
      ["Dm9"],
      ["G9"],
      ["Cmaj7"],
      ["Am9"],
      ["Dm7"],
      ["Gsus4"],
    ],
  },
  {
    id: 2,
    title: "Variation",
    slots: [
      ["Cmaj7"],
      ["Am9"],
      ["Fadd9"],
      ["G9"],
      ["Am7"],
      ["Dm9"],
      ["Fmaj7"],
      ["Gsus4"],
    ],
  },
  {
    id: 3,
    title: "Alternative",
    slots: [
      ["Cadd9"],
      ["E7", "Am9"],
      ["Fmaj7"],
      ["Dm9"],
      ["G7"],
      ["Cadd9"],
      ["Fadd9"],
      ["Gsus4"],
    ],
  },
];


const NOTE_TO_PC = {
  C: 0,
  "C#": 1,
  Db: 1,
  D: 2,
  "D#": 3,
  Eb: 3,
  E: 4,
  Fb: 4,
  "E#": 5,
  F: 5,
  "F#": 6,
  Gb: 6,
  G: 7,
  "G#": 8,
  Ab: 8,
  A: 9,
  "A#": 10,
  Bb: 10,
  B: 11,
  Cb: 11,
};


const PC_TO_SHARP = [
  "C",
  "C#",
  "D",
  "D#",
  "E",
  "F",
  "F#",
  "G",
  "G#",
  "A",
  "A#",
  "B",
];


const CHORD_INTERVALS = {
  "": [0, 4, 7],
  m: [0, 3, 7],
  dim: [0, 3, 6],

  maj7: [0, 4, 7, 11],
  m7: [0, 3, 7, 10],
  "7": [0, 4, 7, 10],

  add9: [0, 4, 7, 14],
  m9: [0, 3, 7, 10, 14],
  "9": [0, 4, 7, 10, 14],

  sus4: [0, 5, 7],
  m7b5: [0, 3, 6, 10],
};


const PIANO_KEYS = [
  { note: "C3", type: "white" },
  { note: "C#3", type: "black" },
  { note: "D3", type: "white" },
  { note: "D#3", type: "black" },
  { note: "E3", type: "white" },
  { note: "F3", type: "white" },
  { note: "F#3", type: "black" },
  { note: "G3", type: "white" },
  { note: "G#3", type: "black" },
  { note: "A3", type: "white" },
  { note: "A#3", type: "black" },
  { note: "B3", type: "white" },

  { note: "C4", type: "white" },
  { note: "C#4", type: "black" },
  { note: "D4", type: "white" },
  { note: "D#4", type: "black" },
  { note: "E4", type: "white" },
  { note: "F4", type: "white" },
  { note: "F#4", type: "black" },
  { note: "G4", type: "white" },
  { note: "G#4", type: "black" },
  { note: "A4", type: "white" },
  { note: "A#4", type: "black" },
  { note: "B4", type: "white" },

  { note: "C5", type: "white" },
  { note: "C#5", type: "black" },
  { note: "D5", type: "white" },
  { note: "D#5", type: "black" },
  { note: "E5", type: "white" },
];


function parseChordSymbol(symbol) {
  const qualities = [
    "m7b5",
    "maj7",
    "add9",
    "sus4",
    "m9",
    "m7",
    "dim",
    "m",
    "9",
    "7",
  ];

  const rootMatch = symbol.match(
    /^([A-G](?:#|b)?)/
  );

  if (!rootMatch) {
    throw new Error(
      `Cannot parse chord: ${symbol}`
    );
  }

  const root = rootMatch[1];

  const suffix = symbol.slice(
    root.length
  );

  let quality = "";

  for (const candidate of qualities) {
    if (suffix === candidate) {
      quality = candidate;
      break;
    }
  }

  if (
    suffix !== ""
    && quality === ""
  ) {
    throw new Error(
      `Unsupported chord quality: ${symbol}`
    );
  }

  return {
    root,
    quality,
  };
}


function midiToNoteName(midiNumber) {
  const pc =
    midiNumber % 12;

  const octave =
    Math.floor(
      midiNumber / 12
    ) - 1;

  return (
    PC_TO_SHARP[pc]
    + octave
  );
}


function chordToNotes(
  chordSymbol,
  rootOctave = 3
) {
  const {
    root,
    quality,
  } = parseChordSymbol(
    chordSymbol
  );

  const rootPc =
    NOTE_TO_PC[root];

  if (
    rootPc === undefined
  ) {
    throw new Error(
      `Unknown root: ${root}`
    );
  }

  const intervals =
    CHORD_INTERVALS[quality];

  if (!intervals) {
    throw new Error(
      `Unknown quality: ${quality}`
    );
  }

  let rootMidi =
    12 * (
      rootOctave + 1
    ) + rootPc;

  if (rootMidi < 48) {
    rootMidi += 12;
  }

  return intervals.map(
    (interval) =>
      midiToNoteName(
        rootMidi + interval
      )
  );
}


function stripOctave(note) {
  return note.replace(
    /\d/g,
    ""
  );
}


function App() {
  const [vibe, setVibe] =
    useState(
      "dreamy nostalgic floating"
    );

  const [keyName, setKeyName] =
    useState("C Major");

  const [section, setSection] =
    useState("Chorus");

  const [complexity, setComplexity] =
    useState(0.65);

  const [bpm, setBpm] =
    useState(82);

  const [
    progressions,
    setProgressions,
  ] = useState(
    FALLBACK_PROGRESSIONS
  );

  const [
    parameters,
    setParameters,
  ] = useState({
    complexity: 0.65,
    chromaticism: 0.46,
    tension: 0.20,
    resolution: 0.25,
  });

  const [
    playingId,
    setPlayingId,
  ] = useState(null);

  const [
    activeChord,
    setActiveChord,
  ] = useState(null);

  const [
    activeNotes,
    setActiveNotes,
  ] = useState([]);

  const [
    activeSlotIndex,
    setActiveSlotIndex,
  ] = useState(null);

  const [
    isGenerating,
    setIsGenerating,
  ] = useState(false);

  // NEW: user-visible error state
  const [
    error,
    setError,
  ] = useState("");

  const stopFlag =
    useRef(false);

  const synthRef =
    useRef(null);


  function createSynth() {
    const synth =
      new Tone.PolySynth(
        Tone.Synth
      ).toDestination();

    synth.set({
      oscillator: {
        type: "triangle",
      },

      envelope: {
        attack: 0.025,
        decay: 0.22,
        sustain: 0.44,
        release: 1.3,
      },
    });

    synth.volume.value = -12;

    return synth;
  }


  function showChord(
    chord
  ) {
    try {
      const notes =
        chordToNotes(
          chord
        );

      setActiveChord(
        chord
      );

      setActiveNotes(
        notes
      );

      return notes;
    } catch (error) {
      console.error(
        error
      );

      setActiveChord(
        chord
      );

      setActiveNotes([]);

      return [];
    }
  }


  function clearKeyboard() {
    setActiveChord(null);
    setActiveNotes([]);
    setActiveSlotIndex(null);
  }


  async function playSingleChord(
    chord
  ) {
    await Tone.start();

    const notes =
      showChord(chord);

    if (
      notes.length === 0
    ) {
      return;
    }

    const synth =
      createSynth();

    synth.triggerAttackRelease(
      notes,
      "1n"
    );

    window.setTimeout(
      () => {
        synth.dispose();
        clearKeyboard();
      },
      2600
    );
  }


  function stopPlayback() {
    stopFlag.current = true;

    if (
      synthRef.current
    ) {
      synthRef.current.releaseAll();
      synthRef.current.dispose();
      synthRef.current = null;
    }

    setPlayingId(null);
    clearKeyboard();
  }


  async function playProgression(
    progression
  ) {
    if (
      playingId ===
      progression.id
    ) {
      stopPlayback();
      return;
    }

    stopPlayback();

    await Tone.start();

    stopFlag.current =
      false;

    setPlayingId(
      progression.id
    );

    const synth =
      createSynth();

    synthRef.current =
      synth;

    const beatSeconds =
      60 / Number(bpm);

    const slotSeconds =
      beatSeconds * 4;

    for (
      let slotIndex = 0;
      slotIndex <
      progression.slots.length;
      slotIndex += 1
    ) {
      if (
        stopFlag.current
      ) {
        break;
      }

      setActiveSlotIndex(
        slotIndex
      );

      const slot =
        progression
          .slots[
            slotIndex
          ];

      const chordDuration =
        slotSeconds /
        slot.length;

      for (
        let chordIndex = 0;
        chordIndex <
        slot.length;
        chordIndex += 1
      ) {
        if (
          stopFlag.current
        ) {
          break;
        }

        const chord =
          slot[
            chordIndex
          ];

        const notes =
          showChord(
            chord
          );

        if (
          notes.length >
          0
        ) {
          synth
            .triggerAttackRelease(
              notes,
              chordDuration
              * 0.82
            );
        }

        await new Promise(
          (resolve) =>
            window.setTimeout(
              resolve,
              chordDuration
              * 1000
            )
        );
      }
    }

    if (
      !stopFlag.current
    ) {
      synth.dispose();

      synthRef.current =
        null;

      setPlayingId(null);
      clearKeyboard();
    }
  }


  async function handleGenerate() {

    // ================================================
    // INPUT VALIDATION
    // ================================================

    if (!vibe.trim()) {
      setError(
        "Describe your vibe first."
      );

      return;
    }

    if (
      !Number.isFinite(Number(bpm))
      ||
      Number(bpm) < 40
      ||
      Number(bpm) > 200
    ) {
      setError(
        "BPM must be between 40 and 200."
      );

      return;
    }


    // Clear previous error before a new request.
    setError("");

    setIsGenerating(
      true
    );


    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/generate",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body:
              JSON.stringify({
                vibe:
                  vibe.trim(),

                key:
                  keyName,

                section,

                complexity,

                bpm,
              }),
          }
        );


      // ================================================
      // BACKEND ERROR
      // ================================================

      if (
        !response.ok
      ) {
        let message =
          `Generation failed (${response.status}).`;

        try {
          const errorData =
            await response.json();

          if (
            errorData.detail
          ) {
            message =
              errorData.detail;
          }
        } catch {
          // If backend did not return JSON,
          // keep the generic message.
        }

        throw new Error(
          message
        );
      }


      const data =
        await response.json();


      // ================================================
      // RESPONSE VALIDATION
      // ================================================

      if (
        !Array.isArray(
          data.progressions
        )
      ) {
        throw new Error(
          "Invalid progression data received from the backend."
        );
      }


      console.log(
        "Vibe CHORDing:",
        data
      );


      const titles = [
        "Vibe Match",
        "Variation",
        "Alternative",
      ];


      const formatted =
        data.progressions.map(
          (
            slots,
            index
          ) => ({
            id:
              index + 1,

            title:
              titles[index]
              ||
              `Variation ${index + 1}`,

            slots,
          })
        );


      setProgressions(
        formatted
      );


      if (
        data.parameters
      ) {
        setParameters(
          data.parameters
        );

        setComplexity(
          data.parameters
            .complexity
        );
      }


      // Successful generation clears
      // any previous error message.
      setError("");

      stopPlayback();


    } catch (error) {

      console.error(
        "Vibe CHORDing generation error:",
        error
      );


      // Network failure usually means
      // FastAPI is not currently running.
      if (
        error instanceof TypeError
      ) {
        setError(
          "Couldn’t connect to the harmony engine. Check that the backend is running and try again."
        );
      } else {
        setError(
          error.message
          ||
          "Couldn’t generate chords. Please try again."
        );
      }


    } finally {

      setIsGenerating(
        false
      );

    }
  }


  function randomizeVibe() {
    const vibes = [
      "dreamy nostalgic floating",
      "warm emotional nostalgic",
      "dark mysterious tense",
      "bright uplifting summer",
      "bittersweet romantic",
      "dramatic tense stable",
    ];

    const index =
      Math.floor(
        Math.random()
        * vibes.length
      );

    setVibe(
      vibes[index]
    );

    // Remove old validation message
    // after supplying a new vibe.
    setError("");
  }


  let displayNotes = [];

  if (
    activeChord
  ) {
    try {
      displayNotes =
        chordToNotes(
          activeChord
        ).map(
          stripOctave
        );
    } catch {
      displayNotes = [];
    }
  }


  return (
    <div className="app">

      <main className="shell">

        <header className="header">

          <div>

            <div className="brand-vibe neon-soft">
              Vibe
            </div>

            <div className="brand-chording">

              <span className="letter red">
                C
              </span>

              <span className="letter orange">
                H
              </span>

              <span className="letter yellow">
                O
              </span>

              <span className="letter green">
                R
              </span>

              <span className="letter blue">
                D
              </span>

              <span className="ivory neon-soft">
                ing
              </span>

            </div>

            <p className="tagline">
              ✦ Compose with your vibe.
            </p>

          </div>


          <button
            className="random-vibe"
            onClick={
              randomizeVibe
            }
          >
            ✧ Random Vibe
          </button>

        </header>


        <section className="compose-section">

          <div className="speech-input">

            <textarea
              value={vibe}
              onChange={
                (
                  event
                ) => {
                  setVibe(
                    event
                      .target
                      .value
                  );

                  if (error) {
                    setError("");
                  }
                }
              }
              maxLength={
                120
              }
            />

            <span className="character-count">
              {vibe.length}
              {" / 120"}
            </span>

          </div>


          <div className="control-grid">

            <label className="control-card">

              <span className="control-title">
                ♫ Key
              </span>

              <select
                value={
                  keyName
                }
                onChange={
                  (
                    event
                  ) =>
                    setKeyName(
                      event
                        .target
                        .value
                    )
                }
              >

                <optgroup label="Major">
                  <option>C Major</option>
                  <option>Db Major</option>
                  <option>D Major</option>
                  <option>Eb Major</option>
                  <option>E Major</option>
                  <option>F Major</option>
                  <option>F# Major</option>
                  <option>G Major</option>
                  <option>Ab Major</option>
                  <option>A Major</option>
                  <option>Bb Major</option>
                  <option>B Major</option>
                </optgroup>

                <optgroup label="Minor">
                  <option>C Minor</option>
                  <option>C# Minor</option>
                  <option>D Minor</option>
                  <option>Eb Minor</option>
                  <option>E Minor</option>
                  <option>F Minor</option>
                  <option>F# Minor</option>
                  <option>G Minor</option>
                  <option>G# Minor</option>
                  <option>A Minor</option>
                  <option>Bb Minor</option>
                  <option>B Minor</option>
                </optgroup>

              </select>

            </label>


            <label className="control-card">

              <span className="control-title">
                ☷ Section
              </span>

              <select
                value={
                  section
                }
                onChange={
                  (
                    event
                  ) =>
                    setSection(
                      event
                        .target
                        .value
                    )
                }
              >
                <option>Verse</option>
                <option>Pre-Chorus</option>
                <option>Chorus</option>
                <option>Bridge</option>
              </select>

            </label>


            <label className="control-card complexity-card">

              <span className="control-title">
                ✦ Complexity
              </span>

              <div className="complexity-row">

                <span>
                  Simple
                </span>

                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={
                    complexity
                  }
                  onChange={
                    (
                      event
                    ) =>
                      setComplexity(
                        Number(
                          event
                            .target
                            .value
                        )
                      )
                  }
                />

                <span>
                  Complex
                </span>

                <strong>
                  {Number(
                    complexity
                  ).toFixed(
                    2
                  )}
                </strong>

              </div>

            </label>


            <label className="control-card">

              <span className="control-title">
                ◷ BPM
              </span>

              <input
                className="bpm-input"
                type="number"
                min="40"
                max="200"
                value={bpm}
                onChange={
                  (
                    event
                  ) =>
                    setBpm(
                      Number(
                        event
                          .target
                          .value
                      )
                    )
                }
              />

            </label>

          </div>


          <button className="topline-button">
            ＋ Add Topline
          </button>


          <button
            className="generate-button"
            onClick={
              handleGenerate
            }
            disabled={
              isGenerating
            }
          >
            {isGenerating
              ? "✦ CHORDing..."
              : "✦ Start CHORDing ✦"}
          </button>


          {/* ==========================================
              USER-VISIBLE ERROR MESSAGE
          ========================================== */}

          {error && (
            <div
              className="error-message"
              role="alert"
            >
              <span className="error-symbol">
                !
              </span>

              <span>
                {error}
              </span>
            </div>
          )}

        </section>


        <section className="workspace-section">

          <div className="results-column">

            <div className="results-heading">

              <span>
                ✧ Generated Progressions
              </span>

              <span className="results-count">
                8 slots · 3 suggestions
              </span>

            </div>


            <div className="progression-stack">

              {progressions.map(
                (
                  progression
                ) => (

                  <article
                    className="progression-card"
                    key={
                      progression.id
                    }
                  >

                    <div className="progression-top">

                      <span className="progression-number">
                        0
                        {
                          progression.id
                        }
                      </span>


                      <div className="progression-info">

                        <h3>
                          {
                            progression.title
                          }
                        </h3>

                        <p>
                          {vibe}
                        </p>

                      </div>


                      <span className="section-badge">
                        {
                          section
                        }
                      </span>

                    </div>


                    <div className="slot-grid">

                      {progression.slots.map(
                        (
                          slot,
                          slotIndex
                        ) => (

                          <div
                            key={
                              slotIndex
                            }
                            className={
                              activeSlotIndex ===
                              slotIndex
                              &&
                              playingId ===
                              progression.id

                                ? "harmonic-slot active"

                                : "harmonic-slot"
                            }
                          >

                            <span className="slot-number">
                              {
                                slotIndex +
                                1
                              }
                            </span>


                            <div className="slot-chords">

                              {slot.map(
                                (
                                  chord,
                                  chordIndex
                                ) => (

                                  <div
                                    className="slot-chord-wrap"
                                    key={
                                      chord
                                      +
                                      chordIndex
                                    }
                                  >

                                    <button
                                      className={
                                        activeChord ===
                                        chord

                                          ? "chord-button active"

                                          : "chord-button"
                                      }
                                      onClick={
                                        () =>
                                          playSingleChord(
                                            chord
                                          )
                                      }
                                    >
                                      {
                                        chord
                                      }
                                    </button>


                                    {
                                      chordIndex
                                      <
                                      slot.length -
                                      1
                                      && (
                                        <span className="slot-arrow">
                                          →
                                        </span>
                                      )
                                    }

                                  </div>

                                )
                              )}

                            </div>

                          </div>

                        )
                      )}

                    </div>


                    <div className="card-actions">

                      <button
                        className={
                          playingId ===
                          progression.id

                            ? "play-button active"

                            : "play-button"
                        }
                        onClick={
                          () =>
                            playProgression(
                              progression
                            )
                        }
                      >

                        {
                          playingId ===
                          progression.id

                            ? "■ Stop"

                            : "▶ Play"
                        }

                      </button>

                      <button>
                        ↻ Loop
                      </button>

                      <button>
                        ♡ Save
                      </button>

                      <button>
                        ⇩ MIDI
                      </button>

                    </div>

                  </article>

                )
              )}

            </div>

          </div>


          <aside className="voicing-column">

            <section className="keyboard-section sticky-keyboard">

              <div className="keyboard-header">

                <span>
                  ♫ Live Voicing
                </span>

                <strong>
                  {
                    activeChord
                    ||
                    "Click a chord to preview"
                  }
                </strong>

              </div>


              <div className="active-chord-info">

                <div className="big-chord">
                  {
                    activeChord
                    || "—"
                  }
                </div>


                <div className="note-pills">

                  {
                    displayNotes.length >
                    0

                      ? displayNotes.map(
                          (
                            note,
                            index
                          ) => (

                            <span
                              key={
                                note
                                +
                                index
                              }
                            >
                              {
                                note
                              }
                            </span>

                          )
                        )

                      : (
                        <span className="empty-note">
                          chord tones
                        </span>
                      )
                  }

                </div>

              </div>


              <div className="piano">

                {PIANO_KEYS.map(
                  (
                    pianoKey
                  ) => {

                    const isActive =
                      activeNotes.includes(
                        pianoKey.note
                      );

                    return (

                      <div
                        key={
                          pianoKey.note
                        }
                        className={
                          `piano-key ${pianoKey.type} ${
                            isActive
                              ? "pressed"
                              : ""
                          }`
                        }
                        title={
                          pianoKey.note
                        }
                      >

                        {
                          pianoKey.type ===
                          "white"
                          && (
                            <span>
                              {
                                pianoKey.note
                              }
                            </span>
                          )
                        }

                      </div>

                    );
                  }
                )}

              </div>


              <div className="voicing-hint">

                <span>
                  ✦ click any chord
                </span>

                <span>
                  split slot = 2 + 2 beats
                </span>

              </div>

            </section>

          </aside>

        </section>


        <section className="metric-bar">

          <div className="metric">

            <span>
              ✦ Complexity
            </span>

            <strong className="metric-yellow">
              {
                Number(
                  parameters
                    .complexity
                ).toFixed(2)
              }
            </strong>

          </div>


          <div className="metric">

            <span>
              ♯ Chromaticism
            </span>

            <strong className="metric-blue">
              {
                Number(
                  parameters
                    .chromaticism
                ).toFixed(2)
              }
            </strong>

          </div>


          <div className="metric">

            <span>
              ≋ Tension
            </span>

            <strong className="metric-pink">
              {
                Number(
                  parameters
                    .tension
                ).toFixed(2)
              }
            </strong>

          </div>


          <div className="metric">

            <span>
              ◎ Resolution
            </span>

            <strong className="metric-cyan">
              {
                Number(
                  parameters
                    .resolution
                ).toFixed(2)
              }
            </strong>

          </div>

        </section>

      </main>

    </div>
  );
}


export default App;