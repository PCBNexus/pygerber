"""`box` module contains definition of `Box` class used to represent 2D boxes."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from pydantic import Field

from pygerber.vm.types.model import ModelType
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self


class Box(ModelType):
    """Represents a box in 2D space."""


class AutoBox(Box):
    """Represents a automatically calculated box in 2D space."""

    min_x: float = Field(default=math.inf)
    min_y: float = Field(default=math.inf)
    max_x: float = Field(default=-math.inf)
    max_y: float = Field(default=-math.inf)

    @classmethod
    def from_vectors(cls, *vectors: Vector) -> Self:
        """Create a box from vectors."""
        assert len(vectors) > 0
        min_x = vectors[0].x
        min_y = vectors[0].y
        max_x = vectors[0].x
        max_y = vectors[0].y

        for vector in vectors[1:]:
            min_x = min(min_x, vector.x)
            min_y = min(min_y, vector.y)
            max_x = max(max_x, vector.x)
            max_y = max(max_y, vector.y)

        return cls(
            min_x=min_x,
            min_y=min_y,
            max_x=max_x,
            max_y=max_y,
        )

    @classmethod
    def from_fixed_box(cls, box: FixedBox) -> AutoBox:
        """Create a box from a fixed box."""
        return cls(
            min_x=box.min_x,
            min_y=box.min_y,
            max_x=box.max_x,
            max_y=box.max_y,
        )

    def to_fixed_box(
        self, center: Vector | Literal["mean", "zero"] = "mean"
    ) -> FixedBox:
        """Convert to a fixed box."""
        if isinstance(center, str):
            if center == "mean":
                center = Vector(
                    x=(self.min_x + self.max_x) / 2, y=(self.min_y + self.max_y) / 2
                )
            elif center == "zero":
                center = Vector(x=0, y=0)

        return FixedBox(
            center=center,
            width=self.max_x - self.min_x,
            height=self.max_y - self.min_y,
        )

    def __add__(self, other: object) -> AutoBox:
        """Add a vector to the box."""
        if isinstance(other, AutoBox):
            return AutoBox(
                min_x=min(self.min_x, other.min_x),
                min_y=min(self.min_y, other.min_y),
                max_x=max(self.max_x, other.max_x),
                max_y=max(self.max_y, other.max_y),
            )
        if isinstance(other, FixedBox):
            return AutoBox(
                min_x=min(self.min_x, other.min_x),
                min_y=min(self.min_y, other.min_y),
                max_x=max(self.max_x, other.max_x),
                max_y=max(self.max_y, other.max_y),
            )

        return NotImplemented

    def __iadd__(self, other: object) -> Self:
        """Add a vector to the box."""
        if isinstance(other, AutoBox):
            self.min_x = min(self.min_x, other.min_x)
            self.min_y = min(self.min_y, other.min_y)
            self.max_x = max(self.max_x, other.max_x)
            self.max_y = max(self.max_y, other.max_y)
            return self

        if isinstance(other, FixedBox):
            self.min_x = min(self.min_x, other.min_x)
            self.min_y = min(self.min_y, other.min_y)
            self.max_x = max(self.max_x, other.max_x)
            self.max_y = max(self.max_y, other.max_y)
            return self

        return NotImplemented

    def __radd__(self, other: object) -> AutoBox:
        """Add a vector to the box."""
        if isinstance(other, AutoBox):
            return self + other

        if isinstance(other, FixedBox):
            return self + other

        return NotImplemented


class FixedBox(Box):
    """Represents a fixed box in 2D space.

    Used to specify size and coordinate space of a layer.
    """

    center: Vector
    width: float
    height: float

    @classmethod
    def new(cls, center: tuple[float, float], width: float, height: float) -> FixedBox:
        """Create a new box from a tuple."""
        return cls(center=Vector.from_tuple(center), width=width, height=height)

    @property
    def min_x(self) -> float:
        """Get minimum x coordinate of box."""
        return self.center.x - self.width / 2

    @property
    def min_y(self) -> float:
        """Get minimum y coordinate of box."""
        return self.center.y - self.height / 2

    @property
    def max_x(self) -> float:
        """Get maximum x coordinate of box."""
        return self.center.x + self.width / 2

    @property
    def max_y(self) -> float:
        """Get maximum y coordinate of box."""
        return self.center.y + self.height / 2
