# Copyright 2021, The TensorFlow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tree aggregation algorithm.

`TreeAggregator` and `EfficientTreeAggregator` compute cumulative sums of noise
based on tree aggregation. When using an appropriate noise function (e.g.,
Gaussian noise), it allows for efficient differentially private algorithms under
continual observation, without prior subsampling or shuffling assumptions.
"""

import abc
from typing import Any, Callable, Collection, Optional, Tuple, Union

import attr
import tensorflow as tf


class ValueGenerator(metaclass=abc.ABCMeta):
  """Base class establishing interface for stateful value generation.

  A `ValueGenerator` maintains a state, and each time `next` is called, a new
  value is generated and the state is advanced.
  """

  @abc.abstractmethod
  def initialize(self):
    """Makes an initialized state for the ValueGenerator.

    Returns:
      An initial state.
    """

  @abc.abstractmethod
  def next(self, state):
    """Gets next value and advances the ValueGenerator.

    Args:
      state: The current state.

    Returns:
      A pair (value, new_state) where value is the next value and new_state
        is the advanced state.
    """


class GaussianNoiseGenerator(ValueGenerator):
  """Gaussian noise generator with counter as pseudo state.

  Produces i.i.d. spherical Gaussian noise at each step shaped according to a
  nested structure of `tf.TensorSpec`s.
  """

  def __init__(self,
               noise_std: float,
               specs: Collection[tf.TensorSpec],
               seed: Optional[int] = None):
    """Initializes the GaussianNoiseGenerator.

    Args:
      noise_std: The standard deviation of the noise.
      specs: A nested structure of `tf.TensorSpec`s specifying the shape of the
        noise to generate.
      seed: An optional integer seed. If None, generator is seeded from the
        clock.
    """
    self.noise_std = noise_std
    self.specs = specs
    self.seed = seed

  def initialize(self):
    """Makes an initial state for the GaussianNoiseGenerator.

    Returns:
      An initial state.
    """
    if self.seed is None:
      return tf.cast(
          tf.stack([
              tf.math.floor(tf.timestamp() * 1e6),
              tf.math.floor(tf.math.log(tf.timestamp() * 1e6))
          ]),
          dtype=tf.int64)
    else:
      return tf.constant(self.seed, dtype=tf.int64, shape=(2,))

  def next(self, state):
    """Gets next value and advances the GaussianNoiseGenerator.

    Args:
      state: The current state.

    Returns:
      A pair (sample, new_state) where sample is a new sample and new_state
        is the advanced state.
    """
    flat_structure = tf.nest.flatten(self.specs)
    flat_seeds = [state + i for i in range(len(flat_structure))]
    nest_seeds = tf.nest.pack_sequence_as(self.specs, flat_seeds)

    def _get_noise(spec, seed):
      return tf.random.stateless_normal(
          shape=spec.shape, seed=seed, stddev=self.noise_std)

    nest_noise = tf.nest.map_structure(_get_noise, self.specs, nest_seeds)
    return nest_noise, flat_seeds[-1] + 1


class StatelessValueGenerator(ValueGenerator):
  """A wrapper for stateless value generator that calls a no-arg function."""

  def __init__(self, value_fn):
    """Initializes the StatelessValueGenerator.

    Args:
      value_fn: The function to call to generate values.
    """
    self.value_fn = value_fn

  def initialize(self):
    """Makes an initialized state for the StatelessValueGenerator.

    Returns:
      An initial state (empty, because stateless).
    """
    return ()

  def next(self, state):
    """Gets next value.

    Args:
      state: The current state (simply passed through).

    Returns:
      A pair (value, new_state) where value is the next value and new_state
        is the advanced state.
    """
    return self.value_fn(), state


@attr.s(eq=False, frozen=True, slots=True)
class TreeState(object):
  """Class defining state of the tree.

  Attributes:
    level_buffer: A `tf.Tensor` saves the last node value of the left child
      entered for the tree levels recorded in `level_buffer_idx`.
    level_buffer_idx: A `tf.Tensor` for the tree level index of the
      `level_buffer`.  The tree level index starts from 0, i.e.,
      `level_buffer[0]` when `level_buffer_idx[0]==0` recorded the noise value
      for the most recent leaf node.
   value_generator_state: State of a stateful `ValueGenerator` for tree node.
  """
  level_buffer = attr.ib(type=tf.Tensor)
  level_buffer_idx = attr.ib(type=tf.Tensor)
  value_generator_state = attr.ib(type=Any)


@tf.function
def get_step_idx(state: TreeState) -> tf.Tensor:
  """Returns the current leaf node index based on `TreeState.level_buffer_idx`."""
  step_idx = tf.constant(-1, dtype=tf.int32)
  for i in tf.range(len(state.level_buffer_idx)):
    step_idx += tf.math.pow(2, state.level_buffer_idx[i])
  return step_idx


# TODO(b/192464750): instead of saving noise `TreeState.level_buffer`, we can
# save the random seed and online generate noise. This could save some memory
# and disk.


class TreeAggregator():
  """Tree aggregator to compute accumulated noise in private algorithms.

  This class implements the tree aggregation algorithm for noise values to
  efficiently privatize streaming algorithms based on Dwork et al. (2010)
  https://dl.acm.org/doi/pdf/10.1145/1806689.1806787. A buffer at the scale of
  tree depth is maintained and updated when a new conceptual leaf node arrives.

  Attributes:
    value_generator: A `ValueGenerator` or a no-arg function to generate a noise
      value for each tree node.
  """

  def __init__(self, value_generator: Union[ValueGenerator, Callable[[], Any]]):
    """Initialize the aggregator with a noise generator.

    Args:
      value_generator: A `ValueGenerator` or a no-arg function to generate a
        noise value for each tree node.
    """
    if isinstance(value_generator, ValueGenerator):
      self.value_generator = value_generator
    else:
      self.value_generator = StatelessValueGenerator(value_generator)

  def init_state(self) -> TreeState:
    """Returns initial `TreeState`.

    Initializes `TreeState` for a tree of a single leaf node: the respective
    initial node value in `TreeState.level_buffer` is generated by the value
    generator function, and the node index is 0.
    """
    value_generator_state = self.value_generator.initialize()
    level_buffer_idx = tf.TensorArray(dtype=tf.int32, size=1, dynamic_size=True)
    level_buffer_idx = level_buffer_idx.write(0, tf.constant(
        0, dtype=tf.int32)).stack()

    new_val, value_generator_state = self.value_generator.next(
        value_generator_state)
    level_buffer_structure = tf.nest.map_structure(
        lambda x: tf.TensorArray(dtype=tf.float32, size=1, dynamic_size=True),
        new_val)
    level_buffer = tf.nest.map_structure(lambda x, y: x.write(0, y).stack(),
                                         level_buffer_structure, new_val)

    return TreeState(
        level_buffer=level_buffer,
        level_buffer_idx=level_buffer_idx,
        value_generator_state=value_generator_state)

  @tf.function
  def _get_cumsum(self, level_buffer: Collection[tf.Tensor]) -> tf.Tensor:
    return tf.nest.map_structure(lambda x: tf.reduce_sum(x, axis=0),
                                 level_buffer)

  @tf.function
  def get_cumsum_and_update(self,
                            state: TreeState) -> Tuple[tf.Tensor, TreeState]:
    """Returns tree aggregated value and updated `TreeState` for one step.

    `TreeState` is updated to prepare for accepting the *next* leaf node. Note
    that `get_step_idx` can be called to get the current index of the leaf node
    before calling this function. This function accept state for the current
    leaf node and prepare for the next leaf node because TFF prefers to know
    the types of state at initialization.

    Args:
      state: `TreeState` for the current leaf node, index can be queried by
        `tree_aggregation.get_step_idx(state.level_buffer_idx)`.
    """

    level_buffer_idx, level_buffer, value_generator_state = (
        state.level_buffer_idx, state.level_buffer, state.value_generator_state)
    cumsum = self._get_cumsum(level_buffer)

    new_level_buffer = tf.nest.map_structure(
        lambda x: tf.TensorArray(  # pylint: disable=g-long-lambda
            dtype=tf.float32,
            size=0,
            dynamic_size=True),
        level_buffer)
    new_level_buffer_idx = tf.TensorArray(
        dtype=tf.int32, size=0, dynamic_size=True)
    # `TreeState` stores the left child node necessary for computing the cumsum
    # noise. To update the buffer, let us find the lowest level that will switch
    # from a right child (not in the buffer) to a left child.
    level_idx = 0  # new leaf node starts from level 0
    while tf.less(level_idx, len(level_buffer_idx)) and tf.equal(
        level_idx, level_buffer_idx[level_idx]):
      level_idx += 1
    # Left child nodes for the level lower than `level_idx` will be removed
    # and a new node will be created at `level_idx`.
    write_buffer_idx = 0
    new_level_buffer_idx = new_level_buffer_idx.write(write_buffer_idx,
                                                      level_idx)
    new_value, value_generator_state = self.value_generator.next(
        value_generator_state)
    new_level_buffer = tf.nest.map_structure(
        lambda x, y: x.write(write_buffer_idx, y), new_level_buffer, new_value)
    write_buffer_idx += 1
    # Buffer index will now different from level index for the old `TreeState`
    # i.e., `level_buffer_idx[level_idx] != level_idx`. Rename parameter to
    # buffer index for clarity.
    buffer_idx = level_idx
    while tf.less(buffer_idx, len(level_buffer_idx)):
      new_level_buffer_idx = new_level_buffer_idx.write(
          write_buffer_idx, level_buffer_idx[buffer_idx])
      new_level_buffer = tf.nest.map_structure(
          lambda nb, b: nb.write(write_buffer_idx, b[buffer_idx]),
          new_level_buffer, level_buffer)
      buffer_idx += 1
      write_buffer_idx += 1
    new_level_buffer_idx = new_level_buffer_idx.stack()
    new_level_buffer = tf.nest.map_structure(lambda x: x.stack(),
                                             new_level_buffer)
    new_state = TreeState(
        level_buffer=new_level_buffer,
        level_buffer_idx=new_level_buffer_idx,
        value_generator_state=value_generator_state)
    return cumsum, new_state


class EfficientTreeAggregator():
  """Efficient tree aggregator to compute accumulated noise.

  This class implements the efficient tree aggregation algorithm based on
  Honaker 2015 "Efficient Use of Differentially Private Binary Trees".
  The noise standard deviation for a node at depth d is roughly
  `sigma * sqrt(2^{d-1}/(2^d-1))`. which becomes `sigma / sqrt(2)` when
  the tree is very tall.

  Attributes:
    value_generator: A `ValueGenerator` or a no-arg function to generate a noise
      value for each tree node.
  """

  def __init__(self, value_generator: Union[ValueGenerator, Callable[[], Any]]):
    """Initialize the aggregator with a noise generator.

    Args:
      value_generator: A `ValueGenerator` or a no-arg function to generate a
        noise value for each tree node.
    """
    if isinstance(value_generator, ValueGenerator):
      self.value_generator = value_generator
    else:
      self.value_generator = StatelessValueGenerator(value_generator)

  def init_state(self) -> TreeState:
    """Returns initial `TreeState`.

    Initializes `TreeState` for a tree of a single leaf node: the respective
    initial node value in `TreeState.level_buffer` is generated by the value
    generator function, and the node index is 0.

    Returns:
      An initialized `TreeState`.
    """
    value_generator_state = self.value_generator.initialize()
    level_buffer_idx = tf.TensorArray(dtype=tf.int32, size=1, dynamic_size=True)
    level_buffer_idx = level_buffer_idx.write(0, tf.constant(
        0, dtype=tf.int32)).stack()

    new_val, value_generator_state = self.value_generator.next(
        value_generator_state)
    level_buffer_structure = tf.nest.map_structure(
        lambda x: tf.TensorArray(dtype=tf.float32, size=1, dynamic_size=True),
        new_val)
    level_buffer = tf.nest.map_structure(lambda x, y: x.write(0, y).stack(),
                                         level_buffer_structure, new_val)

    return TreeState(
        level_buffer=level_buffer,
        level_buffer_idx=level_buffer_idx,
        value_generator_state=value_generator_state)

  @tf.function
  def _get_cumsum(self, state: TreeState) -> tf.Tensor:
    """Returns weighted cumulative sum of noise based on `TreeState`."""
    # Note that the buffer saved recursive results of the weighted average of
    # the node value (v) and its two children (l, r), i.e., node = v + (l+r)/2.
    # To get unbiased estimation with reduced variance for each node, we have to
    # reweight it by 1/(2-2^{-d}) where d is the depth of the node.
    level_weights = tf.math.divide(
        1., 2. - tf.math.pow(.5, tf.cast(state.level_buffer_idx, tf.float32)))

    def _weighted_sum(buffer):
      expand_shape = [len(level_weights)] + [1] * (len(tf.shape(buffer)) - 1)
      weighted_buffer = tf.math.multiply(
          buffer, tf.reshape(level_weights, expand_shape))
      return tf.reduce_sum(weighted_buffer, axis=0)

    return tf.nest.map_structure(_weighted_sum, state.level_buffer)

  @tf.function
  def get_cumsum_and_update(self,
                            state: TreeState) -> Tuple[tf.Tensor, TreeState]:
    """Returns tree aggregated value and updated `TreeState` for one step.

    `TreeState` is updated to prepare for accepting the *next* leaf node. Note
    that `get_step_idx` can be called to get the current index of the leaf node
    before calling this function. This function accept state for the current
    leaf node and prepare for the next leaf node because TFF prefers to know
    the types of state at initialization. Note that the value of new node in
    `TreeState.level_buffer` will depend on its two children, and is updated
    from bottom up for the right child.

    Args:
      state: `TreeState` for the current leaf node, index can be queried by
        `tree_aggregation.get_step_idx(state.level_buffer_idx)`.
    """
    cumsum = self._get_cumsum(state)

    level_buffer_idx, level_buffer, value_generator_state = (
        state.level_buffer_idx, state.level_buffer, state.value_generator_state)
    new_level_buffer = tf.nest.map_structure(
        lambda x: tf.TensorArray(  # pylint: disable=g-long-lambda
            dtype=tf.float32,
            size=0,
            dynamic_size=True),
        level_buffer)
    new_level_buffer_idx = tf.TensorArray(
        dtype=tf.int32, size=0, dynamic_size=True)
    # `TreeState` stores the left child node necessary for computing the cumsum
    # noise. To update the buffer, let us find the lowest level that will switch
    # from a right child (not in the buffer) to a left child.
    level_idx = 0  # new leaf node starts from level 0
    new_value, value_generator_state = self.value_generator.next(
        value_generator_state)
    while tf.less(level_idx, len(level_buffer_idx)) and tf.equal(
        level_idx, level_buffer_idx[level_idx]):
      # Recursively update if the current node is a right child.
      node_value, value_generator_state = self.value_generator.next(
          value_generator_state)
      new_value = tf.nest.map_structure(
          lambda l, r, n: 0.5 * (l[level_idx] + r) + n, level_buffer, new_value,
          node_value)
      level_idx += 1
    # A new (left) node will be created at `level_idx`.
    write_buffer_idx = 0
    new_level_buffer_idx = new_level_buffer_idx.write(write_buffer_idx,
                                                      level_idx)
    new_level_buffer = tf.nest.map_structure(
        lambda x, y: x.write(write_buffer_idx, y), new_level_buffer, new_value)
    write_buffer_idx += 1
    # Buffer index will now different from level index for the old `TreeState`
    # i.e., `level_buffer_idx[level_idx] != level_idx`. Rename parameter to
    # buffer index for clarity.
    buffer_idx = level_idx
    while tf.less(buffer_idx, len(level_buffer_idx)):
      new_level_buffer_idx = new_level_buffer_idx.write(
          write_buffer_idx, level_buffer_idx[buffer_idx])
      new_level_buffer = tf.nest.map_structure(
          lambda nb, b: nb.write(write_buffer_idx, b[buffer_idx]),
          new_level_buffer, level_buffer)
      buffer_idx += 1
      write_buffer_idx += 1
    new_level_buffer_idx = new_level_buffer_idx.stack()
    new_level_buffer = tf.nest.map_structure(lambda x: x.stack(),
                                             new_level_buffer)
    new_state = TreeState(
        level_buffer=new_level_buffer,
        level_buffer_idx=new_level_buffer_idx,
        value_generator_state=value_generator_state)
    return cumsum, new_state
