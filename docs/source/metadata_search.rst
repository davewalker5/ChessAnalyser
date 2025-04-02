Metadata Search
===============

.. note::
    The analyser includes a "run" script at the top of the project folder structure. This sets up
    the Virtual Environment and passes command line arguments supplied to the script through to the
    analyser. This simplifies running the application so it's recommended, though not mandatory, to
    use it. This document assumes it is being used.

The following searches the game metadata for entries matching the specified text:

.. code-block:: bash

    run.sh --search "phrase"

If any matching games are found, a table of game information for each match is printed in the current
window. If no matches are found, a message to that effect is displayed.

The search is case-insensitive and the phrase can contain spaces and special characters, in which case
it must be enclosed in double quotes, as shown. If it does not contain spaces, quoting it is optional.
