# -*- coding: utf-8 -*-
from common import m, a, run_command


'''rawファイル(raw_path)からメルケプストラムを抽出しmcep_pathに出力する'''
def raw_to_mcep(raw_path, mcep_path, binary=False):
    x2x_in = 'x2x +sf %s' % raw_path
    frame = 'frame -l 400 -p 80'
    window = 'window -l 400 -L 512'
    if binary:
        mcep = 'mcep -l 512 -m %d -a %f > %s' % (m, a, mcep_path)
        res = run_command([x2x_in, frame, window, mcep])
    else:
        mcep = 'mcep -l 512 -m %d -a %f' % (m, a)
        x2x_out = 'x2x +fa%d > %s' % (m + 1, mcep_path)
        res = run_command([x2x_in, frame, window, mcep, x2x_out])
    print('returned %d: %s' % (res, raw_path))

'''wavファイル(wave_path)からメルケプストラムを抽出しmcep_pathに出力する'''
def wav_to_mcep(wave_path, mcep_path, binary=False):
    bcut = 'bcut +s -s 22 %s' % wave_path
    x2x_in = 'x2x +sf'
    frame = 'frame -l 400 -p 80'
    window = 'window -l 400 -L 512'
    if binary:
        mcep = 'mcep -l 512 -m %d -a %f > %s' % (m, a, mcep_path)
        res = run_command([bcut, x2x_in, frame, window, mcep])
    else:
        mcep = 'mcep -l 512 -m %d -a %f' % (m, a)
        x2x_out = 'x2x +fa%d > %s' % (m + 1, mcep_path)
        res = run_command([bcut, x2x_in, frame, window, mcep, x2x_out])
    print('returned %d: %s' % (res, wave_path))
