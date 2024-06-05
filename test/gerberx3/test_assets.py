from __future__ import annotations

import json
from dataclasses import dataclass
from test.gerberx3.common import (
    GERBER_ASSETS_INDEX,
    REFERENCE_ASSETS_MANAGER,
    Asset,
    CaseGenerator,
    ConfigBase,
    highlight_differences,
)

import pytest
from PIL import Image

from pygerber.gerberx3.parser2.parser2 import Parser2
from pygerber.gerberx3.renderer2.raster import RasterRenderer2, RasterRenderer2Hooks
from pygerber.gerberx3.renderer2.svg import SvgRenderer2, SvgRenderer2Hooks
from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer


@dataclass
class Config(ConfigBase):
    """Configuration for the test."""

    dpmm: int = 20
    as_expression: bool = False
    compare_with_reference: bool = True


@CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "A64-OLinuXino-rev-G.*": Config(dpmm=40),
        "flashes.*": Config(dpmm=40),
        "flashes.00_circle+h_4_tbh.grb": Config(
            xfail=True,
            xfail_message="Should warn, no mechanism implemented yet.",
        ),
        "ucamco.4.9.1.*": Config(dpmm=100),
        "ucamco.4.9.6.*": Config(dpmm=300),
        "ucamco.4.10.4.9.*": Config(dpmm=50),
        "ucamco.4.11.4.*": Config(dpmm=1),
        "expressions.*": Config(as_expression=True),
        "incomplete.*": Config(skip=True),
    },
    Config,
).parametrize
def test_raster_renderer2(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip()

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    tokenizer = Tokenizer()

    if config.as_expression:
        stack = tokenizer.tokenize_expressions(source)
    else:
        stack = tokenizer.tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)

    ref = RasterRenderer2(RasterRenderer2Hooks(dpmm=config.dpmm)).render(cmd_buf)

    output_file_path = asset.get_output_file(".raster_renderer2").with_suffix(".png")
    ref.save_to(output_file_path)

    if config.compare_with_reference:
        reference_path = REFERENCE_ASSETS_MANAGER.get_asset_path(
            ".raster_renderer2", asset.relative_path
        ).with_suffix(".png")
        reference_image = Image.open(reference_path).convert("RGBA")

        output_image = Image.open(output_file_path).convert("RGBA")

        if reference_image != output_image:
            diff_image_dest = asset.get_output_file(
                ".diff_raster_renderer2"
            ).with_suffix(".png")
            diff_image = highlight_differences(output_image, reference_image)

            diff_image.save(diff_image_dest)

            msg = "Image mismatch."
            raise ValueError(msg)


@CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "expressions.*": Config(as_expression=True),
        "incomplete.*": Config(skip=True),
    },
    Config,
).parametrize
def test_svg_renderer2(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip()

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    tokenizer = Tokenizer()

    if config.as_expression:
        stack = tokenizer.tokenize_expressions(source)
    else:
        stack = tokenizer.tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)

    ref = SvgRenderer2(SvgRenderer2Hooks()).render(cmd_buf)

    output_file_path = asset.get_output_file(".svg_renderer2").with_suffix(".svg")
    ref.save_to(output_file_path)

    if config.compare_with_reference:
        reference_path = REFERENCE_ASSETS_MANAGER.get_asset_path(
            ".svg_renderer2", asset.relative_path
        ).with_suffix(".svg")

        output_file_content = output_file_path.read_bytes()
        reference_file_content = reference_path.read_bytes()

        if output_file_content != reference_file_content:
            msg = "File mismatch."
            raise ValueError(msg)


@CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "A64-OLinuXino-rev-G.*": Config(skip=True),
        "A64-OLinuXino-rev-G.A64-OlinuXino_Rev_G-B_Cu.gbr": Config(skip=False),
        "ATMEGA328-Motor-Board.*": Config(skip=True),
        "ATMEGA328-Motor-Board.ATMEGA328_Motor_Board-B.Cu.gbl": Config(skip=False),
        "expressions.*": Config(as_expression=True),
        "incomplete.*": Config(skip=True),
    },
    Config,
).parametrize
def test_parser2(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip(reason=config.skip_reason)

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    tokenizer = Tokenizer()

    if config.as_expression:
        stack = tokenizer.tokenize_expressions(source)
    else:
        stack = tokenizer.tokenize(source)

    parser = Parser2()
    cmd_buf = parser.parse(stack)

    output = cmd_buf.model_dump_json(indent=2, serialize_as_any=True)
    output_file_path = asset.get_output_file(".parser2").with_suffix(".json")
    output_file_path.write_text(output)

    if config.compare_with_reference:
        reference_path = REFERENCE_ASSETS_MANAGER.get_asset_path(
            ".parser2", asset.relative_path
        ).with_suffix(".json")

        output_file_content = json.loads(output_file_path.read_text())
        reference_file_content = json.loads(reference_path.read_text())

        assert output_file_content == reference_file_content


@CaseGenerator(
    GERBER_ASSETS_INDEX,
    {
        "A64-OLinuXino-rev-G.*": Config(skip=True),
        "A64-OLinuXino-rev-G.A64-OlinuXino_Rev_G-B_Cu.gbr": Config(skip=False),
        "ATMEGA328-Motor-Board.*": Config(skip=True),
        "ATMEGA328-Motor-Board.ATMEGA328_Motor_Board-B.Cu.gbl": Config(skip=False),
        "expressions.*": Config(as_expression=True),
        "incomplete.*": Config(skip=True),
    },
    Config,
).parametrize
def test_tokenizer(asset: Asset, config: Config) -> None:
    if config.skip:
        pytest.skip(reason=config.skip_reason)

    if config.xfail:
        pytest.xfail(config.xfail_message)

    source = asset.absolute_path.read_text()
    tokenizer = Tokenizer()

    if config.as_expression:
        stack = tokenizer.tokenize_expressions(source)
    else:
        stack = tokenizer.tokenize(source)

    assert len(stack) > 0
