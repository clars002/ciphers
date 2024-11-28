"""
File containing small utility operations used elsewhere in the
code.
"""

import os


def clear_screen():
    """
    Clears the terminal output.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def preview_text(text: str):
    """
    Creates a "preview" version of text by placing it in quotes and
    abridging it if longer than 512 characters.

    Args:
        text (str): Text to be previewed.

    Returns:
        str: The generated preview.
    """
    preview = f'"{text[:512]}..."' if len(text) > 512 else f'"{text}"'
    return preview
