# Introduction

Official Elo ratings are a population-level ranking system, not a performance analyser, and do not incorporate engine-based analysis or move quality. Ratings are derived solely from game results against rated opponents according to the following formula:

$$
\text{New Rating} = \text{Old Rating} + K \cdot (\text{Actual Score} - \text{Expected Score})
$$

Where:

- Actual score = 1 (win), 0.5 (draw), 0 (loss)
- Expected score is calculated from the rating difference
- K controls how fast ratings move

Crucially, the rating system assumes, by design, that performance fluctuates (a player may have a "bad day", for instance) while underlying strength only changes slowly.

The models in this project instead use engine-evaluated accuracy as a proxy for ***playing strength***, enabling personal performance tracking independent of opponent ratings. They can legitimately be labelled *"a rating-like measure of how strong the play in a given game was, expressed on an Elo-like scale"*.

The differences between these models and the official Elo rating system are summarised below:

| Official Elo                            | Modelled Playing Strength            |
| --------------------------------------- | ------------------------------------ |
| Result-based                            | Move-quality-based                   |
| Relative to opponents                   | Relative to players own distribution |
| No engines                              | Engine-evaluated                     |
| Estimates long-term underlying strength | Measures immediate playing quality   |
| Population ranking                      | Personal performance tracking        |

The models are heuristic, inspired by community observations that *Average Centipawn Loss (ACPL)* may correlate with ***playing strength***.

Similar exponential relationships between ACPL and Elo have been discussed informally in chess communities (e.g. Lichess forums and engine analysis blogs). The specific formulation used here, including parameter selection and normalisation, is independently derived and calibrated using the author’s own game data.

The models are intended as an interpretive and comparative tool, not a replacement for official rating systems.

# Modelling Playing Strength

The intention is to build personal performance rating model based on *Average Centipawn Loss (ACPL)*, without relying on any official Elo rating. The core idea is to map how accurately a player played in a game (as measured by ACPL from a chess engine) onto a rating-like scale that is:

- Consistent across that players own games
- Comparable over time
- Independent of opponents’ ratings
- Robust to missing or unreliable Elo data

The result is intended to be a model that:

- Allows assignment of a personal performance rating
- On a stable, interpretable scale
- Suitable for trend analysis, comparisons, and visualisation

## Why Model Playing Strength?

If the aim is analysis of personal playing strength over time, ACPL alone has some drawbacks. It's engine dependent, making comparisons between engines difficult, and raw ACPL values are poorly suited to aggregation due to heavy-tailed distributions and non-linear relationships with playing strength.

In contrast, the playing strength models transform ACPL into a rating-like strength estimate, naturally compressing extreme values and making averaging a meaningful summary of typical performance.

The advantages of modelling playing strength are:

- A single, stable, engine-agnostic performance scale
- Meaningful aggregation and trend analysis over time
- Comparability across different analysis engines
- Sensitivity to short-term form and fatigue
- Separation of playing quality from game results
- Earlier detection of genuine improvement
- Explicit modelling of consistency and variability
- ... and, not least, the enjoyment of exploring the data more deeply!

## Key Assumptions

- Lower ACPL means stronger play  
- ACPL is engine-dependent, so:
  - Use a single engine first (single-engine notebook)
  - Normalise across engines (multi-engine notebook)
- The *shape* of the relationship matters more than the absolute scale

## The Single Engine Model

Playing strength, or performance, is modelled using an exponential decay function:

$$
\text{Strength}_{\text{est}}(a) = R_{\min} + (R_{\max} - R_{\min}) \cdot e^{-k \cdot (a - a_{\text{best}})}
$$

### Parameters

- a = ACPL for a given game
- a(best) = ACPL corresponding to the strongest games (typically the 5th percentile)
- R(max) = rating assigned to the strongest performances
- R(min) = rating assigned to the weakest performances
- k = decay constant controlling how quickly performance drops as ACPL increases

### Interpreting the Parameters

- R(max) sets the *ceiling* for personal performance scale  
- R(min) sets the *floor*  
- a(best) anchors the curve to the best play  
- k encodes the player consistency:
  - higher k - steeper drop-off (inconsistent performance)
  - lower k - gentler slope (stable performance)

The parameter k is derived directly from the spread of ACPL values and is inversely proportional to that spread:

$$
k \propto \frac{1}{a_\text{worst} - a_\text{best}}
$$

It controls the curvature and is an indicator of how “wide” the performance distribution is.

## Exponential Model

The relationship between ACPL and playing strength is strongly *non-linear*. A single extra centipawn of error does not have the same meaning everywhere on the scale:

- Increasing ACPL from 10 to 20 usually reflects a *large* drop in playing strength
- Increasing ACPL from 60 to 70 often reflects a much *smaller* difference

In other words, early increases in ACPL matter far more than later ones.

An exponential decay model captures this behaviour naturally.

### Intuition

The model assumes that each additional unit of ACPL causes a fixed percentage loss of effective playing strength, rather than a fixed absolute loss and this matches chess reality:

- Small inaccuracies at high levels are very costly  
- Once play becomes very inaccurate, additional mistakes change little  
- Strength decays quickly at first, then more slowly

### Mathematical Form

The exponential form of the model ensures that:

- Performance is bounded between R(min) and R(max)
- The curve is smooth
- The largest rating drops occur at low ACPL values
- Later ACPL increases have diminishing impact

### Why not linear?

A linear model would imply that every additional centipawn of error costs the *same* amount of strength but this is not consistent with observed play:

- Elite games cluster at very low ACPL
- Small errors at that level are, or can be, decisive
- Large ACPL values mostly reflect already-lost positions

## The Multi-Engine Model

The ACPL calculation uses CPL values from the move analysis from each engine. That CPL is calculated on an internal scale specific to the engine so the ACPL calculated from analyses completed by different engines are not directly comparable. To make them comparable, we first need to:

1. Select an ANCHOR engine
2. Calculate the mean (average, or typical) ACPL for that engine
3. Calculate the standard deviation (spread) of ACPL for that engine

The Z-score included in the player ACPL data frame indicates how good or bad a specific game was compared to what the engine used to analyse that game usually reports:

| Z-Score | Meaning                                    |
| ------- | ------------------------------------------ |
| 0       | An average game for the engine in question |
| +1      | 1 standard deviation worse than average    |
| -1      | 1 standard deviation better than average   |

The Z-scores are used to effectively "map" the ACPL calculated from an analysis completed by a different engine onto the same scale as the anchor engine:

$$
\text{ACPL}_{\text{engine}} = \mu_{\text{anchor}} + z \cdot \sigma_{\text{anchor}}
$$

This equation does the following:

1. Start at the anchor engine's mean
2. Move up or down by the number of standard deviations indicated by the Z-score
3. But measured in units of the anchor engine's standard deviation

## Handling Low ACPL - ACPL Floor

There are a number of scenarios that can result in excessively low ACPL:

| Scenario                                     | Impact on ACPL                                          |
| -------------------------------------------- | ------------------------------------------------------- |
| Opening theory / book lines                  | Many engine-equal moves, little ACPL accumulation       |
| Early opponent blunder                       | Game becomes easy; many moves are “equally winning”     |
| Large evaluation advantage                   | Engine tolerance rises once the position is clearly won |
| Short games                                  | Too few moves for errors to register meaningfully       |
| Forced lines / tactics                       | Limited choice keeps ACPL artificially low              |
| Simple conversions & tablebase-like endgames | Most moves score near-zero loss                         |
| Engine/config effects                        | Depth, time, or engine choice suppresses losses         |
| Dead or trivial positions                    | Symmetry, fortresses, or locked structures              |
| Statistical noise at low values              | Below ~5 ACPL, variance dominates signal                |

However, the exponential model is extremely sensitive to low ACPLs, with small changes in ACPL at the lower end of the scale causing disproportionate changes in performance rating. To mitigate against this, the model applies a floor based on the number of moves in the game to the ACPL values calculated from the analysis.

The floor should also be applied at the point where the performance rating is calculated for a given ACPL, for example using the *chessprf* application.