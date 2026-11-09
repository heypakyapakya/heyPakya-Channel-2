# Generates the MOHAWK MH-P15 HyperFrames project (index.html + scene files).
import json, os, sys

P = sys.argv[1]
os.makedirs(f"{P}/compositions", exist_ok=True)

# ---------------- timeline (seconds) ----------------
# (id, file, start, duration, playback_rate, kind)
SHOTS = []
t = 0.0
def shot(id_, dur, rate=1.0, kind="broll"):
    global t
    SHOTS.append(dict(id=id_, start=round(t, 3), dur=round(dur, 3), rate=rate, kind=kind))
    t = round(t + dur, 3)
    return SHOTS[-1]["start"]

S_GLINT = shot("hook-glint", 1.20)
S_HERO  = shot("hook-hero", 1.44, 0.70)
S_BUZZ  = shot("prob-buzz", 0.80, kind="talk")
S_TALK  = shot("prob-talk", 5.00, kind="talk")      # source offset 2.55
S_SOLA  = shot("sol-a", 3.80, kind="talk")          # source offset 0.00
S_SOLB  = shot("sol-b", 3.22, kind="talk")          # source offset 4.08
S_BOX   = shot("feat-box", 2.40, 0.75)
S_FACE  = shot("feat-face", 1.90, 0.737)
S_CASE  = shot("feat-case", 1.94, 0.722)
S_STRAP = shot("feat-strap", 2.10, 0.667)
S_CTAA  = shot("cta-a", 1.74, kind="talk")          # source offset 0.00
S_CTAB  = shot("cta-b", 6.12, kind="talk")          # source offset 1.92
TOTAL = round(t, 2)

talk  = lambda src: round(S_TALK + (src - 2.55), 3)
sola  = lambda src: round(S_SOLA + src, 3)
solb  = lambda src: round(S_SOLB + (src - 4.08), 3)
ctaa  = lambda src: round(S_CTAA + src, 3)
ctab  = lambda src: round(S_CTAB + (src - 1.92), 3)

F0 = S_BOX
VO = {"vo-hook": (0.05, 3.11), "vo-f1": (F0 + 0.04, 2.425), "vo-f2": (F0 + 2.57, 2.494),
      "vo-f3": (F0 + 5.16, 1.767), "vo-f4": (F0 + 7.03, 1.199)}
END_CARD = ctab(4.64)
CLOSEUP = ctab(6.20)

# ---------------- captions (standard Malay, phrase groups) ----------------
# (text, start, end, highlighted words)
CAPS = [
    ("Pernahkah anda", talk(2.66), talk(3.48), []),
    ("sedang sibuk bekerja,", talk(3.48), talk(4.80), ["sibuk"]),
    ("tetapi asyik perlu melihat telefon", talk(4.80), talk(6.12), ["telefon"]),
    ("setiap kali ada notifikasi?", talk(6.12), talk(7.50), ["notifikasi?"]),
    ("Ha,", sola(0.0) + 0.12, sola(0.70), []),
    ("sebab itulah saya memilih", sola(0.78), sola(2.00), []),
    ("Boleh lihat WhatsApp,", solb(4.14), solb(5.40), ["WhatsApp,"]),
    ("jawab panggilan", solb(5.50), solb(6.20), ["panggilan"]),
    ("dan pelbagai lagi.", solb(6.20), solb(7.28), []),
    ("Memang berbaloi.", ctaa(0.0) + 0.12, ctaa(1.22), ["berbaloi."]),
    ("Mahu satu?", ctaa(1.24), ctaa(1.74), []),
    ("Jangan tunggu lama.", ctab(1.96), ctab(2.98), []),
    ("Klik pautan sekarang", ctab(3.06), ctab(3.88), ["sekarang"]),
    ("dan dapatkan", ctab(3.88), ctab(4.64), []),
]

# ---------------- sound effects (start = event - peak offset) ----------------
SFX = [  # id, file, start, volume
    ("sfx-hook-hit", "impact-bass-1", 0.00, 0.55),
    ("sfx-hook-cut", "whoosh-short", S_HERO - 0.16, 0.40),
    ("sfx-buzz", "notification", S_BUZZ - 0.10, 0.35),
    ("sfx-notif-0", "pop", S_BUZZ + 0.28 - 0.12, 0.30),
    ("sfx-notif-1", "pop", talk(4.80) - 0.12, 0.40),
    ("sfx-notif-2", "notification", talk(5.44) - 0.23, 0.30),
    ("sfx-notif-3", "pop", talk(5.84) - 0.12, 0.40),
    ("sfx-sol-cut", "whoosh", S_SOLA - 0.16, 0.30),
    ("sfx-title", "impact-bass-2", sola(2.00) - 2.06, 0.50),
    ("sfx-chip-1", "pop", solb(4.98) - 0.12, 0.40),
    ("sfx-chip-2", "click", solb(5.56) - 0.07, 0.45),
    ("sfx-chip-3", "ping", solb(6.20) - 0.32, 0.30),
    ("sfx-feat-cut", "whoosh", F0 - 0.16, 0.40),
    ("sfx-spec-1", "ping", F0 + 0.30 - 0.32, 0.30),
    ("sfx-feat-cut-2", "whoosh-short", S_FACE - 0.16, 0.25),
    ("sfx-spec-2", "click", F0 + 2.75 - 0.07, 0.45),
    ("sfx-feat-cut-3", "whoosh", S_CASE - 0.16, 0.22),
    ("sfx-spec-3", "pop", F0 + 5.35 - 0.12, 0.40),
    ("sfx-feat-cut-4", "whoosh-short", S_STRAP - 0.16, 0.25),
    ("sfx-spec-4", "impact-bass-1", F0 + 7.18 - 0.14, 0.45),
    ("sfx-cta-cut", "whoosh", S_CTAA - 0.16, 0.30),
    ("sfx-stamp", "pop", ctaa(0.74) - 0.12, 0.45),
    ("sfx-button", "click", ctab(3.06) - 0.07, 0.50),
    ("sfx-end-cut", "whoosh-short", END_CARD - 0.16, 0.30),
    ("sfx-end", "sparkle", END_CARD + 0.05, 0.35),
    ("sfx-closeup", "whoosh", CLOSEUP - 0.16, 0.25),
]
SFX_DUR = {"impact-bass-1": 2.12, "impact-bass-2": 2.59, "whoosh": 0.57, "whoosh-short": 0.57,
           "pop": 0.72, "ping": 1.32, "notification": 2.46, "click": 0.37, "sparkle": 1.80}

# ---------------- music bed with ducking ----------------
M0 = S_HERO  # music drops on the hero cut
def m(t_abs, v): return {"t": round(max(0, t_abs - M0), 3), "v": v}
MUSIC_LANE = [m(M0, 0.55), m(S_TALK - 0.25, 0.55), m(S_TALK, 0.28), m(F0 - 0.2, 0.28), m(F0, 0.62),
              m(S_CTAA - 0.2, 0.62), m(S_CTAA, 0.28), m(ctab(6.18), 0.28), m(ctab(6.18) + 0.3, 0.85)]
MUSIC_DUR = round(TOTAL - M0, 3)

# ---------------- punch-ins on shot wrappers ----------------
# (wrapper id, time, scale, duration, origin) ; duration 0.0 = hard punch
PUNCH = [
    ("hook-glint", S_GLINT, 1.22, 0.0, "60% 45%"), ("hook-glint", S_GLINT + 0.01, 1.0, 1.15, "60% 45%"),
    ("hook-hero", S_HERO, 1.0, 0.0, "50% 50%"), ("hook-hero", S_HERO + 0.01, 1.12, 1.40, "50% 50%"),
    ("prob-buzz", S_BUZZ, 1.10, 0.0, "40% 70%"), ("prob-buzz", S_BUZZ + 0.01, 1.0, 0.78, "40% 70%"),
    ("prob-talk", S_TALK, 1.0, 0.0, "50% 32%"), ("prob-talk", talk(4.80), 1.10, 0.0, "50% 32%"),
    ("prob-talk", talk(6.70), 1.16, 0.12, "50% 40%"),
    ("sol-a", S_SOLA, 1.15, 0.0, "50% 32%"), ("sol-a", sola(0.78), 1.0, 0.0, "50% 32%"),
    ("sol-a", sola(2.00), 1.08, 0.18, "50% 40%"),
    ("sol-b", S_SOLB, 1.0, 0.0, "50% 32%"), ("sol-b", solb(5.56), 1.10, 0.0, "50% 32%"),
    ("sol-b", solb(6.50), 1.0, 0.0, "50% 32%"),
    ("feat-box", S_BOX, 1.0, 0.0, "50% 50%"), ("feat-box", S_BOX + 0.01, 1.10, 2.35, "50% 50%"),
    ("feat-face", S_FACE, 1.12, 0.0, "50% 50%"), ("feat-face", S_FACE + 0.01, 1.0, 1.85, "50% 50%"),
    ("feat-case", S_CASE, 1.0, 0.0, "40% 50%"), ("feat-case", S_CASE + 0.01, 1.10, 1.90, "40% 50%"),
    ("feat-strap", S_STRAP, 1.10, 0.0, "50% 50%"), ("feat-strap", S_STRAP + 0.01, 1.0, 2.05, "50% 50%"),
    ("cta-a", S_CTAA, 1.12, 0.0, "50% 32%"), ("cta-a", ctaa(1.24), 1.0, 0.0, "50% 32%"),
    ("cta-b", S_CTAB, 1.0, 0.0, "50% 32%"), ("cta-b", ctab(3.06), 1.12, 0.0, "50% 32%"),
    ("cta-b", ctab(3.88), 1.0, 0.0, "50% 32%"),
    ("cta-b", CLOSEUP, 1.0, 0.0, "50% 50%"), ("cta-b", CLOSEUP + 0.01, 1.10, TOTAL - CLOSEUP - 0.05, "50% 50%"),
]
FLASHES = [S_HERO, F0, CLOSEUP]

# =====================================================================
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

shots_html = []
for i, s in enumerate(SHOTS):
    media = (f'muted playsinline' if s["kind"] == "broll"
             else 'playsinline data-has-audio="true" data-volume="1"')
    rate = f' data-playback-rate="{s["rate"]}"' if s["rate"] != 1.0 else ""
    shots_html.append(
        f'      <div class="shot" id="w-{s["id"]}">\n'
        f'        <video id="v-{s["id"]}" class="clip {s["kind"]}" src="assets/video/{s["id"]}.mp4"\n'
        f'          data-start="{s["start"]}" data-duration="{s["dur"]}"{rate} data-track-index="0"\n'
        f'          {media}></video>\n      </div>')

def host(id_, start, dur, track, z, kind="graphics"):
    return (f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html"\n'
            f'        data-start="{round(start,3)}" data-duration="{round(dur,3)}" data-track-index="{track}"\n'
            f'        data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index:{z}"></div>')

hosts = [
    host("hook", 0, S_BUZZ, 2, 50),
    host("problem", S_BUZZ, S_SOLA - S_BUZZ, 3, 51),
    host("solution", S_SOLA, F0 - S_SOLA, 4, 52),
    host("features", F0, S_CTAA - F0, 5, 53),
    host("cta", S_CTAA, TOTAL - S_CTAA, 6, 54),
    host("captions", 0, TOTAL, 7, 60, "captions"),
]

audio = []
for k, (st, d) in VO.items():
    audio.append(f'      <audio id="a-{k}" class="clip" src="assets/audio/{k}.wav" data-start="{round(st,3)}" '
                 f'data-duration="{d}" data-volume="1" data-track-index="10"></audio>')
lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": MUSIC_LANE}]}).replace('"', "&quot;")
audio.append(f'      <audio id="a-music" class="clip" src="assets/audio/music.wav" data-start="{M0}" '
             f'data-duration="{MUSIC_DUR}" data-volume="0.5" data-fade-out="1.2" data-track-index="11"\n'
             f'        data-automation="{lane}"></audio>')
lanes_end = []
for i, (id_, f, st, vol) in enumerate(SFX):
    st = round(max(0.0, st), 3)
    d = min(SFX_DUR[f], round(TOTAL - st, 3))
    li = next((k for k, e in enumerate(lanes_end) if e <= st), None)
    if li is None: lanes_end.append(0); li = len(lanes_end) - 1
    lanes_end[li] = st + d
    audio.append(f'      <audio id="{id_}" class="clip" src="assets/audio/{f}.mp3" data-start="{st}" '
                 f'data-duration="{d}" data-volume="{vol}" data-track-index="{12 + li}"></audio>')

punch_js = []
for wid, at, sc, d, origin in PUNCH:
    at = round(at, 3)
    if d == 0:
        punch_js.append(f'      tl.set("#w-{wid}", {{ scale: {sc}, transformOrigin: "{origin}" }}, {at});')
    else:
        punch_js.append(f'      tl.to("#w-{wid}", {{ scale: {sc}, transformOrigin: "{origin}", duration: {round(d,3)}, ease: "power2.out" }}, {at});')
flash_js = []
for at in FLASHES:
    flash_js.append(f'      tl.to("#flash", {{ opacity: 0.85, duration: 0.05, ease: "none" }}, {round(at-0.03,3)});')
    flash_js.append(f'      tl.to("#flash", {{ opacity: 0, duration: 0.22, ease: "power2.out" }}, {round(at+0.02,3)});')

index = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --ground: #060607;
        --ink: #ffffff;
        --red: #e3141b;
        --steel: #b9bec6;
        --font-display: "Archivo Black", sans-serif;
        --font-ui: "Montserrat", sans-serif;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ground); }}
      .shot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; z-index: 1; }}
      .shot video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #flash {{ position: absolute; inset: 0; background: #fff6f0; opacity: 0; z-index: 90; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- FOOTAGE: cut, pauses removed, graded with data-color-grading -->
{chr(10).join(shots_html)}

      <!-- MOTION GRAPHICS -->
{chr(10).join(hosts)}

      <div id="flash" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-layout-ignore></div>

      <!-- AUDIO: VO (Malaysian Malay), music bed, SFX -->
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // punch-ins and slow pushes (wrappers are untimed; the <video> carries the timing)
{chr(10).join(punch_js)}
      // light flashes on the big cuts
{chr(10).join(flash_js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(f"{P}/index.html", "w").write(index)

# =====================================================================
COMMON_CSS = '''
    #root { position: absolute; inset: 0; overflow: hidden; font-family: "Montserrat", sans-serif; color: #fff; }
    .scrim-top { position: absolute; left: 0; top: 0; width: 1080px; height: 760px;
      background: linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.35) 45%, rgba(0,0,0,0) 100%); opacity: 0; }
    .disp { font-family: "Archivo Black", sans-serif; text-transform: uppercase; letter-spacing: -0.01em; line-height: 0.98;
      text-shadow: 0 6px 28px rgba(0,0,0,0.55); }
    .red { color: #ff1f26; }
    .disp.red { -webkit-text-stroke: 3px rgba(0,0,0,0.75); paint-order: stroke fill; }
'''

def scene(id_, dur, css, body, js):
    return f'''<template>
  <style>{COMMON_CSS}{css}
  </style>
  <div id="root" data-composition-id="{id_}" data-width="1080" data-height="1920" data-duration="{round(dur,3)}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{id_}"] = tl;
  </script>
</template>
'''

# ---------------- HOOK ----------------
hook_dur = S_BUZZ
L3 = VO["vo-hook"][0] + 1.52 - 0.04
hook = scene("hook", hook_dur, '''
    #h-block { position: absolute; left: 0; top: 236px; width: 1080px; text-align: center; }
    #h-tag { display: inline-block; background: #e3141b; color: #fff; font-family: "Archivo Black", sans-serif;
      font-size: 46px; padding: 10px 30px 12px; border-radius: 10px; letter-spacing: 0.04em; transform-origin: 50% 50%; }
    #h-l1 { font-size: 104px; margin-top: 26px; }
    #h-l2 { font-size: 86px; margin-top: 6px; }
    #h-l3wrap { position: absolute; left: 0; top: 640px; width: 1080px; text-align: center; }
    #h-l3 { display: inline-block; font-family: "Montserrat", sans-serif; font-weight: 900; font-size: 62px;
      letter-spacing: 0.02em; text-shadow: 0 4px 22px rgba(0,0,0,0.7); }
    #h-ul { width: 640px; height: 10px; margin: 14px auto 0; background: #e3141b; border-radius: 5px; transform-origin: 0% 50%; }
    #h-arrow { width: 70px; height: 70px; margin: 26px auto 0; }''',
'''    <div class="scrim-top" id="h-scrim"></div>
    <div id="h-block">
      <div id="h-tag">STOP!</div>
      <div id="h-l1" class="disp">Jangan beli</div>
      <div id="h-l2" class="disp red">jam pintar lain</div>
    </div>
    <div id="h-l3wrap">
      <div id="h-l3">SEBELUM MELIHAT INI</div>
      <div id="h-ul"></div>
      <svg id="h-arrow" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
    </div>''',
f'''    tl.fromTo("#h-scrim", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01 }}, 0);
    tl.fromTo("#h-tag", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, 0);
    tl.fromTo("#h-l1", {{ scale: 1.12, opacity: 1 }}, {{ scale: 1, duration: 0.35, ease: "power3.out" }}, 0);
    tl.fromTo("#h-l2", {{ scale: 1.12, opacity: 1 }}, {{ scale: 1, duration: 0.35, ease: "power3.out" }}, 0.04);
    tl.to("#h-block", {{ y: -8, duration: 0.06, ease: "none" }}, {S_HERO - 0.02});
    tl.to("#h-block", {{ y: 0, duration: 0.25, ease: "elastic.out(1,0.4)" }}, {S_HERO + 0.04});
    tl.fromTo("#h-l3", {{ opacity: 0, y: 34 }}, {{ opacity: 1, y: 0, duration: 0.22, ease: "back.out(2)" }}, {round(L3,3)});
    tl.fromTo("#h-ul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {round(L3+0.08,3)});
    tl.fromTo("#h-arrow", {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 8, duration: 0.25, ease: "power2.out" }}, {round(L3+0.2,3)});
    tl.to("#h-arrow", {{ y: 0, duration: 0.2, ease: "sine.inOut", yoyo: true, repeat: 1 }}, {round(L3+0.45,3)});
    tl.to(["#h-block", "#h-l3wrap", "#h-scrim"], {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {round(hook_dur-0.14,3)});''')
open(f"{P}/compositions/hook.html", "w").write(hook)

# ---------------- PROBLEM ----------------
p0 = S_BUZZ
pdur = S_SOLA - S_BUZZ
ICON = {
 "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 "check": '<path d="M20 6L9 17l-5-5"/>',
 "down": '<path d="M12 5v14M5 12l7 7 7-7"/>',
}
def svg(name, size=40, stroke="#fff", sw=2.4):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

NOTIFS = [  # id, icon, color, app, title, body, in(local), out(local), top
    ("n1", "chat", "#25d366", "WHATSAPP", "Kumpulan Kerja", "27 mesej baharu", 0.05, talk(4.80) - p0 - 0.05, 220),
    ("n2", "mail", "#3b82f6", "E-MEL", "Pengurus", "Sila semak laporan segera", 0.28, talk(4.80) - p0 - 0.05, 372),
    ("n3", "phone", "#ef4444", "TELEFON", "Panggilan tidak dijawab", "Pejabat (2)", talk(4.80) - p0, pdur - 0.12, 220),
    ("n4", "chat", "#25d366", "WHATSAPP", "Mak", "Dah makan ke belum?", talk(5.44) - p0, pdur - 0.12, 372),
    ("n5", "cal", "#f59e0b", "KALENDAR", "Mesyuarat", "Bermula dalam 5 minit", talk(5.84) - p0, pdur - 0.12, 524),
]
pcss = '''
    .notif { position: absolute; left: 70px; width: 700px; height: 132px; border-radius: 30px;
      background: rgba(28,28,32,0.78); border: 1.5px solid rgba(255,255,255,0.14);
      box-shadow: 0 18px 40px rgba(0,0,0,0.45); display: flex; align-items: center; padding: 0 26px; gap: 22px; opacity: 0; }
    .notif .ic { width: 78px; height: 78px; border-radius: 20px; display: flex; align-items: center; justify-content: center; flex: none; }
    .notif .tx { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
    .notif .app { font-size: 28px; font-weight: 800; letter-spacing: 0.12em; color: rgba(255,255,255,0.55); }
    .notif .tt { font-size: 32px; font-weight: 800; color: #fff; white-space: nowrap; }
    .notif .bd { font-size: 28px; font-weight: 600; color: rgba(255,255,255,0.8); white-space: nowrap; }
    .notif .now { position: absolute; right: 26px; top: 20px; font-size: 28px; font-weight: 700; color: rgba(255,255,255,0.5); }'''
pbody, pjs = [], []
for nid, ic, col, app, tt, bd, tin, tout, top in NOTIFS:
    pbody.append(f'''    <div class="notif" id="p-{nid}" style="top:{top}px">
      <div class="ic" style="background:{col}">{svg(ic, 44)}</div>
      <div class="tx"><div class="app">{app}</div><div class="tt">{esc(tt)}</div><div class="bd">{esc(bd)}</div></div>
      <div class="now">kini</div>
    </div>''')
    pjs.append(f'    tl.fromTo("#p-{nid}", {{ opacity: 0, x: -80, scale: 0.92 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.26, ease: "back.out(1.8)" }}, {round(tin,3)});')
    pjs.append(f'    tl.to("#p-{nid}", {{ opacity: 0, x: -40, duration: 0.12, ease: "power2.in" }}, {round(tout-0.12,3)});')
    pjs.append(f'    tl.set("#p-{nid}", {{ visibility: "hidden" }}, {round(tout,3)});')
open(f"{P}/compositions/problem.html", "w").write(scene("problem", pdur, pcss, "\n".join(pbody), "\n".join(pjs)))

# ---------------- SOLUTION ----------------
s0 = S_SOLA; sdur = F0 - S_SOLA
tin = sola(2.00) - s0 - 0.02; tout = sola(3.80) - s0 - 0.02
CHIPS = [("c1", "chat", "WhatsApp", solb(4.98) - s0), ("c2", "phone", "Jawab Panggilan", solb(5.56) - s0),
         ("c3", "grid", "&amp; Pelbagai Lagi", solb(6.20) - s0)]
scss = '''
    #s-title { position: absolute; left: 0; top: 236px; width: 1080px; text-align: center; }
    #s-brand { font-weight: 900; font-size: 54px; letter-spacing: 0.42em; padding-left: 0.42em; color: #e3141b;
      text-shadow: 0 4px 18px rgba(0,0,0,0.6); }
    #s-model { font-size: 176px; margin-top: 4px; filter: drop-shadow(0 8px 24px rgba(0,0,0,0.6)); }
    #s-model span { background: linear-gradient(100deg, #d6dade 0%, #ffffff 36%, #ffffff 50%, #eef0f3 64%, #c4c9cf 100%);
      background-size: 240% 100%; background-position: 100% 0; -webkit-background-clip: text; background-clip: text; color: transparent; }
    #s-rule { width: 560px; height: 8px; margin: 18px auto 0; border-radius: 4px; background: #e3141b; transform-origin: 50% 50%; }
    .chip { position: absolute; left: 70px; height: 104px; border-radius: 52px; padding: 0 40px 0 14px; display: flex; align-items: center; gap: 22px;
      background: rgba(14,14,16,0.78); border: 1.5px solid rgba(255,255,255,0.16); box-shadow: 0 14px 36px rgba(0,0,0,0.45); opacity: 0; }
    .chip .ic { width: 76px; height: 76px; border-radius: 38px; background: #e3141b; display: flex; align-items: center; justify-content: center; }
    .chip .lb { font-size: 44px; font-weight: 800; white-space: nowrap; }'''
sbody = ['''    <div class="scrim-top" id="s-scrim"></div>
    <div id="s-title">
      <div id="s-brand">MOHAWK</div>
      <div id="s-model" class="disp"><span>MH-P15</span></div>
      <div id="s-rule"></div>
    </div>''']
sjs = [f'    tl.fromTo("#s-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {round(tin,3)});',
       f'    tl.fromTo("#s-brand", {{ opacity: 0, scaleX: 1.35 }}, {{ opacity: 1, scaleX: 1, duration: 0.45, ease: "power3.out" }}, {round(tin,3)});',
       f'    tl.fromTo("#s-model", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.28, ease: "power4.out" }}, {round(tin+0.04,3)});',
       f'    tl.fromTo("#s-model span", {{ backgroundPosition: "100% 0" }}, {{ backgroundPosition: "0% 0", duration: 1.1, ease: "power2.inOut" }}, {round(tin+0.25,3)});',
       f'    tl.fromTo("#s-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.out" }}, {round(tin+0.12,3)});',
       f'    tl.to(["#s-title", "#s-scrim"], {{ opacity: 0, duration: 0.14, ease: "power2.in" }}, {round(tout-0.14,3)});',
       f'    tl.set("#s-title", {{ visibility: "hidden" }}, {round(tout,3)});']
for i, (cid, ic, lb, at) in enumerate(CHIPS):
    sbody.append(f'    <div class="chip" id="s-{cid}" style="top:{250 + i*128}px"><div class="ic">{svg(ic, 40)}</div><div class="lb">{lb}</div></div>')
    sjs.append(f'    tl.fromTo("#s-{cid}", {{ opacity: 0, x: -70, scale: 0.9 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.24, ease: "back.out(2)" }}, {round(at-0.04,3)});')
    sjs.append(f'    tl.to("#s-{cid}", {{ opacity: 0, x: -30, duration: 0.12, ease: "power2.in" }}, {round(sdur-0.16,3)});')
open(f"{P}/compositions/solution.html", "w").write(scene("solution", sdur, scss, "\n".join(sbody), "\n".join(sjs)))

# ---------------- FEATURES ----------------
fdur = S_CTAA - F0
SPECS = [  # id, value html, counter, label, in, out
    ("f1", '<span id="f1-num">0.00</span>&quot;', ("f1-num", 0.0, 1.43, 2), "SKRIN AMOLED", 0.10, 2.50),
    ("f2", '5ATM', None, "KALIS AIR HINGGA 50 METER", 2.62, 5.10),
    ("f3", '<span id="f3-num">0</span> HARI', ("f3-num", 0, 10, 0), "HAYAT BATERI", 5.22, 7.00),
    ("f4", 'LASAK', None, "TAHAN HENTAKAN", 7.08, fdur - 0.06),
]
fcss = '''
    #f-kicker { position: absolute; left: 70px; top: 226px; display: flex; align-items: center; gap: 18px; opacity: 0; }
    #f-kicker .bar { width: 12px; height: 58px; border-radius: 6px; background: #e3141b; }
    #f-kicker .tx { font-weight: 900; font-size: 46px; letter-spacing: 0.03em; text-shadow: 0 4px 18px rgba(0,0,0,0.7); }
    .spec { position: absolute; left: 70px; top: 1000px; width: 940px; }
    .spec .idx { font-weight: 800; font-size: 28px; letter-spacing: 0.2em; color: #e3141b; opacity: 0; }
    .spec .valwrap { overflow: hidden; height: 168px; margin-top: 6px; }
    .spec .val { font-size: 150px; line-height: 168px; opacity: 0; white-space: nowrap; }
    .spec .acc { width: 150px; height: 10px; border-radius: 5px; background: #e3141b; margin-top: 6px; transform-origin: 0 50%; }
    .spec .lb { font-weight: 800; font-size: 42px; color: #dfe3e8; letter-spacing: 0.04em; margin-top: 16px; opacity: 0;
      text-shadow: 0 3px 14px rgba(0,0,0,0.8); white-space: nowrap; }
    .scrim-bot { position: absolute; left: 0; top: 860px; width: 1080px; height: 560px;
      background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 45%, rgba(0,0,0,0.5) 70%, rgba(0,0,0,0) 100%); opacity: 0; }'''
fbody = ['''    <div class="scrim-bot" id="f-scrim"></div>
    <div id="f-kicker"><div class="bar"></div><div class="tx">KENAPA MOHAWK MH-P15?</div></div>''']
fjs = ['    tl.fromTo("#f-kicker", { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, 0.08);',
       '    tl.fromTo("#f-scrim", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.05);',
       f'    tl.to(["#f-kicker", "#f-scrim"], {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {round(fdur-0.14,3)});']
for i, (sid, val, ctr, lb, a, b) in enumerate(SPECS):
    fbody.append(f'''    <div class="spec" id="f-{sid}">
      <div class="idx" id="f-{sid}-idx">0{i+1} / 04</div>
      <div class="valwrap"><div class="val disp" id="f-{sid}-val">{val}</div></div>
      <div class="acc" id="f-{sid}-acc"></div>
      <div class="lb" id="f-{sid}-lb">{lb}</div>
    </div>''')
    fjs += [f'    tl.fromTo("#f-{sid}-acc", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {a});',
            f'    tl.fromTo("#f-{sid}-idx", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});',
            f'    tl.fromTo("#f-{sid}-val", {{ opacity: 0, y: 150 }}, {{ opacity: 1, y: 0, duration: 0.32, ease: "power4.out" }}, {round(a+0.04,3)});',
            f'    tl.fromTo("#f-{sid}-lb", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, {round(a+0.14,3)});',
            f'    tl.to("#f-{sid}", {{ opacity: 0, y: -20, duration: 0.12, ease: "power2.in" }}, {round(b-0.12,3)});',
            f'    tl.set("#f-{sid}", {{ visibility: "hidden" }}, {round(b,3)});']
    if ctr:
        el, v0, v1, dp = ctr
        fjs.append(f'    {{ const o = {{ v: {v0} }}; const n = document.getElementById("{el}");\n'
                   f'      tl.to(o, {{ v: {v1}, duration: 0.7, ease: "power2.out", onUpdate: () => {{ n.textContent = o.v.toFixed({dp}); }} }}, {round(a+0.04,3)}); }}')
open(f"{P}/compositions/features.html", "w").write(scene("features", fdur, fcss, "\n".join(fbody), "\n".join(fjs)))

# ---------------- CTA ----------------
c0 = S_CTAA; cdur = TOTAL - S_CTAA
stamp_in = ctaa(0.74) - c0; stamp_out = ctaa(1.74) - c0 - 0.05
btn_in = ctab(3.06) - c0 - 0.02; end_in = END_CARD - c0
ccss = '''
    #c-stamp { position: absolute; left: 744px; top: 250px; width: 250px; height: 250px; opacity: 0; }
    #c-stamp .disc { position: absolute; inset: 0; border-radius: 50%; background: #e3141b; border: 8px solid #fff;
      box-shadow: 0 16px 40px rgba(0,0,0,0.5); display: flex; flex-direction: column; align-items: center; justify-content: center; }
    #c-stamp .w { font-family: "Archivo Black", sans-serif; font-size: 29px; margin-top: 0px; }
    #c-btnwrap { position: absolute; left: 0; top: 930px; width: 1080px; display: flex; justify-content: center; }
    #c-btn { display: flex; align-items: center; gap: 22px; padding: 0 52px; height: 132px; border-radius: 66px; background: #e3141b;
      box-shadow: 0 0 0 6px rgba(255,255,255,0.9), 0 20px 50px rgba(227,20,27,0.45); opacity: 0; }
    #c-btn .t { font-family: "Archivo Black", sans-serif; font-size: 50px; white-space: nowrap; }
    #c-end { position: absolute; left: 0; top: 230px; width: 1080px; text-align: center; opacity: 0; }
    #c-brand { font-weight: 900; font-size: 54px; letter-spacing: 0.42em; padding-left: 0.42em; color: #e3141b; text-shadow: 0 4px 18px rgba(0,0,0,0.6); }
    #c-model { font-size: 180px; margin-top: 4px; }
    #c-sub { font-weight: 800; font-size: 38px; letter-spacing: 0.22em; color: #dfe3e8; margin-top: 14px; text-shadow: 0 3px 14px rgba(0,0,0,0.8); }
    #c-get { position: absolute; left: 0; top: 1150px; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; opacity: 0; }
    #c-get .pill { background: #fff; color: #0b0b0c; font-family: "Archivo Black", sans-serif; font-size: 50px; padding: 18px 54px 20px; border-radius: 60px;
      box-shadow: 0 18px 44px rgba(0,0,0,0.5); }
    #c-get .arr { width: 84px; height: 84px; border-radius: 42px; background: #e3141b; display: flex; align-items: center; justify-content: center; }'''
cbody = f'''    <div class="scrim-top" id="c-scrim"></div>
    <div id="c-stamp"><div class="disc">{svg("check", 96, "#fff", 3.4)}<div class="w">BERBALOI!</div></div></div>
    <div id="c-btnwrap"><div id="c-btn">{svg("down", 52, "#fff", 3)}<div class="t">KLIK PAUTAN SEKARANG</div></div></div>
    <div id="c-end">
      <div id="c-brand">MOHAWK</div>
      <div id="c-model" class="disp">MH-P15</div>
      <div id="c-sub">LASAK &bull; PINTAR &bull; TAHAN LAMA</div>
    </div>
    <div id="c-get"><div class="pill">DAPATKAN SEKARANG</div><div class="arr" id="c-arr">{svg("down", 48, "#fff", 3)}</div></div>'''
cjs = f'''    tl.fromTo("#c-stamp", {{ opacity: 0, scale: 2.2, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: -10, duration: 0.3, ease: "back.out(2.2)" }}, {round(stamp_in-0.04,3)});
    tl.to("#c-stamp", {{ opacity: 0, scale: 0.85, duration: 0.14, ease: "power2.in" }}, {round(stamp_out-0.14,3)});
    tl.set("#c-stamp", {{ visibility: "hidden" }}, {round(stamp_out,3)});
    tl.fromTo("#c-btn", {{ opacity: 0, scale: 0.6, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.4)" }}, {round(btn_in,3)});
    tl.to("#c-btn", {{ scale: 1.06, duration: 0.24, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {round(btn_in+0.4,3)});
    tl.to("#c-btn", {{ opacity: 0, scale: 0.9, duration: 0.14, ease: "power2.in" }}, {round(end_in-0.16,3)});
    tl.set("#c-btn", {{ visibility: "hidden" }}, {round(end_in,3)});
    tl.fromTo("#c-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {round(end_in,3)});
    tl.fromTo("#c-end", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power4.out" }}, {round(end_in+0.02,3)});
    tl.fromTo("#c-brand", {{ scaleX: 1.35 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {round(end_in+0.02,3)});
    tl.fromTo("#c-get", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, {round(end_in+0.25,3)});
    tl.to("#c-arr", {{ y: 16, duration: 0.28, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {round(end_in+0.6,3)});'''
open(f"{P}/compositions/cta.html", "w").write(scene("cta", cdur, ccss, cbody, cjs))

# ---------------- CAPTIONS ----------------
kcss = '''
    .cap { position: absolute; left: 0; top: 1150px; width: 1080px; padding: 0 90px; text-align: center; opacity: 0; overflow: visible; }
    .cap .in { display: inline-block; font-weight: 900; font-size: 66px; line-height: 1.12; text-transform: uppercase; letter-spacing: 0.01em;
      color: #fff; -webkit-text-stroke: 3px rgba(0,0,0,0.85); paint-order: stroke fill;
      text-shadow: 0 6px 22px rgba(0,0,0,0.65); }
    .cap .hl { color: #ff2a2f; }'''
kbody, kjs = [], []
prev_b = 0
for i, (txt, a, b, hls) in enumerate(CAPS):
    words = []
    for w in txt.split():
        words.append(f'<span class="hl">{esc(w)}</span>' if w in hls else esc(w))
    kbody.append(f'    <div class="cap" id="cap-{i}"><span class="in">{" ".join(words)}</span></div>')
    a = round(max(a - 0.04, prev_b), 3); b = round(b, 3); prev_b = b
    kjs += [f'    tl.fromTo("#cap-{i}", {{ opacity: 0, y: 16, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "back.out(2.5)" }}, {a});',
            f'    tl.to("#cap-{i}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {round(b-0.08,3)});',
            f'    tl.set("#cap-{i}", {{ opacity: 0, visibility: "hidden" }}, {b});']
open(f"{P}/compositions/captions.html", "w").write(scene("captions", TOTAL, kcss, "\n".join(kbody), "\n".join(kjs)))

json.dump({"total": TOTAL, "shots": SHOTS, "captions": CAPS, "vo": VO, "end_card": END_CARD}, open(f"{P}/timeline.json", "w"), indent=1)
print("TOTAL", TOTAL, "F0", F0, "CTA", S_CTAA, "END", END_CARD)
