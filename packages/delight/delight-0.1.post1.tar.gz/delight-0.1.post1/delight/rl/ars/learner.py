import sys
import time
from pprint import pprint

import numpy as np
import ray
import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F
from typing import Any, Union, Optional, Dict, List, ClassVar, Tuple
import omlet.utils as U
from omlet.distributed import get_worker_context
from .shared_noise import SharedNoiseTable
from .shared_space import SharedSpace


__all__ = ["ARSLearner"]


class ARSLearner:
    def __init__(
        self,
        encoder: nn.Module,
        selfsup: nn.Module,
        selfsup_lr: float,
        ars_lr: float,
        input_dim: int,
        action_shape: Tuple[int],
        action_range,
        delta_std: float,  # perturb std
        num_envs: int,
        num_deltas: int,
        top_k_deltas: int,
        shared_space: SharedSpace,
        shared_noise: np.ndarray,
        seed: int,
    ):
        """
        NOTE:
            num_envs, num_deltas, top_k_deltas are for *single* process
            actual deltas are 2*deltas due to mirroring perturbations
        """
        assert ray.is_initialized()
        self.ctx = get_worker_context()
        self.encoder = encoder.to(self.ctx.device)
        self.selfsup = self.ctx.data_parallel(selfsup)
        self.selfsup_optimizer = torch.optim.Adam(
            self.selfsup.parameters(), lr=selfsup_lr
        )
        self.ars_lr = ars_lr
        self.input_dim = input_dim
        self.action_dim = action_shape[0]
        self.action_range = action_range
        self.policy = torch.zeros((self.action_dim, input_dim), device=self.ctx.device)
        self.delta_std = delta_std
        assert num_envs <= num_deltas * 2
        assert top_k_deltas <= num_deltas
        # TODO: we can lift this restriction later
        assert num_envs % 2 == 0 and num_deltas % (num_envs // 2) == 0  # mirroring
        self.num_deltas = num_deltas
        self.num_envs = num_envs
        self.top_k_deltas = top_k_deltas
        self.shared_space = shared_space
        self.noise_table = SharedNoiseTable(
            shared_noise,
            policy_shape=(self.action_dim, self.input_dim),
            seed=seed + 17 * self.ctx.global_rank,
        )
        self._perturbed_policy = None  # (N, action_dim, input_dim)
        # only active for master process, collected from all workers
        self._results: Dict[str, List[np.ndarray]] = {
            "noise_indices": [],
            "positive_rewards": [],
            "negative_rewards": [],
        }

    def broadcast_policy(self):
        self.ctx.broadcast(self.policy)  # from master to all workers
        if self.is_master:
            ray.get(self.shared_space.clear.remote())
        self._perturbed_policy = None
        self.barrier()

    def perturb_policy(self, n: int):
        self._perturbed_policy, _noise_indices = self.noise_table.perturb_policy(
            self.policy, delta_std=self.delta_std, n=n, mirror=True
        )
        self._results["noise_indices"].append(_noise_indices)

    def clear(self):
        for key in self._results:
            self._results[key] = []

    @property
    def all_num_deltas(self):
        return self.num_deltas * self.ctx.world_size

    @property
    def all_top_k_deltas(self):
        return self.top_k_deltas * self.ctx.world_size

    def gather_results(self):
        """
        Call after all num_deltas are collected
        """
        # for non-master processes, submit to shared space
        if not self.is_master:
            # force execute
            ray.get(self.shared_space.push.remote(**self._results))
        self.barrier()
        results = {}
        if self.is_master:
            other_results = ray.get(self.shared_space.pull.remote())
            for key in self._results.keys():
                results[key] = other_results[key]
                results[key].extend(self._results[key])
                results[key] = np.concatenate(results[key])
                assert len(results[key]) == self.all_num_deltas
        self.clear()
        return results

    @property
    def is_master(self):
        return self.ctx.is_global_master()

    def barrier(self):
        self.ctx.barrier()

    def act_perturbed(self, obs):
        # obs is 2*N due to mirroring
        assert obs.shape[0] == self.num_envs
        assert self._perturbed_policy.size(0) == obs.shape[0]
        with torch.no_grad():
            obs = U.any_to_torch_tensor(
                obs, dtype=torch.float32, device=self.ctx.device
            )
            h = self.encoder(obs)
            assert h.ndim == 2
            actions = torch.bmm(self._perturbed_policy, h.unsqueeze(2)).squeeze(2)
            actions = actions.clamp(*self.action_range)
            return U.any_to_numpy(actions)

    def dprint(self, *args):
        if self.ctx.is_global_master():
            print(*args)

    def update_ars(self, collector):
        """
        Run a single gradient update on ARS policy
        """
        completed = 0
        timer = U.Timer()
        self.broadcast_policy()
        while completed < self.num_deltas:
            timer.start()
            # maximal deltas we can process at one time is num_envs//2 for mirroring
            n = self.num_envs // 2
            self.perturb_policy(n)
            results = collector.collect_one_episode(
                act_fn=self.act_perturbed, add_to_buffer=True
            )
            assert np.sum(results["episode_dones"]) == self.num_envs
            # first half of rewards are from positive perturbations
            # second half are negatives
            pos, neg = np.split(results["episode_rewards"], 2)
            assert pos.shape[0] == neg.shape[0] == n
            self._results["positive_rewards"].append(pos)
            self._results["negative_rewards"].append(neg)
            completed += n
            self.dprint("inference one episode", timer.elapsed_str())

        all_results = self.gather_results()  # also clear the result buffers
        return self.update_policy(all_results)

    def update_policy(self, results):
        if not self.is_master:
            return

        rewards = np.stack(
            [results["positive_rewards"], results["negative_rewards"]], axis=1
        )
        num_deltas = self.all_num_deltas
        top_k_deltas = self.all_top_k_deltas
        assert rewards.shape == (num_deltas, 2)
        max_rewards = np.max(rewards, axis=1)
        assert max_rewards.shape == (num_deltas,)

        idx = np.arange(max_rewards.size)[
            max_rewards
            >= np.percentile(max_rewards, 100 * (1 - (top_k_deltas / num_deltas)))
        ]
        noise_ids = results["noise_indices"][idx]
        rollout_rewards = rewards[idx, :]

        # normalize rewards by their standard deviation
        rollout_rewards /= np.std(rollout_rewards)

        # aggregate rollouts to form g_hat, the gradient used to compute SGD step
        self.dprint(rollout_rewards.shape)
        # FIXME: make batched_weighted_sum on torch GPU
        g_hat, count = self.batched_weighted_sum(
            rollout_rewards[:, 0] - rollout_rewards[:, 1],
            (self.noise_table.get(idx, reshape=False).numpy() for idx in noise_ids),
            batch_size=500,
        )
        g_hat /= noise_ids.size
        self.dprint("Euclidean norm of update step:", np.linalg.norm(g_hat))
        g_hat = U.any_to_torch_tensor(
            g_hat, dtype=torch.float32, device=self.policy.device
        )
        g_hat = g_hat.view(self.policy.size())
        self.policy += self.ars_lr * g_hat
        return {
            'episode_reward_mean': np.mean(rewards),
            'episode_reward_max': np.max(rewards),
            'episode_reward_min': np.min(rewards),
            'episode_reward_std': np.std(rewards),
        }

    @staticmethod
    def itergroups(items, group_size):
        assert group_size >= 1
        group = []
        for x in items:
            group.append(x)
            if len(group) == group_size:
                yield tuple(group)
                del group[:]
        if group:
            yield tuple(group)

    def batched_weighted_sum(self, weights, vecs, batch_size):
        total = 0
        num_items_summed = 0
        for batch_weights, batch_vecs in zip(
            self.itergroups(weights, batch_size), self.itergroups(vecs, batch_size)
        ):
            assert len(batch_weights) == len(batch_vecs) <= batch_size
            total += np.dot(
                np.asarray(batch_weights, dtype=np.float64),
                np.asarray(batch_vecs, dtype=np.float64),
            )
            num_items_summed += len(batch_weights)
        return total, num_items_summed

    def update_selfsup(self, replay_dataset):
        batch = next(replay_dataset)
        assert isinstance(batch.obs, tuple)
        assert isinstance(batch.obs_next, tuple)
        assert len(batch.obs) == len(batch.obs_next)

        self.selfsup.train()
        pred_action, pred_reward = self.selfsup(batch.obs[0], batch.obs_next[0])
        action_loss = F.mse_loss(pred_action, batch.action)
        reward_loss = F.mse_loss(pred_reward, batch.reward)
        selfsup_loss = action_loss + reward_loss * 10.0
        self.selfsup_optimizer.zero_grad()
        selfsup_loss.backward()
        self.selfsup_optimizer.step()
        return {
            "reward/train_batch": batch.reward.mean(),
            "train/selfsup_loss": selfsup_loss,
            "train/pred_action_loss": action_loss,
            "train/pred_reward_loss": reward_loss,
        }
