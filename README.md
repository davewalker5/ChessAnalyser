[![GitHub issues](https://img.shields.io/github/issues/davewalker5/ChessAnalyser)](https://github.com/davewalker5/ChessAnalyser/issues)
[![Releases](https://img.shields.io/github/v/release/davewalker5/ChessAnalyser.svg?include_prereleases)](https://github.com/davewalker5/ChessAnalyser/releases)
[![License: MIT](https://img.shields.io/badge/License-mit-blue.svg)](https://github.com/davewalker5/ChessAnalyser/blob/main/LICENSE)
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/davewalker5/ChessAnalyser)](https://github.com/davewalker5/ChessAnalyser/)

# Chess Analyser

The Chess Analyser is a command-line tool for analysing chess games stored as PGN files. It was developed in
response to a need to analyse games using UCI compliant engines on older operating systems that are not supported by some of the modern chess GUIs.

It provides the following functionality:

- The ability to load games from PGN files and store them in a SQLite database
- Analysis of stored games using local installations of UCI-compliant chess engines, with storage of the analysis in the database
- Reporting on the analysis to:
   - The console
   - XLSX spreadsheets
   - DOCX documents
- Export of PGN files with the evaluations and move annotations included

The application uses the [python-chess](https://github.com/niklasf/python-chess) library to communicate with the analysis engines and applies the scoring algorithms from [Lichess](https://lichess.org/page/accuracy) and [En Croissant](https://github.com/franciscoBSalgueiro/en-croissant) to the per-move analysis results to score each move.

# Getting Started

The repository includes documentation in RST format that covers setting up and running the application. To build the documentation, the following pre-requisites must be met:

- An installation of Python 3

The documentation can be built as follows:

1. Clone the repository
2. In the root of the working copy, run the following command to build the virtual environment:

```
./make_venv.sh
```

3. Change to the "docs" folder and run the following command:

```
./make_docs.sh
```

Once built, the documentation can be browsed from the following HTML document:

```
docs/build/html/index.html
```

# Authors

- **Dave Walker** - _Initial work_

# Feedback

To file issues or suggestions, please use the [Issues](https://github.com/davewalker5/ChessAnalyser/issues) page for this project on GitHub.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
