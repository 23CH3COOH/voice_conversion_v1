# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import subprocess


m = 25  # メルケプストラム次数（実際はパワー項を追加して26次元ベクトルになる）
a = 0.42  # all-pass constant

class GraphItems:
    def __init__(self):
        self.arrays = []
        self.labels = []
        self.xlabel = 'frame'
        self.ylabel = ''
        self.title = ''

def draw_graph(graph_items, output_path):
    fig = plt.figure()
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
    
    fig = plt.figure()
    ax_1 = fig.add_subplot(2, 2, 1)
    ax_2 = fig.add_subplot(2, 2, 2)
    draw_graph_one_side(ax_1, graph_items_1)
    draw_graph_one_side(ax_2, graph_items_2)
    fig.savefig(output_path)

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
