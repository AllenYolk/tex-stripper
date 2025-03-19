import re


def remove_comments(lines) -> list:
    """Remove comments from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without comments
    """
    # Comment lines: start with %
    lines = [l for l in lines if not l.startswith('%')]

    # Remove inline comments: from % to the end of the line
    # Caution: don't remove `\%`
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == "%" and (j == -1 or l[j - 1] != "\\"):
                lines[i] = l[:j].strip()
                break

    return lines


def remove_authors(lines) -> list:
    """Remove authors from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without authors
    """
    text = "\n".join(lines)
    pattern = re.compile(r"\\author(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})")

    text = pattern.sub("", text)

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines


def remove_labels(lines) -> list:
    """Remove labels from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without labels
    """
    new_lines = []
    pattern = re.compile(r"\\label\{.*?\}")
    for l in lines:
        l = pattern.sub("", l).strip()
        if l:  # not empty
            new_lines.append(l)
    return new_lines


def remove_preamble(lines) -> list:
    r"""Remove the preamble from a list of lines. 
    If a \title{} is detected in the preamble, leave the block there not removed.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without the preamble
    """
    # find `\begin{document}`
    pattern_begin_document = re.compile(r"\\begin\{document\}")
    begin_document_idx = None
    for i, l in enumerate(lines):
        if pattern_begin_document.search(l):
            begin_document_idx = i
            break

    # preamble: 0 ~ begin_document_idx-1
    preamble_text = "\n".join(lines[:begin_document_idx])
    main_lines = lines[begin_document_idx:]
    # find possible `\title`
    pattern_title = re.compile(r"(\\title{(.*?)})", re.DOTALL)
    title = pattern_title.search(preamble_text)
    if title:
        main_lines = [title.group(1).strip()] + main_lines

    main_text = "\n".join(main_lines)
    lines = main_text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]
    return lines


def remove_inline_commands(lines) -> list:
    """Remove inline commands from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        list: a list of stripped lines without inline commands
    """
    inline_command_list = [
        r"\\maketitle",
        r"\\linenumbers",
        r"\\nolinenumbers",
        r"\\justifying",
        r"\\newpage",
        r"\\IEEEdisplaynontitleabstractindextext",
        r"\\IEEEpeerreviewmaketitle",
        r"^\\markboth",  # all commands starting with \markboth
        r"^\\if",  # all commands starting with \if
        r"^\\fi",  # all commands starting with \fi
    ]
    pattern = "|".join(inline_command_list)
    pattern = re.compile(pattern)

    new_lines = []
    for l in lines:
        if pattern.search(l):
            continue
        new_lines.append(l)

    return new_lines


def remove_bibliography(lines) -> list:
    """Remove bibliography from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without bibliography
    """
    pattern = re.compile(r"(\\bibliography{.*?}|\\bibliographystyle{.*?})")

    new_lines = []
    for l in lines:
        if pattern.search(l):
            continue
        new_lines.append(l)

    return new_lines
