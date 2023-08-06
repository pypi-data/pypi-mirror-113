import collections

import numpy as np
import gym


class GibsonHWC2CHW(gym.ObservationWrapper):
    def observation(self, obs):
        obs = obs.copy()  # shallow copy
        if 'rgb' in obs:
            obs['rgb'] = obs['rgb'].transpose(2, 0, 1)
        if 'normal' in obs:
            obs['normal'] = obs['normal'].transpose(2, 0, 1)
        return obs


class GibsonRGBFloat2Int(gym.ObservationWrapper):
    def observation(self, obs):
        obs = obs.copy()  # shallow copy
        if 'rgb' in obs:
            obs['rgb'] = (obs['rgb'] * 255.).astype(np.uint8)
        return obs


class SingleModality(gym.ObservationWrapper):
    def __init__(self, env, modality: str):
        super().__init__(env)
        self._modality = modality

    def observation(self, obs):
        assert isinstance(obs, collections.abc.Mapping)
        return obs[self._modality]