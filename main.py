import env
from c2 import Cube
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.ddpg.policies import MlpPolicy
# from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
# from stable_baselines3 import DDPG
from gym.wrappers.time_limit import TimeLimit
from sb3_contrib import TQC
import numpy as np
import time
import torch as th

base_env = env.RubiksEnv(moves_per_step=1)
check_env(base_env)

wrapped_env = TimeLimit(base_env, max_episode_steps=200)


param_noise = None
action_noise = None

policy_kwargs = dict(n_critics=2, n_quantiles=25,  # activation_fn=th.nn.ReLU,
                     # vf doesnt exist on TQC (?)
                     # pi = actor network, qf = critic network, vf = value network
                     net_arch=dict(pi=[256, 256], qf=[512, 512, 512])
                     # net_arch=[32, 32]
                     )

# policy_kwargs = dict(n_critics=2, n_quantiles=25, n_env=)
model = TQC("MlpPolicy", wrapped_env,
            top_quantiles_to_drop_per_net=2,
            ent_coef="auto",
            verbose=3,
            policy_kwargs=policy_kwargs,
            learning_rate=.0003,
            learning_starts=50,
            gamma=0.99,
            tau=0.005)

model.learn(total_timesteps=250000, log_interval=5, progress_bar=True)
model.save("tqc_rubiks")

del model  # remove to demonstrate saving and loading

model = TQC.load("tqc_rubiks")

for i in range(0, 10):
    obs = base_env.reset()
    print(i, "First cube state:")
    base_env.cube.print()
    for x in range(0, 300):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = base_env.step(action)
        if x % 50 == 0:
            print(i, x,  "reward:", reward)
            base_env.cube.print()
        if done:
            print(i, x, "Done!")
            time.sleep(2)
            score = base_env._get_info()
            print("score:", score)
            print("Cube state at done:")
            obs = base_env.reset()


# exit()
""" 
sys.modules["gym"] = gym


env = env.RubiksEnv(moves_per_step=1)
check_env(env)

# Define and Train the agent
model = A2C('CnnPolicy', env).learn(total_timesteps=1000)


env = gym.make('MountainCarContinuous-v0')

# the noise objects for DDPG
n_actions = env.action_space.shape[-1]
param_noise = None
action_noise = OrnsteinUhlenbeckActionNoise(
    mean=np.zeros(n_actions), sigma=float(0.5) * np.ones(n_actions))

model = DDPG(MlpPolicy, env, verbose=1,
             param_noise=param_noise, action_noise=action_noise)
model.learn(total_timesteps=400000)
model.save("ddpg_mountain")

del model  # remove to demonstrate saving and loading

model = DDPG.load("ddpg_mountain")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()


cube = Cube()
cube.print()
cube.print("both")
exit()
 """
