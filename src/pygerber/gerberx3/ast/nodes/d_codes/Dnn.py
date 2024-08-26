"""`pygerber.nodes.d_codes.DNN` module contains definition of `DNN` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerberx3.ast.nodes.d_codes.D import D
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class Dnn(D):
    """Represents DNN Gerber command."""

    aperture_id: ApertureIdStr

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_dnn(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_dnn
