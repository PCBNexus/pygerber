"""Parser level abstraction of draw operation for Gerber AST parser, version 2."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.parser2.state2 import Command2State2Proxy
from pygerber.gerberx3.state_enums import Mirroring, Polarity

if TYPE_CHECKING:
    from typing_extensions import Self


class Command2(FrozenGeneralModel):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    attributes: ImmutableMapping[str, str] = Field(default_factory=ImmutableMapping)
    polarity: Polarity
    state: Command2State2Proxy

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        raise NotImplementedError

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        raise NotImplementedError

    def command_to_json(self) -> str:
        """Dump draw operation."""
        return json.dumps(
            {
                "cls": f"{self.__module__}.{self.__class__.__qualname__}",
                "dict": json.loads(self.model_dump_json()),
            },
        )

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"
