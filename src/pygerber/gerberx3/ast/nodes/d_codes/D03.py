"""`pygerber.nodes.d_codes.D03` module contains definition of `D03` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class D03(Node):
    """Represents D03 Gerber command."""

    x: Coordinate
    y: Coordinate

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_d03(self)