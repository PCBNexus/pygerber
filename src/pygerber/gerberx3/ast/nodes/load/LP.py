"""`pygerber.nodes.load.LP` module contains definition of `LP` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.enums import Polarity

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class LP(Node):
    """Represents LP Gerber extended command."""

    polarity: Polarity

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_lp(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_lp
