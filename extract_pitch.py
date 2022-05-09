# -*- coding: utf-8 -*-
from common import m, a, run_command


'''rawファイル(raw_path)からピッチを抽出しpitch_pathに出力する'''
def raw_to_pitch(raw_path, pitch_path):
    x2x_in = 'x2x +sf %s' % raw_path
    pitch = 'pitch -a 1 -s 16 -p 80 > %s' % pitch_path
    res = run_command([x2x_in, pitch])
    print('returned %d: %s' % (res, raw_path))

'''wavファイル(wave_path)からピッチを抽出しpitch_pathに出力する'''
def wav_to_pitch(wave_path, pitch_path):
    bcut = 'bcut +s -s 22 %s' % wave_path
    x2x_in = 'x2x +sf'
    pitch = 'pitch -a 1 -s 16 -p 80 > %s' % pitch_path
    res = run_command([bcut, x2x_in, pitch])
    print('returned %d: %s' % (res, wave_path))
