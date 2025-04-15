Data Management
===============

.. include:: run_script_note.rst

Listing Available Metadata Items
--------------------------------

To list the available metadata items that can be set for a game, run the following command:

.. code-block:: bash

    run.sh --list-metadata


Setting Metadata Values
-----------------------

To set the value of an item of game meta=data, run the following command:

.. code-block:: bash

    run.sh --set --reference "<unique-game-reference>" --metadata "<item-name>" --value "<item-value>"

Where <item-name> is the name of the metadata item to set and <item-value> is the value to set it to.
Quoting is required only if the values contain spaces or special characters.

The value is updated if the meta-data item already exists for the game or created if not.

By default, the update is silent but the "--verbose" option can be added to the above command to produce more
verbose output.


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
