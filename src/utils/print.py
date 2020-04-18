
from termcolor import colored


def PRINT(text, text_color='blue', text_highlights=None, attributes=None):
    """
    Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if text_highlights is not None:
        if attributes is not None:
            print(colored(text, text_color, text_highlights, attributes))
        else:
            print(colored(text, text_color, text_highlights))

    else:
        if attributes is not None:
            print(colored(text, text_color, attributes=attributes))
        else:
            print(colored(text, text_color))

