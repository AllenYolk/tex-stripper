import re


def unwrap_text(lines):
    """Unwrap text.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped text
    """
    pattern_font = re.compile(r"\\(textbf|textit|emph|underline|uline){(.*?)}")
    pattern_color = re.compile(r"\\textcolor{.*?}{(.*?)}")
    for i, l in enumerate(lines):
        l = pattern_font.sub(r"\2", l)
        l = pattern_color.sub(r"\1", l)
        lines[i] = l

    return lines


def unwrap_footnotes(lines):
    """Unwrap footnotes.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped footnotes
    """
    # find the footnote environment
    pattern_footnote = re.compile(r"\\footnote{(.*?)}")
    for i, l in enumerate(lines):
        l = pattern_footnote.sub(r"(Note: \1)", l)
        lines[i] = l
    return lines


def unwrap_figures(lines):
    """Unwrap figures.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped figure
    """
    # join the lines
    text = "\n".join(lines)

    # find the figure environment and its caption
    pattern_figure = re.compile(r"(\\begin{figure}.*?\\end{figure})", re.DOTALL)
    pattern_caption = re.compile(r"\\caption{(.*?)}", re.DOTALL)

    figures = pattern_figure.findall(text)
    i = 0
    for fig in figures:
        cap = pattern_caption.search(fig)
        if cap:
            # merge the caption into one line
            i += 1
            cap = cap.group(1).split("\n")
            cap = " ".join([c.strip() for c in cap if c.strip()])
            cap = f"Figure {i}: " + cap
            text = text.replace(fig, cap)
        else:
            text = text.replace(fig, "")

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines


def unwrap_tables(lines):
    """Unwrap tables.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped tables
    """
    # join the lines
    text = "\n".join(lines)

    # find the figure environment and its caption
    pattern_table = re.compile(r"(\\begin{table}.*?\\end{table})", re.DOTALL)
    pattern_caption = re.compile(r"\\caption{(.*?)}", re.DOTALL)

    tables = pattern_table.findall(text)
    i = 0
    for tab in tables:
        cap = pattern_caption.search(tab)
        if cap:
            i += 1
            cap = cap.group(1).split("\n")
            cap = " ".join([c.strip() for c in cap if c.strip()])
            cap = f"Table {i}: " + cap
            text = text.replace(tab, cap)
        else:
            text = text.replace(tab, "")

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines
