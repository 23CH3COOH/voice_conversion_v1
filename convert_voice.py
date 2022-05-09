# -*- coding: utf-8 -*-
import os
import numpy as np
import subprocess
import struct
import joblib
from scipy.stats import multivariate_normal
from extract_mcep import wav_to_mcep
from extract_pitch import wav_to_pitch
from synthesizer import synthesize_to_wav

# メルケプストラム次数
# 実際はパワー項を追加して26次元ベクトルになる
m = 25

# GMMのコンポーネント数
K = 32

def convert_mcep(source_mcep_file, converted_mcep_file, gmm):
    source_mcep = np.loadtxt(source_mcep_file)
    fp = open(converted_mcep_file, 'wb')

    d = m + 1

    # 式9の多次元正規分布のオブジェクトを作成しておく
    gauss = []
    for k in range(K):
        gauss.append(multivariate_normal(gmm.means_[k, 0:d], gmm.covariances_[k, 0:d, 0:d]))

    # 式11のフレームtに依存しない項を計算しておく
    ss = []
    for k in range(K):
        ss.append(np.dot(gmm.covariances_[k, d:, 0:d], np.linalg.inv(gmm.covariances_[k, 0:d, 0:d])))

    # 各フレームをGMMで変形する
    for t in range(len(source_mcep)):
        x_t = source_mcep[t]
        y_t = convert_frame(x_t, gmm, gauss, ss)
        fp.write(struct.pack('f' * (m+1), *y_t))
    fp.close()

# 式(13)の計算
def convert_frame(x, gmm, gauss, ss):
    # 式(9)の分母だけ先に計算
    denom = np.zeros(K)
    for n in range(K):
        denom[n] = gmm.weights_[n] * gauss[n].pdf(x)

    y = np.zeros_like(x)
    for k in range(K):
        y += P(k, x, gmm, gauss, denom) * E(k, x, gmm, ss)
    return y

# 式(9)の計算
def P(k, x, gmm, gauss, denom):
    return denom[k] / np.sum(denom)

# 式(11)の計算
def E(k, x, gmm, ss):
    d = m + 1
    return gmm.means_[k, d:] + np.dot(ss[k], x - gmm.means_[k, 0:d])

def convert_voice(wav_path_from, wav_path_to, gmm_path):
    # 変換元のwavファイルからメルケプストラムとピッチを抽出
     # numpyで読みやすいようにアスキー形式で保存
    print('extract mcep ...')
    source_mcep_file = 'source.mcep_ascii'
    wav_to_mcep(wav_path_from, source_mcep_file, binary=False)
    print('extract pitch ...')
    source_pitch_file = 'source.pitch'
    wav_to_pitch(wav_path_from, source_pitch_file)

    # GMMをロード
    gmm = joblib.load(gmm_path)

    # 変換元のメルケプストラムをGMMで変換
    # SPTKで合成できるようにバイナリ形式で保存
    print('convert mcep ...')
    converted_mcep_file = 'converted.mcep'
    convert_mcep(source_mcep_file, converted_mcep_file, gmm)

    # 変換元のピッチと変換したメルケプストラムから再合成
    print('synthesis ...')
    synthesize_to_wav(source_pitch_file, converted_mcep_file, wav_path_to,
                      channels=1, sampling_rate=16000, delete_temp_raw=False)

    # 一時ファイルを削除
    os.remove(source_mcep_file)
    os.remove(source_pitch_file)
    os.remove(converted_mcep_file)
