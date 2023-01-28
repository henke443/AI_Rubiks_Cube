from c2 import Cube
from itertools import groupby, permutations, product
import random
from scipy import stats
import numpy as np
import zlib
import matplotlib.pyplot as plt

entropy_after_n_iterations = 6


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


possible_moves = "U U' L L' B B' R R' F F' D D'".split(" ")


def gen_random_moves(n):
    return " ".join(random.choices(possible_moves, k=n))


def entropy(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    return stats.entropy(counts, base=base)


def gen_all_moves(k):
    return list(product(possible_moves, repeat=k))


def find_slowest_repeating(all_moves):

    best_scramble = ""
    best_scramble_score = -1

    res_all_score = []
    res_all_moves = []

    for moves in all_moves:
        cube = Cube()

        if type(moves) == str:
            if moves.strip() == "":
                continue
        else:
            moves = " ".join(moves)

        for i in range(0, 2000):
            cube.moves(moves)
            all_is_equal = True
            for j in range(0, 6):
                if not all_equal([cube.get_color(x) for x in cube.layer(j)]):
                    all_is_equal = False
            if all_is_equal:
                res_all_score.append(i)
                res_all_moves.append(moves)
                if i >= best_scramble_score:
                    best_scramble = moves
                    best_scramble_score = i
                    print("Repeats after:", i)
                    print("Moves:", moves, "\n")
                break
            # print(i, "all_is_equal:", all_is_equal)

    return {
        "best": best_scramble,
        "best_score": best_scramble_score,
        "all_score": res_all_score,
        "all_moves": res_all_moves
    }


def find_highest_entropy(all_moves, after_n_iter):

    best_scramble = ""
    best_scramble_score = -1

    worst_scramble = ""
    worst_scramble_score = 100

    res_all_moves = []
    res_all_score = []

    for moves in all_moves:
        cube = Cube()

        moves = " ".join(moves) if not type(moves) == "str" else moves
        all_data = []
        for i in range(0, after_n_iter):
            cube.moves(moves)
            all_is_equal = True

            all_layers_data = []
            for j in range(0, 6):
                layer_data = [cube.get_color(x) for x in cube.layer(j)]
                all_layers_data.extend(layer_data)
                if not all_equal(layer_data):
                    all_is_equal = False
            all_data.extend(all_layers_data)
            if all_is_equal:
                break

        # print("all_data:", all_data)
        all_data = list(zlib.compress(np.array(all_data)))

        _entropy = len(all_data)  # entropy(all_data)
        res_all_score.append(_entropy)
        res_all_moves.append(moves)
        if _entropy >= best_scramble_score:
            best_scramble = moves
            best_scramble_score = _entropy
            print("Entropy", _entropy)
            print("Scramble:", moves, "\n")
        if _entropy < worst_scramble_score:
            worst_scramble_score = _entropy
            worst_scramble = moves
            print("Worst entropy:", _entropy)
            print("Worst scramble:", moves, "\n")

    return {
        "best": best_scramble,
        "best_score": best_scramble_score,
        "worst": worst_scramble,
        "worst_score": worst_scramble_score,
        "all_score": res_all_score,
        "all_moves": res_all_moves
    }


repeating_res_moves = []
entropy_res_moves = []
entropy_res = []
repeating_res = []
avg_entropy_res = []
avg_repeating_res = []

print(find_slowest_repeating(["L U' D R' F"]))

samples = 1
for i in range(5, 6):
    samples_entropy_res = []
    samples_repeating_res = []
    samples_avg_entropy_res = []
    samples_avg_repeating_res = []

    print("Generating moves...")
    all_moves = [
        gen_random_moves(i) for x in range(0, samples)
    ] if samples > 1 else gen_all_moves(i)
    # print("All moves:", all_moves)

    print("Number of moves:", len(all_moves))
    _entropy_res = find_highest_entropy(all_moves, 20)
    # print(_entropy_res)
    print(find_slowest_repeating(
        [_entropy_res["best"], _entropy_res["worst"]]))
    _repeating_res = find_slowest_repeating(all_moves)

    entropy_res_moves.append(_entropy_res["best"])
    entropy_res.append(_entropy_res["best_score"])
    avg_entropy_res.append(
        sum(_entropy_res["all_score"])/len(_entropy_res["all_score"]))

    repeating_res_moves.append(_repeating_res["best"])
    repeating_res.append(_repeating_res["best_score"])
    avg_repeating_res.append(
        sum(_repeating_res["all_score"])/len(_repeating_res["all_score"]))

plt.plot(entropy_res)
plt.plot(avg_entropy_res)
plt.show()
plt.plot(repeating_res)
plt.plot(avg_repeating_res)
plt.show()

# print(_entropy_res["all_moves"][258])
# print(_repeating_res["all_moves"][258])
