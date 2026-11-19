# REVIEW — Integer (Matematik Tingkatan 1, Bab 1)

60 s · 1080×1920 (9:16) · 30 fps · HyperFrames 0.9.70 · three.js r158 (vendored in `assets/lib/`)

## Source
Google Drive folder (5 photos): the cover of *Nota Berdiagram Matematik Tingkatan 1 KSSM*, the contents page,
and pages 1–3 of Bab 1 Nombor Nisbah: *Integer positif dan negatif*, *Penambahan integer*, *Penolakan integer*.
Every number and rule in the film comes from those pages (the worked examples −3 + 7, −5 + 3, 4 − 7, −1 − 4 are
the book's own). The colour code follows the book: start number green, operation salmon, answer yellow, red arcs.

## Story (one idea: tambah → kanan, tolak → kiri)
| Time | Scene file | Beat |
| --- | --- | --- |
| 0–6 | `hook.html` + world | "Boleh ke 4 tolak 7?" — 3D cubes 4 − 7 = ? tumble in; the ? spins |
| 6–17 | `def.html` | the 3D number line builds from 0 outward; definition; negatif / positif / sifar glow |
| 17–25 | `arah.html` | tiles rise on columns as a staircase: left smaller, right bigger; terkecil −5, terbesar 5 |
| 25–39 | `tambah.html` | a ball hops right: −3 + 7 = 4, −5 + 3 = −2 (arc + "+1…+7" counter per hop) |
| 39–53 | `tolak.html` | hops left: 4 − 7 = −3 (answers the opening question), −1 − 4 = −5 |
| 53–60 | `rumusan.html` | INGAT! cards; the tiles wave right, then left |

`compositions/world.html` holds the whole 3D world for 0–60 s, drawn from time alone in an `hf-seek` listener.
Its `EX` table and camera `KEYS` are mirrored in the scene chip timings and in `tools/build_index.py`
(which writes the 72 sound-effect clips into `index.html`). Change a time in one place → change it in all three.

## Sound
- **Voiceover (BM)**: 18 lines by ElevenLabs voice *Aisyah – Patient Malay School Tutor* (`JOCyls6Fdo4qfmTUnFrJ`,
  model `eleven_multilingual_v2`, flow `1SXi6fizFPyP6uO6JDbZ`). Raw takes are `assets/voice/lNN.mp3`;
  `tools/prep_voice.sh` trims silence, speeds them 12% (pitch kept) and levels them into `vNN.wav`.
  Each line starts on its picture (table `VO` in `tools/build_index.py`); visual cues were moved to match
  (labels in `def.html`, `arah.html`, highlight times in `world.html`). No line overlaps the next.
- **Music**: ElevenLabs 60 s instrumental (`assets/audio/music.mp3`) at 0.16 under the voice, 1.5 s fade-out.
- **Effects**: bundled Pixabay SFX at 80% of their earlier level: hop ticks, chip pops, scene whooshes,
  riser + bass hit + chime on the payoff 4 − 7 = −3.
- Sound was measured, not heard.

## Checks
- `check`: 0 errors. Contrast 19/19 WCAG AA.
- Kept on purpose: `dead_stretch` at 27.9–31.6 s and 41.8–45.5 s — false positive, the check reads the DOM and
  the motion there (the ball hopping) is in the WebGL canvas.
- Kept: a few `outside_safe_zone` warnings (headers near the top, chips near the bottom for some platforms).
  All text sits inside the 168–1330 px band; the platform zones disagree with each other.

## Weakest shot / next time
- The full-line overview (6–17 s, 53–60 s): 11 tiles across a 1080 px width leaves each tile ~80 px — readable on
  a phone but small. With more time: a slow dolly along the line instead of the static wide.
- Large empty floor under the line in the overview shots (that area is under platform UI anyway).
