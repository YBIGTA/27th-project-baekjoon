from __future__ import annotations
import re


def extract_code_block(markdown_text: str) -> str | None:
    """Extract the first fenced code block from markdown.

    Supports both ```lang\n...\n``` and ```\n...\n``` forms.
    Returns the inner code without backticks, or None if not found.
    """
    patterns = [
        r"```[ \t]*[a-zA-Z0-9._+-]+[ \t]*\r?\n([\s\S]*?)\r?\n?```",
        r"```\r?\n([\s\S]*?)\r?\n?```",
    ]
    for pat in patterns:
        match = re.search(pat, markdown_text)
        if match:
            return match.group(1).strip()
    return None
