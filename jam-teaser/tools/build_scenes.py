"""Writes compositions/*.html for the teaser. Re-run after editing SCENES; the
output files are plain HyperFrames scenes and can also be edited directly."""
NOTE: this was the first-pass scaffold. The scenes were then edited in place (colour grades via
`hyperframes media-treatment`, end-card layout, kicker backing). Re-running this OVERWRITES those edits.
import json, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "compositions"

# id, image, duration, kicker, big lines, camera (scale from->to, x drift px), text y (top of block)
SCENES = [
  ("hook",  "dial",  0.9, "",                 ["JAM NI", "LAIN MACAM."], (1.22, 1.08, -20), 980),
  ("tough", "tough", 0.6, "TAHAN HENTAKAN",   ["LASAK."],               (1.18, 1.06,  40), 1010),
  ("water", "water", 0.6, "HINGGA 50 METER",  ["KALIS AIR."],           (1.06, 1.20,   0), 1010),
  ("dual",  "dual",  0.6, "ANALOG + DIGITAL", ["SERBA BOLEH."],         (1.20, 1.07, -40), 1010),
  ("wrist", "wrist", 0.5, "DI PERGELANGAN",   ["GAYA PREMIUM."],        (1.10, 1.22,  30), 1050),
  ("face",  "face",  0.7, "PILIHAN RAMAI",    ["WAJIB ADA."],           (1.04, 1.16,   0), 1090),
  ("end",   "hero",  1.1, "SMAEL",            ["BERANI", "BEZA."],      (1.32, 1.06,   0), 900),
]

TPL = """<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #03060c; }}
    #{p}-shake, #{p}-cam {{ position: absolute; inset: 0; }}
    #{p}-img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    #{p}-scrim {{ position: absolute; inset: 0;
      background: linear-gradient(180deg, rgba(3,6,12,.55) 0%, rgba(3,6,12,0) 22%, rgba(3,6,12,0) 42%,
                  rgba(3,6,12,.62) 58%, rgba(3,6,12,.70) 70%, rgba(3,6,12,.25) 86%, rgba(3,6,12,.55) 100%); }}
    #{p}-sweep {{ position: absolute; top: -200px; left: 0; width: 520px; height: 2320px;
      background: linear-gradient(90deg, rgba(150,200,255,0) 0%, rgba(170,215,255,.28) 45%, rgba(255,236,210,.40) 50%, rgba(170,215,255,.28) 55%, rgba(150,200,255,0) 100%);
      mix-blend-mode: screen; }}
    #{p}-text {{ position: absolute; left: 54px; right: 54px; top: {ty}px; text-align: center; }}
    #{p}-kicker {{ font-family: Montserrat, sans-serif; font-weight: 700; font-size: 34px; letter-spacing: .34em;
      color: #e0ab72; text-shadow: 0 2px 18px rgba(0,0,0,.8); margin-bottom: 18px; }}
    #{p}-rule {{ width: 140px; height: 3px; margin: 0 auto 22px; background: linear-gradient(90deg, rgba(224,171,114,0), #e0ab72, rgba(224,171,114,0)); }}
    .{p}-big {{ font-family: "League Gothic", sans-serif; font-size: {fs}px; line-height: 1; letter-spacing: .015em;
      color: #f5f2ec; text-shadow: 0 10px 50px rgba(0,0,0,.75), 0 0 2px rgba(0,0,0,.6); }}
    {extra_css}
  </style>
  <div id="root" data-composition-id="{p}" data-width="1080" data-height="1920">
    <div id="{p}-shake"><div id="{p}-cam">
      <img id="{p}-img" src="assets/img/{img}.jpg" alt=""{img_style} />
    </div></div>
    <div id="{p}-scrim"></div>
    <div id="{p}-sweep" data-layout-ignore></div>
    <div id="{p}-text">
      {kicker_html}
      {big_html}
    </div>
    {extra_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const D = {d};
    // camera push + drift across the whole shot
    tl.fromTo("#{p}-cam", {{ scale: {s0}, x: 0 }}, {{ scale: {s1}, x: {dx}, duration: D, ease: "none" }}, 0);
    // impact shake on the cut
    tl.fromTo("#{p}-shake", {{ x: 16, y: -12, rotation: 0.4 }}, {{ x: 0, y: 0, rotation: 0, duration: 0.22, ease: "elastic.out(1.1, 0.35)" }}, 0);
    // light sweep across the product
    tl.fromTo("#{p}-sweep", {{ x: -700, rotation: 14 }}, {{ x: 1300, rotation: 14, duration: {sweep}, ease: "power2.inOut" }}, {sweep_at});
    {text_tweens}
    {extra_js}
    window.__timelines["{p}"] = tl;
  </script>
</template>
"""

def text_tweens(p, kicker, nbig, first, d):
    js = []
    t = 0.0 if first else 0.04
    if first:  # frame 0 is the thumbnail: the hook line is already on screen, just settling
        for i in range(nbig):
            js.append(f'tl.fromTo("#{p}-big{i}", {{ opacity: 1, scale: 1.12, y: 0 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "expo.out" }}, 0);')
    else:
        for i in range(nbig):
            js.append(f'tl.fromTo("#{p}-big{i}", {{ opacity: 0, scale: 1.55, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.2, ease: "expo.out" }}, {t + 0.07*i:.2f});')
    if kicker:
        js.append(f'tl.fromTo("#{p}-kicker", {{ opacity: 0, scale: 1.25, y: -10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {0.0 if first else 0.1});')
        js.append(f'tl.fromTo("#{p}-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {0.0 if first else 0.12});')
    # slow hold drift so text never sits dead
    js.append(f'tl.fromTo("#{p}-text", {{ scale: 1 }}, {{ scale: 1.035, duration: {d}, ease: "none" }}, 0);')
    return "\n    ".join(js)

for idx, (p, img, d, kicker, big, (s0, s1, dx), ty) in enumerate(SCENES):
    first = idx == 0
    fs = 230 if len(big) > 1 else 210
    kicker_html = (f'<div id="{p}-kicker">{kicker}</div><div id="{p}-rule"></div>' if kicker else "")
    big_html = "\n      ".join(f'<div id="{p}-big{i}" class="{p}-big">{w}</div>' for i, w in enumerate(big))
    extra_css = extra_html = extra_js = ""
    if p == "hook":
        extra_css = """#hook-flare { position: absolute; left: -300px; top: 760px; width: 1680px; height: 10px; border-radius: 50%;
      background: radial-gradient(ellipse at center, rgba(235,245,255,.95) 0%, rgba(90,160,255,.65) 25%, rgba(40,90,255,0) 70%);
      mix-blend-mode: screen; }"""
        extra_html = '<div id="hook-flare" data-layout-ignore></div>'
        extra_js = """tl.fromTo("#hook-flare", { opacity: 0.0, scaleY: 1, x: -260 }, { opacity: 1, scaleY: 3.2, x: 220, duration: 0.55, ease: "power2.out" }, 0.05);
    tl.to("#hook-flare", { opacity: 0, duration: 0.25, ease: "power1.in" }, 0.6);
    // reveal lighting: the dark macro opens up
    tl.fromTo("#hook-img", { "--hf-color-grading-exposure": -0.35 }, { "--hf-color-grading-exposure": 0.28, duration: 0.6, ease: "power2.out" }, 0);"""
    if p == "end":
        extra_css = """#end-tag { position: absolute; left: 0; right: 0; top: 1250px; text-align: center; }
    #end-pill { display: inline-block; padding: 14px 40px; border: 2px solid rgba(224,171,114,.9); border-radius: 999px;
      font-family: Montserrat, sans-serif; font-weight: 700; font-size: 30px; letter-spacing: .4em; color: #f5f2ec;
      background: rgba(3,6,12,.45); }
    #end-glow { position: absolute; left: 140px; top: 520px; width: 800px; height: 800px; border-radius: 50%;
      background: radial-gradient(circle, rgba(80,150,255,.45) 0%, rgba(80,150,255,0) 65%); mix-blend-mode: screen; }"""
        extra_html = '<div id="end-glow" data-layout-ignore></div>\n    <div id="end-tag"><span id="end-pill">SEGERA</span></div>'
        extra_js = """tl.fromTo("#end-glow", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1.25, duration: 0.5, ease: "expo.out" }, 0.03);
    tl.to("#end-glow", { opacity: 0.55, duration: 0.5, ease: "sine.inOut" }, 0.53);
    tl.fromTo("#end-pill", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.38);
"""
    else:
        # exit punch: zoom into the cut
        extra_js += f'\n    tl.fromTo("#{p}-shake", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.09, ease: "power2.in" }}, {d - 0.09:.2f});'
    html = TPL.format(p=p, img=img, d=d, s0=s0, s1=s1, dx=dx, ty=ty, fs=fs,
                      sweep=0.5 if d < 1 else 0.7, sweep_at=0.05 if not first else 0.12,
                      kicker_html=kicker_html, img_style=(' style="--hf-color-grading-exposure: -0.35"' if first else ""), big_html=big_html,
                      text_tweens=text_tweens(p, kicker, len(big), first, d),
                      extra_css=extra_css, extra_html=extra_html, extra_js=extra_js)
    (OUT / f"{p}.html").write_text(html)
    print("wrote", p, d)
