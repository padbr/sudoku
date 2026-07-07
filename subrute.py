#!/usr/bin/env python3

import time
from copy import deepcopy
from itertools import chain

__author__ = "Patrick Denis Browne"
__email__ = "pbrowne575@gmail.com"
__license__ = "GPLv3"

row_indicess = [[(i*9) + j for j in range(9)] for i in range(9)]
col_indicess = [[(i*9) + j for i in range(9)] for j in range(9)]
ssq_offsets = [0, 1, 2, 9, 10, 11, 18, 19, 20]
ssq_starts = [0, 3, 6, 27, 30, 33, 54, 57, 60]
ssq_indicess = [[i+j for j in ssq_offsets] for i in ssq_starts]

def get_row_index(i):
    return i // 9

def get_col_index(i):
    return i % 9

def get_ssq_index(i):
    for j in range(9):
        if i in ssq_indicess[j]:
            return j

def set_game(gamestr):
    game_lists = []
    for elem in list(gamestr):
        n = int(elem)
        if n >= 1:
            game_lists.append([n])
        else:
            game_lists.append([i for i in range(1, 10)])
    sweep(game_lists)
    return game_lists

def sweep(game_lists):
    glen_start = len(list(chain(*game_lists)))
    # k = 0 # debug
    prune = True
    while prune == True:
        for i,elem in enumerate(game_lists):
            if len(elem) == 1:
                row_i = get_row_index(i)
                col_i = get_col_index(i)
                ssq_i = get_ssq_index(i)
                for j in row_indicess[row_i]:
                    if j != i:
                        if elem[0] in game_lists[j]:
                            _ = game_lists[j].pop(game_lists[j].index(elem[0]))
                for j in col_indicess[col_i]:
                    if j != i:
                        if elem[0] in game_lists[j]:
                            _ = game_lists[j].pop(game_lists[j].index(elem[0]))
                for j in ssq_indicess[ssq_i]:
                    if j != i:
                        if elem[0] in game_lists[j]:
                            _ = game_lists[j].pop(game_lists[j].index(elem[0]))
        glen_end = len(list(chain(*game_lists)))
        if glen_end == glen_start:
            prune = False
        glen_start = glen_end


def is_solved(game_lists):
    if max([len(elem) for elem in game_lists]) > 1:
        return False
    for row_indices in row_indicess:
        if not set([game_lists[i][0] for i in row_indices]) == set([i+1 for i in range(9)]):
            return False
    for col_indices in col_indicess:
        if not set([game_lists[i][0] for i in col_indices]) == set([i+1 for i in range(9)]):
            return False
    for ssq_indices in ssq_indicess:
        if not set([game_lists[i][0] for i in ssq_indices]) == set([i+1 for i in range(9)]):
            return False
    return True

def is_broken(game_lists):
    slens = [len(elem) for elem in game_lists]
    if min(slens) == 0:
        return True
    return False

def find_first_unsolved(game_lists):
    slens = [len(elem) for elem in game_lists]
    for i,slen in enumerate(slens):
        if slen > 1:
            return i

def solve(game_lists):
    gls = deepcopy(game_lists)
    sweep(gls)
    if is_broken(gls):
        return
    if is_solved(gls):
        print("SOLVED")
        print_game(gls)
        return
    i = find_first_unsolved(gls)
    for elem in gls[i]:
        ngls = deepcopy(gls)
        ngls[i] = [elem]
        solve(ngls)

def write_square(cell_list):
    if len(cell_list) > 1:
        return ' '
    if len(cell_list) == 0:
        return '!'
    if len(cell_list) == 1:
        return str(cell_list[0])


def write_row(row_indices, game_lists):
    d = [write_square(game_lists[i]) for i in row_indices]
    return ": %s %s %s : %s %s %s : %s %s %s :" % (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

def print_game(game_lists):
    grid_line = ' ' + ' '.join([''.join(['-']*7)]*3)
    outlines = []
    outlines.append(grid_line)
    for i in [0, 3, 6]:
        for j in [0, 1, 2]:
            outlines.append(write_row(row_indicess[i+j], game_lists))
        outlines.append(grid_line)
    output = '\n'.join(outlines)
    print(output)


if __name__ == '__main__':
    gamestr = input("Type or paste a game. Use 0 for unknown numbers.\n")
    game_lists = set_game(gamestr)
    print("Solving:")
    print_game(game_lists)
    print("\n")
    t1 = time.time()
    solve(game_lists)
    t2 = time.time()
    t_total = t2 - t1
    print(f"{t_total} seconds")
