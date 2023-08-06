"""
ReplayBuffer with data augmentation
"""
import numpy as np

import kornia
import torch
import torch.nn as nn
from enlight.legacy.data import ReplayBuffer

from typing import Tuple, Union


class SimpleReplayBuffer(object):
    """Buffer to store environment transitions."""

    def __init__(self, capacity, obs_shape, action_shape, image_pad, device):
        self.capacity = capacity
        self.device = device  # TODO

        self.aug_trans = nn.Sequential(
            nn.ReplicationPad2d(image_pad),
            kornia.augmentation.RandomCrop((obs_shape[-1], obs_shape[-1])),
        )

        self.obses = np.empty((capacity, *obs_shape), dtype=np.uint8)
        self.next_obses = np.empty((capacity, *obs_shape), dtype=np.uint8)
        self.actions = np.empty((capacity, *action_shape), dtype=np.float32)
        self.rewards = np.empty((capacity, 1), dtype=np.float32)
        self.not_dones = np.empty((capacity, 1), dtype=np.float32)
        self.not_dones_no_max = np.empty((capacity, 1), dtype=np.float32)

        self.idx = 0
        self.full = False

    def __len__(self):
        return self.capacity if self.full else self.idx

    def add(self, obs, action, reward, next_obs, done, done_no_max):
        np.copyto(self.obses[self.idx], obs)
        np.copyto(self.actions[self.idx], action)
        np.copyto(self.rewards[self.idx], reward)
        np.copyto(self.next_obses[self.idx], next_obs)
        np.copyto(self.not_dones[self.idx], not done)
        np.copyto(self.not_dones_no_max[self.idx], not done_no_max)

        self.idx = (self.idx + 1) % self.capacity
        self.full = self.full or self.idx == 0

    def sample(self, batch_size):
        idxs = np.random.randint(
            0, self.capacity if self.full else self.idx, size=batch_size
        )

        obses = self.obses[idxs]
        next_obses = self.next_obses[idxs]
        obses_aug = obses.copy()
        next_obses_aug = next_obses.copy()

        obses = torch.as_tensor(obses, device=self.device).float()
        next_obses = torch.as_tensor(next_obses, device=self.device).float()
        obses_aug = torch.as_tensor(obses_aug, device=self.device).float()
        next_obses_aug = torch.as_tensor(next_obses_aug, device=self.device).float()
        actions = torch.as_tensor(self.actions[idxs], device=self.device)
        rewards = torch.as_tensor(self.rewards[idxs], device=self.device)
        not_dones_no_max = torch.as_tensor(
            self.not_dones_no_max[idxs], device=self.device
        )

        ret = dict(
            obs=obses,
            action=actions,
            reward=rewards,
            obs_next=next_obses,
            not_done=not_dones_no_max,
            obs_aug=obses_aug,
            obs_next_aug=next_obses_aug,
        )

        keys = ['obs', 'obs_next', 'obs_aug', 'obs_next_aug']
        augs = self.aug_trans(torch.cat([ret[k] for k in keys], dim=0))
        for k, chunk in zip(keys, augs.chunk(4, dim=0)):
            ret[k] = chunk
        return ret


class AugReplayBuffer:
    def __init__(self, capacity: int, obs_shape: Tuple[int], action_shape, image_pad: int, device, aug_type: str = 'random_crop'):
        self.buffer = ReplayBuffer(
            capacity, stack_num=0, ignore_obs_next=False, unsqueeze_scalar_dim=True,
            dtypes={
                'obs': np.uint8,
                'obs_next': np.uint8,
                'action': np.float32,
                'reward': np.float32,
                'done': np.float32,
            }
        )

        if aug_type == 'random_crop':
            self.aug_trans = nn.Sequential(
                nn.ReplicationPad2d(image_pad),
                kornia.augmentation.RandomCrop((obs_shape[-1], obs_shape[-1])),
            )
        elif aug_type == 'identity':
            self.aug_trans = nn.Identity()
        else:
            raise NotImplementedError(f'Unsupported augmentation type {aug_type}')

        self.device = device

    def add(self, obs, action, reward, obs_next, done, info):
        self.buffer.add(obs=obs, action=action, reward=reward, obs_next=obs_next, done=done)

    def to_gpu(self, value, to_float: bool):
        value = torch.as_tensor(value, device=self.device)
        if to_float:
            return value.float()
        else:
            return value

    def sample(self, batch_size):
        batch, idx = self.buffer.sample(batch_size)
        ret = {}
        for key in batch.keys():
            ret[key] = batch[key]

        ret['obs_aug'] = batch['obs'].copy()
        ret['obs_next_aug'] = batch['obs_next'].copy()

        for key in ['obs', 'obs_aug', 'obs_next', 'obs_next_aug']:
            ret[key] = self.to_gpu(ret[key], to_float=True)

        for key in ['action', 'reward', 'done']:
            ret[key] = self.to_gpu(ret[key], to_float=False)

        ret['not_done'] = 1. - ret.pop('done')

        # collate augmentation into one CUDA call
        keys = ['obs', 'obs_next', 'obs_aug', 'obs_next_aug']
        augs = self.aug_trans(torch.cat([ret[k] for k in keys], dim=0))
        for k, chunk in zip(keys, augs.chunk(4, dim=0)):
            ret[k] = chunk
        return ret
