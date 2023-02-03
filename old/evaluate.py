from __future__ import annotations

import env
from c2 import Cube
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.ddpg.policies import MlpPolicy
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import BaseCallback
# from stable_baselines3 import DDPG
from gym.wrappers.time_limit import TimeLimit
from sb3_contrib import TQC
import numpy as np
import time
import torch as th

model = TQC.load("tqc_rubiks")

base_env = env.RubiksEnv(moves_per_step=1, n_scramble_moves=20)
check_env(base_env)

successes = 0
tries = 100
for i in range(0, tries):
    obs = base_env.reset()
    base_env.set_steps(20)
    base_env.set_total_steps(20)
    print(i, "First cube state:")
    base_env.render()
    for x in range(0, 300):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = base_env.step(action)
        if done:
            base_env.render()
            successes += 1
            print(i, x, "Done!")
            time.sleep(2)
            score = base_env._get_info()
            print("score:", score)
            print("Cube state at done:")
            obs = base_env.reset()
            break

print("Successes:", successes, "tries", tries)
