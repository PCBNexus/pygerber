"""`pygerber.nodes.g_codes.G90` module contains definition of `G90` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.g_codes.G import G

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class G90(G):
    """Represents G90 Gerber command."""

    def visit(self, visitor: AstVisitor) -> G90:
        """Handle visitor call."""
        return visitor.on_g90(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], G90]:
        """Get callback function for the node."""
        return visitor.on_g90
