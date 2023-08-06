import collections
import pprint
import numpy as np
from copy import deepcopy
from typing import Tuple, Union, Optional, Dict, List
from .core import StreamReplayDataset
from omlet.data import DataDict


class SimpleReplayBuffer:
    def __init__(
        self, capacity: int, dtype: Union[Dict[str, Union[str, type]], None] = None,
    ):
        self.capacity = capacity
        self._size = 0
        self._pointer = 0
        if dtype is None:
            dtype = {}
        self.dtype = dtype
        self.data = None

    def clear(self):
        self._size = 0
        self._pointer = 0
        self.data = None

    def __len__(self) -> int:
        """Return len(self)."""
        return self._size

    def __repr__(self) -> str:
        s = repr(self.data)
        if s.startswith("DataDict"):
            s = "SimpleReplayBuffer" + s[len("DataDict") :]
        return s

    def __getattr__(self, name: str):
        return self.data[name]

    def __getitem__(self, index):
        return self.data[index]

    def add(
        self,
        obs: Union[dict, np.ndarray, List[dict], List[np.ndarray]],
        action: Union[np.ndarray, List[np.ndarray]],
        reward: Union[float, np.ndarray, List[float]],
        done: Union[bool, np.ndarray, List[bool]],
        obs_next: Union[dict, np.ndarray, List[dict], List[np.ndarray]],
        info: Union[dict, List[dict]],
        vectorize: bool = True,
    ):
        if not vectorize:
            obs = [obs]
            action = [action]
            reward = [reward]
            done = [done]
            obs_next = [obs_next]
            info = [info]

        batch_size = len(obs)
        assert batch_size < self.capacity

        batch = DataDict(
            obs=obs,
            action=action,
            reward=reward,
            done=done,
            obs_next=obs_next,
            info=info,
        )

        for key in ["obs", "obs_next"]:
            if DataDict.is_mapping(batch[key][0]):
                batch[key] = DataDict.multi_map(lambda *v: np.stack(v), *batch[key])

        batch.map(
            lambda v: np.stack(v) if DataDict.is_primitive_array(v) else v,
            inplace=True,
        )
        if self.data is None:
            batch.to_numpy(dtype=self.dtype, inplace=True, copy=False)
            # initiate the replay buffer by inferring types from the first batch
            self.data = batch.map(
                # first dim of the shape is batch_size
                lambda v: np.zeros((self.capacity, *v.shape[1:]), v.dtype),
                inplace=False,
            )

        wrap_around = self._pointer + batch_size - self.capacity
        if wrap_around <= 0:
            self.data[self._pointer : self._pointer + batch_size] = batch
            self._pointer += batch_size
        else:
            self.data[self._pointer :] = batch[: batch_size - wrap_around]
            self.data[:wrap_around] = batch[batch_size - wrap_around :]
            self._pointer = wrap_around

        self._size = min(self._size + batch_size, self.capacity)

    def sample(self, batch_size: int, replace: bool = True, with_indices: bool = False):
        if batch_size > self._size:
            assert replace, (
                f"batch size {batch_size} > replay size {self._size}, "
                f"must set replace=True to sample"
            )
        indices = np.random.choice(self._size, batch_size, replace=replace)
        if with_indices:
            return self.data[indices], indices
        else:
            return self.data[indices]


class SimpleUniformReplayDataset(StreamReplayDataset):
    def __init__(self, buffer: SimpleReplayBuffer, batch_size: int, transforms=None):
        super().__init__(batch_size=batch_size, transforms=transforms)
        self.buffer = buffer

    def stop_condition(self, step, last_batch) -> bool:
        """
        Endless stream of replay
        """
        return False

    def produce_batch(self, batch_size: int):
        return self.buffer.sample(batch_size, replace=False, with_indices=False)

    def clear(self):
        self.buffer.clear()
