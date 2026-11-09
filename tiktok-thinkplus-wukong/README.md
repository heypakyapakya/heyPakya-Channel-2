# Lenovo thinkplus WuKong TWS — TikTok affiliate ad (HyperFrames)

**Final video:** `renders/thinkplus-wukong-tiktok.mp4` — 1080×1920, 30 fps, 21.6 s, H.264 + AAC, −13 LUFS.

Style: cinematic, epic, premium unboxing. No dialogue, no voice-over, no faces. Teal-orange colour grade, letterbox bars, on-screen text in Malay.

| Time | Scene | Sound |
|---|---|---|
| 0–4.2 s | Premium black box with orange foil, push-in, light sweep, hook text "Bass Padu. Rasa Premium." | drone, clock ticks, whoosh |
| 4.2–7.2 s | Lid lifts, orange glow and light beam from inside, flash | creak, toms, riser |
| 7.2–10.8 s | Product reveal (case cutout, halo, ring, "WUKONG") | BRAAM + boom + sub drop |
| 10.8–18.0 s | 4 macro detail shots (13mm · BT 6.0 · Touch Control · ENC/IPX5), one cut per bar | taiko groove, ostinato, hit on every cut |
| 18.0–21.6 s | CTA "Tekan Beg Kuning" + COD / Waranti 1 Tahun / Bluetooth 6.0 | final braam + pulse |

## Version 2: 5-second teaser
**Video:** `renders/thinkplus-wukong-teaser-5s.mp4` — 1080×1920, 30 fps, 5.0 s, −14 LUFS. Composition: `teaser.html`. Cover: `renders/cover-teaser.jpg`.

| Time | Scene | Sound |
|---|---|---|
| 0–1.8 s | Box close-up, lid cracks, orange light leaks. "Sesuatu Padu Tiba." | boom, accelerating ticks, creak, riser |
| 1.8 / 2.25 / 2.7 s | Three macro punches on the beat: PADU. / PANTAS. / PREMIUM. | BRAAM, a hit on every cut, ostinato |
| 3.15–5.0 s | Product reveal "WuKong TWS" + "Tekan Beg Kuning" | final braam + chord |

```bash
python3 tools/score_teaser.py assets/audio/teaser_raw.wav
ffmpeg -i assets/audio/teaser_raw.wav -af loudnorm=I=-14:TP=-1 -ar 48000 assets/audio/teaser.wav
npx hyperframes render -c teaser.html -q delivery -o renders/thinkplus-wukong-teaser-5s.mp4
```
`hyperframes check` and `snapshot` only read `index.html`. To check the teaser, copy it as `index.html` into a scratch copy of the project.

## Music
`tools/score.py` synthesizes the whole score (133 BPM, D minor, hybrid trailer). It is deterministic and royalty-free, so there's no copyright-claim risk.
Every visual cut lands on a bar line.

```bash
python3 tools/score.py assets/audio/score_raw.wav
ffmpeg -i assets/audio/score_raw.wav -af loudnorm=I=-14:TP=-1 -ar 48000 assets/audio/score.wav
```

## Edit / re-render
```bash
npx hyperframes check
npx hyperframes snapshot --at 1,8,12,19
npx hyperframes render -q delivery -o renders/thinkplus-wukong-tiktok.mp4
```

Source images (`assets/src/`) are crops of the product listing photos from Google Drive.
`assets/img/` holds the macro crops, the blurred background plates, and the `hero.png` cutout.
