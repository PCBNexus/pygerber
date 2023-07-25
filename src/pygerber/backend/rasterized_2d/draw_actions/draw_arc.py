"""Base class for creating rasterized line draw actions."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from pygerber.backend.abstract.draw_actions.draw_arc import DrawArc
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.backend.rasterized_2d.draw_actions.draw_action_mixin import (
    Rasterized2DDrawActionMixin,
)

if TYPE_CHECKING:
    from pygerber.backend.rasterized_2d.aperture_handle import (
        Rasterized2DPrivateApertureHandle,
    )
    from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend


class Rasterized2DDrawArc(DrawArc, Rasterized2DDrawActionMixin):
    """Base class for creating rasterized line drawing actions."""

    backend: Rasterized2DBackend
    private_handle: Rasterized2DPrivateApertureHandle

    def draw(self) -> None:
        """Execute draw action."""
        logging.debug(
            "Drawing line from %s to %s with %s",
            self.start_position,
            self.end_position,
            self.private_handle,
        )
        if not self.private_handle.is_plain_circle:
            logging.warning(
                "Drawing line with aperture %s is invalid. Only plain circular "
                "apertures are allowed.",
                self.private_handle.aperture_id,
            )

        self._draw_aperture(self.start_position)
        self._draw_arc()
        self._draw_aperture(self.end_position)

        self._draw_bounding_box_if_requested()

    def _draw_arc(self) -> None:
        bbox = self.get_bounding_box() - self.backend.image_coordinates_correction
        pixel_box = bbox.as_pixel_box(self.backend.dpi)

        angle_start = self.arc_space_start_position.angle_between_clockwise(
            Vector2D.UNIT_Y,
        )
        angle_end = self.arc_space_end_position.angle_between_clockwise(Vector2D.UNIT_Y)

        if self.is_clockwise:
            angle_start, angle_end = angle_end, angle_start

        if self.is_multi_quadrant and angle_start == angle_end:
            angle_end += 360

        aperture_size = self.private_handle.image.size
        width = round((aperture_size[0] + aperture_size[1]) / 2)

        self.backend.image_draw.arc(
            xy=pixel_box,
            start=angle_start,
            end=angle_end,
            fill=self.polarity.get_2d_rasterized_color(),
            width=width,
        )
