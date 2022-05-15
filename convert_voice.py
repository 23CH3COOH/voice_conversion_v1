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
from common import read_binary_file


def convert_mcep(source_mcep_file, converted_mcep_file, gmm, m, K):
    d = m + 1

    source_mcep = read_binary_file(source_mcep_file, split_length=d)
    fp = open(converted_mcep_file, 'wb')

    # 式9の多次元正規分布のオブジェクトを作成しておく
    gauss = []
    for k in range(K):
        gauss.append(multivariate_normal(gmm.means_[k, 0:d],
                                         gmm.covariances_[k, 0:d, 0:d]))

    # 式11のフレームtに依存しない項を計算しておく
    ss = []
    for k in range(K):
        ss.append(np.dot(gmm.covariances_[k, d:, 0:d],
                         np.linalg.inv(gmm.covariances_[k, 0:d, 0:d])))

    # 各フレームをGMMで変形する
    for t in range(len(source_mcep)):
        x_t = source_mcep[t]
        y_t = convert_frame(x_t, gmm, gauss, ss, m, K)
        fp.write(struct.pack('f' * d, *y_t))
    fp.close()

# 式(13)の計算
def convert_frame(x, gmm, gauss, ss, m, K):
    # 式(9)の分母だけ先に計算
    denom = np.zeros(K)
    for n in range(K):
        denom[n] = gmm.weights_[n] * gauss[n].pdf(x)

    y = np.zeros_like(x)
    for k in range(K):
        y += P(k, x, gmm, gauss, denom) * E(k, x, gmm, ss, m)
    return y

# 式(9)の計算
def P(k, x, gmm, gauss, denom):
    return denom[k] / np.sum(denom)

# 式(11)の計算
def E(k, x, gmm, ss, m):
    d = m + 1
    return gmm.means_[k, d:] + np.dot(ss[k], x - gmm.means_[k, 0:d])

def convert_voice(wav_path_from, wav_path_to, gmm_path,
        ch=1, fr=16000, m=25, a=0.42, e=0.01, K=32, delete_temp_file=True):
    # 変換元のwavファイルからメルケプストラムとピッチを抽出
    source_mcep_file = 'source.mcep'
    wav_to_mcep(wav_path_from, source_mcep_file, m, a, e)
    source_pitch_file = 'source.pitch'
    wav_to_pitch(wav_path_from, source_pitch_file, frame_rate=16000)

    # GMMをロード
    gmm = joblib.load(gmm_path)

    # 変換元のメルケプストラムをGMMで変換
    # SPTKで合成できるようにバイナリ形式で保存
    converted_mcep_file = 'converted.mcep'
    convert_mcep(source_mcep_file, converted_mcep_file, gmm, m, K)

    # 変換元のピッチと変換したメルケプストラムから再合成
    synthesize_to_wav(source_pitch_file, converted_mcep_file, wav_path_to,
                      ch, fr, m=m, a=a, delete_temp_raw=delete_temp_file)

    # 一時ファイルを削除
    if delete_temp_file:
        os.remove(source_mcep_file)
        os.remove(source_pitch_file)
        os.remove(converted_mcep_file)
