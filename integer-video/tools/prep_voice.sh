#!/usr/bin/env bash
# Speeds each ElevenLabs line up 12% (pitch kept), trims lead/tail silence, levels it.
set -euo pipefail
cd "$(dirname "$0")/../assets/voice"
for f in l*.mp3; do
  n=${f%.mp3}; o="v${n#l}.wav"
  ffmpeg -v error -y -i "$f" -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.12,loudnorm=I=-16:TP=-1.5:LRA=7" -ar 48000 -ac 1 "$o"
done
for f in v*.wav; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"; done
