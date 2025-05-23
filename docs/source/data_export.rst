Data Export
===========

.. include:: run_script_note.rst

Exporting Analysis Results
--------------------------

To export the analysis for a game that's been loaded and analysed, use the following options:

.. code-block:: bash

    run.sh --export --reference "<unique-game-reference>" --engine <engine-name> --xlsx <spreadsheet>
    run.sh --export --reference "<unique-game-reference>" --engine <engine-name> --docx <document>
    run.sh --export --reference "<unique-game-reference>" --engine <engine-name> --pgn <PGN>

The first form exports a report in XLSX format to the specified spreadsheet, the second exports a report in
DOCX format to the specified document file and the final form writes a PGN file for the game annotated with
the evaluation and annotations for each move.

If required, multiple outputs can be specified in a single export command:

.. code-block:: bash

    run.sh --export --reference "<unique-game-reference>" --engine <engine-name> --xlsx <spreadsheet> --docx <document> --pgn <PGN>

This command exports the analysis in both XLSX and DOCX format and writes the annotated PGN file.

By default, export is silent but the "--verbose" option can be added to the above commands to produce more
verbose output.

Exporting Images of the Board
-----------------------------

To export a PNG format image of the board position for a game that's been loaded, but not necessarily analysed, use the following options:

.. code-block:: bash

    run.sh --export --reference "<unique-game-reference>" --image "<image-file-path>" --halfmoves <halfmoves>


"<halfmoves>" indicates the number of halfmoves to fast-forward by before exporting the image. It may also have the value "*" to fast-forward
to the end of the game and export the final position.

By default, export is silent but the "--verbose" option can be added to the above command to produce more
verbose output.

Exporting Movies of a Game
--------------------------

To export an MP4 format move of a game that's been loaded, but not necessarily analysed, use the following options:

.. code-block:: bash

    run.sh --export --reference "<unique-game-reference>" --movie "<movie-file-path>" --duration <n>


"<n>" is the number of seconds for which each move in the game is displayed. The duration should be a positive number e.g. 0.5, 1.

By default, the captions for each frame include only the move. If the game has been analysed using an engine, its move annotations
and evaluations can be included in the caption by adding the "--engine" option:

.. code-block:: bash

    run.sh --export --reference "<unique-game-reference>" --movie "<movie-file-path>" --duration <n> --engine <engine-name>

By default, export is silent but the "--verbose" option can be added to the above commands to produce more
verbose output.
