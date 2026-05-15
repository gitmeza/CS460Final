# The Torchbearer

**Student Name:** Nathan Meza
**Student ID:** 132001594
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  * A single shortest-path from S is not enough because the travel cost depends on which relic was visited last.

- **What decision remains after all inter-location costs are known:**
  * After all inter-locaiton costs are known, we must find the most optimal order in which to visit each relic.

- **Why this requires a search over orders (one sentence):**
  * We must search every possible order and select the one with the lowest total cost.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| _Start Node_ | _The route starts here and we need to find the shortest path to each relic and the exit_ |
| _Relic Node_ | _We need to find the shortest path from each relic to other relics and the exit_ |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary |
| What the keys represent | Source node and destination node |
| What the values represent | Minimum cost from source to destination |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Looking up on a dictionary results in constant time |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** _k+1_
- **Cost per run:** _O(m*logn)_
- **Total complexity:** _O(k\*m\*logn)_
- **Justification (one line):** _Running dijkstra for each k+1 nodes which is k relics and the start node,
                                 we get the total of their sum which is O((k+1)mlogn) giving us O(kmlogn)._

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  * When a node v is moved into S, the distance in dist[v] to that node from the source is already at its minimum.

- **For nodes not yet finalized (not in S):**
  * The best route found so far is stored in dist[u] and may the route may still be improved.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  * S is empty, so the invariant over finalized nodes holds true. dist[souce] = 0 and all other nodes
    have dist[u] = inf.

- **Maintenance : why finalizing the min-dist node is always correct:**
  * At each step, we get the unfinalized node with the smallest dist[u] and since travelling to a node
    that is not settled gives dist[w] >= dist[u], adding more nonnegative edges cannot be lower than dist[u].
    Therefore, the invariant is maintained.

- **Termination : what the invariant guarantees when the algorithm ends:**
  * When the algorithm ends, every node has been settled into S and the invariant states dist[v] is the shortest
    path to each reachable node v and every other node is unreachable. Thus, the invariant is true at termination.

### Part 3c: Why This Matters for the Route Planner

* This matters for the route planner because if we do not connect the correct distances to the correct routing decisions,
  the route planner may choose a route that is not actually optimal.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** If we visit the closest relic first, then greedy only takes the minimum cost at each step without
  considering how choosing an alternate relic could lead to a better solution.
- **Counter-example setup:** Suppose S->B costs 4, S->C costs 1, S->D costs 2, B->C costs 100, B->D costs 1, B->T costs 1, C->B costs 1,
  C->D costs 100, C->T costs 1, D->B costs 1, D->C costs 1, and D->T costs 100.
- **What greedy picks:** Greedy would go to C first, S->C->B->D->T so total cost is 103.
- **What optimal picks:** Optimal picks B first, S->B->D->C->T so total cost is 7.
- **Why greedy loses:** Greedy loses because it prioritizes the cheapest path first, which ends up hurting the entire route since T becomes
  expensive with this choice.

### What the Algorithm Must Explore

- The algorithm must explore every possible order of traversal through the relics to determine which order is the most optimal.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | currently occupied node |
| Relics already collected | relics_remaining | set[node] | set of relics remaining |
| Fuel cost so far | cost_so_far | float | cost accumulated so far on route |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | a hash set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | a hash set allows for fast lookups and giving O(1) time complexity |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** _O(k!)_
- **Why:** _In the worst case, the algorithm tries every possible order of k relic nodes giving us O(k!)._

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
