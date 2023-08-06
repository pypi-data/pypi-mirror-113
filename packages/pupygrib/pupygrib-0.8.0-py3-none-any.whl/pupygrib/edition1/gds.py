"""Grid description sections of edition 1 GRIB messages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from pupygrib import fields
from pupygrib.base import BaseSection
from pupygrib.edition1.fields import FloatField

if TYPE_CHECKING:
    from numpy.typing import NDArray


class GridDescriptionSection(BaseSection):
    """The grid description section (2) of an edition 1 GRIB message."""

    section2Length = fields.Uint24Field(1)
    numberOfVerticalCoordinateValues = fields.Uint8Field(4)
    pvlLocation = fields.Uint8Field(5)
    dataRepresentationType = fields.Uint8Field(6)

    def _order_values(self, values: NDArray[np.double]) -> NDArray[np.double]:
        return values

    def _get_coordinates(self) -> tuple[NDArray[np.double], NDArray[np.double]]:
        raise NotImplementedError(
            f"pupygrib does not support grids with data reporesentation type "
            f"{self.dataRepresentationType}"
        )


class LatitudeLongitudeGridSection(GridDescriptionSection):
    """A latitude/longitude grid section (2) of an edition 1 GRIB message."""

    Ni = fields.Uint16Field(7)
    Nj = fields.Uint16Field(9)
    latitudeOfFirstGridPoint = fields.Int24Field(11)
    longitudeOfFirstGridPoint = fields.Int24Field(14)
    resolutionAndComponentFlags = fields.Uint8Field(17)
    latitudeOfLastGridPoint = fields.Int24Field(18)
    longitudeOfLastGridPoint = fields.Int24Field(21)
    iDirectionIncrement = fields.Uint16Field(24)
    jDirectionIncrement = fields.Uint16Field(26)
    scanningMode = fields.Uint8Field(28)

    def _order_values(self, values: NDArray[np.double]) -> NDArray[np.double]:
        # Build a grid array from a flat array or a scalar.
        array = super()._order_values(values)
        if array.ndim == 0:
            array = np.full(self.Ni * self.Nj, array)
        if self.scanningMode & 0x20:  # consecutive points in j direction
            if self.scanningMode & 0x40:  # points scan in +j direction
                array = array[::-1]
            array = np.reshape(array, (self.Ni, self.Nj))
            if self.scanningMode & 0x80:  # points scan in -i direction
                array = np.fliplr(array)
        else:  # consecutive points in i direction
            if self.scanningMode & 0x80:  # points scan in -i direction
                array = array[::-1]
            array = np.reshape(array, (self.Nj, self.Ni))
            if self.scanningMode & 0x40:  # points scan in +j direction
                array = np.flipud(array)
        return array

    def _get_coordinates(self) -> tuple[NDArray[np.double], NDArray[np.double]]:
        # The raw lat/lons are stored in millidegrees.
        lon0 = 1e-3 * self.longitudeOfFirstGridPoint
        lon1 = 1e-3 * self.longitudeOfLastGridPoint
        if self.scanningMode & 0x80:  # points scan in -i direction
            lon0, lon1 = lon1, lon0
        longitudes: NDArray[np.double] = np.linspace(lon0, lon1, self.Ni)
        lat0 = 1e-3 * self.latitudeOfFirstGridPoint
        lat1 = 1e-3 * self.latitudeOfLastGridPoint
        if self.scanningMode & 0x40:  # points scan in +j direction
            lat0, lat1 = lat1, lat0
        latitudes: NDArray[np.double] = np.linspace(lat0, lat1, self.Nj)
        coordinates = np.meshgrid(longitudes, latitudes)
        return (coordinates[0], coordinates[1])


class RotatedLatitudeLongitudeGridSection(LatitudeLongitudeGridSection):
    """A rotated latitude/longitude grid section (2) of a GRIB 1 message."""

    latitudeOfSouthernPole = fields.Int24Field(33)
    longitudeOfSouthernPole = fields.Int24Field(36)
    angleOfRotationInDegrees = FloatField(39)


def get_section(buf: memoryview, offset: int, length: int) -> GridDescriptionSection:
    """Return a new section 2 of the correct type from *buf* at *offset*."""
    griddesc = GridDescriptionSection(buf, offset, length)
    try:
        sectionclass = {
            0: LatitudeLongitudeGridSection,
            10: RotatedLatitudeLongitudeGridSection,
        }[griddesc.dataRepresentationType]
    except KeyError:
        return griddesc
    else:
        return sectionclass(buf, offset, length)
