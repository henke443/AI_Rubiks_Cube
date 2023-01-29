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


class CustomCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """

    def __init__(self, callback, verbose=0):
        super(CustomCallback, self).__init__(verbose)
        self.callback = callback
        # Those variables will be accessible in the callback
        # (they are defined in the base class)
        # The RL model
        # self.model = None  # type: BaseRLModel
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env = None  # type: Union[gym.Env, VecEnv, None]
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = None  # type: Dict[str, Any]
        # self.globals = None  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger = None  # type: logger.Logger
        # # Sometimes, for event callback, it is useful
        # # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """

        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
        # print("_on_step:", self.locals, self.globals)
        self.callback({
            "steps": self.num_timesteps,
            "calls": self.n_calls,
            "total_steps": self.locals["total_timesteps"],
            "learning_starts": self.locals["learning_starts"] if "learning_starts" in self.locals else None,
            "rewards": self.locals["rewards"] if "rewards" in self.locals else None,
            "dones": self.locals["dones"] if "dones" in self.locals else None,
            "infos": self.locals["infos"] if "infos" in self.locals else None,
        })

        return True

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        pass

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass


base_env = env.RubiksEnv(moves_per_step=1)
check_env(base_env)

wrapped_env = TimeLimit(base_env, max_episode_steps=10)


param_noise = None
action_noise = None

policy_kwargs = dict(n_critics=2, n_quantiles=25,  # activation_fn=th.nn.ReLU,
                     # vf doesnt exist on TQC (?)
                     # pi = actor network, qf = critic network, vf = value network
                     # net_arch=dict(pi=[256, 256], qf=[512, 512, 512])
                     net_arch=dict(pi=[128, 128], qf=[256, 256, 256])
                     # net_arch=[32, 32]
                     )

action_noise = OrnsteinUhlenbeckActionNoise(
    mean=np.zeros(wrapped_env.action_space.shape[-1]), sigma=float(0.5) * np.ones(wrapped_env.action_space.shape[-1]))


# policy_kwargs = dict(n_critics=2, n_quantiles=25, n_env=)
model = TQC("MlpPolicy", wrapped_env,
            top_quantiles_to_drop_per_net=2,
            ent_coef="auto",
            verbose=1,
            # action_noise=action_noise,
            policy_kwargs=policy_kwargs,
            learning_rate=.001,
            learning_starts=1e2,
            gamma=0.99,
            tau=0.005)


def callback(options):
    # wrapped_env.reset(options=options)
    if "episode" in options["infos"][0]:
        model.env.env_method("reset", options=options)


model.learn(total_timesteps=2e4, log_interval=20,
            progress_bar=True,
            callback=CustomCallback(callback, verbose=0)
            )
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
