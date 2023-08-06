"""Bit-map section of edition 1 GRIB messages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from pupygrib import fields
from pupygrib.base import BaseField, BaseSection

if TYPE_CHECKING:
    from numpy.typing import NDArray


class BitMapField(BaseField["BitMapSection", "NDArray[np.uint8]"]):
    def get_value(self, section: "BitMapSection", offset: int) -> NDArray[np.uint8]:
        if section.tableReference > 0:
            raise NotImplementedError("pupygrib does not support catalogued bit-maps")

        bitmap: NDArray[np.uint8] = np.frombuffer(
            section.buf, dtype="u1", offset=offset
        )
        unused_bits = section.numberOfUnusedBitsAtEndOfSection3
        return np.unpackbits(bitmap)[:-unused_bits]


class BitMapSection(BaseSection):
    """The bit-map section (3) of an edition 1 GRIB message."""

    section3Length = fields.Uint24Field(1)
    numberOfUnusedBitsAtEndOfSection3 = fields.Uint8Field(4)
    tableReference = fields.Uint16Field(5)
    bitmap = BitMapField(7)
