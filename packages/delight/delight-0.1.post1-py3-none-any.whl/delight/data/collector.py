import math
import numpy as np
import torch

from enlight.envs import BaseVectorEnv
from typing import *


def dummy_preprocess_func(**kwargs):
    return kwargs


class Collector:
    def __init__(
        self,
        env: BaseVectorEnv,
        act_fn: Optional[Callable],
        buffer=None,
        preprocess_fn: Callable[..., Dict[str, Any]] = None,
    ):
        self.env = env
        self.act_fn = act_fn
        self.buffer = buffer
        self.obs = None
        self.num_episodes = 0
        self.num_steps = 0
        self.ep_rewards = np.zeros((self.num_envs,))
        self.all_ep_rewards = []
        if preprocess_fn is None:
            preprocess_fn = dummy_preprocess_func
        self.preprocess_fn = preprocess_fn

    def collect(self, n_steps=None, n_episodes=None):
        assert (n_steps is None) != (
            n_episodes is None
        ), "you can specify only one of n_steps and n_episodes, not both."
        raise NotImplementedError

    @property
    def num_envs(self):
        return len(self.env)

    @property
    def num_vec_steps(self):
        return self.num_steps // self.num_envs

    @staticmethod
    def num_dones(done):
        return int(np.sum(done))

    @staticmethod
    def get_done_idx(done):
        return np.where(done)[0]

    def set_act_fn(self, new_act_fn):
        self.act_fn = new_act_fn

    def reset(self):
        self.obs = self.env.reset()
        self.ep_rewards = np.zeros((self.num_envs,))
        self.all_ep_rewards = []
        self.num_episodes = 0
        self.num_steps = 0

    def collect_episodes(self, n_episodes, act_fn=None):
        """
        For eval
        Args:
            act_fn: can override self.act_fn
        # TODO add_to_buffer: bool turn off adding to buffer
        """
        if act_fn is None:
            act_fn = self.act_fn
        assert (
            act_fn is not None
        ), "please specify act_fn by set_act_fn() or pass in `act_fn` arg"
        completed = 0
        ep_rewards = np.zeros(self.num_envs, dtype=np.float32)
        all_rewards = []
        assert n_episodes >= 1
        obs = self.env.reset()
        while completed < n_episodes:
            with torch.no_grad():
                action = act_fn(obs)

            obs, reward, done, info = self.env.step(action)
            ep_rewards += reward

            n_done = self.num_dones(done)
            if n_done > 0:
                done_idx = self.get_done_idx(done)
                obs = self.env.reset(done_idx)
                all_rewards.extend(ep_rewards[done_idx])
                ep_rewards[done_idx] = 0.0

            completed += n_done
        all_rewards = np.array(all_rewards)
        return {
            "episode_reward_mean": np.mean(all_rewards),
            "episode_reward_std": np.std(all_rewards),
            "episode_rewards": [float(r) for r in all_rewards],
        }

    def collect_one_episode(
        self, min_completed=None, act_fn=None, add_to_buffer: bool = True
    ):
        """
        For eval
        Args:
            act_fn: can override self.act_fn
            min_completed: return when the minimal number of envs have completed their
                episode. Must be between 1 and num_envs. Useful to handle slow stragglers
                None to wait for all envs to finish one episode.
            add_to_buffer: bool
                will only add experience for the first episode
        """
        if act_fn is None:
            act_fn = self.act_fn
        assert (
            act_fn is not None
        ), "please specify act_fn by set_act_fn() or pass in `act_fn` arg"
        if min_completed is None:
            total = self.num_envs  # must complete all envs
        else:
            assert 1 <= min_completed <= self.num_envs
            total = min_completed
        if add_to_buffer:
            assert self.buffer is not None

        ep_rewards = np.zeros(self.num_envs, dtype=np.float64)
        ep_dones = np.zeros(self.num_envs, dtype=np.float32)
        ep_steps = np.zeros(self.num_envs, dtype=np.float32)

        obs = self.env.reset()

        while sum(ep_dones) < total:
            with torch.no_grad():
                action = act_fn(obs)

            obs_next, reward, done, info = self.env.step(action)
            not_done_mask = 1.0 - ep_dones
            ep_rewards += reward * not_done_mask
            ep_steps += not_done_mask

            if add_to_buffer:
                for i in self.get_done_idx(not_done_mask):
                    value_dict = self.preprocess_fn(
                        obs=obs[i],
                        action=action[i],
                        reward=reward[i],
                        obs_next=obs_next[i],
                        done=done[i],
                        info=info[i],
                    )
                    self.buffer.add(**value_dict, vectorize=False)

            n_done = self.num_dones(done)
            if n_done > 0:
                done_idx = self.get_done_idx(done)
                obs_next = self.env.reset(done_idx)
                ep_dones[done_idx] = 1.0

            obs = obs_next

        return {
            "episode_rewards": ep_rewards,
            "episode_dones": ep_dones,
            "episode_steps": ep_steps,
        }

    def collect_one_vec_step(self, act_fn=None):
        """
        Can temporarily override act_fn
        # TODO add_to_buffer: bool turn off adding to buffer
        """
        if act_fn is None:
            act_fn = self.act_fn
        assert act_fn is not None, (
            "please specify act_fn by set_act_fn() " "or pass in `act_fn` arg"
        )
        assert self.buffer is not None
        assert self.obs is not None, "you should call collector.reset() first"
        with torch.no_grad():
            action = act_fn(self.obs)

        obs_next, reward, done, info = self.env.step(action)
        assert len(self.ep_rewards) == len(reward)
        self.ep_rewards += reward

        assert len(self.obs) == len(obs_next) == self.num_envs
        for i in range(self.num_envs):
            value_dict = self.preprocess_fn(
                obs=self.obs[i],
                action=action[i],
                reward=reward[i],
                obs_next=obs_next[i],
                done=done[i],
                info=info[i],
            )
            # FIXME: vectorize add
            self.buffer.add(**value_dict, vectorize=False)

        ep_rewards = []
        n_done = self.num_dones(done)
        if n_done > 0:
            done_idx = self.get_done_idx(done)
            obs_next = self.env.reset(done_idx)
            self.num_episodes += n_done
            ep_rewards.extend(self.ep_rewards[done_idx])
            self.all_ep_rewards.extend(ep_rewards)
            self.ep_rewards[done_idx] = 0.0

        self.num_steps += self.num_envs
        self.obs = obs_next

        return ep_rewards

    def collect_steps(self, *, n_steps=None, n_vec_steps=None, act_fn=None):
        assert bool(n_steps is None) != bool(n_vec_steps is None), (
            "you must specify one and only one of `n_steps` or `n_vec_steps`. "
            "one `vec_step` is equivalent to num_env `step`s"
        )
        if n_steps is None:
            n_vec_steps = int(n_vec_steps)
        else:
            n_vec_steps = math.ceil(n_steps / self.num_envs)
        assert n_vec_steps >= 1
        ep_rewards = []
        for _ in range(n_vec_steps):
            epr = self.collect_one_vec_step(act_fn=act_fn)
            ep_rewards.extend(epr)
        return ep_rewards
