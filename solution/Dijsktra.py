import heapq as heap
from search.algorithms import State
from search.map import Map


def dijkstra_search(start, goal, map_instance):
    open_list = []  # Priority queue for open states
    closed_set = set()  # Set to store visited states
    expanded_nodes = 0  # Counter for the number of expanded nodes

    # Initialize the start state's g-value and cost
    start.set_g(0)
    start.set_cost(0)

    # Create a custom hashable representation of the start state
    start_key = (start.get_x(), start.get_y())

    # Push the start state into the open list
    heap.heappush(open_list, (start.get_cost(), start_key, start))

    while open_list:
        # Get the state with the lowest cost from the open list
        _, current_key, current_state = heap.heappop(open_list)
        expanded_nodes += 1

        # Check if the current state is the goal state
        if current_state == goal:
            return current_state.get_g(), expanded_nodes

        # Add the current state to the closed set
        closed_set.add(current_key)

        # Generate successor states and process them
        for successor in map_instance.successors(current_state):
            # Create a custom hashable representation of the successor state
            successor_key = (successor.get_x(), successor.get_y())

            # Skip states already in the closed set
            if successor_key in closed_set:
                continue

            # Calculate the tentative g-value for the successor
            tentative_g = current_state.get_g() + map_instance.cost(successor.get_x() - current_state.get_x(), successor.get_y() - current_state.get_y())

            # If the successor is not in the open list or has a better g-value, update it
            if not any(successor_key == key for _, key, _ in open_list) or tentative_g < successor.get_g():
                successor.set_g(tentative_g)
                successor.set_cost(tentative_g)

                # Push the successor into the open list
                heap.heappush(open_list, (successor.get_cost(), successor_key, successor))

    # If the open list is empty and no solution is found
    return -1, expanded_nodes