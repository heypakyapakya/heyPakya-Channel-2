"""Original cinematic-epic teaser score, synthesized (5.0 s, D minor).
Cut points: 0.0 hook | 0.9 | 1.5 | 2.1 | 2.7 | 3.2 | 3.9 end-card slam."""
import numpy as np, wave, sys
SR = 48000; DUR = 5.0; N = int(SR*DUR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)
t_all = np.arange(N)/SR

def onepole_lp(x, fc):
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2*np.pi*fc/SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1-a[i])*x[i] + a[i]*s; y[i] = s
    return y
def lp(x, fc, n=2):
    for _ in range(n): x = onepole_lp(x, fc)
    return x
def hp(x, fc): return x - lp(x, fc, 1)
def saw(f, t, ph=0.0): return 2*((f*t+ph) % 1.0) - 1
def add(sig, start, gl=1.0, gr=1.0):
    i = int(start*SR); n = min(len(sig), N-i)
    if n <= 0: return
    L[i:i+n] += sig[:n]*gl; R[i:i+n] += sig[:n]*gr

def braam(dur, gain, open_t=0.12):
    t = np.arange(int(dur*SR))/SR
    notes = [36.71, 73.42, 110.0, 146.83, 174.61, 220.0]
    out = np.zeros_like(t)
    for k, f in enumerate(notes):
        for d in (-0.004, 0.0, 0.005):
            out += saw(f*(1+d), t, rng.random()) / (1 + 0.35*k)
    env = np.minimum(t/0.015, 1) * np.exp(-t/(dur*0.55))
    cutoff = 180 + 2600*np.exp(-np.maximum(t-open_t, 0)/0.35) * np.minimum(t/open_t, 1)
    out = lp(out, cutoff, 2)
    out = np.tanh(out*1.8) * env
    return out*gain

def taiko(gain, f0=150, f1=48):
    t = np.arange(int(0.9*SR))/SR
    f = f1 + (f0-f1)*np.exp(-t/0.05)
    body = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.28)
    skin = hp(rng.standard_normal(len(t)), 700) * np.exp(-t/0.025) * 0.5
    return np.tanh((body + skin)*1.6) * gain

def sub_boom(gain, dur=1.1):
    t = np.arange(int(dur*SR))/SR
    f = 30 + 45*np.exp(-t/0.12)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.45) * gain

# 1. Low drone bed (D1/A1), swelling to the slam, harmonics so it reads on phones
drone = (saw(36.71, t_all) + 0.7*saw(55.0, t_all) + 0.4*saw(73.42*1.003, t_all))
drone = lp(drone, 420, 2)
swell = np.interp(t_all, [0, 0.4, 3.85, 3.9, 4.0, 5.0], [0.0, 0.18, 0.42, 0.0, 0.5, 0.0])
add(drone*swell, 0.0)

# 2. String ostinato 0.9 -> 3.88 (D minor 16ths), rising intensity
pattern = [146.83, 146.83, 174.61, 146.83, 220.0, 146.83, 174.61, 196.0]
step = 1/8.5
t0 = 0.9; k = 0
while t0 < 3.86:
    f = pattern[k % 8]
    n = int(step*0.95*SR); t = np.arange(n)/SR
    prog = (t0-0.9)/3.0
    note = (saw(f*0.998, t) + saw(f*1.003, t) + 0.5*saw(f*2, t))
    note = lp(note, 900 + 3200*prog, 1) * np.minimum(t/0.006, 1) * np.exp(-t/0.09)
    acc = 1.0 if k % 4 == 0 else 0.7
    pan = 0.75 if k % 2 else 1.0
    add(note*(0.10 + 0.16*prog)*acc, t0, pan, 1.75-pan)
    t0 += step; k += 1

# 3. Hits on every cut
add(braam(0.95, 0.55), 0.0); add(sub_boom(0.8), 0.0); add(taiko(0.55), 0.0)
for c in (0.9, 1.5, 2.1, 2.7, 3.2):
    add(taiko(0.42 + 0.05*(c-0.9)), c, 1.0, 0.9)
    add(taiko(0.22, 220, 90), c + step*2, 0.8, 1.0)   # answering flam

# 4. Riser 3.2 -> 3.88, then 1-frame breath of silence before the slam
rt = np.arange(int(0.68*SR))/SR; prog = rt/0.68
noise = rng.standard_normal(len(rt))
riser = hp(noise, 300 + 5000*prog**2) * prog**2.2 * 0.35
riser += np.sin(2*np.pi*np.cumsum(220 + 1400*prog**2)/SR) * prog**3 * 0.12
add(riser, 3.2)

# 5. End-card slam at 3.9
add(braam(1.1, 0.75, 0.08), 3.9); add(sub_boom(1.0, 1.1), 3.9); add(taiko(0.7), 3.9)
ct = np.arange(int(1.1*SR))/SR
crash = hp(rng.standard_normal(len(ct)), 2500) * np.exp(-ct/0.5) * 0.12
add(crash, 3.9)

# 6. Hall reverb (FFT convolution, stereo decorrelated IR)
def reverb(x, seed):
    r = np.random.default_rng(seed); n = int(1.8*SR); t = np.arange(n)/SR
    ir = r.standard_normal(n) * np.exp(-t/0.42); ir[:int(0.02*SR)] = 0
    ir = lp(ir, 5000, 1); ir /= np.sqrt(np.sum(ir**2))
    m = 1 << int(np.ceil(np.log2(len(x)+n)))
    return np.fft.irfft(np.fft.rfft(x, m)*np.fft.rfft(ir, m), m)[:len(x)]
L2 = L + 0.28*reverb(L, 1); R2 = R + 0.28*reverb(R, 2)
# tail fade + soft clip + normalize to -1 dBFS sample peak
fade = np.interp(t_all, [0, 4.7, 5.0], [1, 1, 0]); fade[:int(0.004*SR)] = np.linspace(0,1,int(0.004*SR))
st = np.stack([L2, R2], 1) * fade[:, None]
st = np.tanh(st/np.max(np.abs(st))*1.3)
st *= 10**(-1.5/20)/np.max(np.abs(st))
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype('<i2').tobytes())
print('ok', sys.argv[1])
