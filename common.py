# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import struct


m = 25  # メルケプストラム次数（実際はパワー項を追加して26次元ベクトルになる）
a = 0.42  # all-pass constant
K = 32  # GMMのコンポーネント数

class GraphItems:
    def __init__(self):
        self.arrays = []
        self.labels = []
        self.xlabel = 'frame'
        self.ylabel = ''
        self.title = ''

def draw_graph(graph_items, output_path):
    fig = plt.figure(figsize=(7.2, 5.4))
    if graph_items.labels:
        for ar, lb in zip(graph_items.arrays, graph_items.labels):
            plt.plot(ar, label=lb)
        plt.legend()
    else:
        for ar in graph_items.arrays:
            plt.plot(ar)
    plt.grid()
    plt.xlabel(graph_items.xlabel)
    plt.ylabel(graph_items.ylabel)
    plt.title(graph_items.title)
    fig.savefig(output_path)
    plt.clf()
    plt.close()

def draw_graph_two_screen(graph_items_1, graph_items_2, output_path):
    def draw_graph_one_side(ax, graph_items):
        if graph_items.labels:
            for ar, lb in zip(graph_items.arrays, graph_items.labels):
                ax.plot(ar, label=lb)
            ax.legend()
        else:
            for ar, in graph_items.arrays:
                ax.plot(ar)
        ax.grid()
        ax.set_xlabel(graph_items.xlabel)
        ax.set_ylabel(graph_items.ylabel)
        ax.set_title(graph_items.title)
    
    fig = plt.figure(figsize=(14.4, 5.4))
    ax_1 = fig.add_subplot(2, 2, 1)
    ax_2 = fig.add_subplot(2, 2, 2)
    draw_graph_one_side(ax_1, graph_items_1)
    draw_graph_one_side(ax_2, graph_items_2)
    fig.savefig(output_path)
    plt.clf()
    plt.close()

# コマンドの戻り値が0またはno_printing_resultsに入れば戻り値を標準出力しない
def run_command(commands, no_printing_results=[], delimiter=' | '):
    if type(commands) == str:
        res = subprocess.call(commands, shell=True)
    elif type(commands) == list:
        commands = delimiter.join(commands)
        res = subprocess.call(commands, shell=True)
    if not (res == 0 or res in no_printing_results):
        print('Returned %d: %s' % (res, commands))
    return res

'''
バイナリファイル(file_path)からone_record_bytes[byte]ずつ読み込み
1次元のnumpy.ndarray配列で返す（split_lengthを正の整数とした場合は2次元になる）
'''
def read_binary_file(file_path, split_length=None, one_record_bytes=4):
    res = np.array([])
    f = open(file_path, 'rb')
    while True:
        data = f.read(one_record_bytes)
        if len(data) == 0:
            break
        res = np.append(res, struct.unpack('<f', data)[0])
    f.close()
    if split_length is not None:
        if res.size % split_length > 0:
            msg = 'Warning: record size of %s is not dividable by %d.'
            print(msg % (file_path, split_length))
        return res.reshape(res.size // split_length, split_length)
    return res
