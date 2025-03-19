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


def unwrap_headings(lines):
    """Unwrap titles.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped titles
    """
    pattern_part = re.compile(r"\\part{(.*?)}")
    pattern_chapter = re.compile(r"\\chapter\*?{(.*?)}")
    pattern_section = re.compile(
        r"\\(section|subsection|subsubsection)\*?{(.*?)}"
    )
    pattern_paragraph = re.compile(r"\\(paragraph|subparagraph){(.*?)}")

    for i, l in enumerate(lines):
        l = pattern_part.sub(r"\1", l)
        l = pattern_chapter.sub(r"\1", l)
        l = pattern_section.sub(r"\2", l)
        l = pattern_paragraph.sub(r"\2", l)
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
    pattern_figure = re.compile(
        r"(\\begin{figure\*?}.*?\\end{figure\*?})", re.DOTALL
    )
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
    pattern_table = re.compile(
        r"(\\begin{table\*?}.*?\\end{table\*?})", re.DOTALL
    )
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


def unwrap_lists(lines):
    r"""Unwrap lists.
    Assume that each `\item` is on a separate line.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped lists
    """
    pattern_env = re.compile(r"\\(begin|end){(itemize|enumerate)}")
    pattern_item = re.compile(r"\\item (.*)")

    result_lines = []
    for l in lines:
        result_l = l
        if pattern_env.match(l):
            continue  # skip the environment lines
        if pattern_item.match(l):
            result_l = pattern_item.sub(r"\1", l)
        result_lines.append(result_l.strip())

    return result_lines


def unwrap_title(lines):
    r"""Unwrap the title.
    This function is for \title{...} in the document environment. \title{...}
    in the preamble will be processed by remove_preamble() as a special case!!
    Allow multiple lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped title
    """
    text = "\n".join(lines)

    pattern_title = re.compile(r"(\\title{(.*?)})", re.DOTALL)

    title = pattern_title.search(text)
    if title:
        text = text.replace(title.group(1), title.group(2))

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines


def unwrap_abstract(lines):
    r"""Unwrap abstract.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped abstract
    """
    text = "\n".join(lines)

    pattern_abstract = re.compile(
        r"(\\begin{abstract}(.*?)\\end{abstract})", re.DOTALL
    )

    abstract = pattern_abstract.search(text)
    if abstract:
        text = text.replace(abstract.group(1), abstract.group(2))

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines


def unwrap_document(lines):
    r"""Unwrap the document environment.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with unwrapped document
    """
    text = "\n".join(lines)

    pattern_document = re.compile(
        r"(\\begin{document}(.*?)\\end{document})", re.DOTALL
    )

    document = pattern_document.search(text)
    if document:
        text = text.replace(document.group(1), document.group(2))

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines


def unwrap_pseudocode(lines) -> list:
    """Unwrap pseudocode from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        list: a list of stripped lines without pseudocode
    """
    text = "\n".join(lines)

    # Pseudocode: \begin{algorithm} ... \end{algorithm}
    pattern = re.compile(r"(\\begin{algorithm}.*?\\end{algorithm})", re.DOTALL)
    pattern_caption = re.compile(r"\\caption{(.*?)}", re.DOTALL)

    algorithms = pattern.findall(text)
    i = 0
    for algorithm in algorithms:
        cap = pattern_caption.search(algorithm)
        if cap:
            i += 1
            cap = cap.group(1).split("\n")
            cap = " ".join([c.strip() for c in cap if c.strip()])
            cap = f"Algorithm {i}: " + cap
            text = text.replace(algorithm, cap)
        else:
            text = text.replace(algorithm, "")

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines
