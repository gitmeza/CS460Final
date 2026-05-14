"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: ___________________________
Student ID:   ___________________________

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    
    TODO
    """
    return( "Why a single shortest-path run from S is not enough:\n"
        "A single shortest-path from S is not enough because the travel cost depends on which relic was visited last.\n"
        "What decision remains after all inter-location costs are known:\n"
        "After all inter-locaiton costs are known, we must find the most optimal order in which to visit each relic.\n"
        "Why this requires a search over orders (one sentence):\n"
        "We must search every possible order and select the one with the lowest total cost.\n"
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    TODO
    """
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    TODO
    """
    # Initialise every distance to infinity, source costs 0
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
 
    heap = [(0, source)]
 
    # Track which nodes have been settled
    settled = set()
 
    while heap:
        current_dist, u = heapq.heappop(heap)
 
        if u in settled:
            continue
        settled.add(u)
 
        # Check each outgoing edge from u
        for v, weight in graph[u]:
            candidate = current_dist + weight
            if candidate < dist.get(v, float('inf')):
                dist[v] = candidate
                heapq.heappush(heap, (candidate, v))
 
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    TODO
    """
    dist_table = {}
    for source in select_sources(spawn, relics, exit_node):
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    return(
        "Part 3: Algorithm Correctness\n"
        "Part 3a: What the Invariant Means\n"
        "For nodes already finalized (in S):\n"
        "When a node v is moved into S, the distance in dist[v] to that node from the source is already at its minimum.\n\n"
        
        "For nodes not yet finalized (not in S):\n"
        "The best route found so far is stored in dist[u] and may the route may still be improved.\n\n"

        "Part 3b: Why Each Phase Holds\n"
        "Initialization : why the invariant holds before iteration 1:\n"
        "S is empty, so the invariant over finalized nodes holds true. dist[souce] = 0 and all other nodes have dist[u] = inf.\n\n"

        "Maintenance : why finalizing the min-dist node is always correct:\n"
        "At each step, we get the unfinalized node with the smallest dist[u] and since travelling to a node that is not settled gives dist[w] >= dist[u], it cannot be lower than dist[u]. Therefore, the invariant is maintained.\n\n"

        "Termination : what the invariant guarantees when the algorithm ends:\n"
        "When the algorithm ends, every node has been settled into S and the invariant states dist[v] is the shortest path to each reachable node v and every other node is unreachable. Thus, the invariant is true at termination.\n\n"

        "Part 3c: Why This Matters for the Route Planner\n"
        "This matters for the route planner because if we do not connect the correct distances to the correct routing decisions, the route planner may choose a route that is not actually optimal.\n"
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return(
        "Part 4: Search Design\n"
        "Why Greedy Fails\n"
        "The failure mode: If we visit the closest relic first, then greedy only takes the minimum cost at each step without considering how choosing an alternate relic could lead to a better solution.\n\n"
        
        "Counter-example setup: Suppose S->B costs 4, S->C costs 1, S->D costs 2, B->C costs 100, B->D costs 1, B->T costs 1, C->B costs 1, C->D costs 100, C->T costs 1, D->B costs 1, D->C costs 1, and D->T costs 100.\n\n"
        
        "What greedy picks: Greedy would go to C first, S->C->B->D->T so total cost is 103.\n\n"
        
        "What optimal picks: Optimal picks B first, S->B->D->C->T so total cost is 7.\n\n"
        
        "Why greedy loses: Greedy loses because it prioritizes the cheapest path first, which ends up hurting the entire route since T becomes expensive with this choice.\n\n"
        
        "What the Algorithm Must Explore\n"
        "The algorithm must explore every possible order of traversal through the relics to determine which order is the most optimal.\n"
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    # No more relics, so exit
    if not relics:
        direct = dist_table.get(spawn, {}).get(exit_node, float('inf'))
        if direct < float('inf'):
            return (direct, [])
        return (float('inf'), [])
 
    # Best so far
    best = [float('inf'), []]
 
    relics_remaining = set(relics)
 
    _explore(
        dist_table=dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=[],
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best
    )
 
    if best[0] == float('inf'):
        return (float('inf'), [])
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    
    # If the cost so far is more than or equal to the best solution, then we prune.
    # This is safe because we are not going to miss out on a better solution by pruning 
    # since the cost is the same or worse than the best solution.
    if cost_so_far >= best[0]:
        return

    # If the cost so far plus the cheapest cost from the next relic to the exit 
    # is more than or equal to the best solution, then we also prune.
    # This is safe because we are pruning a route that doesn't beat the best solution.
    if relics_remaining:
        min_additional = float('inf')
        src_dist = dist_table.get(current_loc, {})
        for r in relics_remaining:
            # Cost from current position to relic r
            to_r = src_dist.get(r, float('inf'))
            # Cheapest cost from relic r to the exit
            from_r = dist_table.get(r, {}).get(exit_node, float('inf'))
            leg = to_r + from_r
            if leg < min_additional:
                min_additional = leg
        if cost_so_far + min_additional >= best[0]:
            return

    if not relics_remaining:
        cost_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total = cost_so_far + cost_to_exit
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return

    src_dist = dist_table.get(current_loc, {})
    for next_relic in list(relics_remaining):
        travel_cost = src_dist.get(next_relic, float('inf'))
        if travel_cost == float('inf'):
            # If next relic is unreachable, then skip
            continue
 
        new_cost = cost_so_far + travel_cost
        relics_remaining.remove(next_relic)
        relics_visited_order.append(next_relic)
 
        _explore(
            dist_table=dist_table,
            current_loc=next_relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=new_cost,
            exit_node=exit_node,
            best=best
        )

        relics_visited_order.pop()
        relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
