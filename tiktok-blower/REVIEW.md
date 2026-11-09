# AETHSTEEL 998VF — TikTok affiliate 30s (9:16)

Render: `renders/aethsteel-998vf-tiktok-30s.mp4` (1080x1920, 30 fps, 30.0 s, -13.3 LUFS, true peak -1.0 dBTP).

## Struktur
| Masa | Babak | Isi |
|---|---|---|
| 0.0–2.4 | Hook | "DAUN KERING PENUH LAMAN?" / "Jangan sapu dulu… tengok ni." |
| 2.4–5.0 | Product reveal | Produk masuk dengan riser + impact, "INI RAHSIANYA", AETHSTEEL 998VF |
| 5.0–8.6 | Model demo | Angkat blower, dialog "Tak payah sapu lama-lama", punch-in macro produk |
| 8.6–11.4 | Product macro | Kipas turbo: 300W · 33,000 pusingan/minit · 2.6 m³/minit |
| 11.4–16.3 | Model demo | Tiup daun, "Tiup je semua ke satu tempat", "Cepat, mudah, tak penat sangat" |
| 16.3–19.2 | Product details | "Satu alat, dua fungsi": TIUP/SEDUT, bateri 21V, 2 bateri, kelajuan boleh laras |
| 19.2–24.4 | Model demo | Mod sedut, "Dah kumpul, sedut pulak", "Laman bersih, kerja pun settle" |
| 24.4–30.0 | End card | "Laman bersih. Tanpa penat." + "Masih nak menyapu esok pagi?" + CTA "TEKAN BEG KUNING" |

## Keputusan kreatif
- Dialog: suara model dalam klip asal dikekalkan (dialog atas skrin, bibir sync), tiada voice-over/narator. Kapsyen ikut apa yang dia sebut; baris rasa ingin tahu (hook, kicker, end card) dalam Bahasa Melayu standard.
- Muzik: cinematic epic (taiko, brass, strings ostinato, 120 BPM) dijana secara lokal dengan MusicGen medium; di-duck ke ~0.3 bila model bercakap, penuh dalam babak produk.
- Colour grading: teal-orange (shadow 200°, highlight 35°), contrast +0.16, highlights -0.18, vibrance +0.14, vignette 0.32, grain 0.12 — via `hyperframes media-treatment`.
- Semua teks dalam band selamat TikTok (168–1330 px), jauh dari rail butang kanan.
- Spec diambil dari listing (300W, 33000 r/min, 2.6 m³/min, 21V, 2x bateri). Harga tidak dimasukkan kerana baucar berubah.

## Yang diukur vs dilihat
- Diukur: `check` lulus (0 error), loudness, peak, tempoh. Dilihat: snapshot setiap babak & seam.
- Bunyi diukur, bukan didengar. Muzik AI (MusicGen) — kualiti boleh ditingkatkan dengan katalog muzik HeyGen (`npx hyperframes auth login`).

## Amaran yang dikekalkan
- `contrast_aa_failure` pada kapsyen "Cepat," (emas atas daun): kapsyen ada outline hitam 14px yang check tak kira.

## Kalau ada masa lagi
- Babak macro guna gambar listing (kualiti sederhana); klip close-up sebenar kipas lebih kuat.
