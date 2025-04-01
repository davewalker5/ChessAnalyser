Chess Engine Installation
=========================

.. note::
   The Chess Analyser repository doesn't include the analysis engines, that must be downloaded
   and installed separately, per this document. The table further down this page lists the engines
   that have been tested with the anlyser and provides URLs for download sites

Per-Engine, Per-OS Folders
--------------------------

- The environment variable ENGINES_ROOT should be set to the full path to the folder under which all the engines are installed
- Each engine is then organised in its own sub-folder under that parent folder
- The binaries for the engine for each OS are placed in an OS-specific folder under the engine-specific folder
- For example, suppose the ENGINES_ROOT environment variable pointed to /home/user/ChessEngines
- In that case, the folder structure for the Komodo engine would look like this:

.. code-block::

    /home/user/ChessEngines
    └── Komodo
        ├── Linux
        │   ├── komodo-14.1-linux
        │   └── komodo-14.1-linux-bmi2
        ├── OSX
        │   ├── komodo-14.1-64-bmi2-osx
        │   └── komodo-14.1-64-osx
        └── Windows
            ├── komodo-14.1-64bit-bmi2.exe
            └── komodo-14.1-64bit.exe

- The OS-specific folder for each engine contains the binary and any supporting files, organised as required by the engine
- Typically, the engines are supplied as tarballs or compressed archives that can be downloaded and extracted into the correct folder

Engine Definitions
------------------

- The "engines.json" file contains the definitions for the supported engines in JSON format
- Each entry has the following form:


.. code-block:: json

    "stockfish": {
        "name": "Stockfish",
        "skip_mate": false,
        "executable": {
            "Linux": "Stockfish/Linux/stockfish-ubuntu-x86-64-avx2",
            "Darwin": "Stockfish/OSX/stockfish",
            "Windows": ""
        }
    }


- Where:
   - "name" is the display name
   - "skip_mate" is a boolean that controls whether the final, mating move is passed to the engine (false) or not (true)
   - "executable" is a dictionary of paths to the engine's executable for each supported OS, relative to the ENGINES_ROOT folder
- The keys for entries in the "executable" dictionary should be the OS name as returned by platform.system()
- The "skip_mate" flag is necessary as the response from some engines for the mating move isn't handled by python-chess

Supported Engines
-----------------

- The following engines have been tested with the application and are configured in the engines.json by default:

+-------------+---------------------------------------------------+
| **Name**    | **Web Site**                                      |
+-------------+---------------------------------------------------+
| Berserk     | https://github.com/jhonnold/berserk               |
+-------------+---------------------------------------------------+
| byte-knight | https://github.com/DeveloperPaul123/byte-knight   |
+-------------+---------------------------------------------------+
| Combusken   | https://github.com/mhib/combusken                 |
+-------------+---------------------------------------------------+
| Critter     | https://www.vlasak.biz/critter/                   |
+-------------+---------------------------------------------------+
| Defenchess  | https://komodochess.com/downloads.htm             |
+-------------+---------------------------------------------------+
| Dragon      | https://komodochess.com/downloads.htm             |
+-------------+---------------------------------------------------+
| FoxSEE      | https://github.com/buildingwheels/FoxSEE          |
+-------------+---------------------------------------------------+
| Koivisto    | https://github.com/Luecx/Koivisto                 |
+-------------+---------------------------------------------------+
| Komodo      | https://komodochess.com/downloads.htm             |
+-------------+---------------------------------------------------+
| Laser       | https://github.com/jeffreyan11/laser-chess-engine |
+-------------+---------------------------------------------------+
| RubiChess   | https://github.com/Matthies/RubiChess             |
+-------------+---------------------------------------------------+
| Simbelmyne  | https://github.com/sroelants/simbelmyne           |
+-------------+---------------------------------------------------+
| Stockfish   | https://github.com/official-stockfish/Stockfish   |
+-------------+---------------------------------------------------+
| Wasp        | http://waspchess.com/                             |
+-------------+---------------------------------------------------+
