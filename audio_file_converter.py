# -*- coding: utf-8 -*-
from common import run_command


def wav_to_raw(wave_path, raw_path):
    res = run_command('sox %s %s' % (wave_path, raw_path))

def raw_to_wav(raw_path, wave_path, channels, frame_rate):
    sox = 'sox -e signed-integer -c %d -b 16 -r %d %s %s'
    res = run_command(sox % (channels, frame_rate, raw_path, wave_path))


if __name__ == '__main__':
    raw_path = 'resynthesis_test/aoi_uekibachi.raw'
    raw_to_wav(raw_path, raw_path.replace('.raw', '.wav'), 1, 16000)
