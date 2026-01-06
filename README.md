# AI Rubik’s Cube Solver (2×2)

## Project Overview
This project implements an AI agent that learns to solve a **2×2 Rubik’s Cube from scratch using reinforcement learning**.  
The system is trained **without any hard-coded cube algorithms, heuristics, or human-designed solving strategies**, relying solely on environment interaction and reward feedback to discover solutions.

The project focuses on **environment design, reward engineering, and learning stability** for complex combinatorial problems with sparse terminal rewards.

---

## Project Purpose
The primary objective is to explore how reinforcement learning agents can acquire **spatial reasoning, reversible action planning, and long-horizon decision making** in a constrained deterministic environment.

The 2×2 Rubik’s Cube provides an ideal testbed due to:

- **8 corner cubies** with ~3.6 million reachable configurations  
- **Deterministic state transitions** — every action produces a predictable result  
- **Well-defined goal state** — a solved configuration is unambiguous  
- **Challenging planning horizon** — requires multi-step reasoning and backtracking  

---

## Learning Setup and Evolution

This project is intentionally iterative: the **environment interface** stays stable (reset/step), while the **learning formulation** (state encoding, action set, reward shaping, curriculum) evolves as experiments reveal limitations.

To make progress measurable and reproducible, each iteration is tracked as a “version” below.

---

### Environment Interface (Stable)

Regardless of the learning version, the environment exposes:

- `reset(scramble_len) -> state`
- `step(action) -> state, reward, done, info`

Where:
- `state` is the observation given to the agent
- `reward` is a shaped signal encouraging progress
- `done` indicates solved or max-moves reached
- `info` logs metrics (e.g., corner correctness, move count)

This separation lets the simulation remain correct while training logic changes independently.

---

## Formulation Versions

### V0 — Baseline Formulation (Initial Attempt)

**Goal:** Validate cube mechanics + RL pipeline end-to-end.

**Observation (state):**
- Raw sticker colors stored as a `6 × 4` array (`np.int` values in {0..5})
- Passed to the agent as a flattened vector of length 24

**Action space:**
- 18 moves: `{U, U', U2, D, D', D2, F, F', F2, B, B', B2, R, R', R2, L, L', L2}`

**Reward (initial):**
- Face-based “completion”:
  - Reward increased when a face became more uniform (more stickers matching a dominant color)
  - Bonus for fully uniform faces
  - Step penalty to discourage long solutions

**Outcome / why it stalled:**
- This reward created **false local optima**: states with visually uniform faces but incorrect cubie identities
- The agent learned “surface-level” improvements that didn’t reliably translate to solvability
- Moves like R and L', U and D', F and B' produce the same result logically, leading to an unecessarily complex action space
- Result: semi-consistent solves only on very short scrambles (≈ 2 moves)

---

### V1 — Cubie-Aligned Reward Shaping (Current Direction)

**Goal:** Align learning signal with real cube structure.

**Observation:**
- Still based on sticker colors, but evaluation uses **corner cubies** (sets of 3 stickers)

**Action space:**
- 9 moves (removed unecessary moves)

**Reward (improved):**
- Corner-based progress:
  - Reward tracks **correct corner cubies** (correct set of colors per corner)
  - Larger terminal reward for solved state
  - Small step penalty remains

**Why this is better:**
- Rubik’s Cube solvedness is defined by **correct pieces in correct locations and orientations**
- Corner correctness is a more faithful proxy than face color clustering
- Reduces reward hacking and improves generalization to deeper scrambles

---

### V3 — Curriculum Learning (Implemented / Iterating)

**Motivation:** Learning from deep scrambles from scratch is too sparse and unstable.

**Approach:**
- Start training at small scramble lengths (e.g., 2)
- Gradually increase to larger scrambles (e.g., 10) based on:
  - episode count schedule, or
  - success-rate thresholds

**Expected benefits:**
- Frequent early successes → usable learning signal
- Gradual scaling → transferable sub-policies and better convergence

---

## Last Updated
January 2025
