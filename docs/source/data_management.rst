Data Management
===============

.. include:: run_script_note.rst

Deleting Game Analysis From A Single Engine
-------------------------------------------

To delete the analysis of a game done by a single, specified engine, run the following command:

.. code-block:: bash

    run.sh --delete --reference "<unique-game-reference>" --engine <engine-name>

Where <engine-name> is the key for the engine as configured in the "engines.json" file (refer to the
engine installation documentation for details).

You will be prompted to confirm the deletion before the data is deleted.

By default, deletion is silent but the "--verbose" option can be added to the above command to produce more
verbose output.

Deleting All Analyses For a Game
--------------------------------

To delete all analyses of a game, irrespective of the engine used, run the following command:

.. code-block:: bash

    run.sh --delete --reference "<unique-game-reference>" --engine "*"

You will be prompted to confirm the deletion before the data is deleted.

By default, deletion is silent but the "--verbose" option can be added to the above command to produce more
verbose output.

Deleting All Data for a Game
----------------------------

To delete all data relating to a game, run the following command:

.. code-block:: bash

    run.sh --delete --reference "<unique-game-reference>"

You will be prompted to confirm the deletion before the data is deleted.

By default, deletion is silent but the "--verbose" option can be added to the above command to produce more
verbose output.
