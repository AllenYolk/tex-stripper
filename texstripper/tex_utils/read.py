from pathlib import Path
import re


def read_tex_recursively(file_path: Path, root: Path) -> list:
    r"""Read a Tex file recursively (\input and \include commands).

    Args:
        file_path (Path): path to the (main) Tex file
        root (Path): the directory where the Tex file is located. This is used
            to resolve relative paths.

    Returns:
        list: a list of stripped lines from the Tex project.
    """
    file_path = Path(file_path)
    # add .tex, if needed
    if file_path.suffix != ".tex":
        file_path = file_path.with_suffix(".tex")
    root = Path(root)

    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines if l.strip()]

    pattern = re.compile(r"\\(input|include)\{(.*?)\}")
    new_lines = []
    for l in lines:
        match = pattern.search(l)
        if match is None:
            new_lines.append(l)
        else:  # \input or \include detected in the current line
            relative_path = match.group(2)
            corrected_path = root / relative_path
            internal_lines = read_tex_recursively(corrected_path, root)
            new_lines.extend(internal_lines)

    return new_lines
