# -*- coding: utf-8 -*-
from glob import glob
from audio_file_analyzer import get_wav_header
from extract_mcep import wav_to_mcep
from extract_pitch import wav_to_pitch
from synthesizer import synthesize_to_wav


def resynthesize(wav_path):
    _header = wav_path.replace('.wav', '.header')
    channels, frame_rate = get_wav_header(wav_path, out_file_path=_header)

    _pitch = wav_path.replace('.wav', '.pitch')
    wav_to_pitch(wav_path, _pitch)

    _mcep = wav_path.replace('.wav', '.mcep')
    # テキスト形式で出力すると最終出力のwavファイルが無音になる模様
    wav_to_mcep(wav_path, _mcep, binary=True)

    _out_wav = wav_path.replace('.wav', '_resynthesized.wav')
    synthesize_to_wav(_pitch, _mcep, _out_wav, channels, frame_rate)


if __name__ == '__main__':
    audio_folder = 'resynthesis_test/'
    for wav_path in glob(audio_folder + '*.wav'):
        if '_resynthesized.wav' in wav_path:
            continue
        resynthesize(wav_path)
