import numpy as np
import env
import copy


class RubiksGame:

    def __init__(self):
        self.env = env.RubiksEnv(
            moves_per_step=1, n_scramble_moves=5, obs_dim="flat")
        self.env.steps = 1
        self.env.total_steps = 10000
        self.env.reset(fixed_extra_scrambles=-1)

        self.correct_state = copy.copy(self.env._solved_obs)

        print("correct state:", self.correct_state)

    def get_init_board(self, step=None, total_steps=None):
        if not step:
            self.env._load_obs(self.correct_state)
            self.env.reset(fixed_extra_scrambles=0)
        else:
            self.env._load_obs(self.correct_state)
            self.env.steps = step
            self.env.total_steps = total_steps
            self.env.reset()
            if self.env._extra_scramble_moves > 0:
                print("extra_scrambles:", self.env._extra_scramble_moves)

        return self.env._get_obs()

    def get_board_size(self):
        return self.env.observation_space.shape[0]

    def get_valid_moves(self, board):
        # All moves are invalid by default
        valid_moves = [1] * self.get_action_size()

        return valid_moves

    def get_action_size(self):
        return self.env.action_space.n

    def get_next_state(self, state, action, total_moves=0):
        before_data = self.env._get_obs()
        self.env._load_obs(state)

        self.env.cube.total_moves = self.env._extra_scramble_moves + total_moves

        self.env.cube.moves(self.env._discrete_action_to_action(action))
        to_return = self.env._get_obs()
        self.env._load_obs(before_data)
        # print("get_next_state action", action)
        # print("get_next_state prev state", state)
        # print("get_next_state after state", to_return)
        return to_return

    def is_win(self):
        if self.env._get_info()["distance"] == 0:
            return True

        return False

    def get_reward(self, state):
        before_data = self.env._get_obs()
        self.env._load_obs(state)
        score = self.env._get_info()["score"]
        # if score > 0:
        # print("reward state\n", state)
        # print("score", score)
        self.env._load_obs(before_data)
        return None if score < 0 else score


if __name__ == "__main__":
    game = RubiksGame()
    print(game.get_init_board())
    print(game.get_board_size())
    print(game.get_action_size())
