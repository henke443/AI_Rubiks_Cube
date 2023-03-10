from __future__ import annotations

# import c2
from .c2 import Cube
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

    def __init__(self, moves_per_step=1, terminate_after_n_moves: int | str = False,
                 n_scramble_moves=40, max_moves=0, flat_obs: bool | str = "2d"):
        super(RubiksEnv, self).__init__()

        if flat_obs == True:
            flat_obs = "flat"
        elif flat_obs == False:
            flat_obs = "2d"

        self.steps = 0
        self.total_steps = 0

        self._n_scramble_moves = n_scramble_moves
        self._terminate_after_n_moves = terminate_after_n_moves
        self.all_moves = ["U", "U'", "L", "L'", "B",
                          "B'", "R", "R'", "F", "F'", "D", "D'"]

        self.base_moves = ["U", "L", "B", "R", "F", "D"]

        self.moves_per_step = moves_per_step

        # actions_min = [np.float32(-1)]*len(self.base_moves)*moves_per_step
        # actions_max = [np.float32(1)]*len(self.base_moves)*moves_per_step

        if self.moves_per_step > 1:
            self.action_space = spaces.MultiDiscrete(
                np.full((self.moves_per_step), len(self.all_moves)))
            # self.action_space = spaces.Box(
            #    0, len(self.all_moves)-1, dtype=np.int8, shape=(len(self.all_moves), ))
        else:
            self.action_space = spaces.Discrete(len(self.all_moves))

        self._full_obs_info = False

        self._flat_obs = flat_obs

        if self._flat_obs == "flat":
            self.observation_space = spaces.Box(
                0, 5, shape=(54,), dtype=np.int8
            )

        elif self._flat_obs == "2d":
            self.observation_space = spaces.Box(
                0, 53, shape=(6, 9), dtype=np.int8)

        elif self._flat_obs == "3d":
            self.observation_space = spaces.Box(
                0, 53, shape=(6, 9, 54 if self._full_obs_info else 6), dtype=np.int8)

        self._max_moves = max_moves
        self._extra_scramble_moves = 0

        self._has_reset_logged = False
        self._solved_before = 0

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

    def _discrete_action_to_action(self, action):
        # print("got action:", action)
        return self.all_moves[action]

    def _get_multi_dim_obs(self):
        # One cubie face color is desribed a vector of length 6
        # One face is described by 6 cubie face colors
        # One cube is described by 6 faces
        # 6x3x3

        # np.array([color_map[self.cube.get_color(x)] for x in self.cube._data], dtype=np.int8)

        full_info = self._full_obs_info

        retVal = None
        if self._flat_obs == "3d":
            retVal = np.zeros(
                shape=(6, 9, 53 if full_info else 6), dtype=np.bool_)
        else:
            retVal = np.zeros(shape=(6, 9), dtype=np.int8)

        for cube_face_i in range(0, 6):

            for cubie_face_i in range(0, 9):

                # cubie_face = np.array([])
                for row_i in range(0, 3):
                    discrete_row = np.array(
                        self.cube.get_strip(
                            cube_face_i, "row", row_i
                        ), dtype=np.int8)

                    for row_el in discrete_row:
                        if self._flat_obs == "3d":
                            bin_cubie_face = np.zeros(
                                shape=(53 if full_info else 6,), dtype=np.bool_)
                            bin_cubie_face[row_el if full_info else row_el % 6] = 1
                            # cubie_face = bin_cubie_face
                            retVal[cube_face_i][cubie_face_i] = bin_cubie_face
                        else:
                            retVal[cube_face_i][cubie_face_i] = row_el

        return retVal

    def _get_flat_obs(self):
        color_map = {
            "Y": 0,
            "O": 1,
            "G": 2,
            "R": 3,
            "B": 4,
            "W": 5
        }
        return np.array([color_map[self.cube.get_color(x)] for x in self.cube._data], dtype=np.int8)

    def _get_flat_info(self):
        solved = self._solved_obs
        # print("Solved:", solved)
        current = self._get_flat_obs()
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
        # score = 1-distance  # score of 1 when distance is 0 = solved

        if hasattr(self, "_scramble_distance"):
            pass
            # Remove scramble_distance from score
            # if scramble is solved (scramble_distance = 0)
            # and score is 1, then remove 1 and score is 0
            # score = score - (1-self._scramble_distance)
            # Clip it between -1 and 1 (should already be the case but I tried before with 0 <= x <= 1)
            # score = max(0, min(1, score))

        score = 0
        if distance == 0:
            # score = 1
            scramble_moves = 1+self._extra_scramble_moves
            moves_after_scramble = max(
                1, self.cube.total_moves - scramble_moves)

            # moves_usage = moves_after_scramble / self._max_moves
            # scramble_usage = scramble_moves / self._n_scramble_moves

            # toReturn = 1-(percent_moves_usage / scramble_moves)

            # score = 1  # moves_after_scramble/self._max_moves

            # alt_score = ((1-moves_usage) + scramble_usage)/2
            # alt_score = max(0, min(1, alt_score**2 + 0.5))
            score = 0.5*min(1, scramble_moves/self._n_scramble_moves) + \
                0.5*min(1, scramble_moves/moves_after_scramble)

            # score *= self._max_moves

            # score = (moves_usage - 1) ** 2 * (scramble_usage - 1/self._n_scramble_moves) ** 2 \
            #    / ((moves_usage - 1) ** 2 + (scramble_usage - 1/self._n_scramble_moves) ** 2)

            # print("\nSolved once! Score:", score,
            #      "Scramble moves:", 1+self._extra_scramble_moves, "solved in:", moves_after_scramble)  # "alt_score:", alt_score)
            self._solved_before = 1
        # if score < -1 or score > 1:
        #    print("WTF:", score, distance)
        #    exit()
        return {
            "distance": distance,
            # "speed": speed,
            "score": score
        }

    def _get_multi_dim_info(self):
        solved = self._solved_obs
        # print("Solved:", solved)
        current = self._get_multi_dim_obs()
        is_solved = True
        for cube_face_i, cube_face in enumerate(current):
            for i, cubie_face in enumerate(cube_face):
                if self._flat_obs == "2d":
                    if cubie_face != solved[cube_face_i][i]:
                        is_solved = False
                else:
                    if list(cubie_face).index(1) != list(solved[cube_face_i][i]).index(1):
                        is_solved = False
        return {
            "score": 1 if is_solved else -1,
            "distance": 0 if is_solved else 1
        }

    def set_steps(self, step):
        self.steps = step

    def set_total_steps(self, total_steps):
        self.total_steps = total_steps

    def step(self, action):

        if hasattr(self, "episode_returns"):
            print("in step:", self.episode_returns)
        # print("asd:", self.steps)
        moves = ""

        if self.moves_per_step > 1:
            many_moves = []
            for n in action:
                # print("action:", action, n)
                many_moves.append(self._discrete_action_to_action(n))
                moves = " ".join(many_moves)
        else:
            moves = self._discrete_action_to_action(action)

        self.cube.moves(moves)

        observation = self._get_flat_obs() if self._flat_obs else self._get_multi_dim_obs()
        info = self._get_flat_info() if self._flat_obs else self._get_multi_dim_info()

        # An episode is done if cube is solved
        terminated = info["distance"] == 0

        score = info["score"]

        # Also terminate if moves are greater than some amount this episode... This is bad because in new versions of gym
        # it works differently, where you return terminated, truncated, info instead of terminated, info.
        # I tried using TimeLimit which should theoretically be a better approach but then my model suicides and
        # makes a policy that is as shitty as possible, not sure why.
        # if self._terminate_after_n_moves != False and self.cube.total_moves >= self._terminate_after_n_moves+self._n_scramble_moves:
        #    terminated = True

        # if self.render_mode == "human":
        #    self._render_frame()

        return observation, score, terminated, {}  # truncated, {}

    def reset(self, options=None):
        # We need the following line to seed self.np_random
        # super().reset(seed=seed)
        # random.seed(seed)

        if options:
            print("reset options:", options)

        self._solved_before = 0

        # print("reset options:", options)
        self._extra_scramble_moves = 0

        self._extra_scramble_moves = round(
            np.tanh((self.steps / (self.total_steps+1))
                    ) * self._n_scramble_moves
        )

        if self._extra_scramble_moves > 0:
            if bool(random.getrandbits(1)):
                self._extra_scramble_moves = np.random.randint(
                    0, self._extra_scramble_moves)

        # if not self._has_reset_logged and self.steps % 500 < 100:
        #    self._has_reset_logged = True
        #    print("reset() steps extra_scramble_moves:",
        #          self._extra_scramble_moves)
            # print("asd", self.total_steps, self.steps)
        # else:
        #    self._has_reset_logged = False

        self.cube = Cube()

        self._solved_obs = self._get_flat_obs(
        ) if self._flat_obs else self._get_multi_dim_obs()

        scramble_moves = []
        while len(scramble_moves) != 1 + self._extra_scramble_moves:
            for i in range(0, 1 + self._extra_scramble_moves):
                scramble_moves.append(random.choice(self.base_moves))

                while i > 0 and scramble_moves[i-1] == scramble_moves[i]:
                    scramble_moves[i] = random.choice(self.base_moves)

        scramble_moves = " ".join([
            x + ("'" if bool(random.getrandbits(1)) else "")
            for x in scramble_moves
        ])

        if len(scramble_moves) < 1:
            print("Scramble moves 2 was less than 1")
            print("scramble_moves", scramble_moves)
            exit()
        # print("Scramble moves:", scramble_moves, self._extra_scramble_moves)

        # print("asd", self._extra_scramble_moves)

        self.cube.moves(scramble_moves)

        # set the scramble "distance to solved", 0 is solved, 1 is furthest away from solved
        self._scramble_distance = self._get_flat_info(
        )["distance"] if self._flat_obs else 1

        observation = self._get_flat_obs() if self._flat_obs else self._get_multi_dim_obs()

        # print("Got observation:", observation)
        # info = self._get_multi_dim_info()

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
    env.cube = Cube()
    print(env._get_multi_dim_info())
    print(env._get_multi_dim_obs().shape)

    # env.render()
    print("\nThen doing R U R:\n")
    env.cube.moves("R U R")
    print(env._get_multi_dim_info())
    print(env._get_multi_dim_obs())
    # env.render()
