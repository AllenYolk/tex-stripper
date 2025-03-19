#!/usr/bin/env python
import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

import tex_utils


def process_lines(lines):
    lines = tex_utils.remove_comments(lines)
    lines = tex_utils.remove_preamble(lines)
    lines = tex_utils.remove_authors(lines)
    lines = tex_utils.remove_labels(lines)
    lines = tex_utils.remove_bibliography(lines)
    lines = tex_utils.remove_inline_commands(lines)
    lines = tex_utils.replace_citations(lines)
    lines = tex_utils.replace_references(lines)
    lines = tex_utils.replace_equation_references(lines)
    lines = tex_utils.replace_named_reference(lines)
    lines = tex_utils.replace_inline_math(lines)
    lines = tex_utils.replace_input_and_include(lines)
    lines = tex_utils.unwrap_title(lines)
    lines = tex_utils.unwrap_document(lines)
    lines = tex_utils.unwrap_abstract(lines)
    lines = tex_utils.unwrap_headings(lines)
    lines = tex_utils.unwrap_text(lines)
    lines = tex_utils.unwrap_footnotes(lines)
    lines = tex_utils.unwrap_lists(lines)
    lines = tex_utils.unwrap_figures(lines)
    lines = tex_utils.unwrap_tables(lines)
    lines = tex_utils.unwrap_pseudocode(lines)
    lines = tex_utils.replace_math_blocks(lines)
    return lines


def main():
    parser = argparse.ArgumentParser(description='Strip TeX to plain text.')
    parser.add_argument(
        "-s", "--source", help="Source file", type=str, required=True
    )
    parser.add_argument(
        "-o", "--output", help="Target file", type=str, default="output.txt"
    )
    args = parser.parse_args()
    source = Path(args.source)
    output = Path(args.output)

    lines = tex_utils.read_tex_recursively(source, root=source.parent)

    lines = process_lines(lines)

    with open(output, 'w') as f:
        for line in lines:
            f.write(line.strip() + '\n\n')


if __name__ == "__main__":
    main()
