"""GerberX3 format parser."""


from __future__ import annotations

import logging
from enum import Enum
from typing import Callable, Generator, Optional

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_actions.draw_action import DrawAction
from pygerber.backend.abstract.draw_actions_handle import DrawActionsHandle
from pygerber.backend.rasterized_2d.backend_cls import Rasterized2DBackend
from pygerber.gerberx3.parser.errors import OnUpdateDrawingStateError, ParserError
from pygerber.gerberx3.parser.state import State
from pygerber.gerberx3.tokenizer.tokenizer import TokenStack
from pygerber.gerberx3.tokenizer.tokens.token import Token


class Parser:
    """Gerber X3 parser object."""

    def __init__(
        self,
        tokens: TokenStack,
        options: Optional[ParserOptions] = None,
    ) -> None:
        """Initialize parser.

        Parameters
        ----------
        tokens : TokenStack
            Gerber X3 tokens retrieved with Tokenizer.
        options : ParserOptions | None
            Additional options for modifying parser behavior.
        """
        self.tokens = tokens
        self.options = ParserOptions() if options is None else options
        self.state = (
            State()
            if self.options.initial_state is None
            else self.options.initial_state
        )
        self.draw_actions: list[DrawAction] = []

    @property
    def backend(self) -> Backend:
        """Get reference to backend object."""
        return self.options.backend

    def parse(self) -> DrawActionsHandle:
        """Parse token stack."""
        for _ in self.parse_iter():
            pass

        return self.get_draw_actions_handle()

    def get_draw_actions_handle(self) -> DrawActionsHandle:
        """Return handle to drawing actions."""
        return self.backend.get_draw_actions_handle_cls()(
            self.draw_actions,
            self.backend,
        )

    def parse_iter(self) -> Generator[Token, None, None]:
        """Iterate over tokens in stack and parse them."""
        for token in self.tokens:
            self._update_drawing_state(token)

            yield token

    def _update_drawing_state(self, token: Token) -> None:
        try:
            self.state, actions = token.update_drawing_state(self.state, self.backend)
            if actions is not None:
                self.draw_actions.extend(actions)

        except Exception as e:  # noqa: BLE001
            if self.options.on_update_drawing_state_error == ParserOnErrorAction.Ignore:
                pass

            elif (
                self.options.on_update_drawing_state_error == ParserOnErrorAction.Raise
            ):
                if not isinstance(e, ParserError):
                    raise OnUpdateDrawingStateError from e

                raise

            elif self.options.on_update_drawing_state_error == ParserOnErrorAction.Warn:
                logging.warning(
                    "Encountered fatal error during call to update_drawing_state() "
                    "of '%s' token. Parser will skip this token and continue.",
                    token,
                )
            else:
                self.options.on_update_drawing_state_error(e, self, token)


class ParserOnErrorAction(Enum):
    """Possible error actions."""

    Ignore = "ignore"
    Warn = "warn"
    Raise = "raise"


class ParserOptions:
    """Container class for Gerber parser options."""

    def __init__(
        self,
        backend: Backend | None = None,
        initial_state: State | None = None,
        on_update_drawing_state_error: Callable[[Exception, Parser, Token], None]
        | ParserOnErrorAction = ParserOnErrorAction.Raise,
    ) -> None:
        """Initialize options."""
        self.backend = Rasterized2DBackend() if backend is None else backend
        self.initial_state = initial_state
        self.on_update_drawing_state_error = on_update_drawing_state_error
