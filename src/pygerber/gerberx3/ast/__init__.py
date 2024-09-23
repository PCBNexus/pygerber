"""`pygerber.gerberx3.ast` package contains all the node classes used to represent
the Gerber X3 abstract syntax tree.
"""

from __future__ import annotations

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.builder import GerberX3Builder
from pygerber.gerberx3.ast.errors import (
    ApertureNotFoundError,
    ApertureNotSelectedError,
    AstError,
    CoordinateFormatNotSetError,
    DirectADHandlerDispatchNotSupportedError,
    PackedCoordinateTooLongError,
    PackedCoordinateTooShortError,
    SourceNotAvailableError,
    VisitorError,
)
from pygerber.gerberx3.ast.expression_eval_visitor import ExpressionEvalVisitor
from pygerber.gerberx3.ast.node_finder import NodeFinder
from pygerber.gerberx3.ast.nodes import File
from pygerber.gerberx3.ast.state_tracking_visitor import (
    ApertureStorage,
    ArcInterpolation,
    Attributes,
    CoordinateFormat,
    ImageAttributes,
    PlotMode,
    ProgramStop,
    State,
    StateTrackingVisitor,
    Transform,
)

__all__ = [
    "AstVisitor",
    "GerberX3Builder",
    "AstError",
    "VisitorError",
    "StateTrackingVisitor",
    "DirectADHandlerDispatchNotSupportedError",
    "ApertureNotSelectedError",
    "ApertureNotFoundError",
    "SourceNotAvailableError",
    "CoordinateFormatNotSetError",
    "PackedCoordinateTooLongError",
    "PackedCoordinateTooShortError",
    "ExpressionEvalVisitor",
    "NodeFinder",
    "State",
    "CoordinateFormat",
    "Attributes",
    "ImageAttributes",
    "Transform",
    "PlotMode",
    "ArcInterpolation",
    "ApertureStorage",
    "ProgramStop",
]


def get_final_state(ast: File) -> State:
    visitor = StateTrackingVisitor()
    ast.visit(visitor)
    return visitor.state
