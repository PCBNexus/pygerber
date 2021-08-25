# -*- coding: utf-8 -*-
from __future__ import annotations

from PIL import Image, ImageDraw
from pygerber.meta.aperture import RectangularAperture
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.util import PillowUtilMethdos


class PillowObround(RectangularAperture, PillowUtilMethdos):
    draw_canvas: ImageDraw.ImageDraw

    def flash(self, spec: FlashSpec) -> None:
        self.prepare_flash_spec(spec)
        self.draw_canvas.line()

    def line(self, spec: LineSpec) -> None:
        self.prepare_line_spec(spec)

    def arc(self, spec: ArcSpec) -> None:
        self.prepare_arc_spec(spec)
