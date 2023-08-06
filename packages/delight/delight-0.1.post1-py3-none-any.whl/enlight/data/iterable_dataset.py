import torch
import itertools
from torch.utils.data import IterableDataset, DataLoader
from typing import Union, Tuple


def singleton_collate_fn(tensor_list):
    """
    Our dataset directly returns batched tensors instead of single samples,
    so for DataLoader we don't need a real collate_fn.
    """
    assert (
        len(tensor_list) == 1
    ), "INTERNAL: _singleton_collate_fn only allows a single item"
    return tensor_list[0]


class ReplayDataset(IterableDataset):
    """
    Dataset wrapper around ReplayBuffer to accommodate PyTorch-LightningModule API
    """

    def __init__(self, buffer, batch_size: int, epoch_length: Union[int, str]) -> None:
        """
        batch_size: number of experience tuples to sample at a time
        epoch_length:
            number of iterations in an artificially defined epoch
            if 'inf', never stop
        """
        super().__init__()
        self.buffer = buffer
        self.batch_size = batch_size
        assert epoch_length == "inf" or isinstance(epoch_length, int)
        self.epoch_length = epoch_length

    def __iter__(self) -> Tuple:
        for i in itertools.count():
            yield self.buffer.sample(self.batch_size)
            if self.epoch_length != "inf" and i >= self.epoch_length - 1:
                break

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
            collate_fn=singleton_collate_fn,
        )


class CounterDataset(IterableDataset):
    def __init__(self, epoch_length: int) -> None:
        """
        epoch_length:
            How many times to iterate over

        yields:
            (dummy input [i], target [i])
        """
        super().__init__()
        assert epoch_length == "inf" or isinstance(epoch_length, int)
        self.epoch_length = epoch_length

    def __iter__(self) -> Tuple:
        for i in itertools.count():
            yield torch.tensor([i], dtype=torch.int64), torch.tensor(
                [i], dtype=torch.int64
            )
            if self.epoch_length != "inf" and i >= self.epoch_length - 1:
                break

    def get_dataloader(self) -> DataLoader:
        """
        Our dataset directly returns batched tensors instead of single samples,
        so for DataLoader we don't need a real collate_fn and set batch_size=1
        """
        return DataLoader(
            self,
            batch_size=1,
            num_workers=0,
            pin_memory=False,
            shuffle=False,
            collate_fn=singleton_collate_fn,
        )
