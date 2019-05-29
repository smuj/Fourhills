import textwrap
from typing import List


def format_indented_paragraph(text: str, line_width: int) -> list:
    """Wrap a paragraph of text with approriate indentation on subsequent lines.

    Parameters
    ----------
    text : str
        The text to format.
    line_width : int
        The maximum width a line can be.

    Returns
    -------
    list of str
        The wrapped lines of text.
    """
    return textwrap.wrap(text, width=line_width, tabsize=4, subsequent_indent="    ")


def wrap_lines_paragraph(lines: List[str], line_width: int) -> List[str]:
    """Wrap any lines which are too long, indenting subsequent lines.

    Parameters
    ----------
    lines : list of str
        The lines of strings to wrap.
    line_width : int
        The maximum width a line can be.

    Returns
    -------
    list of str
        The wrapped lines of text.
    """
    output_lines = list()
    for line in lines:
        output_lines.extend(
            textwrap.wrap(line, width=line_width, tabsize=4, subsequent_indent="    ")
        )

    return output_lines


def format_list(title: str, items: list, line_width: int) -> list:
    """Join items with commas to create a text list, wrapping when necessary.

    Parameters
    ----------
    title : str
        The title to place at the start of the list.
    items : list of str
        List of the items
    line_width : int
        The maximum width a line can be.

    Returns
    -------
    list of str
        The wrapped lines of text.
    """
    # Create a text list of the items separated by commas
    item_list = ", ".join(items)
    # Add the title
    full_text = f"{title}: {item_list}"
    # Wrap the text
    return format_indented_paragraph(full_text, line_width)


def centre_pad(s, line_width):
    """Pad a string with spaces, centre-aligned."""
    return "{:^{width}}".format(s, width=line_width)
