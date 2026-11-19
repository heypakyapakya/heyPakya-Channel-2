"""Generates index.html: scene hosts + every sound effect, from one timing table."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "index.html")
W, H, DUR = 1080, 1920, 60

SCENES = [  # id, start, duration
    ("hook", 0, 6), ("def", 6, 11), ("arah", 17, 8),
    ("tambah", 25, 14), ("tolak", 39, 14), ("rumusan", 53, 7),
]
EX = [  # mirrors compositions/world.html
    dict(n0=-3, k=7, tDrop=26.0, tHop=27.2, hop=0.6),
    dict(n0=-5, k=3, tDrop=33.3, tHop=34.3, hop=0.6),
    dict(n0=4, k=7, tDrop=40.0, tHop=41.2, hop=0.6),
    dict(n0=-1, k=4, tDrop=48.4, tHop=49.4, hop=0.6),
]
F = 1 / 30  # one frame: sound lands just after its picture
sfx = []  # (time, file, volume, extra-attrs)
def add(t, f, v=0.8, extra=""): sfx.append((round(t + F, 3), f, v, extra))

# hook
add(0.85, "pop.mp3", 0.7); add(1.33, "pop.mp3", 0.6)
add(2.75, "sparkle.mp3", 0.6)
add(4.75, "whoosh.mp3", 0.8)
# number line build: one tick per pair of tiles landing
for a in range(6):
    add(6.9 + a * 0.2 + 0.3, "key-press.mp3" if a % 2 else "click-soft.mp3", 0.55)
# labels
for t in (10.45, 12.45, 14.25): add(t, "pop.mp3", 0.6)
add(16.85, "whoosh-short.mp3", 0.7)
# staircase: a tick as each column tops out
for ci in range(11):
    add(17.7 + ci * 0.12 + 0.45, "click-soft.mp3" if ci % 2 else "key-press.mp3", 0.45)
add(22.05, "pop.mp3", 0.6); add(22.65, "pop.mp3", 0.6)
add(24.85, "whoosh.mp3", 0.75)
# worked examples
CHIP_POPS = [26.6, 27.3, 33.7, 34.3, 40.6, 41.2, 48.7, 49.3]
for t in CHIP_POPS: add(t + 0.05, "pop.mp3", 0.5)
for i, ex in enumerate(EX):
    add(ex["tDrop"] + 0.42, "pop.mp3", 0.7)
    for j in range(ex["k"]):
        add(ex["tHop"] + ex["hop"] * (j + 1), "click-soft.mp3" if j % 2 else "key-press.mp3", 0.6)
    land = ex["tHop"] + ex["hop"] * ex["k"]
    if i == 2:  # the payoff: answers the opening question
        add(land - 3.47, "riser.mp3", 0.45, ' data-duration="3.6" data-fade-out="0.15"')
        add(land, "impact-bass-1.mp3", 0.6)
        add(land + 0.1, "chime.mp3", 0.7)
    else:
        add(land + 0.1, "sparkle.mp3", 0.55)
add(38.85, "whoosh-short.mp3", 0.7)
add(52.85, "whoosh.mp3", 0.75)
# recap
add(54.05, "pop.mp3", 0.6); add(55.05, "pop.mp3", 0.6); add(55.85, "chime.mp3", 0.7)

sfx.sort()
import subprocess
def dur(f):
    o = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(HERE,"..","assets","audio",f)],capture_output=True,text=True).stdout
    return round(float(o) - 0.01, 3)
DURS = {f: dur(f) for f in {x[1] for x in sfx}}
lanes_end = []  # greedy lanes from 2 upward
placed = []
for t, f, v, x in sfx:
    d = 3.6 if "data-duration" in x else DURS[f]
    d = min(d, DUR - t)
    x = x.replace(' data-duration="3.6"', "")
    for li, e in enumerate(lanes_end):
        if e <= t: lanes_end[li] = t + d; lane = li; break
    else:
        lanes_end.append(t + d); lane = len(lanes_end) - 1
    placed.append((t, f, v, x, round(d, 3), lane + 2))
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
    f'data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" '
    f'data-width="{W}" data-height="{H}" style="z-index:2"></div>'
    for sid, s, d in SCENES)
audio = "\n".join(
    f'      <audio id="sfx-{i:02d}" class="clip" src="assets/audio/{f}" data-start="{t}" '
    f'data-duration="{d}" data-track-index="{ln}" data-volume="{v}"{x}></audio>'
    for i, (t, f, v, x, d, ln) in enumerate(placed))

html = f"""<!doctype html>
<html lang="ms">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/lib/gsap.min.js"></script>
    <script src="assets/lib/three.min.js"></script>
    <style>
      :root {{
        --ground: #1e1650;
        --ink: #ffffff;
        --font-display: "Nunito", sans-serif;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: var(--ground); }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: var(--font-display); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
      <div id="world" data-composition-id="world" data-composition-src="compositions/world.html" data-start="0" data-duration="{DUR}" data-track-index="0" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:1"></div>
{hosts}
{audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(OUT, "w").write(html)
print("wrote", OUT, len(sfx), "sfx")
