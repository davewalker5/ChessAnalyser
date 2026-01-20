Scoring
=======

The scoring scheme employed by the analyser is an implementation of the scheme used by En Croissant [#2]_.

Score Normalisation
-------------------

A score, x, is normalised as follows:

- If the player is black, x = x * -1
- If it's a MATE score, the following formula is used to determine the CP loss

.. code-block:: python

    x = MATE_SCORE * sign(x)


- MATE_SCORE is defined as 1000
- sign(x) returns 1 if x > 0, -1 if x < 0 and 0 if x = 0
- The sign() function can be implemented in Python as follows:


.. code-block:: python

    def sign(x):
        """
        Given a value, x, return the sign of that value

        :param x: Value
        :return: -1 if x < 0, 1 if x > 0, 0 if x = 0
        """
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0


- The following is then used as the normalised score:

+---------------------------------------+----------------------+
| **Conditions**                        | **Normalised Score** |
+---------------------------------------+----------------------+
| cp >= -MATE_SCORE && cp <= MATE_SCORE | cp                   |
+---------------------------------------+----------------------+
| cp < -MATE_SCORE                      | -MATE_SCORE          |
+---------------------------------------+----------------------+
| cp > MATE_SCORE                       | MATE_SCORE           |
+---------------------------------------+----------------------+

CP Loss Calculation
-------------------

- Requires the CP score for the previous move and the score for the current move
- If this is the first halfmove, the prev_score has a CP value of 15
- Both the prev_score and score are normalised as described above
- The CP loss is then calculated as the maximum of 0 and (prev_score - score)
- A collection of CP losses are calculated, one for each move

Accuracy Calculation
--------------------

- Requires the CP score for the previous move and the score for the current move
- If this is the first halfmove, the prev_score has a CP value of 15
- Both the prev_score and score are normalised as described above
- Per the Lichess documentation [#1]_, the "win%" value is calculated for the prev_score and score using the following formula:

.. code-block:: python

    import math
    prev_win_percent = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * prev_score)) - 1)
    win_percent = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * score)) - 1)


- Per the Lichess documentation [#1]_, an accuracy value is calculated as:

.. code-block:: python

    import math
    accuracy = 103.1668 * math.exp(-0.04354 * (prev_win_percent - win_percent)) - 3.1669 + 1


- The following is then calculated as the accuracy for the current move:

+--------------------+--------------+
| **Conditions**     | **Accuracy** |
+--------------------+--------------+
| a >= 0 && a <= 100 | a            |
+--------------------+--------------+
| a < 0              | 0            |
+--------------------+--------------+
| a > 100            | 100          |
+--------------------+--------------+

- A collection of CP losses are calculated, one for each move

ACPL Calculation
----------------

- If cp_losses is a list of individual cp_loss values, ACPL is calculated as a simple mean or average:


.. code-block:: python

    import statistics
    acpl = statistics.mean(cp_losses)


ELO Estimation
--------------

- ELO is estimated from the ACPL using the following estimation [#3]_, [#4]_:

.. math::

   \mathrm{ELO} = 3100 e^{-0.01 \,\mathrm{ACPL}}

Overall Accuracy Calculation
----------------------------

- If accuracies is a list if individual accuracy values, the overall accuracy is calculated as a "harmonic mean"
- The harmonic mean is defined as the number of values divided by the sum of their reciprocals
- Using the Python statistics package, it's calculated as follows:


.. code-block:: python

    import statistics
    acpl = statistics.harmonic_mean(cp_losses)


References
----------

.. [#1] `Lichess accuracy calculation <https://lichess.org/page/accuracy>`_
.. [#2] `En Croissant <https://github.com/franciscoBSalgueiro/en-croissant>`_
.. [#3] `Estimating ELO using ACPL <https://lichess.org/forum/general-chess-discussion/how-to-estimate-your-elo-for-a-game-using-acpl-and-what-it-realistically-means?utm_source=chatgpt.com>`_
.. [#4] "Using Heuristic-Search Based Engines for Estimating Human Skill at Chess", Matej Guid, Ivan Bratko, 2011