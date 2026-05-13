# The Torchbearer

**Student Name:** Nathan Meza
**Student ID:** 132001594
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  * A single shortest-path from S is not enough because the travel cost depends on which relic was visited last.

- **What decision remains after all inter-location costs are known:**
  * After all inter-locaiton costs are known, we must find the most optimal order in which to visit each relic.

- **Why this requires a search over orders (one sentence):**
  * We must search every possible order and select the one with the lowest total cost.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| _Start Node_ | _The route starts here and we need to find the shortest path to each relic and the exit_ |
| _Relic Node_ | _We need to find the shortest path from each relic to other relics and the exit_ |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary |
| What the keys represent | Source node and destination node |
| What the values represent | Minimum cost from source to destination |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Looking up on a dictionary results in constant time |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** _k+1_
- **Cost per run:** _O(m*logn)_
- **Total complexity:** _O(k\*m\*logn)_
- **Justification (one line):** _Running dijkstra for each k+1 nodes which is k relics and the start node,
                                 we get the total of their sum which is O((k+1)mlogn) giving us O(kmlogn)._

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  * When a node v is moved into S, the distance in dist[v] to that node from the source is already at its minimum.

- **For nodes not yet finalized (not in S):**
  * The best route found so far is stored in dist[u] and may the route may still be improved.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  * S is empty, so the invariant over finalized nodes holds true. dist[souce] = 0 and all other nodes
    have dist[u] = inf.

- **Maintenance : why finalizing the min-dist node is always correct:**
  * At each step, we get the unfinalized node with the smallest dist[u] and since travelling to a node
    that is not settled gives dist[w] >= dist[u], it cannot be lower than dist[u]. Therefore, the invariant
    is maintained.

- **Termination : what the invariant guarantees when the algorithm ends:**
  * When the algorithm ends, every node has been settled into S and the invariant states dist[v] is the shortest
    path to each reachable node v and every other node is unreachable. Thus, the invariant is true at termination.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

* This matters for the route planner because if we do not connect the correct distances to the correct routing decisions,
  the route planner may choose a route that is not actually optimal.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
