"""Binary data sections of GRIB edition 1."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, cast

import numpy as np

from pupygrib import fields
from pupygrib.base import BaseField, BaseSection
from pupygrib.edition1.fields import FloatField

if TYPE_CHECKING:
    from numpy.typing import NDArray


class BinaryDataSection(BaseSection):
    """The binary data section (4) of an edition 1 GRIB message."""

    section4Length = fields.Uint24Field(1)
    dataFlag = fields.Uint8Field(4)
    binaryScaleFactor = fields.Int16Field(5)
    referenceValue = FloatField(7)
    bitsPerValue = fields.Uint8Field(11)

    def _unpack_values(self) -> NDArray[np.double]:
        raise NotImplementedError("pupygrib does not support the current packing")


class SimpleGridDataField(
    BaseField["SimpleGridDataSection", "NDArray[np.unsignedinteger[Any]]"]
):
    """Simply packed grid-point data values."""

    def get_value(
        self, section: "SimpleGridDataSection", offset: int
    ) -> NDArray[np.unsignedinteger[Any]]:
        bits_per_value = section.bitsPerValue
        if bits_per_value == 0:
            return np.array([], dtype=np.uint)
        if bits_per_value not in (8, 12, 16, 24, 32, 64):
            raise NotImplementedError(
                f"pupygrib does not support {bits_per_value} bits per value"
            )

        native_dtype = bits_per_value in (8, 16, 32, 64)
        num_bytes = bits_per_value // 8
        unused_bytes = (section.dataFlag & 0x0F) // 8
        dtype = np.dtype(">u{}".format(num_bytes if native_dtype else 1))
        buf = section.buf[offset : -unused_bytes or None]
        data: NDArray[np.unsignedinteger[Any]] = np.frombuffer(buf, dtype=dtype)
        if bits_per_value == 12:
            data = read_uint12(data)
        elif bits_per_value == 24:
            data = read_uint24(data)

        return data


def read_uint12(data: NDArray[np.uint8]) -> NDArray[np.uint16]:
    # https://stackoverflow.com/questions/44735756/python-reading-12-bit-binary-files
    fst_uint8, mid_uint8, lst_uint8 = (
        np.resize(data, (math.ceil(len(data) / 3), 3)).astype(np.uint16).T
    )
    fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
    snd_uint12 = ((mid_uint8 % 16) << 8) + lst_uint8
    output: NDArray[np.uint16] = np.concatenate(
        (fst_uint12[:, None], snd_uint12[:, None]), axis=1
    )
    output.resize(2 * len(data) // 3, refcheck=False)
    return output


def read_uint24(data: NDArray[np.uint8]) -> NDArray[np.uint32]:
    fst_uint8, mid_uint8, lst_uint8 = (
        np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint32).T
    )
    return (fst_uint8 << 16) + (mid_uint8 << 8) + lst_uint8


class SimpleGridDataSection(BinaryDataSection):
    """A simply packed grid-point data section (4) of GRIB edition 1."""

    values = SimpleGridDataField(12)

    def _unpack_values(self) -> NDArray[np.double]:
        raw_values = self.values
        if raw_values.size == 0:
            raw_values = np.array(0.0)
        unpacked_values = (
            self.referenceValue + raw_values * 2.0 ** self.binaryScaleFactor
        )
        # I assume this needs to be fixed in numpy
        return cast("NDArray[np.double]", unpacked_values)


def get_section(buf: memoryview, offset: int, length: int) -> BinaryDataSection:
    """Return a new section 4 of the correct type from *buf* at *offset*."""
    datadesc = BinaryDataSection(buf, offset, length)
    try:
        sectionclass = {0x00: SimpleGridDataSection}[datadesc.dataFlag & 0xF0]
    except KeyError:
        return datadesc
    else:
        return sectionclass(buf, offset, length)
