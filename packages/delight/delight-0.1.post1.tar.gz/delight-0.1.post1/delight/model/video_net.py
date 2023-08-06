"""
Adapted from torchvision.models.video
"""
import torch
import torch.nn as nn


class Conv3DSimple(nn.Conv3d):
    def __init__(self, in_planes, out_planes, midplanes=None, stride=1, padding=1):
        super().__init__(
            in_channels=in_planes,
            out_channels=out_planes,
            kernel_size=(3, 3, 3),
            stride=stride,
            padding=padding,
            bias=False,
        )

    @staticmethod
    def get_downsample_stride(stride):
        return (stride, stride, stride)


class Conv2Plus1D(nn.Sequential):
    def __init__(self, in_planes, out_planes, midplanes, stride=1, padding=1, time_stride=None):
        if time_stride is None:
            time_stride = stride
        super().__init__(
            nn.Conv3d(
                in_planes,
                midplanes,
                kernel_size=(1, 3, 3),
                stride=(1, stride, stride),
                padding=(0, padding, padding),
                bias=False,
            ),
            nn.GroupNorm(num_groups=16, num_channels=midplanes),
            nn.ReLU(inplace=True),
            nn.Conv3d(
                midplanes,
                out_planes,
                kernel_size=(3, 1, 1),
                stride=(time_stride, 1, 1),
                padding=(padding, 0, 0),
                bias=False,
            ),
        )

    @staticmethod
    def get_downsample_stride(stride, time_stride):
        if time_stride is None:
            time_stride = stride
        return (time_stride, stride, stride)


class Conv3DNoTemporal(nn.Conv3d):
    def __init__(self, in_planes, out_planes, midplanes=None, stride=1, padding=1):
        super().__init__(
            in_channels=in_planes,
            out_channels=out_planes,
            kernel_size=(1, 3, 3),
            stride=(1, stride, stride),
            padding=(0, padding, padding),
            bias=False,
        )

    @staticmethod
    def get_downsample_stride(stride):
        return (1, stride, stride)


class BasicBlock(nn.Module):

    expansion = 1

    def __init__(self, inplanes, planes, conv_builder, stride=1, downsample=None, time_stride=None):
        # from Du Tran's paper: calculate midplane to make R2+1D parameters
        # roughly the same as Conv3D
        # midplanes = (inplanes * planes * 3 * 3 * 3) // (inplanes * 3 * 3 + 3 * planes)
        midplanes = planes * 2
        super().__init__()
        self.conv1 = nn.Sequential(
            conv_builder(inplanes, planes, midplanes, stride, time_stride=time_stride),
            nn.GroupNorm(num_groups=16, num_channels=planes),
            nn.ReLU(inplace=True),
        )
        self.conv2 = nn.Sequential(
            conv_builder(planes, planes, midplanes),
            nn.GroupNorm(num_groups=16, num_channels=planes),
        )
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.conv2(out)
        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, conv_builder, stride=1, downsample=None):
        super().__init__()
        midplanes = (inplanes * planes * 3 * 3 * 3) // (inplanes * 3 * 3 + 3 * planes)

        # 1x1x1
        self.conv1 = nn.Sequential(
            nn.Conv3d(inplanes, planes, kernel_size=1, bias=False),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )
        # Second kernel
        self.conv2 = nn.Sequential(
            conv_builder(planes, planes, midplanes, stride),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )

        # 1x1x1
        self.conv3 = nn.Sequential(
            nn.Conv3d(planes, planes * self.expansion, kernel_size=1, bias=False),
            nn.BatchNorm3d(planes * self.expansion),
        )
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class BasicStem(nn.Sequential):
    """The default conv-batchnorm-relu stem
    """

    def __init__(self):
        super().__init__(
            nn.Conv3d(
                3,
                64,
                kernel_size=(3, 7, 7),
                stride=(1, 2, 2),
                padding=(1, 3, 3),
                bias=False,
            ),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),
        )


class R2Plus1dStem(nn.Sequential):
    """R(2+1)D stem is different than the default one as it uses separated 3D convolution
    """

    def __init__(self, base_channels):
        super(R2Plus1dStem, self).__init__(
            nn.Conv3d(
                3,
                base_channels,
                kernel_size=(1, 3, 3),
                stride=(1, 2, 2),
                padding=(0, 1, 1),
                bias=False,
            ),
            nn.GroupNorm(num_groups=16, num_channels=base_channels),
            nn.ReLU(inplace=True),
            nn.Conv3d(
                base_channels,
                base_channels,
                kernel_size=(3, 1, 1),
                stride=(1, 1, 1),
                padding=(1, 0, 0),
                bias=False,
            ),
            nn.GroupNorm(num_groups=16, num_channels=base_channels),
            nn.ReLU(inplace=True),
        )


class VideoResNet(nn.Module):
    def __init__(
        self,
        block,
        conv_makers,
        layers,
        stem,
        base_channels=64,
        num_classes=400,
        zero_init_residual=False,
        debug=False
    ):
        """Generic resnet video generator.

        Args:
            block (nn.Module): resnet building block
            conv_makers (list(functions)): generator function for each layer
            layers (List[int]): number of blocks per layer
            stem (nn.Module, optional): Resnet stem, if None, defaults to conv-bn-relu. Defaults to None.
            num_classes (int, optional): Dimension of the final FC layer. Defaults to 400.
            zero_init_residual (bool, optional): Zero init bottleneck residual BN. Defaults to False.
        """
        super().__init__()
        self.inplanes = base_channels

        self.stem = stem(base_channels)

        self.layer1 = self._make_layer(
            block, conv_makers[0], base_channels, layers[0], stride=1, time_stride=1
        )
        self.layer2 = self._make_layer(
            block, conv_makers[1], base_channels * 2, layers[1], stride=2, time_stride=1
        )
        self.layer3 = self._make_layer(
            block, conv_makers[2], base_channels * 2, layers[2], stride=2, time_stride=1
        )
        self.layer4 = self._make_layer(
            block, conv_makers[3], base_channels * 4, layers[3], stride=2
        )

        self.avgpool = nn.AdaptiveAvgPool3d((1, 1, 1))
        self.fc = nn.Linear(base_channels * 4 * block.expansion, num_classes)

        # init weights
        self._initialize_weights()
        self.debug = debug

        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck):
                    nn.init.constant_(m.bn3.weight, 0)

    def forward(self, x):
        x = self.stem(x)
        if self.debug:
            print("stem", x.size())

        x = self.layer1(x)
        if self.debug:
            print("layer1", x.size())
        x = self.layer2(x)
        if self.debug:
            print("layer2", x.size())
        x = self.layer3(x)
        if self.debug:
            print("layer3", x.size())
        x = self.layer4(x)
        if self.debug:
            print("layer4", x.size())

        x = self.avgpool(x)
        if self.debug:
            print("avgpool", x.size())
        # Flatten the layer to fc
        x = x.flatten(1)
        if self.debug:
            print("flatten", x.size())
        x = self.fc(x)

        return x

    def _make_layer(self, block, conv_builder, planes, blocks, stride=1, time_stride=None):
        downsample = None

        if stride != 1 or self.inplanes != planes * block.expansion:
            ds_stride = conv_builder.get_downsample_stride(stride, time_stride=time_stride)
            downsample = nn.Sequential(
                nn.Conv3d(
                    self.inplanes,
                    planes * block.expansion,
                    kernel_size=1,
                    stride=ds_stride,
                    bias=False,
                ),
                nn.GroupNorm(num_groups=16, num_channels=planes * block.expansion),
            )
        layers = []
        layers.append(block(self.inplanes, planes, conv_builder, stride, downsample, time_stride=time_stride))

        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes, conv_builder))

        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, (nn.GroupNorm, nn.BatchNorm3d)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


def _video_resnet(arch, pretrained=False, **kwargs):
    model = VideoResNet(**kwargs)

    if pretrained:
        raise NotImplementedError
    return model


def r3d_18(pretrained=False, **kwargs):
    """Construct 18 layer Resnet3D model as in
    https://arxiv.org/abs/1711.11248

    Args:
        pretrained (bool): If True, returns a model pre-trained on Kinetics-400
        progress (bool): If True, displays a progress bar of the download to stderr

    Returns:
        nn.Module: R3D-18 network
    """

    return _video_resnet(
        "r3d_18",
        pretrained,
        block=BasicBlock,
        conv_makers=[Conv3DSimple] * 4,
        layers=[2, 2, 2, 2],
        stem=BasicStem,
        **kwargs
    )


def mc3_18(pretrained=False, **kwargs):
    """Constructor for 18 layer Mixed Convolution network as in
    https://arxiv.org/abs/1711.11248

    Args:
        pretrained (bool): If True, returns a model pre-trained on Kinetics-400
        progress (bool): If True, displays a progress bar of the download to stderr

    Returns:
        nn.Module: MC3 Network definition
    """
    return _video_resnet(
        "mc3_18",
        pretrained,
        block=BasicBlock,
        conv_makers=[Conv3DSimple] + [Conv3DNoTemporal] * 3,
        layers=[2, 2, 2, 2],
        stem=BasicStem,
        **kwargs
    )


def r2plus1d_18(**kwargs):
    """Constructor for the 18 layer deep R(2+1)D network as in
    https://arxiv.org/abs/1711.11248

    Args:
        pretrained (bool): If True, returns a model pre-trained on Kinetics-400
        progress (bool): If True, displays a progress bar of the download to stderr

    Returns:
        nn.Module: R(2+1)D-18 network
    """
    return _video_resnet(
        "r2plus1d_18",
        pretrained=False,
        block=BasicBlock,
        conv_makers=[Conv2Plus1D] * 4,
        layers=[2, 2, 2, 2],
        stem=R2Plus1dStem,
        **kwargs
    )


def r2plus1d_9(**kwargs):
    """
    Input: (N, C, T, H, W)
    Output:

    Returns:
        nn.Module: R(2+1)D-9 network
    """
    return _video_resnet(
        "r2plus1d_9",
        pretrained=False,
        block=BasicBlock,
        conv_makers=[Conv2Plus1D] * 4,
        layers=[1, 1, 1, 1],
        stem=R2Plus1dStem,
        base_channels=32,
        **kwargs
    )
