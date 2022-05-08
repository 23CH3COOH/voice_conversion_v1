# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import subprocess


delimiter = ' | '
m = 25  # メルケプストラム次数（実際はパワー項を追加して26次元ベクトルになる）
a = 0.42  # all-pass constant

def print_cmd_result(res, cmd, successed_msg):
    if res == 0:
        print(successed_msg)
    else:
        print('Returned %d: %s' % (res, cmd))

def draw_single_transition(values, output_path, ylabel='', title=''):
    xlabel = 'frame'
    fig = plt.figure()
    plt.plot(values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    fig.savefig(output_path)

def run_command(commands):
    if type(commands) == str:
        res = subprocess.call(commands, shell=True)
    elif type(commands) == list:
        res = subprocess.call(delimiter.join(commands), shell=True)
    return res
