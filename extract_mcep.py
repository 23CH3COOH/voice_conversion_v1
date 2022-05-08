# -*- coding: utf-8 -*-
import os
from glob import glob
from common import m, a, run_command


def extract_mcep(name_1, name_2):
    if not os.path.exists('mcep/%s/' % name_1):
        os.makedirs('mcep/%s/' % name_1)
    if not os.path.exists('mcep/%s/' % name_2):
        os.makedirs('mcep/%s/' % name_2)
    wav_paths_1 = glob('wav/train/%s/*.wav' % name_1)
    wav_paths_2 = glob('wav/train/%s/*.wav' % name_2)

    for wav_path in wav_paths_1 + wav_paths_2:
        mcep_path = wav_path.replace('wav/train/', 'mcep/').replace('.wav', '.mcep')
        bcut = 'bcut +s -s 22 %s' % wav_path
        x2x_in = 'x2x +sf'
        frame = 'frame -l 400 -p 80'
        window = 'window -l 400 -L 512'
        mcep = 'mcep -l 512 -m %d -a %f' % (m, a)
        x2x_out = 'x2x +fa%d > %s' % (m + 1, mcep_path)
        res = run_command([bcut, x2x_in, frame, window, mcep, x2x_out])
        print('returned %d: %s' % (res, wav_path))
