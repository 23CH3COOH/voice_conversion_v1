# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial.distance import euclidean
from dtw import dtw


'''
2つのmcepファイルin_path_1とin_path_2アライメント（時間同期）をとり、
それぞれout_path_1とout_path_2に出力する
'''
def align_mcep(in_path_1, in_path_2, out_path_1, out_path_2):
    # オリジナルのmcepを読み込み
    mcep1 = np.loadtxt(in_path_1)
    mcep2 = np.loadtxt(in_path_2)

    # DTWで同期を取る（dtwには引数distが必要）
    dist, cost, dummy, path = dtw(mcep1, mcep2, dist=euclidean)
    aligned_mcep1 = mcep1[path[0]]
    aligned_mcep2 = mcep2[path[1]]

    # 同期を取ったmcepをテキスト形式で書き込み
    np.savetxt(out_path_1, aligned_mcep1, fmt='%0.6f')
    np.savetxt(out_path_2, aligned_mcep2, fmt='%0.6f')
