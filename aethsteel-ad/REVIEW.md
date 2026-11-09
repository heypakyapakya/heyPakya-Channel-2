# REVIEW — AETHSTEEL 998VF TikTok ad (30 s, 1080×1920, 30 fps)

## Creative calls
- Story is a neighbour's dialogue that pulls the viewer through the ad, in standard Malay, on screen
  only (no voiceover):
  1. “Laman awak bersih betul… / Upah orang ke?” (hook, readable at frame 0)
  2. “Tak. Rahsianya… / …ada dalam kotak ini.” (premium box)
  3. Product reveal → turbo-fan macro (33,000 r/min · 300W · 2.6 m³/min) → detail callouts
     (trigger, grip, 21V battery) → TIUP / SEDUT 2-in-1
  4. “Patutlah laman awak kemas. / Beli di mana?” → CTA “Tekan beg kuning sekarang”.
- The user's shot list was followed in that order, so no alternative storylines were built.
- Every claim comes from the listing screenshots (specs, 2 batteries, accessories, blower/vacuum).
  No price is shown (the RM30.26 was a voucher price and will change); the "Decker 5 years
  warranty" badge was left out.
- **The premium box is designed, not photographed** — the listing has no packaging photo. It
  carries the real logo (from the listing) in gold foil.
- Product cutouts were made from the listing photos with a local OpenCV matte (the bundled
  background-removal model is for people and cut the product badly).

## Sound
- Music: cinematic epic bed, 100 BPM, generated locally with MusicGen (small) because there was no
  HeyGen sign-in for the music catalog. Normalised to −16.6 LUFS, true peak −4.4 dBTP.
- SFX from the bundled library, each placed so its measured peak lands one frame after its picture:
  whip whooshes, bass hit on the lid, riser into the reveal, impact on the reveal and the CTA, pops on
  the specs, soft whooshes on the callouts.
- The sound was **measured, not heard**.

## Checked
- `hyperframes check`: 0 errors, 0 warnings after the fixes (line holds, contrast on the macro
  labels, the box texture text marked as texture).
- `snapshot --review`: beats, seams and the 360 px phone sheet were looked at.
- TikTok safe zone: all words between y 168–1330 and x 80–940.

## Weakest shot / next steps
- The music is MusicGen-small quality: decent, not production-grade. Signing in to HeyGen
  (`npx hyperframes auth login`) gives the 10k-track catalog; swap `assets/music/epic-cinematic.wav`.
- The model-demo photos are 1672×941 and upscaled ~2× for 9:16, so they are slightly soft.
  Real vertical footage of the product in use would lift the hook most.
- Modes scene (TIUP/SEDUT) uses small listing images (≈600 px) at 1.3–1.5×.
