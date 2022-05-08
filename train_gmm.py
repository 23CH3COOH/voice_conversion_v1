#coding: utf-8
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn import mixture
from common import m


M = 32  # GMMのコンポーネント数

'''変換元と変換先の特徴ベクトルを結合したデータを作成して返す'''
def make_joint_vectors(aligned_mcep_paths_1, aligned_mcep_paths_2, dim):
    # 0行目はvstack()するためのダミー
    X = np.zeros((1, dim))
    Y = np.zeros((1, dim))

    # mcepファイルをロード
    for path_1, path_2 in zip(aligned_mcep_paths_1, aligned_mcep_paths_2):
        mcep1 = np.loadtxt(path_1)
        mcep2 = np.loadtxt(path_2)
        X = np.vstack((X, mcep1))
        Y = np.vstack((Y, mcep2))

    # ダミー行を除く
    X = X[1:, :]
    Y = Y[1:, :]

    # 変換元と変換先の特徴ベクトルを結合
    Z = np.hstack((X, Y))
    return Z

def train_gmm(aligned_mcep_paths_1, aligned_mcep_paths_2, outdir):
    # 変換元と変換先の特徴ベクトルを結合したデータを作成
    Z = make_joint_vectors(aligned_mcep_paths_1, aligned_mcep_paths_2, m + 1)

    # バイナリ形式で保存しておく
    np.save(outdir + 'Z.npy', Z)

    # 混合ガウスモデル
    g = mixture.GaussianMixture(n_components=M, covariance_type='full')
    g.fit(Z)

    # モデルをファイルに保存
    joblib.dump(g, outdir + 'GMM.gmm')

    # 最初の3コンポーネントの平均ベクトルを描画
    for k in range(3):
        plt.plot(g.means_[k, :])
    plt.xlim((0, (m + 1) * 2))
    plt.savefig(outdir + 'mean_vector_of_first3.png')

    # 0番目のコンポーネントの共分散行列を描画
    plt.imshow(g.covariances_[0])
    plt.savefig(outdir + 'covariances_of_first.png')
