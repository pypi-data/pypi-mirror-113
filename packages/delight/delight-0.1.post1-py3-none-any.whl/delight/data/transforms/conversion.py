from typing import Union

import torch
from omlet.data import DataDict


# assume the batch is of the format DataDict(obs, action, obs_next, reward, done, info)


class ToTensor:
    def __init__(
        self,
        device: Union[str, int, torch.device, None],
        dtype: Union[str, torch.dtype, None] = None,
        inplace: bool = True,
        non_blocking: bool = True,
        include_keys=None,
        exclude_keys=("info",),
    ):
        self.dtype = dtype
        self.device = device
        self.inplace = inplace
        self.non_blocking = non_blocking
        self.include_keys = include_keys
        self.exclude_keys = exclude_keys

    def __call__(self, batch: DataDict):
        return batch.to_tensor(
            dtype=self.dtype,
            device=self.device,
            inplace=self.inplace,
            copy=False,
            non_blocking=self.non_blocking,
            include_keys=self.include_keys,
            exclude_keys=self.exclude_keys,
        )


class UnsqueezeScalar:
    def __init__(self, scalar_keys=("reward", "done")):
        self.scalar_keys = scalar_keys

    def __call__(self, batch: DataDict):
        for k in self.scalar_keys:
            t = batch[k]
            if t.ndim == 1:  # only has batch dim
                batch[k] = t.unsqueeze(dim=1)
        return batch


class SetNotDone:
    """
    Instead of `done`, save only `not_done`
    """

    def __call__(self, batch: DataDict):
        assert "done" in batch
        batch.not_done = 1.0 - batch.pop("done")
        return batch
