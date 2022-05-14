# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial.distance import euclidean
from dtw import dtw
from common import m, GraphItems, draw_graph_two_screen
from common import read_binary_file, write_binary_file


class DrawingAlignedMcepsItems:
    def __init__(self):
        self.name = ''
        self.mcep_path_prev = ''
        self.mcep_path_result = ''

def draw_aligned_mceps(items_1, items_2, order, out_path):
    if not isinstance(items_1, DrawingAlignedMcepsItems):
        return
    if not isinstance(items_2, DrawingAlignedMcepsItems):
        return

    mcep_prev_1 = np.loadtxt(items_1.mcep_path_prev)[:, order]
    mcep_prev_2 = np.loadtxt(items_2.mcep_path_prev)[:, order]
    mcep_result_1 = np.loadtxt(items_1.mcep_path_result)[:, order]
    mcep_result_2 = np.loadtxt(items_2.mcep_path_result)[:, order]

    title_prev = '%dth-order mcep (%d records) before aligned'
    graph_items_prev = GraphItems()
    graph_items_prev.arrays = [mcep_prev_1, mcep_prev_2]
    graph_items_prev.labels = [items_1.name, items_2.name]
    graph_items_prev.title = title_prev % (order, mcep_prev_1.size)

    title_result = '%dth-order mcep (%d records) after aligned'
    graph_items_result = GraphItems()
    graph_items_result.arrays = [mcep_result_1, mcep_result_2]
    graph_items_result.labels = [items_1.name, items_2.name]
    graph_items_result.title = title_result % (order, mcep_result_1.size)

    draw_graph_two_screen(graph_items_prev, graph_items_result, out_path)

'''
2つのmcepファイルin_path_1とin_path_2でアライメント（時間同期）をとり、
それぞれout_path_1とout_path_2に出力する
'''
def align_mcep(in_path_1, in_path_2, out_path_1, out_path_2):
    # オリジナルのmcepを読み込み
    mcep_1 = read_binary_file(in_path_1, split_length=(m + 1))
    mcep_2 = read_binary_file(in_path_2, split_length=(m + 1))

    # DTWで同期を取る（dtwには引数distが必要）
    dist, cost, dummy, path = dtw(mcep_1, mcep_2, dist=euclidean)
    aligned_mcep_1 = mcep_1[path[0]]
    aligned_mcep_2 = mcep_2[path[1]]

    # 同期を取ったmcepを書き込み
    write_binary_file(aligned_mcep_1, out_path_1)
    write_binary_file(aligned_mcep_2, out_path_2)
