import sys, torch, soundfile as sf
from transformers import AutoProcessor, MusicgenForConditionalGeneration
torch.manual_seed(int(sys.argv[2]))
p = AutoProcessor.from_pretrained("facebook/musicgen-small")
m = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
torch.set_num_threads(4)
prompt = "energetic modern trap pop instrumental for a tiktok product ad, punchy kick and crisp claps, deep 808 bass, catchy bright synth pluck hook, hi-hat rolls, confident premium vibe, 125 bpm, no vocals"
inp = p(text=[prompt], padding=True, return_tensors="pt")
with torch.no_grad(): a = m.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1550)
sr = m.config.audio_encoder.sampling_rate
sf.write(sys.argv[1], a[0,0].numpy(), sr); print("done", a.shape[-1]/sr)
