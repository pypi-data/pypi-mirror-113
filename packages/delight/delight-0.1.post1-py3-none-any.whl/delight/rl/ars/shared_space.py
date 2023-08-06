"""
Share global stats, like indices into the global noise table
"""

import ray
import numpy as np
from typing import List


@ray.remote
class SharedSpace:
    def __init__(self):
        self.positive_rewards: List[np.ndarray] = []
        self.negative_rewards: List[np.ndarray] = []
        self.noise_indices: List[np.ndarray] = []

    def push(
        self,
        noise_indices: List[np.ndarray],
        positive_rewards: List[np.ndarray],
        negative_rewards: List[np.ndarray],
    ):
        self.noise_indices.extend(noise_indices)
        self.positive_rewards.extend(positive_rewards)
        self.negative_rewards.extend(negative_rewards)

    def pull(self):
        assert (
            len(self.positive_rewards)
            == len(self.negative_rewards)
            == len(self.noise_indices)
        )
        return {
            "noise_indices": self.noise_indices,
            "positive_rewards": self.positive_rewards,
            "negative_rewards": self.negative_rewards,
        }

    def clear(self):
        self.positive_rewards = []
        self.negative_rewards = []
        self.noise_indices = []
