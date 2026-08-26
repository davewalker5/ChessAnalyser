PGN Editor
==========

The PGN Editor is a graphical desktop application for creating, editing, reviewing, replaying, loading and saving chess games in Portable Game Notation (PGN) format. It is independent of the command-line Chess Analyser and does not require a game to be imported into the analyser database.

The editor uses the ``python-chess`` library to maintain the board position, generate Standard Algebraic Notation (SAN), validate moves and read and write PGN files.


Starting the Editor
-------------------

Install the Chess Analyser package and its dependencies in the active Python environment before starting the editor. From that environment, run:

.. code-block:: console

    pgn-editor

The editor can also be started as a Python module:

.. code-block:: console

    python -m pgn_editor

The initial board uses the standard chess starting position, with White at the bottom. The current game is initially unnamed and contains no moves.


Editor Layout
-------------

The editor window contains two main panels:

* The left panel contains the chessboard and coordinates.
* The right panel contains the SAN move list, navigation and playback
  controls, editing controls and a status message.

Compact material summaries sit above and below the board beside the corresponding
player. With White at the bottom, Black's captures are shown above the board and
White's captures below it; flipping the board reverses their positions. Each
summary shows the captured pieces and their total conventional value: pawn 1,
knight 3, bishop 3, rook 5 and queen 9. The summaries follow the currently
displayed position, so they change when navigating or replaying a game.


Editing Game Details
--------------------

The **Game Details** panel above the move list edits the seven standard PGN header fields. Values loaded from a PGN file are displayed automatically and are retained when the game is saved.

.. list-table:: PGN game details
   :header-rows: 1
   :widths: 20 55 25

   * - Field
     - Description
     - Default value
   * - ``Event``
     - Name of the tournament, match or event
     - ``Unknown``
   * - ``Site``
     - Location at which the game was played
     - ``?``
   * - ``Date``
     - Date of the game in PGN ``YYYY.MM.DD`` format
     - ``????.??.??``
   * - ``Round``
     - Round number or identifier within the event
     - ``?``
   * - ``White``
     - Name of the player with the White pieces
     - ``?``
   * - ``Black``
     - Name of the player with the Black pieces
     - ``?``
   * - ``Result``
     - Recorded result of the game
     - ``*``

Enter a value in a text field and then press ``Enter`` or move focus to another control to apply it. Leaving a text field blank restores the default shown above. Editing any game detail marks the document as having unsaved changes, indicated by an asterisk in the window title.


Selecting a Date
~~~~~~~~~~~~~~~~

Select the calendar button beside ``Date`` to open the date picker. Use the left and right arrow buttons to change month, select a numbered day, or select ``Today``. The chosen date is stored in PGN ``YYYY.MM.DD`` format.

The Date field remains directly editable because PGN supports unknown and partial dates. For example, ``2026.??.??`` records a known year with an unknown month and day. Clearing the field restores ``????.??.??``.


Selecting a Result
~~~~~~~~~~~~~~~~~~

Select the game result from the available PGN values:

``*``
    The game is unfinished or its result is unknown.

``1-0``
    White won.

``0-1``
    Black won.

``1/2-1/2``
    The game was drawn.

The editor sets Result automatically when a move ends the game: ``1-0`` or
``0-1`` after checkmate, and ``1/2-1/2`` after a draw recognised by
``python-chess``. Undoing that final move resets Result to ``*``. The field can
still be selected manually when recording a result that is not determined by
the position, such as resignation or an agreed draw.


Saving and Loading Details
~~~~~~~~~~~~~~~~~~~~~~~~~~

Game details are written as PGN header tags when the game is saved. Opening a PGN file populates the editor with the first game's existing header values. Missing or blank supported fields receive the defaults shown above. A failed load or save leaves the current metadata and game unchanged.


Entering Moves
--------------

To enter a move, drag a piece from its current square and drop it on a legal destination square.

When a piece is dragged:

* The source square is highlighted in amber
* Legal empty destination squares are marked with cyan dots
* Legal captures are marked with cyan rings
* A legal destination beneath the pointer is highlighted in green
* An illegal destination beneath the pointer is highlighted in red

After a legal move is dropped, the board is updated and its SAN representation is appended to the move list. White and Black moves are grouped under the appropriate move number, and the latest move remains visible.

The editor validates all moves using the current board position. This includes checks, pins, captures, castling restrictions, en passant and promotion. An illegal drop does not change the board, move history, current file or unsaved state.


Pawn Promotion
~~~~~~~~~~~~~~

When a pawn reaches its final rank, the editor asks whether it should be promoted to a queen, rook, bishop or knight. Cancelling this choice leaves the position unchanged.


Completed Games
~~~~~~~~~~~~~~~

No further moves can be added after checkmate or stalemate. The status area reports checkmate and the winning colour, or reports a draw by stalemate.


Editing a Game
--------------

The editing controls are:

``Undo``
    Removes the final recorded move and displays the new final position. Undo can be repeated until the starting position is reached.

``Clear``
    Removes every move, restores the standard starting position and resets all
    editable game details to their defaults. The current filename is retained,
    and the editor asks for confirmation before resetting moves or non-default
    details.

``Flip``
    Alternates between White-at-bottom and Black-at-bottom orientations. The pieces and board coordinates are reversed without changing the position or move history.

Entering, undoing or clearing moves marks the game as changed. An asterisk in the window title identifies a game with unsaved changes.


Starting a New Game
-------------------

Choose **File > New Game**, or press ``Ctrl+N``, to create a clean, untitled
game. This resets the board, moves, captured-material totals and game details,
and removes the current filename. A later Save therefore asks for a destination.

If the current game has unsaved changes, the editor asks whether to save,
discard or cancel. A cancelled or unsuccessful save leaves the existing game
and filename unchanged.


Navigating Through a Game
-------------------------

A set of media-style navigation controls are presented under the move list:

.. list-table:: Navigation controls
   :header-rows: 1
   :widths: 20 80

   * - Control
     - Action
   * - ``⏮``
     - Jump to the standard starting position
   * - ``◀◀``
     - Move backwards by one half-move
   * - ``▶▶``
     - Move forwards by one half-move
   * - ``⏭``
     - Jump to the final position
   * - ``▶``
     - Play forwards automatically from the displayed position
   * - ``⏸``
     - Pause automatic playback immediately

Controls are disabled when their action is not available. The move that led to the displayed position is highlighted in the move list. At the initial position, no move is highlighted.

Navigation changes only the displayed position. It does not remove moves, alter the saved game or mark the game as changed.


Editing From an Earlier Position
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entering a move while viewing an earlier position creates a new continuation. Because this would discard all moves after the displayed position, the editor asks for confirmation before making the change. Cancelling leaves the complete game unchanged.


Automatic Playback
------------------

Select ``▶`` to replay moves from the displayed position. Playback stops automatically at the end of the game.

The playback slider sets the delay between moves from 0.25 to 5 seconds. The default is 1 second. Changing the slider during playback applies the new delay without restarting the game.

Playback pauses before an action that changes the game, opens another file or closes the application.


Opening PGN Files
-----------------

Select **File > Open** or press ``Ctrl+O`` to open a PGN file. The editor loads the first game, displays its final position and makes its complete main line available for navigation.

If the file contains multiple games, only the first game is loaded and a notification is displayed. Standard PGN header tags from that game are retained when it is saved again.

The editor supports games beginning from the standard chess position. Games that use a custom FEN starting position are not supported.

An empty, unreadable or invalid file produces an explanatory message and leaves the current game unchanged.

If the current game has unsaved changes, the editor asks whether to save, discard or cancel before opening another file.


Saving PGN Files
----------------

Use **File > Save** or press ``Ctrl+S`` to save the current game. The first save opens the operating system's file-selection dialog and defaults to a ``.pgn`` extension. Later saves reuse the current file path.

Use **File > Save As** or press ``Ctrl+Shift+S`` to select a different path. The operating system asks for confirmation before an existing file is overwritten.

Games are saved as standards-compliant PGN containing the main line and known header tags. New games receive valid default tags. A failed save leaves the in-memory game intact and marked as unsaved.


Closing the Editor
------------------

When the editor is closed with unsaved changes, it offers three choices:

``Save``
    Save the game, then close the editor. Cancelling the save-file dialog also cancels closing

``Discard``
    Close without saving the changes

``Cancel``
    Return to the editor without closing it


Keyboard Shortcuts
------------------

.. list-table:: Keyboard shortcuts
   :header-rows: 1
   :widths: 35 65

   * - Shortcut
     - Action
   * - ``Ctrl+O``
     - Open a PGN file
   * - ``Ctrl+S``
     - Save the current game
   * - ``Ctrl+Shift+S``
     - Save the current game to a selected path
   * - ``Ctrl+Z``
     - Undo the final move

On platforms where the operating system maps conventional control shortcuts to a different modifier, the displayed menu shortcut should be followed.


Current Limitations
-------------------

The editor works with one standard-position game and its main line. It does not currently support:

* Editing PGN header tags
* Comments, annotations, variations or numeric annotation glyphs
* Selecting games other than the first game in a multi-game PGN file
* Games beginning from a custom FEN position
* Chess-engine analysis or evaluation
* Clocks or time controls
* Direct integration with online chess services
