# -*- coding: utf-8 -*-
import os
import numpy as np
from glob import glob
from scipy.spatial.distance import euclidean
from dtw import dtw


def align_mcep(conv_from, conv_to):
    align_from = 'mcep_aligned/%s_to_%s/%s/' % (conv_from, conv_to, conv_from)
    align_to = 'mcep_aligned/%s_to_%s/%s/' % (conv_from, conv_to, conv_to)
    if not os.path.exists(align_from):
        os.makedirs(align_from)
    if not os.path.exists(align_to):
        os.makedirs(align_to)
    mcep_dir_from = 'mcep/%s/' % conv_from
    mcep_dir_to = 'mcep/%s/' % conv_to

    for mcep_path1 in glob(mcep_dir_from + '*.mcep'):
        file_name = os.path.basename(mcep_path1)
        mcep_path2 = mcep_dir_to + file_name
        print(file_name)

        # 対応するmcepファイルがなかったら無視する
        if not os.path.exists(mcep_path2):
            print('{} not found.'.format(mcep_path2))
            continue   

        # オリジナルのmcepを読み込み
        mcep1 = np.loadtxt(mcep_path1)
        mcep2 = np.loadtxt(mcep_path2)

        # DTWで同期を取る（dtwには引数distが必要）
        dist, cost, dummy, path = dtw(mcep1, mcep2, dist=euclidean)
        aligned_mcep1 = mcep1[path[0]]
        aligned_mcep2 = mcep2[path[1]]

        # 同期を取ったmcepをテキスト形式で書き込み
        np.savetxt(align_from + file_name, aligned_mcep1, fmt='%0.6f')
        np.savetxt(align_to + file_name, aligned_mcep2, fmt='%0.6f')
