"""`pygerber.gerberx3.formatter` module contains implementation `Formatter` class
which implements configurable Gerber code formatting.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator, Literal, Optional

from pyparsing import cached_property

from pygerber.gerberx3.ast.visitor import AstVisitor

if TYPE_CHECKING:
    from io import StringIO

    from pygerber.gerberx3.ast.nodes.aperture.AB_close import ABclose
    from pygerber.gerberx3.ast.nodes.aperture.AB_open import ABopen
    from pygerber.gerberx3.ast.nodes.aperture.ADC import ADC
    from pygerber.gerberx3.ast.nodes.aperture.ADmacro import ADmacro
    from pygerber.gerberx3.ast.nodes.aperture.ADO import ADO
    from pygerber.gerberx3.ast.nodes.aperture.ADP import ADP
    from pygerber.gerberx3.ast.nodes.aperture.ADR import ADR
    from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
    from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
    from pygerber.gerberx3.ast.nodes.aperture.SR_close import SRclose
    from pygerber.gerberx3.ast.nodes.aperture.SR_open import SRopen
    from pygerber.gerberx3.ast.nodes.attribute.TA import (
        TA_AperFunction,
        TA_DrillTolerance,
        TA_FlashText,
        TA_UserName,
    )
    from pygerber.gerberx3.ast.nodes.attribute.TD import TD
    from pygerber.gerberx3.ast.nodes.attribute.TF import (
        TF_MD5,
        TF_CreationDate,
        TF_FileFunction,
        TF_FilePolarity,
        TF_GenerationSoftware,
        TF_Part,
        TF_ProjectId,
        TF_SameCoordinates,
        TF_UserName,
    )
    from pygerber.gerberx3.ast.nodes.attribute.TO import (
        TO_C,
        TO_CMNP,
        TO_N,
        TO_P,
        TO_CFtp,
        TO_CHgt,
        TO_CLbD,
        TO_CLbN,
        TO_CMfr,
        TO_CMnt,
        TO_CPgD,
        TO_CPgN,
        TO_CRot,
        TO_CSup,
        TO_CVal,
        TO_UserName,
    )
    from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
    from pygerber.gerberx3.ast.nodes.d_codes.D02 import D02
    from pygerber.gerberx3.ast.nodes.d_codes.D03 import D03
    from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn
    from pygerber.gerberx3.ast.nodes.file import File
    from pygerber.gerberx3.ast.nodes.g_codes.G01 import G01
    from pygerber.gerberx3.ast.nodes.g_codes.G02 import G02
    from pygerber.gerberx3.ast.nodes.g_codes.G03 import G03
    from pygerber.gerberx3.ast.nodes.g_codes.G04 import G04
    from pygerber.gerberx3.ast.nodes.g_codes.G36 import G36
    from pygerber.gerberx3.ast.nodes.g_codes.G37 import G37
    from pygerber.gerberx3.ast.nodes.g_codes.G54 import G54
    from pygerber.gerberx3.ast.nodes.g_codes.G55 import G55
    from pygerber.gerberx3.ast.nodes.g_codes.G70 import G70
    from pygerber.gerberx3.ast.nodes.g_codes.G71 import G71
    from pygerber.gerberx3.ast.nodes.g_codes.G74 import G74
    from pygerber.gerberx3.ast.nodes.g_codes.G75 import G75
    from pygerber.gerberx3.ast.nodes.g_codes.G90 import G90
    from pygerber.gerberx3.ast.nodes.g_codes.G91 import G91
    from pygerber.gerberx3.ast.nodes.load.LM import LM
    from pygerber.gerberx3.ast.nodes.load.LN import LN
    from pygerber.gerberx3.ast.nodes.load.LP import LP
    from pygerber.gerberx3.ast.nodes.load.LR import LR
    from pygerber.gerberx3.ast.nodes.load.LS import LS
    from pygerber.gerberx3.ast.nodes.m_codes.M00 import M00
    from pygerber.gerberx3.ast.nodes.m_codes.M01 import M01
    from pygerber.gerberx3.ast.nodes.m_codes.M02 import M02
    from pygerber.gerberx3.ast.nodes.math.assignment import Assignment
    from pygerber.gerberx3.ast.nodes.math.constant import Constant
    from pygerber.gerberx3.ast.nodes.math.operators.binary.add import Add
    from pygerber.gerberx3.ast.nodes.math.operators.binary.div import Div
    from pygerber.gerberx3.ast.nodes.math.operators.binary.mul import Mul
    from pygerber.gerberx3.ast.nodes.math.operators.binary.sub import Sub
    from pygerber.gerberx3.ast.nodes.math.operators.unary.neg import Neg
    from pygerber.gerberx3.ast.nodes.math.operators.unary.pos import Pos
    from pygerber.gerberx3.ast.nodes.math.point import Point
    from pygerber.gerberx3.ast.nodes.math.variable import Variable
    from pygerber.gerberx3.ast.nodes.other.coordinate import (
        CoordinateI,
        CoordinateJ,
        CoordinateX,
        CoordinateY,
    )
    from pygerber.gerberx3.ast.nodes.primitives.code_0 import Code0
    from pygerber.gerberx3.ast.nodes.primitives.code_1 import Code1
    from pygerber.gerberx3.ast.nodes.primitives.code_2 import Code2
    from pygerber.gerberx3.ast.nodes.primitives.code_4 import Code4
    from pygerber.gerberx3.ast.nodes.primitives.code_5 import Code5
    from pygerber.gerberx3.ast.nodes.primitives.code_6 import Code6
    from pygerber.gerberx3.ast.nodes.primitives.code_7 import Code7
    from pygerber.gerberx3.ast.nodes.primitives.code_20 import Code20
    from pygerber.gerberx3.ast.nodes.primitives.code_21 import Code21
    from pygerber.gerberx3.ast.nodes.primitives.code_22 import Code22
    from pygerber.gerberx3.ast.nodes.properties.AS import AS
    from pygerber.gerberx3.ast.nodes.properties.FS import FS
    from pygerber.gerberx3.ast.nodes.properties.IN import IN
    from pygerber.gerberx3.ast.nodes.properties.IP import IP
    from pygerber.gerberx3.ast.nodes.properties.IR import IR
    from pygerber.gerberx3.ast.nodes.properties.MI import MI
    from pygerber.gerberx3.ast.nodes.properties.MO import MO
    from pygerber.gerberx3.ast.nodes.properties.OF import OF
    from pygerber.gerberx3.ast.nodes.properties.SF import SF


class FormatterError(Exception):
    """Formatter error."""


class Formatter(AstVisitor):
    """Gerber X3 compatible formatter."""

    def __init__(  # noqa: PLR0913
        self,
        *,
        indent_character: Literal[" ", "\t"] = " ",
        macro_body_indentation: str = "",
        macro_split_mode: Literal["none", "primitives", "parameters"] = "primitives",
        indent_block_aperture_body: str = "",
        indent_step_and_repeat: str = "",
        float_decimal_places: int = 6,
        float_trim_trailing_zeros: bool = True,
        indent_non_aperture_select_commands: bool = False,
        split_format_select: bool = False,
        split_aperture_definition: bool = False,
        split_extended_command_boundaries: bool = False,
        strip_whitespace_mode: bool = False,
        macro_end_in_new_line: bool = False,
    ) -> None:
        r"""Initialize Formatter instance.

        Parameters
        ----------
        indent_character: Literal[" ", "\t"], optional
            Character used for indentation, by default " "
        macro_body_indentation : str, optional
            Indentation of macro body, by default ""
        macro_split_mode : Literal["none", "primitives", "parameters"], optional
            Changes how macro definitions are formatted, by default "none"
            When "none" is selected, macro will be formatted as a single line.
            ```gerber
            %AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*%
            ```
            When "primitives" is selected, macro will be formatted with each primitive
            on a new line.
            ```gerber
            %AMDonut*
            1,1,$1,$2,$3*
            $4=$1x0.75*
            1,0,$4,$2,$3*%
            ```
        indent_block_aperture_body : str, optional
            _description_, by default ""
        indent_step_and_repeat : str, optional
            _description_, by default ""
        float_decimal_places : int, optional
            _description_, by default 6
        float_trim_trailing_zeros : bool, optional
            _description_, by default True
        indent_non_aperture_select_commands : bool, optional
            _description_, by default False
        split_format_select : bool, optional
            _description_, by default False
        split_aperture_definition : bool, optional
            _description_, by default False
        split_extended_command_boundaries : bool, optional
            _description_, by default False
        strip_whitespace_mode : bool, optional
            _description_, by default False
        macro_end_in_new_line: bool, optional
            _description_, by default False

        """
        super().__init__()
        self.indent_character = indent_character
        self.macro_body_indentation = macro_body_indentation
        self.macro_split_mode = macro_split_mode
        self.indent_block_aperture_body = indent_block_aperture_body
        self.indent_step_and_repeat = indent_step_and_repeat
        self.float_decimal_places = float_decimal_places

        self.float_trim_trailing_zeros = float_trim_trailing_zeros
        self.indent_non_aperture_select_commands = indent_non_aperture_select_commands
        self.split_format_select = split_format_select
        self.split_aperture_definition = split_aperture_definition
        self.split_extended_command_boundaries = split_extended_command_boundaries
        self.strip_whitespace_mode = strip_whitespace_mode
        self.macro_end_in_new_line = macro_end_in_new_line

        self._output: Optional[StringIO] = None

    def format(self, source: File, output: StringIO) -> None:
        """Format Gerber AST according to rules specified in Formatter constructor."""
        self._output = output
        try:
            self.on_file(source)
        finally:
            self._output = None

    @property
    def output(self) -> StringIO:
        """Get output buffer."""
        if self._output is None:
            msg = "Output buffer is not set."
            raise FormatterError(msg)

        return self._output

    def _fmt_double(self, value: float) -> str:
        double = f"{value:.{self.float_decimal_places}f}"
        if self.float_trim_trailing_zeros:
            return double.rstrip("0").rstrip(".")
        return double

    @cached_property
    def lf(self) -> str:
        """Get end of line character."""
        return "" if self.strip_whitespace_mode else "\n"

    @contextmanager
    def _command(self, cmd: str) -> Generator[None, None, None]:
        self._write(cmd)
        yield
        self._write(f"*{self.lf}")

    @contextmanager
    def _extended_command(self, cmd: str) -> Generator[None, None, None]:
        self._write(f"%{cmd}")
        yield
        self._write(f"*%{self.lf}")

    def _write(self, value: str) -> None:
        self.output.write(value)

    def on_ab_close(self, node: ABclose) -> None:
        """Handle `ABclose` node."""
        super().on_ab_close(node)
        with self._extended_command("AB"):
            pass

    def on_ab_open(self, node: ABopen) -> None:
        """Handle `ABopen` node."""
        super().on_ab_open(node)
        with self._extended_command("AB"):
            self._write(node.aperture_identifier)

    def on_adc(self, node: ADC) -> None:
        """Handle `AD` circle node."""
        super().on_adc(node)
        with self._extended_command(f"AD{node.aperture_identifier}C,"):
            self._write(self._fmt_double(node.diameter))

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")

    def on_adr(self, node: ADR) -> None:
        """Handle `AD` rectangle node."""
        super().on_adr(node)

    def on_ado(self, node: ADO) -> None:
        """Handle `AD` obround node."""
        super().on_ado(node)

    def on_adp(self, node: ADP) -> None:
        """Handle `AD` polygon node."""

    def on_ad_macro(self, node: ADmacro) -> None:
        """Handle `AD` macro node."""
        super().on_ad_macro(node)

    def on_am_close(self, node: AMclose) -> None:
        """Handle `AMclose` node."""
        super().on_am_close(node)

    def on_am_open(self, node: AMopen) -> None:
        """Handle `AMopen` node."""
        super().on_am_open(node)

    def on_sr_close(self, node: SRclose) -> None:
        """Handle `SRclose` node."""
        super().on_sr_close(node)

    def on_sr_open(self, node: SRopen) -> None:
        """Handle `SRopen` node."""
        super().on_sr_open(node)

    # Attribute

    def on_ta_user_name(self, node: TA_UserName) -> None:
        """Handle `TA_UserName` node."""
        super().on_ta_user_name(node)

    def on_ta_aper_function(self, node: TA_AperFunction) -> None:
        """Handle `TA_AperFunction` node."""
        super().on_ta_aper_function(node)

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> None:
        """Handle `TA_DrillTolerance` node."""
        super().on_ta_drill_tolerance(node)

    def on_ta_flash_text(self, node: TA_FlashText) -> None:
        """Handle `TA_FlashText` node."""
        super().on_ta_flash_text(node)

    def on_td(self, node: TD) -> None:
        """Handle `TD` node."""
        super().on_td(node)

    def on_tf_user_name(self, node: TF_UserName) -> None:
        """Handle `TF_UserName` node."""
        super().on_tf_user_name(node)

    def on_tf_part(self, node: TF_Part) -> None:
        """Handle `TF_Part` node."""
        super().on_tf_part(node)

    def on_tf_file_function(self, node: TF_FileFunction) -> None:
        """Handle `TF_FileFunction` node."""
        super().on_tf_file_function(node)

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> None:
        """Handle `TF_FilePolarity` node."""
        super().on_tf_file_polarity(node)

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> None:
        """Handle `TF_SameCoordinates` node."""
        super().on_tf_same_coordinates(node)

    def on_tf_creation_date(self, node: TF_CreationDate) -> None:
        """Handle `TF_CreationDate` node."""
        super().on_tf_creation_date(node)

    def on_tf_generation_software(self, node: TF_GenerationSoftware) -> None:
        """Handle `TF_GenerationSoftware` node."""
        super().on_tf_generation_software(node)

    def on_tf_project_id(self, node: TF_ProjectId) -> None:
        """Handle `TF_ProjectId` node."""
        super().on_tf_project_id(node)

    def on_tf_md5(self, node: TF_MD5) -> None:
        """Handle `TF_MD5` node."""
        super().on_tf_md5(node)

    def on_to_user_name(self, node: TO_UserName) -> None:
        """Handle `TO_UserName` node."""
        super().on_to_user_name(node)

    def on_to_n(self, node: TO_N) -> None:
        """Handle `TO_N` node."""
        super().on_to_n(node)

    def on_to_p(self, node: TO_P) -> None:
        """Handle `TO_P` node`."""
        super().on_to_p(node)

    def on_to_c(self, node: TO_C) -> None:
        """Handle `TO_C` node."""
        super().on_to_c(node)

    def on_to_crot(self, node: TO_CRot) -> None:
        """Handle `TO_CRot` node."""
        super().on_to_crot(node)

    def on_to_cmfr(self, node: TO_CMfr) -> None:
        """Handle `TO_CMfr` node."""
        super().on_to_cmfr(node)

    def on_to_cmnp(self, node: TO_CMNP) -> None:
        """Handle `TO_CMNP` node."""
        super().on_to_cmnp(node)

    def on_to_cval(self, node: TO_CVal) -> None:
        """Handle `TO_CVal` node."""
        super().on_to_cval(node)

    def on_to_cmnt(self, node: TO_CMnt) -> None:
        """Handle `TO_CVal` node."""
        super().on_to_cmnt(node)

    def on_to_cftp(self, node: TO_CFtp) -> None:
        """Handle `TO_Cftp` node."""
        super().on_to_cftp(node)

    def on_to_cpgn(self, node: TO_CPgN) -> None:
        """Handle `TO_CPgN` node."""
        super().on_to_cpgn(node)

    def on_to_cpgd(self, node: TO_CPgD) -> None:
        """Handle `TO_CPgD` node."""
        super().on_to_cpgd(node)

    def on_to_chgt(self, node: TO_CHgt) -> None:
        """Handle `TO_CHgt` node."""
        super().on_to_chgt(node)

    def on_to_clbn(self, node: TO_CLbN) -> None:
        """Handle `TO_CLbN` node."""
        super().on_to_clbn(node)

    def on_to_clbd(self, node: TO_CLbD) -> None:
        """Handle `TO_CLbD` node."""
        super().on_to_clbd(node)

    def on_to_csup(self, node: TO_CSup) -> None:
        """Handle `TO_CSup` node."""
        super().on_to_csup(node)

    # D codes

    def on_d01(self, node: D01) -> None:
        """Handle `D01` node."""
        super().on_d01(node)
        with self._command("D01"):
            pass

    def on_d02(self, node: D02) -> None:
        """Handle `D02` node."""
        super().on_d02(node)
        with self._command("D02"):
            pass

    def on_d03(self, node: D03) -> None:
        """Handle `D03` node."""
        super().on_d03(node)
        with self._command("D03"):
            pass

    def on_dnn(self, node: Dnn) -> None:
        """Handle `Dnn` node."""
        super().on_dnn(node)
        with self._command(node.value):
            pass

    # G codes

    def on_g01(self, node: G01) -> None:
        """Handle `G01` node."""
        super().on_g01(node)
        self._write("G01*\n")

    def on_g02(self, node: G02) -> None:
        """Handle `G02` node."""
        super().on_g02(node)
        self._write("G02*\n")

    def on_g03(self, node: G03) -> None:
        """Handle `G03` node."""
        super().on_g03(node)
        self._write("G03*\n")

    def on_g04(self, node: G04) -> None:
        """Handle `G04` node."""
        super().on_g04(node)
        self._write(f"G04{node.string}*\n")

    def on_g36(self, node: G36) -> None:
        """Handle `G36` node."""
        super().on_g36(node)
        self._write("G36*\n")

    def on_g37(self, node: G37) -> None:
        """Handle `G37` node."""
        super().on_g37(node)
        self._write("G37*\n")

    def on_g54(self, node: G54) -> None:
        """Handle `G54` node."""
        self._write("G54")
        super().on_g54(node)

    def on_g55(self, node: G55) -> None:
        """Handle `G55` node."""
        self._write("G55")
        super().on_g55(node)

    def on_g70(self, node: G70) -> None:
        """Handle `G70` node."""
        super().on_g70(node)
        self._write("G70*\n")

    def on_g71(self, node: G71) -> None:
        """Handle `G71` node."""
        super().on_g71(node)
        self._write("G71*\n")

    def on_g74(self, node: G74) -> None:
        """Handle `G74` node."""
        super().on_g74(node)
        self._write("G74*\n")

    def on_g75(self, node: G75) -> None:
        """Handle `G75` node."""
        super().on_g75(node)
        self._write("G75*\n")

    def on_g90(self, node: G90) -> None:
        """Handle `G90` node."""
        super().on_g90(node)
        self._write("G90*\n")

    def on_g91(self, node: G91) -> None:
        """Handle `G91` node."""
        super().on_g91(node)
        self._write("G91*\n")

    # Load

    def on_lm(self, node: LM) -> None:
        """Handle `LM` node."""
        super().on_lm(node)

    def on_ln(self, node: LN) -> None:
        """Handle `LN` node."""
        super().on_ln(node)

    def on_lp(self, node: LP) -> None:
        """Handle `LP` node."""
        super().on_lp(node)

    def on_lr(self, node: LR) -> None:
        """Handle `LR` node."""
        super().on_lr(node)

    def on_ls(self, node: LS) -> None:
        """Handle `LS` node."""
        super().on_ls(node)

    # M Codes

    def on_m00(self, node: M00) -> None:
        """Handle `M00` node."""
        super().on_m00(node)
        with self._command("M00"):
            pass

    def on_m01(self, node: M01) -> None:
        """Handle `M01` node."""
        super().on_m01(node)
        with self._command("M01"):
            pass

    def on_m02(self, node: M02) -> None:
        """Handle `M02` node."""
        super().on_m02(node)
        with self._command("M02"):
            pass

    # Math

    # Math :: Operators :: Binary

    def on_add(self, node: Add) -> None:
        """Handle `Add` node."""
        super().on_add(node)

    def on_div(self, node: Div) -> None:
        """Handle `Div` node."""
        super().on_div(node)

    def on_mul(self, node: Mul) -> None:
        """Handle `Mul` node."""
        super().on_mul(node)

    def on_sub(self, node: Sub) -> None:
        """Handle `Sub` node."""
        super().on_sub(node)

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> None:
        """Handle `Neg` node."""
        super().on_neg(node)

    def on_pos(self, node: Pos) -> None:
        """Handle `Pos` node."""
        super().on_pos(node)

    def on_assignment(self, node: Assignment) -> None:
        """Handle `Assignment` node."""
        super().on_assignment(node)

    def on_constant(self, node: Constant) -> None:
        """Handle `Constant` node."""
        super().on_constant(node)

    def on_point(self, node: Point) -> None:
        """Handle `Point` node."""
        super().on_point(node)

    def on_variable(self, node: Variable) -> None:
        """Handle `Variable` node."""
        super().on_variable(node)

    # Other

    def on_coordinate_x(self, node: CoordinateX) -> None:
        """Handle `Coordinate` node."""
        super().on_coordinate_x(node)
        self._write(f"X{node.value}")

    def on_coordinate_y(self, node: CoordinateY) -> None:
        """Handle `Coordinate` node."""
        super().on_coordinate_y(node)
        self._write(f"Y{node.value}")

    def on_coordinate_i(self, node: CoordinateI) -> None:
        """Handle `Coordinate` node."""
        super().on_coordinate_i(node)
        self._write(f"I{node.value}")

    def on_coordinate_j(self, node: CoordinateJ) -> None:
        """Handle `Coordinate` node."""
        super().on_coordinate_j(node)
        self._write(f"J{node.value}")

    # Primitives

    def on_code_0(self, node: Code0) -> None:
        """Handle `Code0` node."""
        super().on_code_0(node)

    def on_code_1(self, node: Code1) -> None:
        """Handle `Code1` node."""
        super().on_code_1(node)

    def on_code_2(self, node: Code2) -> None:
        """Handle `Code2` node."""
        super().on_code_2(node)

    def on_code_4(self, node: Code4) -> None:
        """Handle `Code4` node."""
        super().on_code_4(node)

    def on_code_5(self, node: Code5) -> None:
        """Handle `Code5` node."""
        super().on_code_5(node)

    def on_code_6(self, node: Code6) -> None:
        """Handle `Code6` node."""
        super().on_code_6(node)

    def on_code_7(self, node: Code7) -> None:
        """Handle `Code7` node."""
        super().on_code_7(node)

    def on_code_20(self, node: Code20) -> None:
        """Handle `Code20` node."""
        super().on_code_20(node)

    def on_code_21(self, node: Code21) -> None:
        """Handle `Code21` node."""
        super().on_code_21(node)

    def on_code_22(self, node: Code22) -> None:
        """Handle `Code22` node."""
        super().on_code_22(node)

    # Properties

    def on_as(self, node: AS) -> None:
        """Handle `AS` node."""
        super().on_as(node)

    def on_fs(self, node: FS) -> None:
        """Handle `FS` node."""
        super().on_fs(node)

    def on_in(self, node: IN) -> None:
        """Handle `IN` node."""
        super().on_in(node)

    def on_ip(self, node: IP) -> None:
        """Handle `IP` node."""
        super().on_ip(node)

    def on_ir(self, node: IR) -> None:
        """Handle `IR` node."""
        super().on_ir(node)

    def on_mi(self, node: MI) -> None:
        """Handle `MI` node."""
        super().on_mi(node)

    def on_mo(self, node: MO) -> None:
        """Handle `MO` node."""
        super().on_mo(node)

    def on_of(self, node: OF) -> None:
        """Handle `OF` node."""
        super().on_of(node)

    def on_sf(self, node: SF) -> None:
        """Handle `SF` node."""
        super().on_sf(node)

    # Root node

    def on_file(self, node: File) -> None:
        """Handle `File` node."""
        super().on_file(node)
