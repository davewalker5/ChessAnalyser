# ELO Modelling

The intention is to build **personal performance rating model** based on *Average Centipawn Loss (ACPL)*, without relying on any official Elo rating. The core idea is to map **how accurately a player played in a game** (as measured by ACPL from a chess engine) onto a **rating-like scale** that is:

- consistent across that players own games  
- comparable over time  
- independent of opponents’ ratings  
- robust to missing or unreliable Elo data  

The result is intended to be a model that:

- allows assignment of a **personal performance rating**
- on a stable, interpretable scale
- suitable for trend analysis, comparisons, and visualisation

## Acknowledgements and notes

This performance model is **heuristic**, inspired by community observations that *Average Centipawn Loss (ACPL)* may correlate with playing strength.

Similar exponential relationships between ACPL and Elo have been discussed informally in chess communities (e.g. Lichess forums and engine analysis blogs). The specific formulation used here, including parameter selection and normalisation, is independently derived and calibrated using the author’s own game data.

This model is intended as an **interpretive and comparative tool**, not a replacement for official rating systems.

## Key Assumptions

- Lower ACPL means stronger play  
- ACPL is engine-dependent, so:
  - Use a single engine first (this notebook)
  - Normalise across engines (multi-engine notebook)
- The *shape* of the relationship matters more than the absolute scale

## The Single Engine Model

Performance is modelled using an exponential decay function:

$$
\text{Elo}_{\text{est}}(a)
= R_{\min}
+ (R_{\max} - R_{\min})
\cdot e^{-k \cdot (a - a_{\text{best}})}
$$

### Parameters

- a = ACPL for a given game
- a(best) = ACPL corresponding to your strongest games (typically the 5th percentile)
- R(max) = rating assigned to your strongest performances
- R(min) = rating assigned to your weakest performances
- k = decay constant controlling how quickly performance drops as ACPL increases

### Interpreting the Parameters

- R(max) sets the *ceiling* for personal rating scale  
- R(min) sets the *floor*  
- a(best) anchors the curve to the best play  
- k encodes the player **consistency**:
  - higher k ⇒ steeper drop-off (inconsistent performance)
  - lower k ⇒ gentler slope (stable performance)

The parameter k is derived directly from the spread of ACPL values and does not require any Elo labels.

## Exponential Model

The relationship between **ACPL** and **playing strength** is strongly *non-linear*. A single extra centipawn of error does **not** have the same meaning everywhere on the scale:

- increasing ACPL from **10 to 20** usually reflects a *large* drop in playing strength
- increasing ACPL from **60 to 70** often reflects a much *smaller* difference

In other words, early increases in ACPL matter far more than later ones.

An **exponential decay model** captures this behaviour naturally.

### Intuition

The model assumes that each additional unit of ACPL causes a **fixed percentage loss** of effective playing strength, rather than a fixed absolute loss.

This matches chess reality:

- small inaccuracies at high levels are very costly  
- once play becomes very inaccurate, additional mistakes change little  
- strength decays quickly at first, then more slowly

### Mathematical Form

The exponential form of the model ensures that:

- performance is bounded between R(min) and R(max)
- the curve is smooth and monotonic
- the largest rating drops occur at low ACPL values
- later ACPL increases have diminishing impact

### Why not linear?

A linear model would imply that:

- every additional centipawn of error costs the *same* amount of strength

This is not consistent with observed play:

- elite games cluster at very low ACPL
- small errors at that level are decisive
- large ACPL values mostly reflect already-lost positions

The exponential form reflects this asymmetry without requiring any Elo labels.

### Practical benefits

- stable behaviour at extreme ACPL values  
- intuitive interpretation of the decay parameter k
- easy comparison across engines or normalised ACPL scales  
- robust performance estimation without opponent ratings

For these reasons, an exponential model provides a good balance between simplicity, interpretability, and empirical realism.
