# -*- coding: utf-8 -*-
from glob import glob
from audio_file_analyzer import get_wav_header
from extract_pitch import wav_to_pitch, draw_pitch
from extract_mcep import wav_to_mcep, draw_single_mcep
from synthesizer import synthesize_to_wav, synthesize_to_wav_no_pitch
from common import binary_to_text


def resynthesize(wav_path, m, a, e, with_pitch=True):
    _header = wav_path.replace('.wav', '.header')
    channels, frame_rate = get_wav_header(wav_path, out_file_path=_header)

    if with_pitch:
        print('Extracting pitch...')
        _pitch = wav_path.replace('.wav', '.pitch')
        _pitch_text = wav_path.replace('.wav', '.pitch_ascii')
        _pitch_fig = wav_path.replace('.wav', '_pitch.png')
        wav_to_pitch(wav_path, _pitch)
        binary_to_text(_pitch, _pitch_text)
        draw_pitch(_pitch_text, _pitch_fig)

    print('Extracting mel cepstrum...')
    _mcep = wav_path.replace('.wav', '.mcep')
    _mcep_text = wav_path.replace('.wav', '.mcep_ascii')
    wav_to_mcep(wav_path, _mcep, m, a, e)
    binary_to_text(_mcep, _mcep_text, m + 1)
    draw_single_mcep(_mcep_text, 0, wav_path.replace('.wav', '_mcep_0.png'))
    draw_single_mcep(_mcep_text, 1, wav_path.replace('.wav', '_mcep_1.png'))
    draw_single_mcep(_mcep_text, 2, wav_path.replace('.wav', '_mcep_2.png'))

    print('Synthesizing...')
    _out_wav = wav_path.replace('.wav', '_resynthesized.wav')
    if with_pitch:
        synthesize_to_wav(_pitch, _mcep, _out_wav, channels, frame_rate, m, a)
    else:
        synthesize_to_wav_no_pitch(_mcep, _out_wav, channels, frame_rate, m, a)


if __name__ == '__main__':
    audio_folder = 'resynthesis_test/'
    m = 25
    a = 0.42
    e = 0.01
    for wav_path in glob(audio_folder + '*.wav'):
        if '_resynthesized.wav' in wav_path:
            continue
        print('Start resynthesize: %s' % wav_path)
        resynthesize(wav_path, m, a, e)
