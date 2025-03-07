# TexStripper

## Motivation

Grammarly is a popular tool for checking grammar and spelling errors in English text. However, LaTeX documents are not well supported by Grammarly, as LaTeX commands will interfere with the grammar checking process. Removing LaTeX syntax from the document is tiresome. **TexStripper** aims to provide a simple tool to strip LaTeX syntax from the document, so that the document can be checked by Grammarly.

## Installation and Usage

1. Clone the repository:

```shell
git clone https://github.com/AllenYolk/tex-stripper.git
```

2. Run the script with Python:

```shell
python tex_stripper.py -s <path_to_source_file> -o <path_to_output_file>
```

TODO: add `setup.py` to make `texstripper` a globally available command-line tool.

## Functionality

*Remove* the following LaTeX components from a `.tex` file:

* Comments: `% ...`, both between lines and inline
* Labels: `\label{...}`

*Replace* the following LaTeX components with a placeholder:

* Citations: `\cite{...}` or `~\cite{...}`
* References: `\ref{...}` or `~\ref{...}`
* Equation references: `\eqref{...}` or `~\eqref{...}`
* Named references: `\nameref{...}` or `~\nameref{...}`
* Inline math: `$...$`
* Math blocks: `\begin{equation} ... \end{equation}`, `\begin{align} ... \end{align}`

*Unwrap* the following LaTex commands while keeping the contents:

* Bold: `\textbf{...}`
* Italic: `\textit{...}`
* Underline: `\underline{...}`, `\uline{...}`
* Emphasis: `\emph{...}`
* Color: `\textcolor{...}{...}`; only the second argument is kept
* Table: `\begin{table} ... \end{table}`; only the caption is kept
* Figure: `\begin{figure} ... \end{figure}`; only the caption is kept

## Acknowledgements

* This project is inspired by [my-yy](https://github.com/my-yy)'s JavaScript-based repository [MyGrammarly](https://github.com/my-yy/MyGrammarly). We appreciate their open-source work!
