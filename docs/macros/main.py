from __future__ import annotations

import os
from pprint import pformat

from mkdocs_macros.plugin import MacrosPlugin


def define_env(env: MacrosPlugin) -> None:
    """This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    @env.macro
    def include_file(filename: str, start_line=0, end_line=None):  # type: ignore[no-untyped-def]
        """Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename) as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return "".join(line_range)

    @env.macro
    def include_code(
        filename: str, language: str, start_line=0, end_line=None, **options: str
    ):
        """Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename) as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]

        options_str = " ".join(f'{k}="{v}"' for k, v in options.items())

        return f"```{language} {options_str}\n" + "".join(line_range) + "```"

    @env.macro
    def pformat_variable(module: str, variable: str) -> str:
        """Pretty format a variable from a module."""
        module = __import__(module, fromlist=[variable])
        value = getattr(module, variable)
        return "```python\n" + variable + " = " + pformat(value) + "\n```"

    @env.macro
    def include_definition(symbol: str, **options: str) -> str:
        """Include the signature of a class without the docstring."""
        options_string = "        ".join(f"{k}: {v}\n" for k, v in options.items())
        return f"""
::: {symbol}
    options:
        {options_string}

"""

    @env.macro
    def run_capture_stdout(command: str, title: str, language: str = "log") -> str:
        """Run a command and capture its stdout."""
        from subprocess import check_output

        return (
            f'```{language} title="$ {title}"\n'
            + check_output(command, shell=True).decode(encoding="utf-8")
            + "```"
        )
