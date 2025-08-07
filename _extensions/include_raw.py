"""Custom Jinja2 extension to include files without rendering them.

This solves the issue where GitHub Actions variables (${{ }}) conflict
with Jinja2 syntax.
"""

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from jinja2 import nodes
from jinja2.ext import Extension

if TYPE_CHECKING:
    from jinja2.parser import Parser


class IncludeRawExtension(Extension):
    """A Jinja2 extension that adds an 'include_raw' tag to include files.

    Without processing them through the Jinja2 template engine.

    Usage:
        {% include_raw '.github/workflows/pre-commit.yml' %}
    """

    tags: ClassVar[set[str]] = {"include_raw"}

    def parse(self, parser: "Parser") -> nodes.Output:
        # Get the tag token
        lineno = next(parser.stream).lineno

        # Parse the filename argument
        filename_node = parser.parse_expression()

        # Create a call node to our _include_raw method
        call_node = self.call_method("_include_raw", [filename_node])

        # Return an output node
        return nodes.Output([call_node], lineno=lineno)

    def _include_raw(self, filename: str) -> str:
        """Read and return file contents without processing them.

        Args:
            filename: Path to the file relative to template root

        Returns:
            Raw file contents or error message

        """
        # Get the template directory from the environment
        template_dir_str = (
            self.environment.loader.searchpath[0]
            if hasattr(self.environment.loader, "searchpath")
            else "."
        )
        template_dir = Path(template_dir_str).resolve()

        # Security: Resolve the requested file path and check it's within template_dir
        requested_path = Path(filename)

        # Prevent absolute paths
        if requested_path.is_absolute():
            msg = f"Absolute paths not allowed: {filename}"
            raise ValueError(msg)

        # Resolve the full path
        full_path = (template_dir / requested_path).resolve()

        # Security check: ensure the resolved path is within template_dir
        if not str(full_path).startswith(str(template_dir)):
            msg = f"Path outside template directory: {filename}"
            raise ValueError(msg)

        return full_path.read_text(encoding="utf-8")


# Export the extension for Copier to use
__all__ = ["IncludeRawExtension"]
