Chess Analysis
==============

The Chess Analyser is a command-line tool for analysing chess games stored as PGN files. It was developed in
response to a need to analyse games using UCI compliant engines on older operating systems that are not
supported by some of the modern chess GUIs.

It provides the following functionality:

- The ability to load games from PGN files and store them in a SQLite database
- Analysis of stored games using local installations of UCI-compliant chess engines, with storage of the analysis in the database
- Reporting on the analysis to:
   - The console
   - XLSX spreadsheets
   - DOCX documents
- Export of the following:
   - PGN files with the evaluations and move annotations included
   - Images (PNG format) of the board at any point in the game
   - Movies (MP4 format) of the game with or without annotations and evaluations shown per move

The application uses the python-chess library [#1]_ to communicate with the analysis engines and applies the scoring
algorithms from Lichess [#2]_ and En Croissant [#3]_ to the per-move analysis results to score each move.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   setup
   engines
   database
   workflow
   data_export
   metadata_search
   data_management
   scoring
   cli
   code/modules


References
==========

.. [#1] `python-chess <https://github.com/niklasf/python-chess>`_
.. [#2] `Lichess accuracy calculation <https://lichess.org/page/accuracy>`_
.. [#3] `En Croissant <https://github.com/franciscoBSalgueiro/en-croissant>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
