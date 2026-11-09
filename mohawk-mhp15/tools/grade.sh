#!/bin/bash
# Applies the colour grade + relight to every footage clip (re-run after build.py).
cd "$1"
TALK='{"preset":"skin-soft","intensity":0.62,"adjust":{"exposure":0.1,"contrast":0.07,"highlights":-0.1,"shadows":0.14,"whites":0.03,"blacks":-0.03,"temperature":0.03,"vibrance":0.05,"saturation":0.03},"wheels":{"shadows":{"hue":205,"amount":0.07,"level":0},"highlights":{"hue":35,"amount":0.05,"level":0}},"details":{"vignette":0.06}}'
BROLL='{"intensity":0.75,"adjust":{"exposure":0.05,"contrast":0.09,"highlights":-0.08,"shadows":0.1,"whites":0.04,"blacks":-0.03,"vibrance":0.05,"saturation":0.04},"wheels":{"shadows":{"hue":205,"amount":0.05,"level":0}},"details":{"vignette":0.04}}'
npx hyperframes media-treatment --project . --file index.html --selector "video.talk" --grading "$TALK" --apply --json 2>/dev/null | python3 -I -c "import sys,json; d=json.load(sys.stdin); print('talk', d.get('ok'), d.get('count'))"
npx hyperframes media-treatment --project . --file index.html --selector "video.broll" --grading "$BROLL" --apply --json 2>/dev/null | python3 -I -c "import sys,json; d=json.load(sys.stdin); print('broll', d.get('ok'), d.get('count'))"
