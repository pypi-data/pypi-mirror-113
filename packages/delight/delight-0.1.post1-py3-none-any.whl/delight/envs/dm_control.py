"""
Adapted from https://github.com/denisyarats/dmc2gym/tree/master/dmc2gym
Wrapper around dm_control
"""
import time

import numpy as np
import gym
from gym import core, spaces
from dm_control import suite
from dm_control.suite import ALL_TASKS as ALL_DM_CONTROL_TASKS
from dm_env import specs
from typing import Union, Tuple, Optional
from .wrappers import FrameStack, TimeLimit
from ._dm_patch import patch_dm_headless_egl_display


__all__ = ["make_dmc", "make_dmc_benchmark", "ALL_DM_CONTROL_TASKS", "DMControlWrapper"]


def make_dmc(
    name: Union[str, Tuple[str, str]],
    seed: Optional[int] = None,
    visualize_reward: bool = True,
    from_pixels: bool = False,
    image_height: int = 84,
    image_width: int = 84,
    camera_id: int = 0,
    frame_skip: int = 1,
    episode_length: int = 1000,
    environment_kwargs: Optional[dict] = None,
    time_limit: Optional[int] = None,
    channels_first: bool = True,
    device_id: Optional[int] = None,
):
    """
    Low-level make

    Args:
        name: full name "cheetah_run", or a tuple (domain, task): ("cheetah", "run")
    """
    patch_dm_headless_egl_display(device_id)

    assert isinstance(name, (str, tuple)), (
        "either specify full_name or a tuple (domain_name, task_name). "
        'Example: full_name "cheetah_run"  or ("cheetah", "run")'
    )

    domain_name, task_name = _full_name_to_domain_task(name)

    if from_pixels:
        assert (
            not visualize_reward
        ), "cannot use visualize reward when learning from pixels"

    # shorten episode length
    max_episode_steps = (episode_length + frame_skip - 1) // frame_skip

    task_kwargs = {}
    if seed is None:
        seed = int(time.time() * 1000000) % 1000000000
    else:
        assert isinstance(seed, int) and seed >= 0
    task_kwargs["random"] = seed
    if time_limit is not None:
        task_kwargs["time_limit"] = time_limit

    env = DMControlWrapper(
        domain_name=domain_name,
        task_name=task_name,
        task_kwargs=task_kwargs,
        environment_kwargs=environment_kwargs,
        visualize_reward=visualize_reward,
        from_pixels=from_pixels,
        height=image_height,
        width=image_width,
        camera_id=camera_id,
        frame_skip=frame_skip,
        channels_first=channels_first,
    )

    return TimeLimit(env, max_episode_steps=max_episode_steps)


def make_dmc_benchmark(
    name: Union[str, Tuple[str, str]],
    seed: Optional[int] = None,
    image_height: int = 84,
    image_width: int = 84,
    frame_skip: int = 4,
    frame_stack: Optional[int] = None,
    device_id: Optional[int] = None,
):
    """
    Add preprocessing wrappers to reproduce the settings in prior works
    Training on visual inputs
    """
    domain_name, task_name = _full_name_to_domain_task(name)
    # per dreamer: https://github.com/danijar/dreamer/blob/02f0210f5991c7710826ca7881f19c64a012290c/wrappers.py#L26
    camera_id = 2 if domain_name == "quadruped" else 0

    env = make_dmc(
        name=name,
        seed=seed,
        image_height=image_height,
        image_width=image_width,
        visualize_reward=False,
        from_pixels=True,
        frame_skip=frame_skip,
        camera_id=camera_id,
        device_id=device_id,
    )
    if frame_stack and frame_stack > 0:
        env = FrameStack(env, k=frame_stack)
    assert env.action_space.low.min() >= -1
    assert env.action_space.high.max() <= 1
    return env


def _full_name_to_domain_task(name):
    if isinstance(name, (tuple, list)):
        assert len(name) == 2
        return tuple(name)
    assert "_" in name
    if name == "ball_in_cup_catch":
        domain_name = "ball_in_cup"
        task_name = "catch"
    elif name == "point_mass_easy":
        domain_name = "point_mass"
        task_name = "easy"
    else:
        domain_name, task_name = name.split("_", 1)
    assert (
        domain_name,
        task_name,
    ) in ALL_DM_CONTROL_TASKS, f"task ({domain_name}, {task_name}) does not exist"
    return domain_name, task_name


def _spec_to_box(spec):
    def extract_min_max(s):
        assert s.dtype == np.float64 or s.dtype == np.float32
        dim = np.int(np.prod(s.shape))
        if type(s) == specs.Array:
            bound = np.inf * np.ones(dim, dtype=np.float32)
            return -bound, bound
        elif type(s) == specs.BoundedArray:
            zeros = np.zeros(dim, dtype=np.float32)
            return s.minimum + zeros, s.maximum + zeros

    mins, maxs = [], []
    for s in spec:
        mn, mx = extract_min_max(s)
        mins.append(mn)
        maxs.append(mx)
    low = np.concatenate(mins, axis=0)
    high = np.concatenate(maxs, axis=0)
    assert low.shape == high.shape
    return spaces.Box(low, high, dtype=np.float32)


def _flatten_obs(obs):
    obs_pieces = []
    for v in obs.values():
        flat = np.array([v]) if np.isscalar(v) else v.ravel()
        obs_pieces.append(flat)
    return np.concatenate(obs_pieces, axis=0)


class DMControlWrapper(core.Env):
    def __init__(
        self,
        domain_name,
        task_name,
        task_kwargs=None,
        visualize_reward={},
        from_pixels=False,
        height=84,
        width=84,
        camera_id=0,
        frame_skip=1,
        environment_kwargs=None,
        channels_first=True,
    ):
        assert (
            "random" in task_kwargs
        ), "please specify a seed, for deterministic behaviour"
        self._from_pixels = from_pixels
        self._height = height
        self._width = width
        self._camera_id = camera_id
        self._frame_skip = frame_skip
        self._channels_first = channels_first

        # create task
        self._env = suite.load(
            domain_name=domain_name,
            task_name=task_name,
            task_kwargs=task_kwargs,
            visualize_reward=visualize_reward,
            environment_kwargs=environment_kwargs,
        )

        # true and normalized action spaces
        self._true_action_space = _spec_to_box([self._env.action_spec()])
        self._norm_action_space = spaces.Box(
            low=-1.0, high=1.0, shape=self._true_action_space.shape, dtype=np.float32
        )

        # create observation space
        if from_pixels:
            shape = [3, height, width] if channels_first else [height, width, 3]
            self._observation_space = spaces.Box(
                low=0, high=255, shape=shape, dtype=np.uint8
            )
        else:
            self._observation_space = _spec_to_box(
                self._env.observation_spec().values()
            )

        self._state_space = _spec_to_box(self._env.observation_spec().values())

        self.current_state = None

        # set seed
        self.seed(seed=task_kwargs.get("random", 1))

    @property
    def unwrapped(self):
        return self._env

    def _get_obs(self, time_step):
        if self._from_pixels:
            obs = self.render(
                height=self._height, width=self._width, camera_id=self._camera_id
            )
            if self._channels_first:
                obs = obs.transpose(2, 0, 1).copy()
        else:
            obs = _flatten_obs(time_step.observation)
        return obs

    def _convert_action(self, action):
        action = action.astype(np.float64)
        true_delta = self._true_action_space.high - self._true_action_space.low
        norm_delta = self._norm_action_space.high - self._norm_action_space.low
        action = (action - self._norm_action_space.low) / norm_delta
        action = action * true_delta + self._true_action_space.low
        action = action.astype(np.float32)
        return action

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def state_space(self):
        return self._state_space

    @property
    def action_space(self):
        return self._norm_action_space

    def __getattr__(self, name):
        return getattr(self._env, name)

    def seed(self, seed):
        self._true_action_space.seed(seed)
        self._norm_action_space.seed(seed)
        self._observation_space.seed(seed)

    def step(self, action):
        assert self._norm_action_space.contains(action)
        action = self._convert_action(action)
        assert self._true_action_space.contains(action)
        reward = 0
        extra = {"internal_state": self._env.physics.get_state().copy()}

        for _ in range(self._frame_skip):
            time_step = self._env.step(action)
            reward += time_step.reward or 0
            done = time_step.last()
            if done:
                break
        obs = self._get_obs(time_step)
        self.current_state = _flatten_obs(time_step.observation)
        extra["discount"] = time_step.discount
        return obs, reward, done, extra

    def reset(self):
        time_step = self._env.reset()
        self.current_state = _flatten_obs(time_step.observation)
        obs = self._get_obs(time_step)
        return obs

    def render(self, mode="rgb_array", height=None, width=None, camera_id=0):
        assert mode == "rgb_array", "only support rgb_array mode, given %s" % mode
        height = height or self._height
        width = width or self._width
        camera_id = camera_id or self._camera_id
        return self._env.physics.render(height=height, width=width, camera_id=camera_id)
