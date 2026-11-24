#!/bin/zsh
# Scroll-Video: assets-roh/video/<ROH>.mp4 -> site/assets/vid/<name>.mp4 (+ -m), 30 fps, dichte Keyframes fürs Spulen
# Aufruf: tools/vid.sh V1-buero buero [loop]
cd "${0:A:h}/.."
src=assets-roh/video/$1.mp4; out=site/assets/vid/$2
mkdir -p site/assets/vid
if [[ "$3" == loop ]]; then g=30; else g=3; fi
ffmpeg -v error -y -i $src -an -r 30 -c:v libx264 -preset slow -crf 20 -g $g -keyint_min 1 -pix_fmt yuv420p -movflags +faststart $out.mp4
ffmpeg -v error -y -i $src -an -r 30 -c:v libx264 -preset slow -crf 24 -g $g -keyint_min 1 -pix_fmt yuv420p -movflags +faststart $out-m.mp4
ls -la $out.mp4 $out-m.mp4 | awk '{print $5, $9}'
