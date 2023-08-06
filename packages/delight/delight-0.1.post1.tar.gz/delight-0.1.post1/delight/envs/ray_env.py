import gym

try:
    import ray
except ImportError:
    pass

import numpy as np
from typing import Optional, Tuple, List, Callable, Union, Dict
from .vec_env import BaseVectorEnv, _run_preamble


__all__ = ["RayVectorEnv"]


@ray.remote
class _RayEnvWrapper:
    def __init__(self, env_fn, disable_gym_warnings, gpu_id, os_envs):
        _run_preamble(
            disable_gym_warnings=disable_gym_warnings, gpu_id=gpu_id, os_envs=os_envs,
        )
        self.env = env_fn()

    def reset(self):
        return self.env.reset()

    def step(self, *args, **kwargs):
        return self.env.step(*args, **kwargs)

    def seed(self, *args, **kwargs):
        return self.env.seed(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self.env.render(*args, **kwargs)

    def close(self):
        return self.env.close()


class RayVectorEnv(BaseVectorEnv):
    """Vectorized environment wrapper based on
    `ray <https://github.com/ray-project/ray>`_. However, according to our
    test, it is about two times slower than
    :class:`~tianshou.env.SubprocVectorEnv`.

    .. seealso::

        Please refer to :class:`~tianshou.env.BaseVectorEnv` for more detailed
        explanation.
    """

    def __init__(
        self,
        env_fns: List[Callable[[], gym.Env]],
        obs_dtype=None,
        reward_dtype=None,
        done_dtype=None,
        disable_gym_warnings: bool = True,
        gpu_id=None,
        os_envs=None,
    ) -> None:
        super().__init__(
            env_fns,
            obs_dtype=obs_dtype,
            reward_dtype=reward_dtype,
            done_dtype=done_dtype,
        )
        try:
            if not ray.is_initialized():
                ray.init()
        except NameError:
            raise ImportError(
                "Please install ray to support RayVectorEnv: pip3 install ray"
            )
        self.envs = [
            _RayEnvWrapper.remote(e, disable_gym_warnings, gpu_id, os_envs)
            for e in env_fns
        ]
        self._reset_obj_ids = [None] * self.num_envs

    def step(
        self, action: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[Dict]]:
        assert len(action) == self.num_envs
        result = ray.get([e.step.remote(a) for e, a in zip(self.envs, action)])
        obs, rew, done, info = zip(*result)
        return self._stack_step(obs, rew, done, info)

    def reset_request(self, i: int):
        self._reset_obj_ids[i] = self.envs[i].reset.remote()

    def reset_get(self, i: int):
        return ray.get(self._reset_obj_ids[i])

    def seed(self, seed: Optional[Union[int, List[int]]] = None) -> None:
        if not hasattr(self.envs[0], "seed"):
            return
        if np.isscalar(seed):
            seed = [seed + _ for _ in range(self.num_envs)]
        elif seed is None:
            seed = [seed] * self.num_envs
        return ray.get([e.seed.remote(s) for e, s in zip(self.envs, seed)])

    def render(self, **kwargs) -> None:
        if not hasattr(self.envs[0], "render"):
            return
        return ray.get([e.render.remote(**kwargs) for e in self.envs])

    def close(self) -> None:
        return ray.get([e.close.remote() for e in self.envs])
