"""`pygerber.nodes.d_codes.D01` module contains definition of `D01` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.d_codes.D import D
from pygerber.gerberx3.ast.nodes.other.coordinate import (
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class D01(D):
    """Represents D01 Gerber command."""

    x: Optional[CoordinateX] = Field(default=None)
    y: Optional[CoordinateY] = Field(default=None)
    i: Optional[CoordinateI] = Field(default=None)
    j: Optional[CoordinateJ] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_d01(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_d01
