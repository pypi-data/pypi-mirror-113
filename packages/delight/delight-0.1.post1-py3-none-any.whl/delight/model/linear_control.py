import torch
import torch.nn as nn
import torch.optim
import torch.nn.functional as F
from typing import Any, Union, Optional, Dict, List
from enlight.model.backbone import mlp
from enlight.model.video_net import r2plus1d_9
import enlight.utils as U
from enlight.rl import distributions


class TemporalShift(nn.Module):
    def __init__(self, net, n_frames, n_div=8, inplace=False):
        super().__init__()
        self.net = net
        self.n_frames = n_frames
        self.fold_div = n_div
        self.inplace = inplace

    def forward(self, x):
        x = self.shift(x, self.n_frames, fold_div=self.fold_div, inplace=self.inplace)
        return self.net(x)

    @staticmethod
    def shift(x, n_frames, fold_div=8, inplace=False):
        nt, c, h, w = x.size()
        n_batch = nt // n_frames
        x = x.view(n_batch, n_frames, c, h, w)

        fold = c // fold_div
        if inplace:
            # Due to some out of order error when performing parallel computing.
            # May need to write a CUDA kernel.
            raise NotImplementedError
            # out = InplaceShift.apply(x, fold)
        else:
            out = torch.zeros_like(x)
            out[:, :-1, :fold] = x[:, 1:, :fold]  # shift left
            out[:, 1:, fold: 2 * fold] = x[:, :-1, fold: 2 * fold]  # shift right
            out[:, :, 2 * fold:] = x[:, :, 2 * fold:]  # not shift

        return out.view(nt, c, h, w)


class Encoder(nn.Module):
    """Convolutional encoder for image-based observations."""

    def __init__(self, obs_shape, feature_dim):
        super().__init__()

        assert len(obs_shape) == 3
        self.num_layers = 4
        self.num_filters = 32
        self.output_dim = 35
        self.feature_dim = feature_dim

        self.convs = nn.ModuleList(
            [
                nn.Conv2d(obs_shape[0], self.num_filters, 3, stride=2),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
            ]
        )

        self.head = nn.Sequential(
            nn.Linear(self.num_filters * 35 * 35, feature_dim),
            nn.LayerNorm(feature_dim),
            # nn.ReLU(),
            # nn.Linear(feature_dim, self.feature_dim),
            # nn.LayerNorm(self.feature_dim),
            # nn.ReLU(),
        )

    def forward_conv(self, obs):
        obs = obs / 255.0
        # self.outputs["obs"] = obs

        conv = torch.relu(self.convs[0](obs))
        # self.outputs["conv1"] = conv

        for i in range(1, self.num_layers):
            conv = torch.relu(self.convs[i](conv))
            # self.outputs["conv%s" % (i + 1)] = conv

        h = conv.view(conv.size(0), -1)
        return h

    def forward(self, obs):
        h = self.forward_conv(obs)
        out = self.head(h)
        # if not self.output_logits:
        #     out = torch.tanh(out)
        out = torch.tanh(out)
        return out

    def copy_conv_weights_from(self, source):
        """
        Hack to avoid DDP error "unused gradient in distributed"
        """
        self.convs = source.convs
        self.head = source.head


class TSMEncoder(nn.Module):
    """Convolutional encoder for image-based observations."""

    def __init__(self, obs_shape, feature_dim):
        super().__init__()
        assert len(obs_shape) == 3
        self.n_frames = obs_shape[0] // 3  # 3 for RGB
        self.num_layers = 4
        self.num_filters = 32
        self.output_dim = 35
        self.output_logits = False
        self.feature_dim = feature_dim

        self.convs = nn.ModuleList(
            [
                # 3 for RGB
                nn.Conv2d(3, self.num_filters, 3, stride=2),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
                nn.Conv2d(self.num_filters, self.num_filters, 3, stride=1),
            ]
        )

        self.head = nn.Sequential(
            nn.Linear(self.num_filters * 35 * 35, self.feature_dim),
            nn.LayerNorm(self.feature_dim),
        )

        self.outputs = dict()

    def forward_conv(self, obs):
        # obs [N, T*C, H, W]
        obs = obs / 255.0
        N, TC, H, W = obs.size()
        obs = obs.view(N * self.n_frames, TC//self.n_frames, H, W)
        self.outputs["obs"] = obs

        x = torch.relu(self.convs[0](obs))
        self.outputs["conv1"] = x

        for i in range(1, self.num_layers):
            x = TemporalShift(self.convs[i], self.n_frames, n_div=8)(x)
            x = torch.relu(x)
            self.outputs["conv%s" % (i + 1)] = x

        NT, C, H, W = x.size()
        x = x.view(N, NT // N, C, H, W)
        # average consensus as in TSN
        x = x.mean(dim=1, keepdim=False)  # -> [N, C, H, W]

        h = x.view(x.size(0), -1)
        return h

    def forward(self, obs):
        h = self.forward_conv(obs)
        out = self.head(h)
        out = torch.tanh(out)
        return out

    def copy_conv_weights_from(self, source):
        """Tie convolutional layers"""
        self.convs = source.convs
        self.head = source.head

    def log(self, logger, step):
        pass


class Actor(nn.Module):
    """torch.distributions implementation of an diagonal Gaussian policy."""

    def __init__(self, encoder, action_shape, hidden_dim, hidden_depth, log_std_bounds):
        super().__init__()

        self.encoder = encoder

        self.log_std_bounds = log_std_bounds
        self.trunk = mlp(
            self.encoder.feature_dim, hidden_dim, 2 * action_shape[0], hidden_depth
        )

        self.outputs = dict()
        self.apply(U.weight_init)

    def forward(self, obs, detach_encoder=False):
        obs = self.encoder(obs)
        if detach_encoder:
            obs = obs.detach()

        mu, log_std = self.trunk(obs).chunk(2, dim=-1)

        # constrain log_std inside [log_std_min, log_std_max]
        log_std = torch.tanh(log_std)
        log_std_min, log_std_max = self.log_std_bounds
        log_std = log_std_min + 0.5 * (log_std_max - log_std_min) * (log_std + 1)
        std = log_std.exp()

        self.outputs["mu"] = mu
        self.outputs["std"] = std

        dist = distributions.SquashedNormal(mu, std)
        return dist

    def log(self, logger, step):
        pass
        # for k, v in self.outputs.items():
        #     logger.log_histogram(f'train_actor/{k}_hist', v, step)
        #
        # for i, m in enumerate(self.trunk):
        #     if type(m) == nn.Linear:
        #         logger.log_param(f'train_actor/fc{i}', m, step)


class Critic(nn.Module):
    """Critic network, employes double Q-learning."""

    def __init__(self, encoder, action_shape, hidden_dim, hidden_depth):
        super().__init__()

        self.encoder = encoder

        self.Q1 = mlp(
            self.encoder.feature_dim + action_shape[0], hidden_dim, 1, hidden_depth
        )
        self.Q2 = mlp(
            self.encoder.feature_dim + action_shape[0], hidden_dim, 1, hidden_depth
        )

        self.outputs = dict()
        self.apply(U.weight_init)

    def forward(self, obs, action, detach_encoder=False):
        assert obs.size(0) == action.size(0)
        obs = self.encoder(obs)
        if detach_encoder:
            obs = obs.detach()

        obs_action = torch.cat([obs, action], dim=-1)
        q1 = self.Q1(obs_action)
        q2 = self.Q2(obs_action)

        self.outputs["q1"] = q1
        self.outputs["q2"] = q2

        return q1, q2

    def log(self, logger, step):
        pass
        # self.encoder.log(logger, step)
        #
        # for k, v in self.outputs.items():
        #     logger.log_histogram(f'train_critic/{k}_hist', v, step)
        #
        # assert len(self.Q1) == len(self.Q2)
        # for i, (m1, m2) in enumerate(zip(self.Q1, self.Q2)):
        #     assert type(m1) == type(m2)
        #     if type(m1) is nn.Linear:
        #         logger.log_param(f'train_critic/q1_fc{i}', m1, step)
        #         logger.log_param(f'train_critic/q2_fc{i}', m2, step)
