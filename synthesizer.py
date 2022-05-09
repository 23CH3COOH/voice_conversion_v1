# -*- coding: utf-8 -*-
import os
from common import m, a, run_command

'''
ピッチ(pitch_path)とメルケプストラム(mcep_path)から音声を合成し
rawファイル(raw_path)に出力する
'''
def synthesize_to_raw(pitch_path, mcep_path, raw_path):
    excite = 'excite -p 80 %s' % pitch_path
    mlsadf = 'mlsadf -m %d -a 0.42 -p 80 %s' % (m, mcep_path)
    clip = 'clips -y -32000 32000'
    x2x = 'x2x +fs > %s' % raw_path
    res = run_command([excite, mlsadf, clip, x2x])

def raw_to_wav(raw_path, wave_path, channel, sampling_rate):
    sox = 'sox -e signed-integer -c %d -b 16 -r %d %s %s'
    res = run_command(sox % (channel, sampling_rate, raw_path, wave_path))

'''
ピッチ(pitch_path)とメルケプストラム(mcep_path)から音声を合成し
wavファイル(wave_path)に出力する
'''
def synthesize_to_wav(pitch_path, mcep_path, wave_path,
                      channel, sampling_rate, delete_temp_raw=True):
    synthesize_to_raw(pitch_path, mcep_path, 'temp.raw')
    raw_to_wav('temp.raw', wave_path, channel, sampling_rate)
    if delete_temp_raw:
        os.remove('temp.raw')
