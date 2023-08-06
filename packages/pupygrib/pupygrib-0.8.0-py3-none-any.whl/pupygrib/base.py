"""Base classes for GRIB messages of edition 1 and 2."""

from __future__ import annotations

import datetime
import itertools
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Union

import numpy as np

from pupygrib.fields import BaseField as BaseField
from pupygrib.utils import ReadableBuffer

if TYPE_CHECKING:
    from numpy.typing import NDArray


class SectionMeta(type):
    """Meta class for GRIB message sections.

    This meta class automatically assign names to fields from the
    attribute name they are given on the class.  It is also
    responsible for assigning the fieldnames property to sections.

    """

    def __init__(
        cls, name: str, bases: tuple[type, ...], namespace: dict[str, object]
    ) -> None:
        fieldnames = set(
            itertools.chain.from_iterable(
                base.fieldnames for base in bases if issubclass(base, BaseSection)
            )
        )
        for key, value in namespace.items():
            if isinstance(value, BaseField):
                value.name = key
                fieldnames.add(key)
        cls.fieldnames = fieldnames


class BaseSection(metaclass=SectionMeta):
    """Base class for sections of GRIB messages.

    The *data* argument should be a memoryview of the whole GRIB
    message.  *offset* and *length* gives the slice that belongs to
    this section of that view.

    """

    fieldnames: set[str]

    def __init__(self, buf: memoryview, offset: int, length: int) -> None:
        self.offset = offset
        self.end = offset + length
        self.buf = buf[self.offset : self.end]


ValueArray = Union["NDArray[np.double]", "np.ma.MaskedArray[Any, np.dtype[np.double]]"]


class Message(metaclass=ABCMeta):
    """Abstact base class for GRIB messages of edition 1 and 2."""

    def __init__(self, buf: ReadableBuffer, filename: str | None = None) -> None:
        self.filename = filename
        self.buf = memoryview(buf)

    @property
    @abstractmethod
    def edition(self) -> int:
        """The integer edition number of this message."""
        raise NotImplementedError

    @abstractmethod
    def get_coordinates(self) -> tuple[NDArray[np.double], NDArray[np.double]]:
        """Return the coordinates of this message's data points."""
        raise NotImplementedError

    @abstractmethod
    def get_time(self) -> datetime.datetime:
        """Return the reference time of the message."""
        raise NotImplementedError

    @abstractmethod
    def get_values(self) -> ValueArray:
        """Return the data values of this message."""
        raise NotImplementedError
