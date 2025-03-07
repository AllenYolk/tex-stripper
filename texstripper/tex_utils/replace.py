import re

CITATION_PLACEHOLDER_FORMAT = "[{}]"
REF_PLACEHOLDER_FORMAT = "{}"
EQREF_PLACEHOLDER_FORMAT = "({})"
NAMEREF_PLACEHOLDER_FORMAT = "<{}>"

MATH_PLACEHOLDER = "<MATH>"


def _replace_tilde_pattern_with_format(
    lines, pattern, placeholder_format
) -> list:
    """Replace a pattern with a placeholder. The pattern might start with a 
    tilde ~; in that case, a space is added before the placeholder. The 
    placeholder is generated from the given format.

    Args:
        lines (list): a list of stripped lines
        pattern (str): a regular expression pattern without preceding tilde ~
        placeholder_format (str): a placeholder format

    Returns
        a list of stripped lines with the pattern replaced by the placeholder
    """
    pattern = re.compile(r"~?" + pattern)
    idx = 0
    for i, l in enumerate(lines):
        matches = pattern.findall(l)
        for m in matches:
            idx += 1
            placeholder = placeholder_format.format(idx)
            if m.startswith("~"):
                l = l.replace(m, " " + placeholder)
            else:
                l = l.replace(m, placeholder)
        lines[i] = l
    return lines


def _replace_tilde_pattern(lines, pattern, placeholder) -> list:
    """Replace a pattern with a placeholder. The pattern might start with a 
    tilde ~; in that case, a space is added before the placeholder.

    Args:
        lines (list): a list of stripped lines
        pattern (str): a regular expression pattern without preceding tilde ~
        placeholder (str): a placeholder

    Returns
        a list of stripped lines with the pattern replaced by the placeholder
    """
    pattern = re.compile(r"~?" + pattern)
    for i, l in enumerate(lines):
        matches = pattern.findall(l)
        for m in matches:
            if m.startswith("~"):
                l = l.replace(m, " " + placeholder)
            else:
                l = l.replace(m, placeholder)
        lines[i] = l
    return lines


def replace_citations(lines) -> list:
    """Replace citations with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with citations replaced by placeholders
    """
    # citations: \cite{...} or ~\cite{...}, inline
    return _replace_tilde_pattern_with_format(
        lines, r"\\cite{.*?}", CITATION_PLACEHOLDER_FORMAT
    )


def replace_references(lines) -> list:
    """Replace references with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with references replaced by placeholders
    """
    # references: \ref{...} or ~\ref{...}, inline
    return _replace_tilde_pattern_with_format(
        lines, r"\\ref{.*?}", REF_PLACEHOLDER_FORMAT
    )


def replace_equation_references(lines) -> list:
    """Replace equation references with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with equation references replaced by placeholders
    """
    # equation references: \eqref{...} or ~\eqref{...}, inline
    return _replace_tilde_pattern_with_format(
        lines, r"\\eqref{.*?}", EQREF_PLACEHOLDER_FORMAT
    )


def replace_named_reference(lines) -> list:
    """Replace named references with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with named references replaced by placeholders
    """
    # named references: \nameref{...} or ~\nameref{...}, inline
    return _replace_tilde_pattern_with_format(
        lines, r"\\nameref{.*?}", NAMEREF_PLACEHOLDER_FORMAT
    )


def replace_inline_math(lines) -> list:
    """Replace inline math with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with inline math replaced by placeholders
    """
    # inline math: $...$
    return _replace_tilde_pattern(lines, r"\$.*?\$", MATH_PLACEHOLDER)


def replace_math_blocks(lines) -> list:
    """Replace math blocks with a placeholder.

    Args:
        lines (list): a list of stripped lines

    Returns:
        a list of stripped lines with math blocks replaced by placeholders
    """
    # math blocks: \begin{equation}...\end{equation} or \begin{align}...\end{align}
    text = "\n".join(lines)

    pattern = re.compile(
        r"\\begin{(equation|align)}.*?\\end{(equation|align)}", re.DOTALL
    )
    text = pattern.sub(MATH_PLACEHOLDER, text)

    lines = text.split("\n")
    lines = [l.strip() for l in lines if l.strip()]

    return lines
