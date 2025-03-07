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


def remove_labels(lines) -> list:
    """Remove labels from a list of lines.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines without labels
    """
    new_lines = []
    pattern = re.compile(r"\\label{.*?}")
    for l in lines:
        l = pattern.sub("", l).strip()
        if l:  # not empty
            new_lines.append(l)
    return new_lines
