# -*- coding: utf-8 -*-
from common import m, a, run_command


'''wavファイル(wave_path)からメルケプストラムを抽出しmcep_pathに出力する'''
def extract_mcep(wave_path, mcep_path):
    bcut = 'bcut +s -s 22 %s' % wave_path
    x2x_in = 'x2x +sf'
    frame = 'frame -l 400 -p 80'
    window = 'window -l 400 -L 512'
    mcep = 'mcep -l 512 -m %d -a %f' % (m, a)
    x2x_out = 'x2x +fa%d > %s' % (m + 1, mcep_path)
    res = run_command([bcut, x2x_in, frame, window, mcep, x2x_out])
    print('returned %d: %s' % (res, wave_path))
