# -*- coding: utf-8 -*-
import numpy as np
from common import run_command, GraphItems, draw_graph, binary_to_text


def draw_pitch(text_pitch_path, figure_path):
    pitch = np.loadtxt(text_pitch_path)
    graph_items = GraphItems()
    graph_items.arrays = [pitch]
    graph_items.title = 'pitch (%d records)' % pitch.size
    draw_graph(graph_items, figure_path)

'''rawファイル(raw_path)からピッチを抽出しpitch_pathに出力する'''
def raw_to_pitch(raw_path, pitch_path, frame_rate=16000):
    x2x_in = 'x2x +sf %s' % raw_path
    pitch = 'pitch -a 1 -s %f -p 80 > %s' % (frame_rate / 1000.0, pitch_path)
    res = run_command([x2x_in, pitch])

'''wavファイル(wave_path)からピッチを抽出しpitch_pathに出力する'''
# frame_rateは読み込むWavファイルに合わせず16000[Hz]のままの方がいいみたい？
def wav_to_pitch(wave_path, pitch_path, frame_rate=16000):
    bcut = 'bcut +s -s 22 %s' % wave_path
    x2x_in = 'x2x +sf'
    pitch = 'pitch -a 1 -s %f -p 80 > %s' % (frame_rate / 1000.0, pitch_path)
    res = run_command([bcut, x2x_in, pitch])


if __name__ == '__main__':
    path = 'other_test_file/aoi_uekibachi'  # 拡張子抜きのパス
    raw_to_pitch(path + '.raw', path + '.pitch')
    binary_to_text(path + '.pitch', path + '.pitch_ascii')
    draw_pitch(path + '.pitch_ascii', path + '_pitch.png')
