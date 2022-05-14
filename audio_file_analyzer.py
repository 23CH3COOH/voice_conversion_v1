# -*- coding: utf-8 -*-
import csv
import wave
from common import run_command


def extract_amplitudes(raw_path, out_file_path):
    res = run_command('dmp +s %s > %s' % (raw_path, out_file_path))

def get_wav_header(wave_path, out_file_path=None, return_all=False):
    wf = wave.open(wave_path, 'r')
    channels = wf.getnchannels()
    frame_rate = wf.getframerate()
    frame_su = wf.getnframes()
    time_length = float(wf.getnframes()) / wf.getframerate()
    sample_byte = wf.getsampwidth()
    wf.close()

    if out_file_path and type(out_file_path) == str:
        body = [['チャンネル数', 'Channels', channels],
                ['サンプリング周波数', 'FrameRate', frame_rate],
                ['フレーム数', 'Frames', frame_su],
                ['長さ', 'TimeLength', time_length],
                ['1サンプルのバイト数', 'SampleWidth', sample_byte]]
        f = open(out_file_path, 'w', newline='')
        writer = csv.writer(f)
        writer.writerows(body)
        f.close()

    if return_all:
        return channels, frame_rate, frame_su, time_length, sample_byte
    else:
        return channels, frame_rate


if __name__ == '__main__':
    print(get_wav_header('other_test_file/aoi_uekibachi.wav'))
