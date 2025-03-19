# TexStripper

## Motivation

Grammarly is a popular tool for checking grammar and spelling errors in English text. However, LaTeX documents are not well supported by Grammarly, as LaTeX commands will interfere with the grammar checking process. Removing LaTeX syntax from the document is tiresome. **TexStripper** aims to provide a simple tool to strip LaTeX syntax from the document, so that the document can be checked by Grammarly.

## Installation

### Install from PyPI

```shell
pip install texstripper
```

### Install from Github

1. Clone the repository:

```shell
git clone https://github.com/AllenYolk/tex-stripper.git
```

2. Install the package to your Python environment:

```shell
cd tex-stripper
pip install .
```

## Usage

```shell
python texstripper/cli.py -s <path_to_source_file> -o <path_to_output_file>
```

## Functionality

**Read** TeX scripts recursively according to the `\input{...}` and `\include{...}` commands.

* So, you only need to run `texstripper` once on `main.tex`, and all the subfiles will be processed.

**Remove** the following LaTeX components from a `.tex` file:

* Comments: `% ...`, both between lines and inline
* Preamble: the part before `\begin{document}`
* Authors: `\author{...}`
* Labels: `\label{...}`
* Bibliography: `\bibliography{...}`, `\bibliographystyle{...}`
* Miscellaneous inline commands: `\maketitle`, `\linenumbers`, `\nolinenumbers`, `\newpage`, ...
    * See `texstripper/tex_utils/remove.py` for more details.

**Replace** the following LaTeX components with a placeholder:

* Citations: `\cite{...}` or `~\cite{...}`
* References: `\ref{...}` or `~\ref{...}`
* Equation references: `\eqref{...}` or `~\eqref{...}`
* Named references: `\nameref{...}` or `~\nameref{...}`
* Inline math: `$...$`
* Math blocks: `\begin{equation} ... \end{equation}`, `\begin{align} ... \end{align}`
* Input & include: `\input{...}`, `\include{...}`

**Unwrap** the following LaTex commands while keeping the contents:

* Title: `\title{...}`
* Document: `\begin{document} ... \end{document}`
* Abstract: `\begin{abstract} ... \end{abstract}`
* Part & chapter & section & paragraph: `\part{}`, `\chapter{...}`, `\section{...}`, `\subsection{...}`, `\subsubsection{...}`, `\paragraph{...}`, `\subparagraph{...}`
* Bold: `\textbf{...}`
* Italic: `\textit{...}`
* Underline: `\underline{...}`, `\uline{...}`
* Emphasis: `\emph{...}`
* Color: `\textcolor{...}{...}`; only the second argument is kept
* Footnote: `\footnote{...}`
* List: `\begin{itemize} ... \item ... \end{itemize}`, `\begin{enumerate} ... \item ... \end{enumerate}`; only the list items are kept
* Table: `\begin{table} ... \end{table}`; only the caption is kept
* Figure: `\begin{figure} ... \end{figure}`; only the caption is kept
* Pseudocode: `\begin{algorithm} ... \end{algorithm}`; only the caption is kept

## Acknowledgements

* This project is inspired by [my-yy](https://github.com/my-yy)'s JavaScript-based repository [MyGrammarly](https://github.com/my-yy/MyGrammarly). We appreciate their open-source work!
