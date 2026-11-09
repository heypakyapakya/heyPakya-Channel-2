"""5-second teaser score for teaser.html, built from the same instruments as score.py.

Grid: 133.33 BPM (0.45 s/beat). Hits: 1.8 (BRAAM), 2.25, 2.7 (macro punches), 3.15 (reveal).

usage: python3 tools/score_teaser.py assets/audio/teaser_raw.wav
"""

import os
import sys
import wave

import numpy as np

# Load the instrument + DSP definitions from score.py (everything above its arrangement).
_src = open(os.path.join(os.path.dirname(__file__), "score.py")).read()
_lib = _src[: _src.index("# ---------------------------------------------------------------- harmony")]
ns = {"__name__": "score_lib"}
exec(compile(_lib, "score.py", "exec"), ns)

SR, BEAT = ns["SR"], 0.45
DUR = 5.0
N = int(DUR * SR) + SR
ns["N"] = N
ns["rng"] = np.random.default_rng(20261110)
dry, verb = ns["Bus"](), ns["Bus"]()
ns["dry"], ns["verb"] = dry, verb
send = ns["send"]
boom, taiko, snare, tick, braam, pad = (ns[k] for k in ("boom", "taiko", "snare", "tick", "braam", "pad"))
pluck_saw, riser, whoosh, sub_drop, creak = (ns[k] for k in ("pluck_saw", "riser", "whoosh", "sub_drop", "creak"))
hz, lp, hp, bp, saw, env_adsr, t_axis = (ns[k] for k in ("hz", "lp", "hp", "bp", "saw", "env_adsr", "t_axis"))

HIT, P2, P3, REVEAL = 1.8, 2.25, 2.7, 3.15

# 0–1.8: cold-open hit, drone, accelerating ticks, lid creak, riser
send(boom(2.0, 95, 30), 0.0, 0.75, wet=0.5)
n = int(1.9 * SR)
t = t_axis(n)
drone = (np.sin(2 * np.pi * hz(26) * t) * 0.6 + lp(saw(hz(38), n), 280) * 0.5) * env_adsr(n, 0.05, 0.1, 1.0, 0.1)
send(drone, 0.0, 0.3, wet=0.2)
sl, sr = pad([81, 86, 89], 1.9, cutoff=5200, attack=0.6, release=0.2)
dry.add_st(sl * 0.08, sr * 0.08, 0.0)
verb.add_st(sl * 0.12, sr * 0.12, 0.0)
tt = 0.0
step = BEAT / 2
while tt < HIT - 0.05:  # ticks accelerate 8ths -> 32nds
    send(tick(), tt, 0.14, pan=0.3 if int(tt / 0.05) % 2 else -0.3, wet=0.25)
    tt += step
    step = max(BEAT / 8, step * 0.9)
send(whoosh(0.9, 300, 7000), 0.05, 0.3, pan=-0.2, wet=0.4)
send(creak(0.4), 0.45, 0.45, wet=0.3)
send(taiko(0.7, 150, 60), 0.45, 0.5, wet=0.4)
for k, tt in enumerate([0.9, 1.35, 1.575, 1.6875]):
    send(taiko(0.5), tt, 0.4 + 0.08 * k, pan=(-0.3, 0.3)[k % 2], wet=0.35)
send(riser(HIT - 0.85, 400, 10000), 0.8, 0.5, wet=0.5)
send(whoosh(0.8, 150, 5000)[::-1], HIT - 0.8, 0.35, wet=0.3)

# 1.8: BRAAM + impacts; macro punches on the beat with a driving ostinato
send(braam([26, 38, 45, 50], 1.6, 2800, attack=0.02), HIT, 0.85, wet=0.45)
send(boom(1.6, 120, 30), HIT, 1.0, wet=0.5)
send(sub_drop(1.2), HIT, 0.45, wet=0.0)
send(snare(0.5), HIT, 0.45, wet=0.7)
for tt, notes in ((P2, [34, 46, 53]), (P3, [41, 53, 60])):
    send(boom(1.0, 140, 40), tt, 0.75, wet=0.45)
    send(braam(notes, 0.5, 2200, attack=0.015), tt, 0.45, wet=0.4)
for k in range(12):
    ost = [62, 62, 69, 62, 74, 62, 65, 69]
    send(pluck_saw(hz(ost[k % 8] - 12), 0.2, 2800), HIT + k * BEAT / 4, 0.26, pan=-0.3 if k % 2 else 0.3, wet=0.3)
for k in range(8):  # snare roll into the reveal
    send(snare(0.18), P3 + k * BEAT / 8, 0.1 + 0.25 * k / 7, wet=0.3)

# 3.15: final hero braam + chord, beat pulses, ring-out
send(braam([26, 38, 45, 50, 57], 1.85, 3200, attack=0.02), REVEAL, 0.85, wet=0.5)
send(boom(1.85, 120, 28), REVEAL, 1.0, wet=0.6)
send(sub_drop(1.6, 75, 26), REVEAL, 0.45, wet=0.0)
pl, pr = pad([62, 65, 69, 74], 1.85, cutoff=2600, attack=0.15, release=0.4)
dry.add_st(pl * 0.22, pr * 0.22, REVEAL)
verb.add_st(pl * 0.32, pr * 0.32, REVEAL)
for k in range(1, 4):
    send(taiko(0.6), REVEAL + k * BEAT, 0.45 * (1 - k / 5), pan=(-0.2, 0.2)[k % 2], wet=0.4)

# ---- reverb + master (same chain as score.py) ----
from scipy import signal

ir_n = int(2.0 * SR)
ti = t_axis(ir_n)
irs = []
for seed in (1, 2):
    g = np.random.default_rng(seed)
    ir = lp(g.standard_normal(ir_n) * np.exp(-ti * 2.8), 5200)
    ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    irs.append(ir / np.sqrt(np.sum(ir**2)))
L = dry.L + signal.fftconvolve(verb.L, irs[0])[:N] * 0.9
R = dry.R + signal.fftconvolve(verb.R, irs[1])[:N] * 0.9


def phone_eq(x):
    x = hp(hp(x, 42), 42)
    low = lp(x, 160)
    harm = bp(np.tanh(4 * low / (np.abs(low).max() + 1e-9)), 160, 700)
    return x - 0.3 * low + 0.25 * harm * np.abs(low).max() + 0.5 * bp(x, 1500, 5000)


L, R = phone_eq(L), phone_eq(R)
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = np.tanh(L / peak * 1.6) / np.tanh(1.6), np.tanh(R / peak * 1.6) / np.tanh(1.6)
end = int(DUR * SR)
L, R = L[:end], R[:end]
fade = int(0.25 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)
pcm = (np.clip(np.stack([L, R], 1) * 0.89, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1], f"{DUR}s")
