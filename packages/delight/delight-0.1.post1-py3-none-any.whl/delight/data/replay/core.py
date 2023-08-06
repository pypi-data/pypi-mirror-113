import torch
from torch.utils.data import IterableDataset, DataLoader
from typing import Union, Tuple, Callable, Sequence, Any
import itertools
import omlet.utils as U


class ReplayDataset(IterableDataset):
    def __init__(self, transforms: Union[None, Callable, Sequence[Callable]] = None):
        self._transforms = _process_transforms(transforms)

    def __iter__(self):
        raise NotImplementedError

    def transform(self, batch: Any):
        for t in self._transforms:
            batch = t(batch)
        return batch

    @staticmethod
    def singleton_collate_fn(tensor_list):
        """
        Our dataset directly returns batched tensors instead of single samples,
        so for DataLoader we don't need a real collate_fn.
        """
        assert (
            len(tensor_list) == 1
        ), "INTERNAL: _singleton_collate_fn only allows a single item"
        return tensor_list[0]

    def get_dataloader(self) -> DataLoader:
        """
        Our dataset directly returns batched tensors instead of single samples,
        so for DataLoader we don't need a real collate_fn and set batch_size=1
        """
        return DataLoader(
            self,
            batch_size=1,
            num_workers=0,
            pin_memory=True,
            shuffle=False,
            collate_fn=self.singleton_collate_fn,
        )


def _process_transforms(transforms: Union[None, Callable, Sequence[Callable]] = None):
    if transforms is None:
        return []
    elif callable(transforms):
        return [transforms]
    elif U.is_sequence(transforms):
        for t in transforms:
            assert callable(t), f"transform {t} is not callable"
        return transforms
    else:
        raise ValueError(
            f"transforms {transforms} has unsupported type {type(transforms)}"
        )


class StreamReplayDataset(ReplayDataset):
    def __init__(
        self,
        batch_size: int,
        transforms: Union[None, Callable, Sequence[Callable]] = None,
    ):
        super().__init__(transforms)
        self.batch_size = batch_size
        self.step = 0

    def produce_batch(self, batch_size: int):
        raise NotImplementedError

    def stop_condition(self, step: int, last_batch: Any) -> bool:
        """
        Always called _after_ produce_batch()
        """
        return False

    def __iter__(self):
        for self.step in itertools.count():
            last_batch = self.produce_batch(self.batch_size)
            yield self.transform(last_batch)
            if self.stop_condition(self.step, last_batch):
                break
