# Copyright 2020-2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""loss"""
import mindspore
import mindspore.common.dtype as mstype
from mindspore import log
from mindspore.common.tensor import Tensor
from mindspore.common.parameter import Parameter
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore import nn
from mindspore.ops.primitive import constexpr
from mindspore.nn.cell import Cell
from mindspore.nn.layer.activation import get_activation
from mindspore._checkparam import Validator as validator
from mindspore._checkparam import Rel
from ... import context

class LossBase(Cell):
    """
    Base class for other losses.

    Other losses derived from this should implement their own `construct` and use method `self.get_loss`
    to apply reduction to loss values.

    Args:
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
            Default: "mean".

    Raises:
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    def __init__(self, reduction='mean'):
        """Initialize Loss."""
        super(LossBase, self).__init__()

        if reduction not in ('mean', 'sum', 'none'):
            raise ValueError(f"reduction method for {reduction} is not supported")

        self.average = True
        self.reduce = True
        if reduction == 'sum':
            self.average = False
        if reduction == 'none':
            self.reduce = False

        self.reduce_mean = P.ReduceMean()
        self.reduce_sum = P.ReduceSum()
        self.mul = P.Mul()
        self.cast = P.Cast()

    def get_axis(self, x):
        shape = F.shape(x)
        length = F.tuple_len(shape)
        perm = F.make_range(0, length)
        return perm

    def get_loss(self, x, weights=1.0):
        """
        Computes the weighted loss.

        Args:
            weights (Union[float, Tensor]): Optional `Tensor` whose rank is either 0, or the same rank as inputs,
            and must be broadcastable to inputs (i.e., all dimensions must be either `1`,
            or the same as the corresponding inputs dimension).
        """
        input_dtype = x.dtype
        x = self.cast(x, mstype.float32)
        weights = self.cast(weights, mstype.float32)
        x = self.mul(weights, x)
        if self.reduce and self.average:
            x = self.reduce_mean(x, self.get_axis(x))
        if self.reduce and not self.average:
            x = self.reduce_sum(x, self.get_axis(x))
        x = self.cast(x, input_dtype)
        return x

    def construct(self, base, target):
        raise NotImplementedError


class _Loss(LossBase):
    """
    Base class for other losses.
    """
    def __init__(self, reduction='mean'):
        """Initialize _Loss."""
        log.warning("'_Loss' is deprecated from version 1.3 and "
                    "will be removed in a future version, use 'LossBase' instead.")
        super(_Loss, self).__init__(reduction)

    def construct(self, base, target):
        raise NotImplementedError


@constexpr
def _check_is_tensor(param_name, input_data, cls_name):
    if input_data is not None and not isinstance(F.typeof(input_data), mstype.tensor_type):
        raise TypeError(f"For '{cls_name}', the '{param_name}' should be '{mstype.tensor_type}', "
                        f"but got '{F.typeof(input_data)}'")

class L1Loss(LossBase):
    r"""
    L1Loss creates a criterion to measure the mean absolute error (MAE) between :math:`x` and :math:`y` element-wise,
    where :math:`x` is the input Tensor and :math:`y` is the target Tensor.

    For simplicity, let :math:`x` and :math:`y` be 1-dimensional Tensor with length :math:`N`,
    the unreduced loss (i.e. with argument reduction set to 'none') of :math:`x` and :math:`y` is given as:

    .. math::
        \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad \text{with } l_n = \left| x_n - y_n \right|,

    where :math:`N` is the batch size. If `reduction` is not 'none', then:

    .. math::
        \ell(x, y) =
        \begin{cases}
            \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    Args:
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
            Default: "mean".

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number of
          additional dimensions.
        - **labels** (Tensor) - Tensor of shape :math:`(N, *)`, same shape as the `logits` in common cases.
          However, it supports the shape of `logits` is different from the shape of `labels`
          and they should be broadcasted to each other.

    Outputs:
        Tensor, loss float tensor, the shape is zero if `reduction` is 'mean' or 'sum',
        while the shape of output is the broadcasted shape if `reduction` is 'none'.

    Raises:
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # Case 1: logits.shape = labels.shape = (3,)
        >>> loss = nn.L1Loss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        0.33333334
        >>> # Case 2: logits.shape = (3,), labels.shape = (2, 3)
        >>> loss = nn.L1Loss(reduction='none')
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([[1, 1, 1], [1, 2, 2]]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        [[0. 1. 2.]
         [0. 0. 1.]]
    """
    def __init__(self, reduction='mean'):
        """Initialize L1Loss."""
        super(L1Loss, self).__init__(reduction)
        self.abs = P.Abs()

    def construct(self, base, target):
        _check_is_tensor('logits', base, self.cls_name)
        _check_is_tensor('labels', target, self.cls_name)
        x = self.abs(base - target)
        return self.get_loss(x)


class MSELoss(LossBase):
    r"""
    MSELoss creates a criterion to measure the mean squared error (squared L2-norm) between :math:`x` and :math:`y`
    element-wise, where :math:`x` is the input and :math:`y` is the target.

    For simplicity, let :math:`x` and :math:`y` be 1-dimensional Tensor with length :math:`N`,
    the unreduced loss (i.e. with argument reduction set to 'none') of :math:`x` and :math:`y` is given as:

    .. math::
        \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad \text{with} \quad l_n = (x_n - y_n)^2.

    where :math:`N` is the batch size. If `reduction` is not 'none', then:

    .. math::
        \ell(x, y) =
        \begin{cases}
            \operatorname{mean}(L), & \text{if reduction} = \text{`mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{`sum'.}
        \end{cases}

    Args:
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
            Default: "mean".

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number of
          additional dimensions.
        - **labels** (Tensor) - Tensor of shape :math:`(N, *)`, same shape as the `logits` in common cases.
          However, it supports the shape of `logits` is different from the shape of `labels`
          and they should be broadcasted to each other.

    Outputs:
        Tensor, loss float tensor, the shape is zero if `reduction` is 'mean' or 'sum',
        while the shape of output is the broadcasted shape if `reduction` is 'none'.

    Raises:
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # Case 1: logits.shape = labels.shape = (3,)
        >>> loss = nn.MSELoss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 1, 1]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        1.6666667
        >>> # Case 2: logits.shape = (3,), labels.shape = (2, 3)
        >>> loss = nn.MSELoss(reduction='none')
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([[1, 1, 1], [1, 2, 2]]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        [[0. 1. 4.]
         [0. 0. 1.]]
    """
    def construct(self, base, target):
        _check_is_tensor('logits', base, self.cls_name)
        _check_is_tensor('labels', target, self.cls_name)
        x = F.square(base - target)
        return self.get_loss(x)


class RMSELoss(LossBase):
    r"""
    RMSELoss creates a criterion to measure the root mean square error between :math:`x` and :math:`y`
    element-wise, where :math:`x` is the input and :math:`y` is the target.

    For simplicity, let :math:`x` and :math:`y` be 1-dimensional Tensor with length :math:`N`,
    the loss of :math:`x` and :math:`y` is given as:

    .. math::
        loss = \sqrt{\frac{1}{N}\sum_{i=1}^{N}{(x_i-y_i)^2}}


    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number of
          additional dimensions.
        - **labels** (Tensor) - Tensor of shape :math:`(N, *)`, same shape as the `logits` in common cases.
          However, it supports the shape of `logits` is different from the shape of `labels`
          and they should be broadcasted to each other.

    Outputs:
        Tensor, weighted loss float tensor and its shape is zero.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # Case 1: logits.shape = labels.shape = (3,)
        >>> loss = nn.RMSELoss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        0.57735026
        >>> # Case 2: logits.shape = (3,), labels.shape = (2, 3)
        >>> loss = nn.RMSELoss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([[1, 1, 1], [1, 2, 2]]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        1.0
    """
    def __init__(self):
        """Initialize RMSELoss."""
        super(RMSELoss, self).__init__()
        self.MSELoss = MSELoss()

    def construct(self, logits, label):
        rmse_loss = F.sqrt(self.MSELoss(logits, label))

        return rmse_loss


class MAELoss(LossBase):
    r"""
    MAELoss creates a criterion to measure the average absolute error between :math:`x` and :math:`y`
    element-wise, where :math:`x` is the input and :math:`y` is the target.

    For simplicity, let :math:`x` and :math:`y` be 1-dimensional Tensor with length :math:`N`,
    the unreduced loss (i.e. with argument reduction set to 'none') of :math:`x` and :math:`y` is given as:

    .. math::
        \ell(x, y) = L = \{l_1,\dots,l_N\}^\top, \quad \text{with } l_n = \left| x_n - y_n \right|,

    where :math:`N` is the batch size. If `reduction` is not 'none', then:

    .. math::
        \ell(x, y) =
        \begin{cases}
            \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
            \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    Args:
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
                         Default: "mean".

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(M, *)` where :math:`*` means, any number of
          additional dimensions.
        - **labels** (Tensor) - Tensor of shape :math:`(N, *)`, same shape as the `logits` in common cases.
          However, it supports the shape of `logits` is different from the shape of `labels`
          and they should be broadcasted to each other.

    Outputs:
        Tensor, weighted loss float tensor, the shape is zero if `reduction` is 'mean' or 'sum',
        while the shape of output is the broadcasted shape if `reduction` is 'none'.

    Raises:
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # Case 1: logits.shape = labels.shape = (3,)
        >>> loss = nn.MAELoss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        0.33333334
        >>> # Case 2: logits.shape = (3,), labels.shape = (2, 3)
        >>> loss = nn.MAELoss(reduction='none')
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([[1, 1, 1], [1, 2, 2]]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        [[0. 1. 2.]
         [0. 0. 1.]]
    """
    def __init__(self, reduction='mean'):
        """Initialize MAELoss."""
        super(MAELoss, self).__init__(reduction)
        self.abs = P.Abs()

    def construct(self, logits, label):
        _check_is_tensor('logits', logits, self.cls_name)
        _check_is_tensor('labels', label, self.cls_name)
        x = self.abs(logits - label)
        return self.get_loss(x)


class SmoothL1Loss(LossBase):
    r"""
    A loss class for learning region proposals.

    SmoothL1Loss can be regarded as modified version of L1Loss or a combination of L1Loss and L2Loss.
    L1Loss computes the element-wise absolute difference between two input Tensor while L2Loss computes the
    squared difference between two input Tensor. L2Loss often leads to faster convergence but it is less
    robust to outliers.

    Given two input :math:`x,\  y` of length :math:`N`, the unreduced SmoothL1Loss can be described
    as follows:

    .. math::
        L_{i} =
        \begin{cases}
        \frac{0.5 (x_i - y_i)^{2}}{\text{beta}}, & \text{if } |x_i - y_i| < \text{beta} \\
        |x_i - y_i| - 0.5 \text{beta}, & \text{otherwise. }
        \end{cases}

    Here :math:`\text{beta}` controls the point where the loss function changes from quadratic to linear.
    Its default value is 1.0. :math:`N` is the batch size. This function returns an
    unreduced loss Tensor.

    Args:
        beta (float): A parameter used to control the point where the function will change from
            quadratic to linear. Default: 1.0.

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number of
          additional dimensions. Data type must be float16 or float32.
        - **labels** (Tensor) - Ground truth data, tensor of shape :math:`(N, *)`,
          same shape and dtype as the `logits`.

    Outputs:
        Tensor, loss float tensor, same shape and dtype as the `logits`.

    Raises:
        TypeError: If `beta` is not a float.
        TypeError: If dtype of `logits` or `labels` is neither float16 not float32.
        ValueError: If `beta` is less than or equal to 0.
        ValueError: If shape of `logits` is not the same as `labels`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> loss = nn.SmoothL1Loss()
        >>> logits = Tensor(np.array([1, 2, 3]), mindspore.float32)
        >>> labels = Tensor(np.array([1, 2, 2]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        [0.  0.  0.5]
    """
    def __init__(self, beta=1.0):
        """Initialize SmoothL1Loss."""
        super(SmoothL1Loss, self).__init__()
        self.beta = beta
        self.smooth_l1_loss = P.SmoothL1Loss(self.beta)

    def construct(self, base, target):
        _check_is_tensor('logits', base, self.cls_name)
        _check_is_tensor('labels', target, self.cls_name)
        return self.smooth_l1_loss(base, target)


class SoftmaxCrossEntropyWithLogits(LossBase):
    r"""
    Computes softmax cross entropy between logits and labels.

    Measures the distribution error between the probabilities of the input (computed with softmax function) and the
    target where the classes are mutually exclusive (only one class is positive) using cross entropy loss.

    Typical input into this function is unnormalized scores denoted as x whose shape is (N, C),
    and the corresponding targets.

    For each instance :math:`x_i`, i ranges from 0 to N-1, the loss is given as:

    .. math::
        \ell(x_i, c) = - \log\left(\frac{\exp(x_i[c])}{\sum_j \exp(x_i[j])}\right)
        =  -x_i[c] + \log\left(\sum_j \exp(x_i[j])\right)

    where :math:`x_i` is a 1D score Tensor, :math:`c` is the index of 1 in one-hot.

    Note:
        While the target classes are mutually exclusive, i.e., only one class is positive in the target, the predicted
        probabilities does not need to be exclusive. It is only required that the predicted probability distribution
        of entry is a valid one.

    Args:
        sparse (bool): Specifies whether labels use sparse format or not. Default: False.
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
            If "none", do not perform reduction. Default: "none".

    Inputs:
        - **logits** (Tensor) - Tensor of shape (N, C). Data type must be float16 or float32.
        - **labels** (Tensor) - Tensor of shape (N, ). If `sparse` is True, The type of
          `labels` is int32 or int64. Otherwise, the type of `labels` is the same as the type of `logits`.

    Outputs:
        Tensor, a tensor of the same shape and type as logits with the component-wise logistic losses.

    Raises:
        TypeError: If `sparse` is not a bool.
        TypeError: If `sparse` is True and dtype of `labels` is neither int32 not int64.
        TypeError: If `sparse` is False and dtype of `labels` is neither float16 not float32.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # case 1: sparse=True
        >>> loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True)
        >>> logits = Tensor(np.array([[3, 5, 6, 9, 12, 33, 42, 12, 32, 72]]), mindspore.float32)
        >>> labels_np = np.array([1]).astype(np.int32)
        >>> labels = Tensor(labels_np)
        >>> output = loss(logits, labels)
        >>> print(output)
        [67.]
        >>> # case 2: sparse=False
        >>> loss = nn.SoftmaxCrossEntropyWithLogits(sparse=False)
        >>> logits = Tensor(np.array([[3, 5, 6, 9, 12, 33, 42, 12, 32, 72]]), mindspore.float32)
        >>> labels_np = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]).astype(np.float32)
        >>> labels = Tensor(labels_np)
        >>> output = loss(logits, labels)
        >>> print(output)
        [30.]
    """
    def __init__(self,
                 sparse=False,
                 reduction='none'):
        """Initialize SoftmaxCrossEntropyWithLogits."""
        super(SoftmaxCrossEntropyWithLogits, self).__init__(reduction)
        self.sparse = validator.check_bool(sparse, "sparse")
        self.reduction = reduction
        self.softmax_cross_entropy = P.SoftmaxCrossEntropyWithLogits()
        self.one_hot = P.OneHot()
        self.on_value = Tensor(1.0, mstype.float32)
        self.off_value = Tensor(0., mstype.float32)
        self.is_cpugpu = context.get_context('device_target') in ["CPU", "GPU"]
        self.sparse_softmax_cross_entropy = P.SparseSoftmaxCrossEntropyWithLogits()

    def construct(self, logits, labels):
        _check_is_tensor('logits', logits, self.cls_name)
        _check_is_tensor('labels', labels, self.cls_name)
        if self.sparse:
            if self.reduction == 'mean':
                x = self.sparse_softmax_cross_entropy(logits, labels)
                return x
            labels = self.one_hot(labels, F.shape(logits)[-1], self.on_value, self.off_value)
        x = self.softmax_cross_entropy(logits, labels)[0]
        return self.get_loss(x)

@constexpr
def _check_label_dtype(labels_dtype, cls_name):
    validator.check_type_name("labels", labels_dtype, [mstype.int32, mstype.int64], cls_name)


class DiceLoss(LossBase):
    r"""
    The Dice coefficient is a set similarity loss. It is used to calculate the similarity between two samples. The
    value of the Dice coefficient is 1 when the segmentation result is the best and 0 when the segmentation result
    is the worst. The Dice coefficient indicates the ratio of the area between two objects to the total area.
    The function is shown as follows:

    .. math::
        dice = 1 - \frac{2 * (pred \bigcap true)}{pred \bigcup true}

    Args:
        smooth (float): A term added to the denominator to improve numerical stability. Should be greater than 0.
                        Default: 1e-5.

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number of
          additional dimensions. The data type must be float16 or float32.
        - **labels** (Tensor) - Tensor of shape :math:`(N, *)`, same shape as the `logits`.
          The data type must be float16 or float32.

    Outputs:
        Tensor, a tensor of shape with the per-example sampled Dice losses.

    Raises:
        ValueError: If the dimension of `logits` is different from `labels`.
        TypeError: If the type of `logits` or `labels` are not Tensor.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> loss = nn.DiceLoss(smooth=1e-5)
        >>> logits = Tensor(np.array([[0.2, 0.5], [0.3, 0.1], [0.9, 0.6]]), mstype.float32)
        >>> labels = Tensor(np.array([[0, 1], [1, 0], [0, 1]]), mstype.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        0.38596618
    """
    def __init__(self, smooth=1e-5):
        """Initialize DiceLoss."""
        super(DiceLoss, self).__init__()
        self.smooth = validator.check_positive_float(smooth, "smooth")
        self.reshape = P.Reshape()

    def construct(self, logits, label):
        _check_is_tensor('logits', logits, self.cls_name)
        _check_is_tensor('labels', label, self.cls_name)
        _check_shape(logits.shape, label.shape)
        intersection = self.reduce_sum(self.mul(logits.view(-1), label.view(-1)))
        unionset = self.reduce_sum(self.mul(logits.view(-1), logits.view(-1))) + \
                   self.reduce_sum(self.mul(label.view(-1), label.view(-1)))

        single_dice_coeff = (2 * intersection) / (unionset + self.smooth)
        dice_loss = 1 - single_dice_coeff

        return dice_loss


@constexpr
def _check_shape(logits_shape, label_shape):
    validator.check('logits_shape', logits_shape, 'label_shape', label_shape)


@constexpr
def _check_ndim_multi(logits_dim, label_dim):
    if logits_dim < 2:
        raise ValueError("Logits dimension should be greater than 1, but got {}".format(logits_dim))
    if label_dim < 2:
        raise ValueError("label dimension should be greater than 1, but got {}".format(label_dim))


@constexpr
def _check_weights(weight_shape, label_shape):
    if weight_shape != label_shape:
        raise ValueError("The weight shape[0] should be equal to label.shape[1].")


class MultiClassDiceLoss(LossBase):
    r"""
    When there are multiple classifications, label is transformed into multiple binary classifications by one hot.
    For each channel section in the channel, it can be regarded as a binary classification problem, so it can be
    obtained through the binary loss of each category, and then the average value.

    Args:
        weights (Union[Tensor, None]): Tensor of shape :math:`(num\_classes, dim)`. The weight shape[0] should be
            equal to labels shape[1].
        ignore_indiex (Union[int, None]): Class index to ignore.
        activation (Union[str, Cell]): Activate function applied to the output of the fully connected layer, eg. 'ReLU'.
            Default: 'softmax'. Choose from: ['softmax', 'logsoftmax', 'relu', 'relu6', 'tanh','Sigmoid']

    Inputs:
        - **logits** (Tensor) - Tensor of shape :math:`(N, C, *)` where :math:`*` means, any number of additional
          dimensions. The logits dimension should be greater than 1. The data type must be float16 or float32.
        - **labels** (Tensor) - Tensor of shape :math:`(N, C, *)`, same shape as the `logits`.
          The labels dimension should be greater than 1. The data type must be loat16 or float32.

    Outputs:
        Tensor, a tensor of shape with the per-example sampled MultiClass Dice Losses.

    Raises:
        ValueError: If the shape of `logits` is different from `labels`.
        TypeError: If the type of `logits` or `labels` is not a Tensor.
        ValueError: If the dimension of `logits` or `labels` is less than 2.
        ValueError: If the weights.shape[0] is not equal to labels.shape[1].
        ValueError: If `weights` is a tensor, but its dimension is not 2.

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> loss = nn.MultiClassDiceLoss(weights=None, ignore_indiex=None, activation="softmax")
        >>> logits = Tensor(np.array([[0.2, 0.5, 0.7], [0.3, 0.1, 0.5], [0.9, 0.6, 0.3]]), mstype.float32)
        >>> labels = Tensor(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]]), mstype.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        0.54958105
    """
    def __init__(self, weights=None, ignore_indiex=None, activation="softmax"):
        """Initialize MultiClassDiceLoss."""
        super(MultiClassDiceLoss, self).__init__()
        activation_list = ['softmax', 'logsoftmax', 'relu', 'relu6', 'tanh', 'sigmoid']

        self.binarydiceloss = DiceLoss(smooth=1e-5)
        self.weights = weights if weights is None else validator.check_value_type("weights", weights, [Tensor])
        if isinstance(self.weights, Tensor) and self.weights.ndim != 2:
            raise ValueError("The weight dim should be 2, but got {}.".format(self.weights.ndim))
        self.ignore_indiex = ignore_indiex if ignore_indiex is None else \
            validator.check_value_type("ignore_indiex", ignore_indiex, [int])
        if isinstance(activation, str) and activation not in activation_list:
            raise ValueError("The activation must be in {}, but got {}.".format(activation_list, activation))

        self.activation = get_activation(activation) if isinstance(activation, str) else activation
        if self.activation is not None and not isinstance(self.activation, Cell):
            raise TypeError("The activation must be str or Cell, but got {}.".format(type(self.activation)))
        self.reshape = P.Reshape()

    def construct(self, logits, label):
        _check_is_tensor('logits', logits, self.cls_name)
        _check_is_tensor('labels', label, self.cls_name)
        _check_shape(logits.shape, label.shape)
        _check_ndim_multi(logits.ndim, label.ndim)
        total_loss = 0

        if self.activation is not None:
            logits = self.activation(logits)

        for i in range(label.shape[1]):
            if i != self.ignore_indiex:
                dice_loss = self.binarydiceloss(logits[:, i], label[:, i])
                if self.weights is not None:
                    _check_weights(self.weights.shape[0], label.shape[1])
                    dice_loss *= self.weights[i]
                total_loss += dice_loss

        return total_loss/label.shape[1]


class SampledSoftmaxLoss(LossBase):
    r"""
    Computes the sampled softmax training loss. This operator can accelerate the trainging of the softmax classifier
    over a large number of classes. It is generally an underestimate of the full softmax loss.

    Args:
        num_sampled (int): The number of classes to randomly sample per batch.
        num_classes (int): The number of possible classes.
        num_true (int): The number of target classes per training example. Default: 1.
        sampled_values (Union[list, tuple]):  List or tuple of (`sampled_candidates`, `true_expected_count`,
            `sampled_expected_count`) returned by a `*CandidateSampler` function.
            Default to None, `UniformCandidateSampler` is applied.
        remove_accidental_hits (bool): Whether to remove "accidental hits"
            where a sampled class equals one of the target classes.  Default is True.
        seed (int): Random seed for candidate sampling. Default: 0
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
            If "none", do not perform reduction. Default: "none".

    Inputs:
        - **weights** (Tensor) - Tensor of shape :math:`(C, dim)`.
        - **bias** (Tensor) - Tensor of shape :math:`(C,)`. The class biases.
        - **labels** (Tensor) - Tensor of shape :math:`(N, num\_true)`, type `int64, int32`. The target classes.
        - **logits** (Tensor) - Tensor of shape :math:`(N, dim)`. The forward activations of the input network.

    Outputs:
        Tensor or Scalar, if `reduction` is 'none', then output is a tensor with shape :math:`(N,)`.
        Otherwise, the output is a scalar.

    Raises:
        TypeError: If `sampled_values` is not a list or tuple.
        TypeError: If dtype of `labels` is neither int32 not int64.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.
        ValueError: If `num_sampled` or `num_true` is great than `num_classes`.
        ValueError: If length of `sampled_values` is not equal to 3.

    Supported Platforms:
        ``GPU``

    Examples:
        >>> mindspore.set_seed(1)
        >>> loss = nn.SampledSoftmaxLoss(num_sampled=4, num_classes=7, num_true=1)
        >>> weights = Tensor(np.random.randint(0, 9, [7, 10]), mindspore.float32)
        >>> biases = Tensor(np.random.randint(0, 9, [7]), mindspore.float32)
        >>> labels = Tensor([0, 1, 2])
        >>> logits = Tensor(np.random.randint(0, 9, [3, 10]), mindspore.float32)
        >>> output = loss(weights, biases, labels, logits)
        >>> print(output)
        [4.6051701e+01 1.4000047e+01 6.1989022e-06]
    """

    def __init__(self, num_sampled, num_classes, num_true=1,
                 sampled_values=None, remove_accidental_hits=True, seed=0,
                 reduction='none'):
        """Initialize SampledSoftmaxLoss."""
        super(SampledSoftmaxLoss, self).__init__(reduction)

        if num_true < 1:
            raise ValueError(f"num_true {num_true} is less than 1.")
        if seed < 0:
            raise ValueError(f"seed {seed} is less than 0.")
        if num_sampled > num_classes:
            raise ValueError(f"num_sampled {num_sampled} is great than num_classes {num_classes}.")
        if num_true > num_classes:
            raise ValueError(f"num_true {num_true} is great than num_classes {num_classes}.")
        if sampled_values is not None:
            if not isinstance(sampled_values, (list, tuple)):
                raise TypeError(f"sampled_values {sampled_values} is not a list or tuple.")
            if len(sampled_values) != 3:
                raise ValueError(f"sampled_values size {len(sampled_values)} is not 3.")

        self.num_sampled = num_sampled
        self.num_classes = num_classes
        self.num_true = num_true
        self.sampled_values = sampled_values
        self.remove_accidental_hits = remove_accidental_hits
        self.seed = seed
        self.sampler = P.UniformCandidateSampler(
            num_true,
            num_sampled,
            True,
            num_classes,
            seed,
            remove_accidental_hits)
        self.cast = P.Cast()
        self.reshape = P.Reshape()
        self.shape = P.Shape()
        self.exp = P.Exp()
        self.log = P.Log()
        self.slice_op = P.Slice()
        self.matmul = P.MatMul(False, True)
        self.gather_v2 = P.Gather()
        self.reduce_max_true = P.ReduceMax(True)
        self.reduce_sum = P.ReduceSum()
        self.reduce_sum_true = P.ReduceSum(True)
        self.concat_dim0 = P.Concat(0)
        self.concat_dim1 = P.Concat(1)
        self.ones_like = P.OnesLike()
        self.zeros_like = P.ZerosLike()
        self.mul = P.Mul()
        self.expand_dims = P.ExpandDims()
        self.dtype = P.DType()

    def construct(self, weights, biases, labels, inputs):
        _check_is_tensor('weights', weights, self.cls_name)
        _check_is_tensor('biases', biases, self.cls_name)
        _check_is_tensor('labels', labels, self.cls_name)
        _check_is_tensor('inputs', inputs, self.cls_name)
        _check_label_dtype(self.dtype(labels), self.cls_name)

        logits, labels = self._compute_sampled_logits(
            weights=weights,
            biases=biases,
            labels=labels,
            inputs=inputs,
            num_true=self.num_true,
            sampled_values=self.sampled_values,
            subtract_log_q=True)

        x = self._softmax_cross_entropy(logits, labels)
        return x

    def _softmax_cross_entropy(self, logits, targets):
        stable_exp_logits = self.exp(logits - self.reduce_max_true(logits, 1))
        pred = stable_exp_logits / self.reduce_sum_true(stable_exp_logits, 1)
        return -self.reduce_sum(targets * self.log(pred + 1.0e-20), 1)

    def _compute_sampled_logits(self, weights,
                                biases,
                                labels,
                                inputs,
                                num_true=1,
                                sampled_values=None,
                                subtract_log_q=True):
        """Helper function for SampledSoftmaxLoss functions.

        Computes sampled output training logits and labels suitable

        Note: In the case where num_true > 1, we assign to each target class
        the target probability 1 / num_true so that the target probabilities
        sum to 1 per-example.

        Args:
            weights (Tensor): Tensor of shape `[num_classes, dim]`.
            biases (Tensor): Tensor of shape `[num_classes]`.
            labels (Tensor): Tensor of shape `[batch_size, num_true]`. The target classes.
            inputs (Tensor): Tensor of shape `[batch_size, dim]`.  The forward
                activations of the input network.
            num_true (int): The number of target classes per training example.
            sampled_values: a tuple of (`sampled_candidates`, `true_expected_count`,
                `sampled_expected_count`) returned by a `UniformCandidateSampler` function.
            subtract_log_q: A `bool`.  whether to subtract the log expected count of
                the labels in the sample to get the logits of the true labels.
                Default is True.
        Returns:
            out_logits: `Tensor` object with shape
                `[batch_size, num_true + num_sampled]`
            out_labels: A Tensor object with the same shape as `out_logits`.
        """

        if not labels.dtype == mstype.int32:
            labels = self.cast(labels, mstype.int32)
        labels = self.reshape(labels, (-1, num_true))
        labels_flat = self.reshape(labels, (-1,))

        # Sample the negative labels.
        #   sampled shape: [num_sampled] tensor
        #   true_expected_count shape is [batch_size, 1] tensor
        #   sampled_expected_count shape is [num_sampled] tensor
        if sampled_values is None:
            sampled_values = self.sampler(labels)

        (sampled, true_expected_count, sampled_expected_count) = sampled_values

        if not sampled.dtype == mstype.int32:
            sampled = self.cast(sampled, mstype.int32)
        all_ids = self.concat_dim0((labels_flat, sampled))
        all_w = self.gather_v2(weights, all_ids, 0)

        n_true = self.shape(labels_flat)[0]
        n_sampled = self.shape(sampled)[0]
        n_dim = self.shape(all_w)[1]

        true_w = self.slice_op(all_w, [0, 0], [n_true, n_dim])
        sampled_w = self.slice_op(all_w, [n_true, 0], [n_sampled, n_dim])
        sampled_logits = self.matmul(inputs, sampled_w)

        all_b = self.gather_v2(biases, all_ids, 0)
        true_b = self.slice_op(all_b, [0], [n_true])
        sampled_b = self.slice_op(all_b, [n_true], [n_sampled])

        new_true_w_shape = (-1, num_true, n_dim)
        row_wise_dots = self.mul(self.expand_dims(inputs, 1),
                                 self.reshape(true_w, new_true_w_shape))

        # We want the row-wise dot plus biases which yields a
        # [batch_size, num_true] tensor of true_logits.
        dots_as_matrix = self.reshape(row_wise_dots, (-1, n_dim))
        true_logits = self.reshape(self.reduce_sum(dots_as_matrix, 1), (-1, num_true))
        true_b = self.reshape(true_b, (-1, num_true))
        true_logits += true_b
        sampled_logits += sampled_b

        if subtract_log_q:
            # Subtract log of Q(l), prior probability that l appears in sampled.
            true_logits -= self.log(true_expected_count)
            sampled_logits -= self.log(sampled_expected_count)

        # Construct output logits and labels. The true labels/logits start at col 0.
        out_logits = self.concat_dim1((true_logits, sampled_logits))

        # true_logits is a float tensor, ones_like(true_logits) is a float
        # tensor of ones. We then divide by num_true to ensure the per-example
        # labels sum to 1.0, i.e. form a proper probability distribution.
        out_labels = self.concat_dim1((
            self.ones_like(true_logits) / num_true,
            self.zeros_like(sampled_logits)
        ))
        return out_logits, out_labels


class BCELoss(LossBase):
    r"""
    BCELoss creates a criterion to measure the binary cross entropy between the true labels and predicted labels.

    Set the predicted labels as :math:`x`, true labels as :math:`y`, the output loss as :math:`\ell(x, y)`.
    Let,

    .. math::
        L = \{l_1,\dots,l_N\}^\top, \quad
        l_n = - w_n \left[ y_n \cdot \log x_n + (1 - y_n) \cdot \log (1 - x_n) \right]

    Then,

    .. math::
        \ell(x, y) = \begin{cases}
        L, & \text{if reduction} = \text{'none';}\\
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    Note:
        Note that the predicted labels should always be the output of sigmoid and the true labels should be numbers
        between 0 and 1.

    Args:
        weight (Tensor, optional): A rescaling weight applied to the loss of each batch element.
            And it must have same shape and data type as `inputs`. Default: None
        reduction (str): Specifies the reduction to be applied to the output.
            Its value must be one of 'none', 'mean', 'sum'. Default: 'none'.

    Inputs:
        - **logits** (Tensor) - The input Tensor with shape :math:`(N, *)` where :math:`*` means, any number
          of additional dimensions. The data type must be float16 or float32.
        - **labels** (Tensor) - The label Tensor with shape :math:`(N, *)`, same shape and data type as `logits`.

    Outputs:
        Tensor or Scalar, if `reduction` is 'none', then output is a tensor and has the same shape as `logits`.
        Otherwise, the output is a scalar.

    Raises:
        TypeError: If dtype of `logits`, `labels` or `weight` (if given) is neither float16 not float32.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.
        ValueError: If shape of `logits` is not the same as `labels` or `weight` (if given).

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> weight = Tensor(np.array([[1.0, 2.0, 3.0], [4.0, 3.3, 2.2]]), mindspore.float32)
        >>> loss = nn.BCELoss(weight=weight, reduction='mean')
        >>> logits = Tensor(np.array([[0.1, 0.2, 0.3], [0.5, 0.7, 0.9]]), mindspore.float32)
        >>> labels = Tensor(np.array([[0, 1, 0], [0, 0, 1]]), mindspore.float32)
        >>> output = loss(logits, labels)
        >>> print(output)
        1.8952923
    """

    def __init__(self, weight=None, reduction='none'):
        """Initialize BCELoss."""
        super(BCELoss, self).__init__()
        self.binary_cross_entropy = P.BinaryCrossEntropy(reduction=reduction)
        self.weight_one = weight is None
        if not self.weight_one:
            self.weight = weight
        else:
            self.ones = P.OnesLike()

    def construct(self, inputs, labels):
        _check_is_tensor('logits', inputs, self.cls_name)
        _check_is_tensor('labels', labels, self.cls_name)
        if self.weight_one:
            weight = self.ones(inputs)
        else:
            weight = self.weight
        loss = self.binary_cross_entropy(inputs, labels, weight)
        return loss


@constexpr
def _check_reduced_shape_valid(ori_shape, reduced_shape, axis, cls_name):
    validator.check_reduce_shape(ori_shape, reduced_shape, axis, cls_name)


class CosineEmbeddingLoss(LossBase):
    r"""
    CosineEmbeddingLoss creates a criterion to measure the similarity between two tensors using cosine distance.

    Given two tensors :math:`x1`, :math:`x2`, and a Tensor label :math:`y` with values 1 or -1:

    .. math::
        loss(x_1, x_2, y) = \begin{cases}
        1-cos(x_1, x_2), & \text{if } y = 1\\
        max(0, cos(x_1, x_2)-margin), & \text{if } y = -1\\
        \end{cases}

    Args:
        margin (float): Should be in [-1.0, 1.0]. Default 0.0.
        reduction (str): Specifies which reduction to be applied to the output. It must be one of
          "none", "mean", and "sum", meaning no reduction, reduce mean and sum on output, respectively. Default "mean".

    Inputs:
        - **logits_x1** (Tensor) - Tensor of shape :math:`(N, *)` where :math:`*` means, any number
          of additional dimensions.
        - **logits_x2** (Tensor) - Tensor of shape :math:`(N, *)`, same shape and dtype as `logits_x1`.
        - **labels** (Tensor) - Contains value 1 or -1. Suppose the shape of `logits_x1` is
          :math:`(x_1, x_2, x_3, ..., x_R)`, then the shape of `labels` must be :math:`(x_1, x_3, x_4, ..., x_R)`.

    Outputs:
        Tensor or Scalar, if `reduction` is "none", its shape is the same as `labels`.
        Otherwise, a scalar value will be returned.

    Raises:
        TypeError: If `margin` is not a float.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.
        ValueError: If `margin` is not in range [-1, 1].

    Supported Platforms:
        ``Ascend`` ``GPU``

    Examples:
        >>> logits_x1 = Tensor(np.array([[0.3, 0.8], [0.4, 0.3]]), mindspore.float32)
        >>> logits_x2 = Tensor(np.array([[0.4, 1.2], [-0.4, -0.9]]), mindspore.float32)
        >>> labels = Tensor(np.array([1, -1]), mindspore.int32)
        >>> cosine_embedding_loss = nn.CosineEmbeddingLoss()
        >>> output = cosine_embedding_loss(logits_x1, logits_x2, labels)
        >>> print(output)
        0.0003425479
    """
    def __init__(self, margin=0.0, reduction="mean"):
        """Initialize CosineEmbeddingLoss."""
        super(CosineEmbeddingLoss, self).__init__(reduction)
        self.reduce_sum = P.ReduceSum()
        self.maximum = P.Maximum()
        validator.check_value_type("margin", margin, [float], self.cls_name)
        self.margin = validator.check_float_range(margin, -1.0, 1.0, Rel.INC_BOTH, "margin", self.cls_name)

    def construct(self, x1, x2, y):
        _check_is_tensor('logits_x1', x1, self.cls_name)
        _check_is_tensor('logits_x2', x2, self.cls_name)
        _check_is_tensor('labels', y, self.cls_name)
        F.same_type_shape(x1, x2)
        _check_reduced_shape_valid(F.shape(x1), F.shape(y), (1,), self.cls_name)
        # if target > 0, 1-cosine(x1, x2)
        # else, max(0, cosine(x1, x2)-margin)
        prod_sum = self.reduce_sum(x1 * x2, (1,))
        square1 = self.reduce_sum(F.square(x1), (1,))
        square2 = self.reduce_sum(F.square(x2), (1,))
        denom = F.sqrt(square1) * F.sqrt(square2)
        cosine = prod_sum / denom

        pos_value = 1.0 - cosine
        neg_value = self.maximum(cosine - self.margin, 0.0)
        zeros = F.zeros_like(cosine)
        pos_part = F.select(y == 1, pos_value, zeros)
        neg_part = F.select(y == -1, neg_value, zeros)
        output_unreduced = pos_part + neg_part

        return self.get_loss(output_unreduced)


class BCEWithLogitsLoss(LossBase):
    r"""
    Adds sigmoid activation function to input logits, and uses the given logits to compute binary cross entropy
    between the labels and the output.

    Sets input `logits` as :math:`X`, input `labels` as :math:`Y`, output as :math:`L`. Then,

    .. math::
        p_{ij} = sigmoid(X_{ij}) = \frac{1}{1 + e^{-X_{ij}}}

    .. math::
        L_{ij} = -[Y_{ij} \cdot log(p_{ij}) + (1 - Y_{ij}) \cdot log(1 - p_{ij})]

    Then,

    .. math::
        \ell(x, y) = \begin{cases}
        L, & \text{if reduction} = \text{'none';}\\
        \operatorname{mean}(L), & \text{if reduction} = \text{'mean';}\\
        \operatorname{sum}(L),  & \text{if reduction} = \text{'sum'.}
        \end{cases}

    Args:
        reduction (str): Type of reduction to be applied to loss. The optional values are 'mean', 'sum', and 'none'.
            If 'none', do not perform reduction. Default:'mean'.
        weight (Tensor, optional): A rescaling weight applied to the loss of each batch element.
            If not None, it must can be broadcast to a tensor with shape of `logits`,
            data type must be float16 or float32. Default: None.
        pos_weight (Tensor, optional): A weight of positive examples. Must be a vector with length equal to the
            number of classes. If not None, it must can be broadcast to a tensor with shape of `logits`,
            data type must be float16 or float32. Default: None.

    Inputs:
        - **logits** (Tensor) - Input logits with shape :math:`(N, *)` where :math:`*` means, any number
          of additional dimensions. The data type must be float16 or float32.
        - **labels** (Tensor) - Ground truth label with shape :math:`(N, *)`, same shape and dtype as `logits`.

    Outputs:
        Tensor or Scalar, if `reduction` is "none", its shape is the same as `logits`.
        Otherwise, a scalar value will be returned.

    Raises:
        TypeError: If data type of `logits` or `labels` is neither float16 nor float32.
        TypeError: If `weight` or `pos_weight` is Parameter.
        TypeError: If data type of `weight` or `pos_weight` is neither float16 nor float32.
        ValueError: If `weight` or `pos_weight` can not be broadcast to a tensor with shape of `logits`.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend``  ``GPU``

    Examples:
        >>> logits = Tensor(np.array([[-0.8, 1.2, 0.7], [-0.1, -0.4, 0.7]]).astype(np.float32))
        >>> labels = Tensor(np.array([[0.3, 0.8, 1.2], [-0.6, 0.1, 2.2]]).astype(np.float32))
        >>> loss = nn.BCEWithLogitsLoss()
        >>> output = loss(logits, labels)
        >>> print(output)
        0.3463612
    """

    def __init__(self, reduction='mean', weight=None, pos_weight=None):
        """Initialize BCEWithLogitsLoss."""
        super(BCEWithLogitsLoss, self).__init__()
        self.bce_with_logits_loss = P.BCEWithLogitsLoss(reduction=reduction)
        if isinstance(weight, Parameter):
            raise TypeError(f"For {self.cls_name}, weight can not be Parameter.")
        if isinstance(pos_weight, Parameter):
            raise TypeError(f"For {self.cls_name}, pos_weight can not be Parameter.")
        self.weight = weight
        self.pos_weight = pos_weight
        self.ones = P.OnesLike()

    def construct(self, predict, target):
        _check_is_tensor('logits', predict, self.cls_name)
        _check_is_tensor('labels', target, self.cls_name)
        ones_input = self.ones(predict)
        if self.weight is not None:
            weight = self.weight
        else:
            weight = ones_input
        if self.pos_weight is not None:
            pos_weight = self.pos_weight
        else:
            pos_weight = ones_input
        loss = self.bce_with_logits_loss(predict, target, weight, pos_weight)
        return loss


@constexpr
def _check_ndim(predict_nidm, target_ndim):
    if predict_nidm < 2 or predict_nidm > 4:
        raise ValueError("The dimensions of predict and target should be between 2 and 4, but got"
                         "predict dim {}.".format(predict_nidm))
    if target_ndim < 2 or target_ndim > 4:
        raise ValueError("The dimensions of target and target should be between 2 and 4, but got"
                         "target dim {}.".format(target_ndim))
    if predict_nidm != target_ndim:
        raise ValueError("The dim of the predicted value and the dim of the target value must be equal, but got"
                         "predict dim {} and target dim {}.".format(predict_nidm, target_ndim))


@constexpr
def _check_channel_and_shape(predict, target):
    if predict == 1:
        raise ValueError("Single channel prediction is not supported.")
    if target not in (1, predict):
        raise ValueError("The target must have a channel or the same shape as predict."
                         "If it has a channel, it should be the range [0, C-1], where C is the number of classes "
                         f"inferred from 'predict': C={predict}.")


@constexpr
def _check_input_dtype(targets_dtype, cls_name):
    validator.check_type_name("targets", targets_dtype, [mstype.int32, mstype.int64, mstype.float16,
                                                         mstype.float32], cls_name)


class FocalLoss(LossBase):
    r"""
    The loss function proposed by Kaiming team in their paper ``Focal Loss for Dense Object Detection`` improves the
    effect of image object detection. It is a loss function to solve the imbalance of categories and the difference of
    classification difficulty. If you want to learn more, please refer to the paper.
    `Focal Loss for Dense Object Detection <https://arxiv.org/pdf/1708.02002.pdf>`_. The function is shown as follows:

    .. math::
        FL(p_t) = -(1-p_t)^\gamma log(p_t)

    Args:
        gamma (float): Gamma is used to adjust the steepness of weight curve in focal loss. Default: 2.0.
        weight (Union[Tensor, None]): A rescaling weight applied to the loss of each batch element. The dimension of
                                      weight should be 1. If None, no weights are applied. Default: None.
        reduction (str): Type of reduction to be applied to loss. The optional values are "mean", "sum", and "none".
                         If "none", do not perform reduction. Default: "mean".

    Inputs:
        - **logits** (Tensor) - Tensor of shape should be :math:`(B, C)` or :math:`(B, C, H)` or :math:`(B, C, H, W)`.
          Where :math:`C` is the number of classes. Its value is greater than 1. If the shape is :math:`(B, C, H, W)`
          or :math:`(B, C, H)`, the :math:`H` or product of :math:`H` and :math:`W` should be the same as labels.
        - **labels** (Tensor) - Tensor of shape should be :math:`(B, C)` or :math:`(B, C, H)` or :math:`(B, C, H, W)`.
          The value of :math:`C` is 1 or it needs to be the same as predict's :math:`C`. If :math:`C` is not 1,
          the shape of target should be the same as that of predict, where :math:`C` is the number of classes.
          If the shape is :math:`(B, C, H, W)` or :math:`(B, C, H)`, the :math:`H` or product of :math:`H`
          and :math:`W` should be the same as logits.

    Outputs:
        Tensor or Scalar, if `reduction` is "none", its shape is the same as `logits`.
        Otherwise, a scalar value will be returned.

    Raises:
        TypeError: If the data type of `gamma` is not a float.
        TypeError: If `weight` is not a Tensor.
        ValueError: If `labels` dim is different from `logits`.
        ValueError: If `labels` channel is not 1 and `labels` shape is different from `logits`.
        ValueError: If `reduction` is not one of 'none', 'mean', 'sum'.

    Supported Platforms:
        ``Ascend``

    Example:
        >>> logits = Tensor([[0.8, 1.4], [0.5, 0.9], [1.2, 0.9]], mstype.float32)
        >>> labels = Tensor([[1], [1], [0]], mstype.int32)
        >>> focalloss = nn.FocalLoss(weight=Tensor([1, 2]), gamma=2.0, reduction='mean')
        >>> output = focalloss(logits, labels)
        >>> print(output)
        0.12516622
    """

    def __init__(self, weight=None, gamma=2.0, reduction='mean'):
        """Initialize FocalLoss."""
        super(FocalLoss, self).__init__(reduction=reduction)

        self.gamma = validator.check_value_type("gamma", gamma, [float])
        if weight is not None and not isinstance(weight, Tensor):
            raise TypeError("The type of weight should be Tensor, but got {}.".format(type(weight)))
        if isinstance(weight, Tensor) and weight.ndim != 1:
            raise ValueError("The dimension of weight should be 1, but got {}.".format(weight.ndim))
        self.weight = weight
        self.expand_dims = P.ExpandDims()
        self.gather_d = P.GatherD()
        self.squeeze = P.Squeeze(axis=1)
        self.tile = P.Tile()
        self.cast = P.Cast()
        self.dtype = P.DType()
        self.logsoftmax = nn.LogSoftmax(1)

    def construct(self, predict, target):
        _check_is_tensor('logits', predict, self.cls_name)
        _check_is_tensor('labels', target, self.cls_name)
        targets = target
        _check_ndim(predict.ndim, targets.ndim)
        _check_channel_and_shape(predict.shape[1], targets.shape[1])
        _check_input_dtype(self.dtype(targets), self.cls_name)

        if predict.ndim > 2:
            predict = predict.view(predict.shape[0], predict.shape[1], -1)
            targets = targets.view(targets.shape[0], targets.shape[1], -1)
        else:
            predict = self.expand_dims(predict, 2)
            targets = self.expand_dims(targets, 2)

        log_probability = self.logsoftmax(predict)

        if target.shape[1] == 1:
            log_probability = self.gather_d(log_probability, 1, self.cast(targets, mindspore.int32))
            log_probability = self.squeeze(log_probability)

        probability = F.exp(log_probability)

        if self.weight is not None:
            convert_weight = self.weight[None, :, None]
            convert_weight = self.tile(convert_weight, (targets.shape[0], 1, targets.shape[2]))
            if target.shape[1] == 1:
                convert_weight = self.gather_d(convert_weight, 1, self.cast(targets, mindspore.int32))
                convert_weight = self.squeeze(convert_weight)
            log_probability = log_probability * convert_weight

        weight = F.pows(-probability + 1.0, self.gamma)
        if target.shape[1] == 1:
            loss = (-weight * log_probability).mean(axis=1)
        else:
            loss = (-weight * targets * log_probability).mean(axis=-1)

        return self.get_loss(loss)
