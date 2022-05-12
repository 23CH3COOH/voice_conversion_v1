# -*- coding: utf-8 -*-
import numpy as np
from common import m, a, run_command, GraphItems, draw_graph


def draw_single_mcep(text_mcep_path, order, figure_path):
    mcep = np.loadtxt(text_mcep_path)[:, order]
    graph_items = GraphItems()
    graph_items.arrays = [mcep]
    graph_items.title = '%dth-order mcep (%d records)' % (order, mcep.size)
    draw_graph(graph_items, figure_path)

def output_mcep_text(binary_mcep_path, text_mcep_path):
    x2x_in = 'x2x %s' % binary_mcep_path
    x2x_out = 'x2x +fa%d > %s' % (m + 1, text_mcep_path)
    res = run_command([x2x_in, x2x_out])

'''rawファイル(raw_path)からメルケプストラムを抽出しmcep_pathに出力する'''
def raw_to_mcep(raw_path, mcep_path, add_periodogram=True):
    x2x_in = 'x2x +sf %s' % raw_path
    frame = 'frame -l 400 -p 80'
    window = 'window -l 400 -L 512'
    mcep = 'mcep -l 512 -m %d -a %f -e 0.01 > %s' % (m, a, mcep_path)
    if not add_periodogram:
        mcep = mcep.replace('-e 0.01 ', '')
    res = run_command([x2x_in, frame, window, mcep])

'''wavファイル(wave_path)からメルケプストラムを抽出しmcep_pathに出力する'''
def wav_to_mcep(wave_path, mcep_path, add_periodogram=True):
    bcut = 'bcut +s -s 22 %s' % wave_path
    x2x_in = 'x2x +sf'
    frame = 'frame -l 400 -p 80'
    window = 'window -l 400 -L 512'
    mcep = 'mcep -l 512 -m %d -a %f -e 0.01 > %s' % (m, a, mcep_path)
    if not add_periodogram:
        mcep = mcep.replace('-e 0.01 ', '')
    res = run_command([bcut, x2x_in, frame, window, mcep])

# 音声によっては以下の警告が出ることがある
# 'mcep : periodogram has '0', use '-e' option to floor it!'
# その場合は -e オプションでピリオドグラムに微小な値を足す必要があるらしい
# 当面扱う音声ではほとんどこの警告が出るので、足すのをデフォルトとした


if __name__ == '__main__':
    path = 'resynthesis_test/aoi_uekibachi'  # 拡張子抜きのパス
    raw_to_mcep(path + '.raw', path + '.mcep')
    output_mcep_text(path + '.mcep', path + '.mcep_ascii')
    draw_single_mcep(path + '.mcep_ascii', 0, path + '_mcep_0order.png')
