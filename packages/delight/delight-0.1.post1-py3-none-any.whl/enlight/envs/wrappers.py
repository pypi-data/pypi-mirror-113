import numpy as np
from collections import deque
import gym


class FrameStack(gym.Wrapper):
    def __init__(self, env, k, generate_obs_space: bool = True):
        super().__init__(env)
        self._k = k
        self._frames = deque([], maxlen=k)
        if generate_obs_space:
            shp = env.observation_space.shape
            self.observation_space = gym.spaces.Box(
                low=0,
                high=1,
                shape=((shp[0] * k,) + shp[1:]),
                dtype=env.observation_space.dtype,
            )
            # FIXME:
            self._max_episode_steps = env._max_episode_steps

    def reset(self):
        obs = self.env.reset()
        for _ in range(self._k):
            self._frames.append(obs)
        return self._get_obs()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self._frames.append(obs)
        return self._get_obs(), reward, done, info

    def _get_obs(self):
        assert len(self._frames) == self._k
        return np.concatenate(list(self._frames), axis=0)


class TimeLimit(gym.Wrapper):
    def __init__(self, env, max_episode_steps=None):
        super().__init__(env)
        self._max_episode_steps = max_episode_steps
        self._elapsed_steps = 0

    def step(self, ac):
        observation, reward, done, info = self.env.step(ac)
        self._elapsed_steps += 1
        if (
            self._max_episode_steps is not None
            and self._elapsed_steps >= self._max_episode_steps
        ):
            done = True
            info["timeout"] = True
        return observation, reward, done, info

    def reset(self, **kwargs):
        self._elapsed_steps = 0
        return self.env.reset(**kwargs)


# Checks whether done was caused my time limits or not
class TimeLimitInfo(gym.Wrapper):
    def __getattr__(self, name):
        return getattr(self.env, name)

    def step(self, action):
        obs, rew, done, info = self.env.step(action)
        if done and self.env._max_episode_steps == self.env._elapsed_steps:
            info["timeout"] = True
        return obs, rew, done, info

    def reset(self, **kwargs):
        assert hasattr(self.env, "_max_episode_steps") and hasattr(
            self.env, "_elapsed_steps"
        ), f"env must have `_max_episode_steps` and `_elapsed_steps` to be compatible with {self.__class__.__name__}. These two variables are added by gym.wrappers.TimeLimit. If your env is registered with gym, it should have this wrapper added."
        return self.env.reset(**kwargs)
