# -*- coding: utf-8 -*-
import os
from audio_file_converter import raw_to_wav
from common import m, a, run_command

'''
ピッチ(pitch_path)とメルケプストラム(mcep_path)から音声を合成し
rawファイル(raw_path)に出力する
'''
def synthesize_to_raw(pitch_path, mcep_path, raw_path):
    excite = 'excite -p 80 %s' % pitch_path
    mlsadf = 'mlsadf -m %d -a %f -p 80 %s' % (m, a, mcep_path)
    clip = 'clips -y -32000 32000'
    x2x = 'x2x +fs > %s' % raw_path
    res = run_command([excite, mlsadf, clip, x2x])

'''
ピッチ(pitch_path)とメルケプストラム(mcep_path)から音声を合成し
wavファイル(wave_path)に出力する
'''
def synthesize_to_wav(pitch_path, mcep_path, wave_path,
                      channels, frame_rate, delete_temp_raw=True):
    synthesize_to_raw(pitch_path, mcep_path, 'temp.raw')
    raw_to_wav('temp.raw', wave_path, channels, frame_rate)
    if delete_temp_raw:
        os.remove('temp.raw')
