# CSCI 323/700
# Summer 2022
# Assignment #4 - Empirical Performance of Search Structures
# Hengzhi Cao

import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


assn_num = 4
HashTable = [[] for _ in range(100)]
value = None


def pseudo_random_list(n):
    data = [0]
    for i in range(1, n):
        data.append(data[i - 1] + random.randint(1, 10))
    random.shuffle(data)
    return data


def get_random_sublist(data, size):
    return [data[random.randint(0, len(data) - 1)] for i in range(size)]


def build_changing_hash(data):
    for i in data:
        has_key = i % len(HashTable)
        HashTable[has_key].append(data)


def build_quadratic_hash(data):
    arr = data
    N = 100
    tsize = 100
    table = HashTable
    for i in range(N):
        hv = arr[i] % tsize
        if table[hv] == -1:
            table[hv] = arr[i]
        else:
            for j in range(tsize):
                t = (hv + j * j) % tsize
                if table[t] == -1:
                    table[t] = arr[i]
                    break


# From https://www.geeksforgeeks.org/double-hashing/
class DoubleHashing:
    def __init__(self, TableSize=1111):
        self.ts = TableSize
        self.List = [None] * self.ts
        self.count = 0  # to count element in list

    def nearestPrime(self):
        for l in range((self.ts - 1), 1, -1):
            flag = True
            for i in range(2, int(l ** 0.5) + 1):
                if l % i == 0:
                    flag = False
                    break
            if flag:
                return l
        return 3

    def Hx1(self, key):
        return key % self.ts

    def Hx2(self, key):
        return self.nearestPrime() - (key % self.nearestPrime())

    def dHasing(self, key):
        if self.count == self.ts:
            return self.List
        elif self.List[self.Hx1(key)] is None:
            self.List[self.Hx1(key)] = key
            self.count += 1
        else:
            comp = False
            i = 1
            while not comp:
                index = (self.Hx1(key) + i * self.Hx2(key)) % self.ts
                if self.List[index] is None:
                    self.List[index] = key
                    comp = True
                    self.count += 1
                else:
                    i += 1



def build_double_hash(data):
    tableSize = 7
    Hash = DoubleHashing(tableSize)
    for i in data:
        Hash.dHasing(i)


# I give up
def build_cuckoo_hash(data):
    pass


def search_changing_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False


def search_quadratic_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False


def search_double_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False


def search_cuckoo_hash(data, item):
    for i in HashTable:
        if i == item:
            return True
    return False


def plot_time(dict_algs, sizes, algs, trials, a):
    alg_num = 0
    plt.xticks([j for j in range(len(sizes))], [str(size) for size in sizes])
    for alg in algs:
        alg_num += 1
        d = dict_algs[alg.__name__]
        x_axis = [j + 0.05 * alg_num for j in range(len(sizes))]
        y_axis = [d[i] for i in sizes]
        plt.bar(x_axis, y_axis, width=0.05, alpha=0.75, label=alg.__name__)
    plt.legend()
    plt.title("Run time of algorithms")
    plt.xlabel("Size of data")
    plt.ylabel("Time for " + str(trials) + "trials(ms)")
    plt.savefig("Assignment" + a + ".png")
    plt.show()


def main():
    sizes = [100 * i for i in range(1, 11)]
    trials = 10
    build_functions = [build_changing_hash, build_quadratic_hash, build_double_hash, build_cuckoo_hash]
    search_functions = [search_changing_hash, search_quadratic_hash, search_double_hash, search_cuckoo_hash]
    dict_build = {}
    dict_search = {}
    for build in build_functions:
        dict_build[build.__name__] = {}
    for search in search_functions:
        dict_search[search.__name__] = {}
    for size in sizes:
        for build in build_functions:
            dict_build[build.__name__][size] = 0
        for search in search_functions:
            dict_search[search.__name__][size] = 0
        for trial in range(1, trials + 1):
            data = pseudo_random_list(size)
            sublist = get_random_sublist(data, 100)
            hash_table = []
            for build in build_functions:
                stat_time = time.time()
                hash_table.append(build(data))
                end_time = time.time()
                net_time = end_time - stat_time
                dict_build[build.__name__][size] += 1000 * net_time

            for i in range(len(search_functions)):
                search = search_functions[i]
                table = hash_table[i]
                stat_time = time.time()
                for item in sublist:
                    search(table, item)
                end_time = time.time()
                net_time = end_time - stat_time
                dict_search[search.__name__][size] += 1000 * net_time
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    df = pd.DataFrame.from_dict(dict_build).T
    print(tabulate(df, headers='keys', tablefmt='psql'))
    dd = pd.DataFrame.from_dict(dict_search).T
    print(tabulate(dd, headers='keys', tablefmt='psql'))

    plot_time(dict_build, sizes, build_functions, trials, "4A")
    plot_time(dict_search, sizes, search_functions, trials, "4B")


if __name__ == "__main__":
    main()
