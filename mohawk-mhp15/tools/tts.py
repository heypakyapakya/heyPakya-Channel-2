import sys, torch, soundfile as sf
from transformers import VitsModel, AutoTokenizer
out = sys.argv[1]
m = VitsModel.from_pretrained("facebook/mms-tts-zlm"); t = AutoTokenizer.from_pretrained("facebook/mms-tts-zlm")
m.config.speaking_rate = 1.08; m.config.noise_scale = 0.6
lines = {
 "vo-hook": "stop! jangan beli jam pintar lain, sebelum tengok yang ni!",
 "vo-f1": "skrin amoled, satu perpuluhan empat tiga inci,",
 "vo-f2": "kalis air, lima a te em,",
 "vo-f3": "bateri tahan sampai sepuluh hari,",
 "vo-f4": "dan memang lasak gila!",
}
for k, txt in lines.items():
    torch.manual_seed(7)
    with torch.no_grad(): w = m(**t(txt, return_tensors="pt")).waveform[0].numpy()
    sf.write(f"{out}/{k}.raw.wav", w, m.config.sampling_rate); print(k, round(len(w)/m.config.sampling_rate,2))
