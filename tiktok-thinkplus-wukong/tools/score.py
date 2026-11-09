"""Cinematic-epic score + sound design for the thinkplus WuKong TikTok ad.

Fully synthesized (numpy/scipy), deterministic, royalty-free.
Grid: 133.33 BPM (0.45 s/beat), 4-beat bars of 1.8 s, 12 bars = 21.6 s.
Every visual cut in index.html sits on a bar line, so hits land on the edit.

usage: python3 tools/score.py assets/audio/score.wav
"""

import sys
import wave

import numpy as np
from scipy import signal

SR = 48000
BEAT = 0.45
BAR = 4 * BEAT
DUR = 21.6
N = int(DUR * SR) + SR  # +1 s tail room, trimmed at the end
rng = np.random.default_rng(20261109)

# Edit points (seconds) — must match index.html
LIGHT_SWEEP = 1.1
LID_CRACK = 4.2
LID_OPEN = 4.9
REVEAL = 7.2
DETAIL_CUTS = [10.8, 12.6, 14.4, 16.2]
CTA = 18.0


def t_axis(n):
    return np.arange(n) / SR


def hz(note):
    """MIDI note -> Hz."""
    return 440.0 * 2 ** ((note - 69) / 12)


def saw(freq, n, phase=0.0):
    ph = (np.cumsum(np.broadcast_to(freq, (n,)) / SR) + phase) % 1.0
    return 2 * ph - 1


def env_adsr(n, a, d, s, r, sustain_len=None):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    s_n = n - a_n - d_n - r_n if sustain_len is None else int(sustain_len * SR)
    s_n = max(s_n, 0)
    e = np.concatenate(
        [
            np.linspace(0, 1, max(a_n, 1)),
            np.linspace(1, s, max(d_n, 1)),
            np.full(s_n, s),
            np.linspace(s, 0, max(r_n, 1)),
        ]
    )
    return np.pad(e, (0, max(0, n - len(e))))[:n]


def lp(x, cutoff):
    b, a = signal.butter(2, min(cutoff, SR / 2 - 100) / (SR / 2), "low")
    return signal.lfilter(b, a, x)


def hp(x, cutoff):
    b, a = signal.butter(2, cutoff / (SR / 2), "high")
    return signal.lfilter(b, a, x)


def bp(x, lo, hi):
    b, a = signal.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band")
    return signal.lfilter(b, a, x)


def sweep_lp(x, cut_curve, block=256):
    """Time-varying 2-pole lowpass; cut_curve has one value per sample."""
    out = np.zeros_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        c = float(np.clip(cut_curve[min(i, len(cut_curve) - 1)], 30, SR / 2 - 200))
        b, a = signal.butter(2, c / (SR / 2), "low")
        out[i : i + block], zi = signal.lfilter(b, a, x[i : i + block], zi=zi)
    return out


def sweep_hp(x, cut_curve, block=256):
    out = np.zeros_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        c = float(np.clip(cut_curve[min(i, len(cut_curve) - 1)], 30, SR / 2 - 200))
        b, a = signal.butter(2, c / (SR / 2), "high")
        out[i : i + block], zi = signal.lfilter(b, a, x[i : i + block], zi=zi)
    return out


class Bus:
    def __init__(self):
        self.L = np.zeros(N)
        self.R = np.zeros(N)

    def add(self, x, at, gain=1.0, pan=0.0):
        i = int(at * SR)
        if i >= N:
            return
        x = x[: N - i]
        gl = gain * np.cos((pan + 1) * np.pi / 4) * np.sqrt(2)
        gr = gain * np.sin((pan + 1) * np.pi / 4) * np.sqrt(2)
        self.L[i : i + len(x)] += x * gl
        self.R[i : i + len(x)] += x * gr

    def add_st(self, l, r, at, gain=1.0):
        i = int(at * SR)
        n = min(len(l), N - i)
        self.L[i : i + n] += l[:n] * gain
        self.R[i : i + n] += r[:n] * gain


dry = Bus()  # direct
verb = Bus()  # reverb send


def send(x, at, gain, pan=0.0, wet=0.3):
    dry.add(x, at, gain, pan)
    verb.add(x, at, gain * wet, pan)


# ---------------------------------------------------------------- instruments
def boom(length=2.2, f0=110, f1=32):
    n = int(length * SR)
    t = t_axis(n)
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 90) * 0.5
    crunch = lp(rng.standard_normal(n), 900) * np.exp(-t * 7) * 0.6
    return np.tanh(1.8 * (body + click + crunch)) * 0.9


def taiko(length=0.9, f0=170, f1=62):
    n = int(length * SR)
    t = t_axis(n)
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    skin = bp(rng.standard_normal(n), 120, 1400) * np.exp(-t * 22) * 0.7
    return np.tanh(1.6 * (body + skin))


def snare(length=0.35):
    n = int(length * SR)
    t = t_axis(n)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    noise = bp(rng.standard_normal(n), 900, 7000) * np.exp(-t * 14)
    return 0.5 * tone + 0.8 * noise


def tick(length=0.05):
    n = int(length * SR)
    t = t_axis(n)
    return bp(rng.standard_normal(n), 3000, 9000) * np.exp(-t * 160)


def braam(notes, length=3.0, bright=2600, attack=0.04):
    n = int(length * SR)
    t = t_axis(n)
    x = np.zeros(n)
    for k, m in enumerate(notes):
        for det in (-0.004, 0.0, 0.0045):
            x += saw(hz(m) * (1 + det), n, phase=(k * 0.13 + det * 50) % 1)
    x /= len(notes) * 3
    cut = 180 + (bright - 180) * np.exp(-((t - 0.12) ** 2) / 0.06) + 420 * np.exp(-t * 0.8)
    cut[t < 0.12] = 180 + (bright - 180) * (t[t < 0.12] / 0.12)
    y = sweep_lp(x, cut)
    y = np.tanh(3.0 * y)
    return y * env_adsr(n, attack, 0.6, 0.55, length - attack - 0.6 - 0.05)


def pad(notes, length, cutoff=1400, attack=0.8, release=0.8):
    n = int(length * SR)
    t = t_axis(n)
    l = np.zeros(n)
    r = np.zeros(n)
    for k, m in enumerate(notes):
        vib = 1 + 0.003 * np.sin(2 * np.pi * (5.1 + k * 0.3) * t)
        l += saw(hz(m) * vib * 0.998, n, phase=k * 0.21)
        r += saw(hz(m) * vib * 1.002, n, phase=k * 0.37)
    e = env_adsr(n, attack, 0.2, 1.0, release)
    out = []
    for ch in (l, r):
        ch = lp(ch / len(notes), cutoff)
        ch = ch + 0.6 * bp(ch, 600, 1100) + 0.4 * bp(ch, 1000, 1500)  # "ah" formant
        out.append(ch * e)
    return out


def pluck_saw(freq, length, cutoff=2200):
    n = int(length * SR)
    t = t_axis(n)
    x = saw(freq * 0.999, n) + saw(freq * 1.001, n, 0.3)
    x = lp(x * 0.5, cutoff)
    return x * np.exp(-t * 9) * np.minimum(1, t / 0.004)


def riser(length, f_lo=300, f_hi=9000):
    n = int(length * SR)
    t = t_axis(n) / length
    noise = rng.standard_normal(n)
    y = sweep_hp(noise, f_lo * (f_hi / f_lo) ** (t ** 1.6))
    tone_f = 110 * 2 ** (t * 3)  # rising 3 octaves
    tone = np.sin(2 * np.pi * np.cumsum(tone_f) / SR) * 0.35 + saw(tone_f * 2, n) * 0.08
    return (y * 0.55 + tone) * (t ** 2.2)


def whoosh(length=1.2, lo=200, hi=6000):
    n = int(length * SR)
    t = t_axis(n) / length
    bell = np.sin(np.pi * t) ** 3
    curve = lo * (hi / lo) ** np.sin(np.pi * t * 0.5)
    return sweep_lp(rng.standard_normal(n), curve) * bell


def sub_drop(length=1.8, f0=70, f1=28):
    n = int(length * SR)
    t = t_axis(n)
    f = f1 + (f0 - f1) * np.exp(-t * 2.2)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)


def creak(length=0.5):
    n = int(length * SR)
    t = t_axis(n)
    pulses = (np.sin(2 * np.pi * (38 + 18 * t) * t) > 0.97).astype(float)
    return bp(pulses + 0.15 * rng.standard_normal(n), 300, 2500) * np.exp(-t * 4)


# ---------------------------------------------------------------- harmony
D2, F2, G2, A2, Bb1, C2 = 38, 41, 43, 45, 34, 36
CHORDS = {  # i – VI – III – VII in D minor
    "Dm": [38, 50, 57, 62, 65],
    "Bb": [34, 46, 53, 58, 62],
    "F": [41, 53, 57, 60, 65],
    "C": [36, 48, 55, 60, 64],
}
OST = {  # 16th-note ostinato figure per chord (MIDI)
    "Dm": [62, 62, 69, 62, 74, 62, 65, 69],
    "Bb": [58, 58, 65, 58, 70, 58, 62, 65],
    "F": [60, 60, 65, 60, 72, 60, 69, 65],
    "C": [60, 60, 67, 60, 72, 60, 64, 67],
}

# ---------------------------------------------------------------- arrangement
# INTRO 0–3.6 : drone, shimmer, clock ticks
drone_n = int(7.2 * SR)
t = t_axis(drone_n)
drone = (np.sin(2 * np.pi * hz(26) * t) * 0.6 + lp(saw(hz(38), drone_n), 260) * 0.5)
drone *= env_adsr(drone_n, 1.2, 0.1, 1.0, 0.4) * (0.6 + 0.4 * np.minimum(1, t / 7))
send(drone, 0.0, 0.32, wet=0.2)
shim_l, shim_r = pad([81, 86, 89], 7.0, cutoff=5200, attack=2.5, release=1.0)
dry.add_st(shim_l * 0.08, shim_r * 0.08, 0.0)
verb.add_st(shim_l * 0.12, shim_r * 0.12, 0.0)
send(boom(2.6, 90, 30), 0.0, 0.8, wet=0.5)  # cold-open hit under the hook
for k in range(int(7.2 / (BEAT / 2))):  # 8th-note clock
    send(tick(), k * BEAT / 2, 0.10 if k % 2 else 0.16, pan=0.35 if k % 2 else -0.35, wet=0.25)
send(whoosh(1.3, 300, 7000), LIGHT_SWEEP, 0.35, pan=-0.2, wet=0.4)

# TENSION 3.6–7.2 : filtered ostinato rising, toms, lid FX, riser
for k in range(16):
    tt = 3.6 + k * BEAT / 2
    cut = 600 + 2400 * (k / 15)
    send(pluck_saw(hz(OST["Dm"][k % 8] - 12), 0.3, cut), tt, 0.3, pan=-0.25 if k % 2 else 0.25, wet=0.35)
send(creak(0.45), LID_CRACK, 0.45, pan=0.1, wet=0.3)
send(taiko(0.8, 150, 60), LID_CRACK, 0.5, wet=0.4)
for k, tt in enumerate([5.4, 5.85, 6.3, 6.525, 6.75, 6.8625, 6.975]):
    send(taiko(0.6), tt, 0.35 + 0.08 * k, pan=(-0.3, 0.3)[k % 2], wet=0.35)
r = riser(REVEAL - LID_OPEN - 0.12)
send(r, LID_OPEN, 0.5, wet=0.5)
send(whoosh(1.6, 150, 5000)[::-1], REVEAL - 1.6, 0.35, wet=0.3)  # reverse-whoosh suck-in

# REVEAL 7.2 : BRAAM + boom + sub drop
send(braam([26, 38, 45, 50], 3.4, 2800), REVEAL, 0.85, wet=0.45)
send(boom(2.8, 120, 30), REVEAL, 1.0, wet=0.5)
send(sub_drop(2.0), REVEAL, 0.45, wet=0.0)
send(snare(0.6), REVEAL, 0.45, wet=0.7)

# EPIC 7.2–18.0 : progression Dm Bb F C Dm Bb, taiko groove, ostinato, choir
prog = ["Dm", "Bb", "Dm", "Bb", "F", "C"]  # bars starting at 7.2 + i*1.8
for i, ch in enumerate(prog):
    b0 = REVEAL + i * BAR
    pl, pr = pad(CHORDS[ch][1:], BAR + 0.4, cutoff=1500 + 150 * i, attack=0.25, release=0.4)
    dry.add_st(pl * 0.24, pr * 0.24, b0)
    verb.add_st(pl * 0.22, pr * 0.22, b0)
    send(lp(saw(hz(CHORDS[ch][0]), int((BAR + 0.1) * SR)), 300) * env_adsr(int((BAR + 0.1) * SR), 0.02, 0.3, 0.8, 0.1), b0, 0.35, wet=0.1)
    # ostinato 16ths, up an octave in the last two bars
    shift = 12 if i >= 4 else 0
    for k in range(16):
        tt = b0 + k * BEAT / 4
        send(pluck_saw(hz(OST[ch][k % 8] - 12 + shift), 0.22, 2600 + 300 * i), tt, 0.26, pan=-0.3 if k % 2 else 0.3, wet=0.3)
    # taiko pattern (1, 2&, 3, 4 + pickup) — busier from bar 3
    pat = [0, 1.5, 2, 3] if i < 2 else [0, 0.75, 1.5, 2, 2.5, 3, 3.5]
    for p in pat:
        send(taiko(), b0 + p * BEAT, 0.55 if p in (0, 2) else 0.38, pan=(-0.2 if p % 1 else 0.2), wet=0.35)
    send(snare(), b0 + BEAT, 0.28, wet=0.5)
    send(snare(), b0 + 3 * BEAT, 0.28, wet=0.5)

# hits on every detail cut (bar lines) + mini braam
for k, tt in enumerate(DETAIL_CUTS):
    send(boom(1.4, 140, 40), tt, 0.75, wet=0.45)
    send(braam([38, 50, 57] if k % 2 == 0 else [34, 46, 53], 1.2, 2200, attack=0.02), tt, 0.4, wet=0.4)
    send(whoosh(0.45, 400, 8000), tt - 0.3, 0.3, pan=(-0.5, 0.5)[k % 2], wet=0.2)

# BUILD into CTA: snare roll over the last bar + riser
b_build = CTA - BAR
for k in range(16):
    send(snare(0.2), b_build + k * BEAT / 4, 0.1 + 0.3 * (k / 15), pan=(-0.15, 0.15)[k % 2], wet=0.3)
send(riser(BAR - 0.05, 500, 12000), b_build, 0.4, wet=0.4)

# CTA 18.0: final braam on Dm, boom, then sustained heroic chord + pulse hits
send(braam([26, 38, 45, 50, 57], 3.6, 3200), CTA, 0.85, wet=0.5)
send(boom(3.0, 120, 28), CTA, 1.0, wet=0.6)
send(sub_drop(2.4, 75, 26), CTA, 0.45, wet=0.0)
pl, pr = pad([62, 65, 69, 74], 3.6, cutoff=2600, attack=0.4, release=1.2)
dry.add_st(pl * 0.2, pr * 0.2, CTA)
verb.add_st(pl * 0.3, pr * 0.3, CTA)
for k in range(1, 8):  # pulse on beats, decaying
    send(taiko(0.7), CTA + k * BEAT, 0.45 * (1 - k / 9), pan=(-0.2, 0.2)[k % 2], wet=0.4)
send(boom(1.8, 90, 30), CTA + 3.15, 0.55, wet=0.6)  # last sting before fade

# ---------------------------------------------------------------- reverb + master
ir_n = int(2.8 * SR)
ti = t_axis(ir_n)
irs = []
for seed in (1, 2):
    g = np.random.default_rng(seed)
    ir = g.standard_normal(ir_n) * np.exp(-ti * 2.4)
    ir = lp(ir, 5200)
    ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    irs.append(ir / np.sqrt(np.sum(ir**2)))
wl = signal.fftconvolve(verb.L, irs[0])[:N]
wr = signal.fftconvolve(verb.R, irs[1])[:N]

L = dry.L + wl * 0.9
R = dry.R + wr * 0.9
# phone-speaker balance: trim deep sub, lift the 1.5-5 kHz presence band
def phone_eq(x):
    x = hp(hp(x, 42), 42)  # 4th-order low cut
    low = lp(x, 160)
    harm = bp(np.tanh(4 * low / (np.abs(low).max() + 1e-9)), 160, 700)  # bass harmonics phones can play
    return x - 0.3 * low + 0.25 * harm * np.abs(low).max() + 0.5 * bp(x, 1500, 5000)


L, R = phone_eq(L), phone_eq(R)
# soft limiter
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 1.6, R / peak * 1.6
L, R = np.tanh(L) / np.tanh(1.6), np.tanh(R) / np.tanh(1.6)

# trim + short fade at the very end
end = int(DUR * SR)
L, R = L[:end], R[:end]
fade = int(0.35 * SR)
L[-fade:] *= np.linspace(1, 0, fade)
R[-fade:] *= np.linspace(1, 0, fade)

out = np.stack([L, R], axis=1) * 0.89
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1], f"{DUR}s")
