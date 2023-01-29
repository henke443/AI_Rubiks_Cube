import env
from c2 import Cube
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.ddpg.policies import MlpPolicy
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
# from stable_baselines3 import DDPG
from gym.wrappers.time_limit import TimeLimit
from sb3_contrib import TQC
import numpy as np
import time
import torch as th

base_env = env.RubiksEnv(moves_per_step=1)
check_env(base_env)

wrapped_env = TimeLimit(base_env, max_episode_steps=20)


param_noise = None
action_noise = None

policy_kwargs = dict(n_critics=2, n_quantiles=25,  # activation_fn=th.nn.ReLU,
                     # vf doesnt exist on TQC (?)
                     # pi = actor network, qf = critic network, vf = value network
                     net_arch=dict(pi=[256, 256], qf=[512, 512, 512])
                     # net_arch=[32, 32]
                     )

action_noise = OrnsteinUhlenbeckActionNoise(
    mean=np.zeros(wrapped_env.action_space.shape[-1]), sigma=float(0.5) * np.ones(wrapped_env.action_space.shape[-1]))


# policy_kwargs = dict(n_critics=2, n_quantiles=25, n_env=)
model = TQC("MlpPolicy", wrapped_env,
            top_quantiles_to_drop_per_net=2,
            ent_coef="auto",
            verbose=3,
            action_noise=action_noise,
            policy_kwargs=policy_kwargs,
            learning_rate=.001,
            learning_starts=1e4,
            gamma=0.99,
            tau=0.005)


def callback(arg1, arg2):
    print("local self:", arg1.self)


model.learn(total_timesteps=1e4+1e5, log_interval=20,
            progress_bar=True, callback=callback)
model.save("tqc_rubiks")


print(env.get_attr("best_found"))
print(max(env.get_attr("best_found")))


del model  # remove to demonstrate saving and loading

model = TQC.load("tqc_rubiks")

for i in range(0, 100):
    obs = base_env.reset()
    print(i, "First cube state:")
    base_env.render()
    for x in range(0, 50):
        action, _states = model.predict(obs, deterministic=False)
        obs, reward, done, info = base_env.step(action)
        if x % 10 == 0:
            print(i, x,  "reward:", reward)
            base_env.render()
        if done:
            print(i, x, "Done!")
            time.sleep(2)
            score = base_env._get_info()
            print("score:", score)
            print("Cube state at done:")
            obs = base_env.reset()
            exit()
