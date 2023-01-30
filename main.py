from __future__ import annotations

import env
from c2 import Cube
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.ddpg.policies import MlpPolicy
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines3.common.callbacks import BaseCallback
# from stable_baselines3.common.vec_env.subproc_vec_env import SubprocVecEnv
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
# from stable_baselines3.common.vec_env.base_vec_env import VecEnv
# from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
# from stable_baselines3 import DDPG
from gym.wrappers.time_limit import TimeLimit
# from sb3_contrib import TQC
from sb3_contrib import QRDQN
# from stable_baselines3 import PPO


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


def main():
    n_envs = 8
    log_interval = 100
    total_timesteps = np.int64(1e6)
    learning_starts = 100

    batch_size = 512  # 2**14
    max_moves_per_episode = 100
    n_scramble_moves = 50
    learning_rate = 3e-5

    pi = [256, 256]
    # qf = [512, 512, 512]

    top_quantiles_to_drop_per_net = 2
    n_critics = 2
    n_quantiles = 50
    gamma = 0.99
    tau = 0.005

    def create_env(*params):
        print("Create env params:", params)
        new_env = env.RubiksEnv(
            moves_per_step=1, n_scramble_moves=n_scramble_moves, max_moves=max_moves_per_episode)
        return Monitor(
            TimeLimit(new_env, max_episode_steps=max_moves_per_episode)
        )

    base_env = env.RubiksEnv(
        moves_per_step=1, n_scramble_moves=n_scramble_moves, max_moves=max_moves_per_episode)
    check_env(base_env)

    # wrapped_env = TimeLimit(base_env, max_episode_steps=max_moves_per_episode)

    envs = DummyVecEnv([create_env for _ in range(n_envs)])

    # VecMonitor(env, )
    policy_kwargs = dict(  # n_critics=n_critics, n_quantiles=n_quantiles,  # activation_fn=th.nn.ReLU,
        # vf doesnt exist on TQC (?)
        # pi = actor network, qf = critic network, vf = value network
        # net_arch=dict(pi=[256, 256], qf=[512, 512, 512])
        net_arch=pi,
        n_quantiles=50
        # net_arch=[32, 32]
    )

    # action_noise = OrnsteinUhlenbeckActionNoise(
    #    mean=np.zeros(wrapped_env.action_space.shape[-1]), sigma=float(0.2) * np.ones(wrapped_env.action_space.shape[-1]))

    # policy_kwargs = dict(n_critics=2, n_quantiles=25, n_env=)
    model = QRDQN("MlpPolicy",
                  envs,
                  verbose=1,
                  # top_quantiles_to_drop_per_net=top_quantiles_to_drop_per_net,
                  # ent_coef="auto",
                  # verbose=1,
                  # n_steps=total_timesteps,
                  # n_epochs=20,
                  learning_rate=learning_rate,
                  batch_size=batch_size,
                  # optimize_memory_usage=False,
                  # action_noise=action_noise,
                  policy_kwargs=policy_kwargs,
                  # learning_rate=learning_rate,
                  # learning_starts=learning_starts,
                  # gamma=gamma,
                  # tau=tau
                  )
    """
    n_epochs: int = 10, gamma: float = 0.99, gae_lambda: float = 0.95, clip_range: float | Schedule = 0.2, clip_range_vf: float | Schedule | None = None, normalize_advantage: bool = True, ent_coef: float = 0, vf_coef: float = 0.5, max_grad_norm: float = 0.5, use_sde: bool = False, sde_sample_freq: int = -1, target_kl: float | None = None
    """

    def callback(options):
        # print("options:", options)
        # wrapped_env.reset(options=options)
        # model.env.set_attr("cur_steps", options["steps"])
        # model.env.set_attr("total_steps", options["total_steps"])
        # model.env.set_attr("steps", options["steps"])
        # model.env.set_attr("total_steps", options["total_steps"])
        model.env.env_method("set_steps", options["steps"])
        model.env.env_method("set_total_steps", options["total_steps"])
        # print("in step:", model.env.get_attr("episode_returns"))
        # print(model.get_env().get_attr("base_moves"))
        # model.env.set_attr("base_moves", ["poop"])
        # print(model.env.get_attr("cur_steps"))
        # print(model.env.get_attr("total_steps"))
        # print()
        # if "episode" in options["infos"][0]:
        # model.env.env_method("reset", options=options)
        # model.env.set_attr("total_steps", options["total_steps"])
        # print("callback options:", options)
        # elif len(options["infos"][0]):
        #    print("wtf?", options)

    model.learn(total_timesteps=total_timesteps,
                log_interval=log_interval,
                progress_bar=True,
                callback=CustomCallback(callback, verbose=0)
                )
    model.save("tqc_rubiks")


if __name__ == "__main__":
    main()
