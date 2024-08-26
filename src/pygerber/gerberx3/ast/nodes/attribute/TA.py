"""`pygerber.nodes.attribute.TA` module contains definition of `TA` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Literal, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.enums import AperFunction

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.ast_visitor import AstVisitor


class TA(Node):
    """Represents TA Gerber extended command."""

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        raise NotImplementedError


class TA_UserName(TA):  # noqa: N801
    """Represents TA Gerber extended command with user name."""

    user_name: str
    fields: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return self.user_name

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_user_name(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_user_name


class TA_AperFunction(TA):  # noqa: N801
    """Represents TA .AperFunction Gerber attribute."""

    function: Optional[AperFunction] = Field(default=None)
    fields: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".AperFunction"

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_aper_function(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_aper_function


class TA_DrillTolerance(TA):  # noqa: N801
    """Represents TA .DrillTolerance Gerber attribute."""

    plus_tolerance: Optional[float] = Field(default=None)
    minus_tolerance: Optional[float] = Field(default=None)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".DrillTolerance"

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_drill_tolerance(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_drill_tolerance


class TA_FlashText(TA):  # noqa: N801
    """Represents TA .FlashText Gerber attribute."""

    string: str
    mode: Literal["B", "C"]
    mirroring: Literal["R", "M"] = Field(default="R")
    font: Optional[str] = Field(default=None)
    size: Optional[str] = Field(default=None)
    comments: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".FlashText"

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_flash_text(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_flash_text
