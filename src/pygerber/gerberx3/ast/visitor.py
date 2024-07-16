"""`pygerber.gerberx3.node_visitor` contains definition of `NodeVisitor` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.nodes.aperture.AB_close import ABclose
    from pygerber.gerberx3.ast.nodes.aperture.AB_open import ABopen
    from pygerber.gerberx3.ast.nodes.aperture.AD import AD
    from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
    from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
    from pygerber.gerberx3.ast.nodes.aperture.SR_close import SRclose
    from pygerber.gerberx3.ast.nodes.aperture.SR_open import SRopen
    from pygerber.gerberx3.ast.nodes.attribute.TA import TA
    from pygerber.gerberx3.ast.nodes.attribute.TD import TD
    from pygerber.gerberx3.ast.nodes.attribute.TF import TF
    from pygerber.gerberx3.ast.nodes.attribute.TO import TO
    from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
    from pygerber.gerberx3.ast.nodes.d_codes.D02 import D02
    from pygerber.gerberx3.ast.nodes.d_codes.D03 import D03
    from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn
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
    from pygerber.gerberx3.ast.nodes.math.expression import Expression
    from pygerber.gerberx3.ast.nodes.math.operators.binary.add import Add
    from pygerber.gerberx3.ast.nodes.math.operators.binary.div import Div
    from pygerber.gerberx3.ast.nodes.math.operators.binary.mul import Mul
    from pygerber.gerberx3.ast.nodes.math.operators.binary.sub import Sub
    from pygerber.gerberx3.ast.nodes.math.operators.unary.neg import Neg
    from pygerber.gerberx3.ast.nodes.math.operators.unary.pos import Pos
    from pygerber.gerberx3.ast.nodes.math.variable import Variable
    from pygerber.gerberx3.ast.nodes.other.command_end import CommandEnd
    from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate
    from pygerber.gerberx3.ast.nodes.other.extended_command_close import (
        ExtendedCommandClose,
    )
    from pygerber.gerberx3.ast.nodes.other.extended_command_open import (
        ExtendedCommandOpen,
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
    from pygerber.gerberx3.ast.nodes.properties.FS import FS
    from pygerber.gerberx3.ast.nodes.properties.IN import IN
    from pygerber.gerberx3.ast.nodes.properties.IP import IP
    from pygerber.gerberx3.ast.nodes.properties.MO import MO
    from pygerber.gerberx3.ast.nodes.properties.OF import OF


class AstVisitor:
    """Interface of a node visitor.

    This class defines interface compliant with visitor pattern.
    For more information on this pattern visit:
    https://refactoring.guru/design-patterns/visitor
    """

    # Aperture

    def on_ab_close(self, node: ABclose) -> None:
        """Handle `ABclose` node."""

    def on_ab_open(self, node: ABopen) -> None:
        """Handle `ABopen` node."""

    def on_ad(self, node: AD) -> None:
        """Handle `AD` node."""

    def on_am_close(self, node: AMclose) -> None:
        """Handle `AMclose` node."""

    def on_am_open(self, node: AMopen) -> None:
        """Handle `AMopen` node."""

    def on_sr_close(self, node: SRclose) -> None:
        """Handle `SRclose` node."""

    def on_sr_open(self, node: SRopen) -> None:
        """Handle `SRopen` node."""

    # Attribute

    def on_ta(self, node: TA) -> None:
        """Handle `TA` node."""

    def on_td(self, node: TD) -> None:
        """Handle `TD` node."""

    def on_tf(self, node: TF) -> None:
        """Handle `TF` node."""

    def on_to(self, node: TO) -> None:
        """Handle `TO` node."""

    # D codes

    def on_d01(self, node: D01) -> None:
        """Handle `D01` node."""

    def on_d02(self, node: D02) -> None:
        """Handle `D02` node."""

    def on_d03(self, node: D03) -> None:
        """Handle `D03` node."""

    def on_dnn(self, node: Dnn) -> None:
        """Handle `Dnn` node."""

    # G codes

    def on_g01(self, node: G01) -> None:
        """Handle `G01` node."""

    def on_g02(self, node: G02) -> None:
        """Handle `G02` node."""

    def on_g03(self, node: G03) -> None:
        """Handle `G03` node."""

    def on_g04(self, node: G04) -> None:
        """Handle `G04` node."""

    def on_g36(self, node: G36) -> None:
        """Handle `G36` node."""

    def on_g37(self, node: G37) -> None:
        """Handle `G37` node."""

    def on_g54(self, node: G54) -> None:
        """Handle `G54` node."""

    def on_g55(self, node: G55) -> None:
        """Handle `G55` node."""

    def on_g70(self, node: G70) -> None:
        """Handle `G70` node."""

    def on_g71(self, node: G71) -> None:
        """Handle `G71` node."""

    def on_g74(self, node: G74) -> None:
        """Handle `G74` node."""

    def on_g75(self, node: G75) -> None:
        """Handle `G75` node."""

    def on_g90(self, node: G90) -> None:
        """Handle `G90` node."""

    def on_g91(self, node: G91) -> None:
        """Handle `G91` node."""

    # Load

    def on_lm(self, node: LM) -> None:
        """Handle `LM` node."""

    def on_ln(self, node: LN) -> None:
        """Handle `LN` node."""

    def on_lp(self, node: LP) -> None:
        """Handle `LP` node."""

    def on_lr(self, node: LR) -> None:
        """Handle `LR` node."""

    def on_ls(self, node: LS) -> None:
        """Handle `LS` node."""

    # M Codes

    def on_m00(self, node: M00) -> None:
        """Handle `M00` node."""

    def on_m01(self, node: M01) -> None:
        """Handle `M01` node."""

    def on_m02(self, node: M02) -> None:
        """Handle `M02` node."""

    # Math

    # Math :: Operators :: Binary

    def on_add(self, node: Add) -> None:
        """Handle `Add` node."""

    def on_div(self, node: Div) -> None:
        """Handle `Div` node."""

    def on_mul(self, node: Mul) -> None:
        """Handle `Mul` node."""

    def on_sub(self, node: Sub) -> None:
        """Handle `Sub` node."""

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> None:
        """Handle `Neg` node."""

    def on_pos(self, node: Pos) -> None:
        """Handle `Pos` node."""

    def on_assignment(self, node: Assignment) -> None:
        """Handle `Assignment` node."""

    def on_constant(self, node: Constant) -> None:
        """Handle `Constant` node."""

    def on_expression(self, node: Expression) -> None:
        """Handle `Expression` node."""

    def on_variable(self, node: Variable) -> None:
        """Handle `Variable` node."""

    # Other

    def on_command_end(self, node: CommandEnd) -> None:
        """Handle `CommandEnd` node."""

    def on_coordinate(self, node: Coordinate) -> None:
        """Handle `Coordinate` node."""

    def on_extended_command_close(self, node: ExtendedCommandClose) -> None:
        """Handle `ExtendedCommandClose` node."""

    def on_extended_command_open(self, node: ExtendedCommandOpen) -> None:
        """Handle `ExtendedCommandOpen` node."""

    # Primitives

    def on_code_0(self, node: Code0) -> None:
        """Handle `Code0` node."""

    def on_code_1(self, node: Code1) -> None:
        """Handle `Code1` node."""

    def on_code_2(self, node: Code2) -> None:
        """Handle `Code2` node."""

    def on_code_4(self, node: Code4) -> None:
        """Handle `Code4` node."""

    def on_code_5(self, node: Code5) -> None:
        """Handle `Code5` node."""

    def on_code_6(self, node: Code6) -> None:
        """Handle `Code6` node."""

    def on_code_7(self, node: Code7) -> None:
        """Handle `Code7` node."""

    def on_code_20(self, node: Code20) -> None:
        """Handle `Code20` node."""

    def on_code_21(self, node: Code21) -> None:
        """Handle `Code21` node."""

    def on_code_22(self, node: Code22) -> None:
        """Handle `Code22` node."""

    # Properties

    def on_fs(self, node: FS) -> None:
        """Handle `FS` node."""

    def on_in(self, node: IN) -> None:
        """Handle `IN` node."""

    def on_ip(self, node: IP) -> None:
        """Handle `IP` node."""

    def on_mo(self, node: MO) -> None:
        """Handle `MO` node."""

    def on_of(self, node: OF) -> None:
        """Handle `OF` node."""