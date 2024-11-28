import os


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def preview_text(text: str):
    preview = f'"{text[:512]}..."' if len(text) > 512 else f'"{text}"'
    return preview
