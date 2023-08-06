import torch
import kornia
import torch.nn as nn
from omlet.data import DataDict
from typing import Callable, List, Tuple


class ApplyAugmentation:
    """
    Please transfer tensors to GPU first before applying augmentation
    """

    def __init__(self, key_list: List[str], num_augs: int, aug_op: Callable):
        assert num_augs >= 1
        self.num_augs = num_augs
        assert callable(aug_op)
        self.aug_op = aug_op
        self.key_list = key_list

    def __call__(self, batch: DataDict):
        # assume all the values in key_list have the same tensor shape
        # collate aug_op over multiple tensors into a single vectorized GPU call
        vec = []
        for k in self.key_list:
            t = batch[k]
            assert isinstance(t, torch.Tensor)
            # batch[k] will be replaced as a tuple (aug0, aug1, aug2 ...)
            vec.append(t)
            for _ in range(self.num_augs - 1):
                vec.append(t.clone())

        # concat along batch dim, then chunk back
        vec = self.aug_op(torch.cat(vec, dim=0)).chunk(len(vec), dim=0)
        vec = list(vec)
        assert len(vec) == self.num_augs * len(self.key_list)
        for k in self.key_list:
            batch[k] = tuple(vec[: self.num_augs])
            del vec[: self.num_augs]
        return batch


class RandomCrop(ApplyAugmentation):
    def __init__(
        self,
        key_list: List[str],
        num_augs: int,
        crop_size: Tuple[int, int],
        image_pad: int,
    ):
        aug_op = nn.Sequential(
            nn.ReplicationPad2d(image_pad), kornia.augmentation.RandomCrop(crop_size),
        )
        super().__init__(key_list=key_list, num_augs=num_augs, aug_op=aug_op)
