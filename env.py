from __future__ import annotations

from c2 import Cube
import sys
import gym
from gym import spaces
import random
from time import perf_counter
import numpy as np


# sys.modules["gym"] = gym


# Good docs on this: https://www.gymlibrary.dev/content/environment_creation/
class RubiksEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, moves_per_step=1, terminate_after_n_moves: int | str = False, n_scramble_moves=40):
        super(RubiksEnv, self).__init__()

        self.n_scramble_moves = n_scramble_moves
        self.terminate_after_n_moves = terminate_after_n_moves
        self.all_moves = ["U", "U'", "L", "L'", "B",
                          "B'", "R", "R'", "F", "F'", "D", "D'"]

        self.base_moves = ["U", "L", "B", "R", "F", "D"]

        self.moves_per_step = moves_per_step

        actions_min = [-1]*len(self.base_moves)*moves_per_step
        actions_max = [1]*len(self.base_moves)*moves_per_step
        self.action_space = spaces.Box(
            np.array(actions_min), np.array(actions_max)
        )

        self.observation_space = spaces.Box(
            0, 5, shape=(54,), dtype=np.int8
        )

    def _vector_action_to_action(self, vec):
        # val = next(([i, x] for i, x in enumerate(vec) if x), None)
        maxv = np.max(vec)
        minv = np.min(vec)

        move = self.base_moves[
            np.where(vec == maxv)[0][0]
        ] if abs(maxv) >= abs(minv) else self.base_moves[
            np.where(vec == minv)[0][0]
        ] + "'"

        # print("move:", move, "\n")
        # action_moves = []
        # for v in ([i, x] for i, x in enumerate(vec) if x):
        #    _move = self.base_moves[v[0] % self.moves_per_step]
        #    if v[1] < 0:
        #        _move += "'"
        #        action_moves.append(_move)
        #    if v[1] > 0:
        #        action_moves.append(_move)
        return move  # " ".join(action_moves)

    def _get_obs(self):
        color_map = {
            "Y": 0,
            "O": 1,
            "G": 2,
            "R": 3,
            "B": 4,
            "W": 5
        }
        return np.array([color_map[self.cube.get_color(x)] for x in self.cube._data], dtype=np.int8)

    def _get_info(self):
        solved = self._solved_obs
        # print("Solved:", solved)
        current = self._get_obs()
        # print("Current:", current)

        distance = 1-(
            sum([
                1 if v == current[i] else 0
                for i, v in enumerate(solved)
            ])
        ) / len(solved)

        # distance = min(1, max(0, distance))

        # speed = 1/self.cube.total_moves

        # score = speed * 0.1 + (1-distance) * 0.9
        score = 1-distance  # score of 1 when distance is 0 = solved

        if hasattr(self, "_scramble_distance"):
            pass
            # Remove scramble_distance from score
            # if scramble is solved (scramble_distance = 0)
            # and score is 1, then remove 1 and score is 0
            # score = score - (1-self._scramble_distance)
            # Clip it between -1 and 1 (should already be the case but I tried before with 0 <= x <= 1)
            # score = max(0, min(1, score))

        if score < -1 or score > 1:
            print("WTF:", score, distance)
            exit()
        return {
            "distance": distance,
            # "speed": speed,
            "score": 1 if score == 1 else 0
        }

    def step(self, action):

        move = self._vector_action_to_action(action)

        self.cube.moves(move)

        observation = self._get_obs()
        info = self._get_info()

        # An episode is done if cube is solved
        terminated = info["distance"] == 0

        score = info["score"]

        # Also terminate if moves are greater than some amount this episode... This is bad because in new versions of gym
        # it works differently, where you return terminated, truncated, info instead of terminated, info.
        # I tried using TimeLimit which should theoretically be a better approach but then my model suicides and
        # makes a policy that is as shitty as possible, not sure why.
        # if self.terminate_after_n_moves != False and self.cube.total_moves >= self.terminate_after_n_moves+self.n_scramble_moves:
        #    terminated = True

        # if self.render_mode == "human":
        #    self._render_frame()

        return observation, score, terminated, {}  # truncated, {}

    def reset(self, options=None):
        # We need the following line to seed self.np_random
        # super().reset(seed=seed)
        # random.seed(seed)

        # print("reset options:", options)

        if options == None:
            print("reset called without options:", options)
        # else:
        #    print("reset options:", options)

        self.cube = Cube()

        self._solved_obs = self._get_obs()

        scramble_moves = " ".join(
            random.choices(
                self.all_moves, k=np.random.randint(0, 3)
            )
        )

        self.cube.moves(scramble_moves)

        # set the scramble "distance to solved", 0 is solved, 1 is furthest away from solved
        self._scramble_distance = self._get_info()["distance"]

        observation = self._get_obs()
        # info = self._get_info()

        # if self.render_mode == "human":
        #    self.render()

        # print("obs:", observation, "len:", len(observation))
        return observation

    def render(self, mode='human'):
        print(self.cube.print())
        pass

    def close(self):
        pass


if __name__ == "__main__":
    env = RubiksEnv()
    env.reset()
    print(env._get_info())
    print(env._get_obs())
    # env.render()
    print("Then doing R U R:")
    env.cube.moves("R U R")
    print(env._get_info())
    print(env._get_obs())
    # env.render()
