#!/usr/bin/env bash
set -e
cd /root/video-gen/towerhouse/audio

# 1. исходники в wav
ffmpeg -y -hide_banner -loglevel error -i moo.ogg -ac 1 -ar 44100 moo_raw.wav
ffmpeg -y -hide_banner -loglevel error -i herd.ogg -t 16 -ac 1 -ar 44100 herd_raw.wav

# 2. обрезаем тишину у мычания
ffmpeg -y -hide_banner -loglevel error -i moo_raw.wav -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1,areverse" moo.wav

# 3. варианты по высоте
ffmpeg -y -hide_banner -loglevel error -i moo.wav -af "asetrate=44100*0.86,atempo=1/0.86,volume=1.0" moo_low.wav
ffmpeg -y -hide_banner -loglevel error -i moo.wav -af "asetrate=44100*1.12,atempo=1/1.12,volume=0.9" moo_hi.wav

# 4. фон: гул телеги + стадо
ffmpeg -y -hide_banner -loglevel error -f lavfi -i "anoisesrc=d=14:c=brown:r=44100" -af "lowpass=f=110,volume=0.055" rumble.wav
ffmpeg -y -hide_banner -loglevel error -i herd_raw.wav -af "lowpass=f=3200,volume=0.10,afade=t=in:d=1.5,afade=t=out:st=12:d=2" herd_bed.wav

# 5. микшуем
ffmpeg -y -hide_banner -loglevel error \
 -i rumble.wav -i herd_bed.wav -i moo.wav -i moo_low.wav -i moo_hi.wav -i moo.wav \
 -filter_complex "\
[2:a]volume=0.95,adelay=1100|1100[m1];\
[3:a]volume=0.75,adelay=4800|4800[m2];\
[4:a]volume=0.85,adelay=8400|8400[m3];\
[5:a]volume=0.55,adelay=11800|11800[m4];\
[0:a][1:a][m1][m2][m3][m4]amix=inputs=6:normalize=0:duration=longest,\
alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
 -map "[a]" -t 14 -ac 1 -ar 44100 mix.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 mix.wav
