# Overview

The Chess Performance Calculator that prompts ACPL and game length for a game and then uses the personal performance models presented in the "performance-modelling" folder to calculate a performance rating.

It's designed to work on a *"TI-84 Plus CE-T Python Edition"* calculator, as that makes it highly portable, though space limitations on the device mandate that the interface, while functional, is extremely simple. It will also run on a desktop machine or laptop if required.

# Configuring the Calculator

First, run the appropriate model (single or multi-engine) and capture the values for the following:

- Short-game threshold
- ACPL floor values
- Model parameters R_MIN, R_MAX, K and ACPL_best

These values needed to be set at the top of the *chessprf.py* script, per the following example:

```
MOVES_SHORT = 25
ACPL_MIN_SHORT = 25
ACPL_MIN_NORMAL = 20
R_MIN = 800
R_MAX = 2300
K = 0.05341958625524604
ACPL_BEST = 23.709467837259233
```

# Running the Calculator on the Desktop

To confirm it's working, enter the following command from the *chessprf* folder:

```bash
python src/chessprf.py
```

The output, including an example, should look something like this:

```
============================
Chess Performance Calculator
============================

ACPL? 26.89
Moves? 18

Performance rating = 2066

ACPL? 
```

To exit the application, just hit "ENTER" in response to one of the "ACPL?" or "Moves?" prompts.

# Transferring to the Calculator

As space is at a premium on the calculator, a minimiser is provided that removes unecessary space from the application file before transferring it. To run the minimiser, enter the following commands from the *chessprf* folder:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python minimiser/minimiser.py
```

This will create a folder called *minimised* in the *minimiser* folder and that folder will contain the minimised source. This is the version that should be transferred to the calculator, using *"TI Connect CE"* software, that can be downloaded from the Texas Instruments web site.

# Running the Application on the Calculator

1. Press the *prgm* button
2. Select *Python App* in the menu and press *enter*
3. Select *CHESSPRF* from the list of available programs and press the *Run* button, indicated at the bottom of the display

The application will load and run. The output and behaviour is identical to that when running it on the desktop.