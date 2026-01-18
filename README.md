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
- **Deterministic state transitions**: every action produces a predictable result  
- **Well-defined goal state**: a solved configuration is unambiguous  
- **Challenging planning horizon**: requires multi-step reasoning and backtracking  

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
**Next steps:**
- Redesign reward function to focus on actual cube pieces (cubies) rather than face colors
- Reduce action space to eliminate redundant moves
---

### V1 — Cubie-Aligned Reward Shaping

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
**Observations:**
- Model struggles with scrambles > 2 moves
- Single hidden layer may have insufficient capacity to capture complex state-action relationships
- Learning plateaus after initial success on 2-move scrambles

**Next steps:**
- Increase model capacity by adding more hidden layers
- Experiment with deeper architectures to learn hierarchical representations
---

### V2 — Enhanced Architecture

**Motivation:** Increase model capacity to learn more complex patterns and relationships between cube states.

**Key Changes:**
- **Neural network architecture:**
  - Added second hidden layer with Rectified Linear Unit activation
  - Architecture: Input (24) → Hidden (256, ReLU) → Hidden (256, ReLU) → Output (9)
  - Increased depth helps capture hierarchical state representations

**Results:**
- **3-move scrambles:** Consistently solved after a few thousand training iterations
- Shows improved learning stability and generalization compared to V1
- The additional layer enables the network to learn more sophisticated feature combinations

**Observations:**
- The deeper architecture better captures the spatial relationships between cubies
- Training convergence is more stable with proper reward shaping from V1
- Still struggles with scrambles beyond 3 moves
- Learning signal becomes sparse for deeper scrambles, leading to slow or stalled progress

**Next steps:**
- Implement target networks to stabilize training.

---

### V3 — Stability + Representation Upgrades (Implemented)

**Motivation:** Improve training stability and state expressiveness to handle deeper scrambles.

**Key Changes:**
- **Target Network (DQN):** Added a separate target network updated every ~1000 training steps to stabilize Bellman targets. This decouples current Q estimates from target Q estimates and reduces non-stationary targets during optimization. 
- **One-Hot State Encoding (24 → 144):** Before, each sticker was stored as a number from 0 to 5, which accidentally makes the model treat colors like they have an order (ex. “5 is bigger than 1”).
Now, each sticker is represented as a 6-value one-hot vector, so the model treats colors as categories instead of numbers. The full cube state becomes a 144-dimensional input.
- **Correct Corners Metric (with Orientation):** The correctness check now counts corners as correct only when both cubie identity and orientation match the goal (corner orientation was mistakenly not considered during previous implementation). This prevents the agent from getting credit for corners that have the right colors but are still twisted wrong.
- **Raised the discount factor to 0.99 (from 0.90):** This encourages the model to focus less on short-term gains and more on future outcomes, improving learning on 4+ move scrambles.
 
**Architecture (unchanged):**
- Input: 144
- Hidden: 256 (ReLU)
- Hidden: 256 (ReLU)
- Output: 9 actions

**Results:**
- 3 move scrambles train significantly faster than previous iteration.
- The agent is now able to solve **4-move scrambles semi-consistently** under the current training setup.
- Training curves are less noisy; target-network updates help reduce oscillations in value estimates.

**Next steps:**
- Implement curriculum learning to gradually increase difficulty
- Start with easy scrambles and progressively move to harder ones as agent improves

---

### V4 — Curriculum Learning (Implemented / Iterating)

**Motivation:** Learning from deep scrambles from scratch is too sparse and unstable.

**Approach:**
- Start training at small scramble lengths (e.g., 2)
- Gradually increase to larger scrambles (e.g., 10) based on:
  - success-rate thresholds

**Expected benefits:**
- Frequent early successes → usable learning signal
- Gradual scaling → transferable sub-policies and better convergence
- Combined with V2 architecture for optimal performance

**Current Status:**
- Implementation in progress
- Testing different curriculum schedules and success thresholds
- Goal: Achieve consistent solving of 4+ move scrambles

**Anticipated challenges:**
- Finding optimal progression rate between scramble difficulties
- Preventing catastrophic forgetting when transitioning to harder scrambles
- Balancing exploration vs exploitation as complexity increases

**Next steps:**
- Fine-tune curriculum progression thresholds
- Experiment with experience replay buffer strategies
- Consider adding memory mechanisms or target networks for stability

## Last Updated
January 17, 2026