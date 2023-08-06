from typing import Callable, Sequence, Union, Any
from ..replay.core import _process_transforms


class Compose:
    """Composes several transforms together.
    """

    def __init__(self, transforms: Union[None, Callable, Sequence[Callable]] = None):
        self._transforms = _process_transforms(transforms)

    def __call__(self, batch: Any):
        for t in self._transforms:
            batch = t(batch)
        return batch

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self._transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string
