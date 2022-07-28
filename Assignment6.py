# CSCI 323/700
# Summer 2022
# Assignment 3 - Empirical Performance of Matrix Multiplication
# Hengzhi Cao

import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

assn_num = 3


# def random_matrix(mn, mx, rows, cols):
#     matrix = [[random.randint(mn, mx) for col in range(0, cols)] for row in range(0, rows)]
#     return np.array(matrix)
#
#
# def all_ones_matrix(mn, nx, rows, cols):
#     matrix = [[1 for col in range(0, cols)] for row in range(0, rows)]
#     return np.array(matrix)
#
#
# # From https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
# def print_matrix(matrix):
#     print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]) + "\n")


def native_search(text, pattern, verbose=True):
    return text.find(pattern)


def Brute_Force(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)

    # A loop to slide pat[] one by one */
    for i in range(n - m + 1):
        j = 0
        while j < m:
            if verbose:
                print('m', m, 'n', n, 'i', i, 'j', j)
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i
    return -1


def Rabin_Karp(text, pattern, verbose=True):
    m = len(pattern)
    n = len(text)
    j = 0
    p = 0  # hash value for pattern
    t = 0  # hash value for txt
    h = 1
    q = 101  # modulo
    d = 256  # num of char

    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if verbose:
                print('p', p, 't', t, 'i', i, 'j', j, 'm', m, 'n', n)
            for j in range(m):
                if text[i + j] != pattern[j]:
                    break
                else:
                    j += 1
            if j == m:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1


def plot_time(dict_algs, sizes, algs, trials):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for algs in algs:
        alg_num += 1
        d = dict_algs[algs.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=algs.__name__)
    plt.legend()
    plt.title("Run time of Algorithms")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trials) + "trials (ms)")
    plt.savefig("Assignment" + str(assn_num) + ".png")
    plt.show()


def run_trials():
    sizes = [10 * i for i in range(1, 11)]
    trials = 1
    algs = [native_search, Brute_Force, Rabin_Karp]
    dict_algs = {}
    for alg in algs:
        dict_algs[alg.__name__] = {}
    for size in sizes:
        for alg in algs:
            dict_algs[alg.__name__][size] = 0
        for trial in range(1, trials + 1):
            for alg in algs:
                start_time = time.time()
                idx = alg(text='', pattern='', verbose=True)
                end_time = time.time()
                net_time = end_time - start_time
                dict_algs[alg.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_algs).T
    print(tabulate(df, headers='keys', tablefmt='psql'))
    plot_time(dict_algs, sizes, algs, trials)


def main():
    # run_trials()
    text = 'loopsdjbeiwm'
    pattern = 'jdb'
    idx1 = native_search(text, pattern, True)
    idx2 = Brute_Force(text, pattern, True)
    idx3 = Rabin_Karp(text, pattern, True)
    print(idx1, idx2, idx3)


if __name__ == "__main__":
    main()
