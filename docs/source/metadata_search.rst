Metadata Search
===============

.. note::
    The analyser includes a "run" script at the top of the project folder structure. This sets up
    the Virtual Environment and passes command line arguments supplied to the script through to the
    analyser. This simplifies running the application so it's recommended, though not mandatory, to
    use it. This document assumes it is being used.

The following performs a sub-string search of the game metadata for entries matching the specified text:

.. code-block:: bash

    run.sh --search "term"

For example, the following will search for games where the date of the game is February 2025:

.. code-block:: bash

    run.sh --search "2025.02"

If any matching games are found, a table of game information for each match is printed in the current
window. If no matches are found, a message to that effect is displayed.

The search is case-insensitive and the search term can contain spaces and special characters, in which case
it must be enclosed in double quotes, as shown. If it does not contain spaces or special characters, the
quotes are optional.

Multiple search terms can be specified, in which case the results are those games that match **all** of
the supplied terms. For example, the following searches for games where the date of the game is 
February 2025 **and** the "Result" metadata indicates that black won:

.. code-block:: bash

    run.sh --search 2025.02 0-1
