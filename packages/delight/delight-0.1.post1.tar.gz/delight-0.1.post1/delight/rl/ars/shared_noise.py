# Code in this file is copied and adapted from
# https://github.com/ray-project/ray/tree/master/python/ray/rllib/es
from typing import Optional

import ray
import numpy as np
import torch


@ray.remote
def create_shared_noise():
    """
    Create a large array of noise to be shared by all workers. Used
    for avoiding the communication of the random perturbations delta.
    """

    seed = 12345
    count = 250000000
    # TODO does it need to be float64?
    noise = np.random.RandomState(seed).randn(count).astype(np.float32)
    return noise


class SharedNoiseTable(object):
    def __init__(self, noise, policy_shape, seed=11):
        """
        Args:
            policy_shape: (action_dim, obs_dim)
        """
        self.rg = np.random.RandomState(seed)
        self.noise = noise
        self.policy_shape = policy_shape
        self._num_elems = np.prod(policy_shape)

    @property
    def max_index(self):
        return len(self.noise) - self._num_elems

    def __getitem__(self, i):
        return self.get(i, reshape=True)

    def get(self, i, reshape=True):
        assert i <= self.max_index, f"index {i} must be smaller than {self.max_index}"
        noise = torch.from_numpy(self.noise[i : i + self._num_elems])
        if reshape:
            return noise.view(self.policy_shape)
        else:
            return noise

    def sample_index(self):
        return self.rg.randint(0, self.max_index + 1)

    def sample(self, n: Optional[int] = None):
        """
        Args:
            n: None: sample only one noise matrix, without batch dimension
                int: return (n, *policy_shape)
        """
        if n is None:
            idx = self.sample_index()
            return self[idx], idx
        else:
            assert n >= 1
            indices = self.rg.choice(self.max_index + 1, n, replace=False)
            noises = [self[i] for i in indices]
            return torch.stack(noises, dim=0), indices

    def perturb_policy(
        self, policy: torch.Tensor, delta_std: float, n: int, mirror: bool = True
    ):
        """
        policy + delta_std
        policy - delta_std

        Returns:
            (2*N, *policy_shape) if mirror else (N, *policy_shape)
        """
        assert n >= 1
        assert policy.size() == self.policy_shape
        with torch.no_grad():
            noises, indices = self.sample(n)
            if policy.is_cuda:
                noises = noises.to(policy.device)
            if mirror:
                noises = torch.cat([noises, -noises], dim=0)
            return noises * delta_std + policy, indices
