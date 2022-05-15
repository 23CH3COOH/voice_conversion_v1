# -*- coding: utf-8 -*-
from sys import float_info


def calc_head_excluding_frames(array, minimum_excluding_frames):
    head_excluding_frames = minimum_excluding_frames
    for i in range(array.shape[0]):
        excluding_frames = 1
        for j in range(1, array.shape[1]):
            if abs(array[i][j] - array[i][j-1]) < float_info.min:
                excluding_frames += 1
            else:
                break
        if excluding_frames > head_excluding_frames:
            head_excluding_frames = excluding_frames
    if head_excluding_frames > 1:
        return head_excluding_frames
    else:
        return 0

def calc_tail_excluding_frames(array, minimum_excluding_frames):
    tail_excluding_frames = minimum_excluding_frames
    for i in range(array.shape[0]):
        excluding_frames = 1
        for j in reversed(range(1, array.shape[1])):
            if abs(array[i][j] - array[i][j-1]) < float_info.min:
                excluding_frames += 1
            else:
                break
        if excluding_frames > tail_excluding_frames:
            tail_excluding_frames = excluding_frames
    if tail_excluding_frames > 1:
        return tail_excluding_frames
    else:
        return 0

# できれば実装をきれいにする
def exclude_both_ends(array_1, array_2, minimum_excluding_frames=3):
    if not array_1.shape == array_2.shape:
        print('Warning: not match shape.')
        return array_1, array_2
    if not array_1.ndim == 2 or not array_2.ndim == 2:
        print('Warning: not 2 dimensions.')
        return array_1, array_2 

    temp_1 = array_1.copy().T
    temp_2 = array_2.copy().T
    temp_1_se = array_1.copy()[minimum_excluding_frames:].T
    temp_2_se = array_2.copy()[minimum_excluding_frames:].T

    p = calc_head_excluding_frames(temp_1, minimum_excluding_frames)
    q = calc_head_excluding_frames(temp_2, minimum_excluding_frames)
    r = calc_head_excluding_frames(temp_1_se, 0)
    s = calc_head_excluding_frames(temp_2_se, 0)
    T = max(p, q)
    U = max(r, s) + 3
    start = max(T, U)

    p = calc_tail_excluding_frames(temp_1, minimum_excluding_frames)
    q = calc_tail_excluding_frames(temp_2, minimum_excluding_frames)
    end = array_1.shape[0] - max(p, q)

    assert start <= end
    return array_1[start:end], array_2[start:end]
