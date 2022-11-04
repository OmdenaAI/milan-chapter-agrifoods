import torch
from torch import nn
import torch.nn.functional as F
from pathlib import Path

from .base import ModelBase


class ConvModel(ModelBase):
    """
    A PyTorch impementation of  CNN structured model 
    """

    def __init__(self,cnn_params,guass_params):
       
        device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
        # save values for reinitialization
        self.in_channels = cnn_params["in_channels"]
        self.dropout = cnn_params["dropout"]
        self.dense_features = cnn_params["dense_features"]
        time = 32

        model = ConvNet(
            in_channels=self.in_channels,
            dropout=self.dropout,
            dense_features=self.dense_features,
            time=time,
        )

        
        if self.dense_features is None:
            num_dense_layers = 2
        else:
            num_dense_layers = len(dense_features)
        model_weight = f"dense_layers.{num_dense_layers - 1}.weight"
        model_bias = f"dense_layers.{num_dense_layers - 1}.bias"

        super().__init__(
            model,
            model_weight,
            model_bias,
            "cnn",
            cnn_params['savedir'],
            guass_params
        )

    def reinitialize_model(self, time=None):

        # the only thing which changes here is the time value, since this affects the
        # size of the first dense layer.

        if time is None:
            time = self.time
        model = ConvNet(
            in_channels=self.in_channels,
            dropout=self.dropout,
            dense_features=self.dense_features,
            time=time,
        )
        if self.device.type != "cpu":
            model = model.cuda()
        self.model = model


class ConvNet(nn.Module):
    """
    A crop yield conv net.

    """

    def __init__(self, in_channels=9, dropout=0.5, dense_features=None, time=32):
        super().__init__()

        # values taken from the paper
        in_out_channels_list = [in_channels, 128, 256, 256, 512, 512, 512]
        stride_list = [None, 1, 2, 1, 2, 1, 2]

        # Figure out the size of the final flattened conv layer, which
        # is dependent on the input size
        num_divisors = sum([1 if i == 2 else 0 for i in stride_list])
        for i in range(num_divisors):
            if time % 2 != 0:
                time += 1
            time /= 2
        print(dense_features)
        
        if dense_features is None:
            dense_features = [2048, 1]
        dense_features.insert(0, int(in_out_channels_list[-1] * time * 4))

        assert len(stride_list) == len(
            in_out_channels_list
        ), "Stride list and out channels list must be the same length!"

        self.convblocks = nn.ModuleList(
            [
                ConvBlock(
                    in_channels=in_out_channels_list[i - 1],
                    out_channels=in_out_channels_list[i],
                    kernel_size=3,
                    stride=stride_list[i],
                    dropout=dropout,
                )
                for i in range(1, len(stride_list))
            ]
        )

        self.dense_layers = nn.ModuleList(
            [
                nn.Linear(
                    in_features=dense_features[i - 1], out_features=dense_features[i]
                )
                for i in range(1, len(dense_features))
            ]
        )

        self.initialize_weights()

    def initialize_weights(self):
        for convblock in self.convblocks:
            nn.init.kaiming_uniform_(convblock.conv.weight.data)
            # http://cs231n.github.io/neural-networks-2/#init
            # see: Initializing the biases
            nn.init.constant_(convblock.conv.bias.data, 0)
        for dense_layer in self.dense_layers:
            nn.init.kaiming_uniform_(dense_layer.weight.data)
            nn.init.constant_(dense_layer.bias.data, 0)

    def forward(self, x, return_last_dense=False):
       
        for block in self.convblocks:
            x = block(x)

        # flatten
        x = x.view(x.shape[0], -1)

        for layer_number, dense_layer in enumerate(self.dense_layers):
            x = dense_layer(x)
            if return_last_dense and (layer_number == len(self.dense_layers) - 2):
                output = x
        if return_last_dense:
            return x, output
        return x


class ConvBlock(nn.Module):
    """
    A 2D convolution, followed by batchnorm, a ReLU activation, and dropout
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride, dropout):
        super().__init__()
        self.conv = Conv2dSamePadding(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=stride,
        )
        self.batchnorm = nn.BatchNorm2d(num_features=out_channels)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        x = self.relu(self.batchnorm(self.conv(x)))
        return self.dropout(x)


class Conv2dSamePadding(nn.Conv2d):
    """Represents the "Same" padding functionality from Tensorflow.
    See: https://github.com/pytorch/pytorch/issues/3867

    This solution is mostly copied from
    https://github.com/pytorch/pytorch/issues/3867#issuecomment-349279036

    Note that the padding argument in the initializer doesn't do anything now
    """

    def forward(self, input):
        return conv2d_same_padding(
            input, self.weight, self.bias, self.stride, self.dilation, self.groups
        )


def conv2d_same_padding(input, weight, bias=None, stride=1, dilation=1, groups=1):
    # stride and dilation are expected to be tuples.

    # first, we'll figure out how much padding is necessary for the rows
    input_rows = input.size(2)
    filter_rows = weight.size(2)
    effective_filter_size_rows = (filter_rows - 1) * dilation[0] + 1
    out_rows = (input_rows + stride[0] - 1) // stride[0]
    padding_rows = max(
        0, (out_rows - 1) * stride[0] + effective_filter_size_rows - input_rows
    )
    rows_odd = padding_rows % 2 != 0

    # same for columns
    input_cols = input.size(3)
    filter_cols = weight.size(3)
    effective_filter_size_cols = (filter_cols - 1) * dilation[1] + 1
    out_cols = (input_cols + stride[1] - 1) // stride[1]
    padding_cols = max(
        0, (out_cols - 1) * stride[1] + effective_filter_size_cols - input_cols
    )
    cols_odd = padding_cols % 2 != 0

    if rows_odd or cols_odd:
        input = F.pad(input, [0, int(cols_odd), 0, int(rows_odd)])

    return F.conv2d(
        input,
        weight,
        bias,
        stride,
        padding=(padding_rows // 2, padding_cols // 2),
        dilation=dilation,
        groups=groups,
    )
