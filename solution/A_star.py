import heapq
import math


def octile_distance(x1, y1, x2, y2):
    """
    Calculate the Octile distance heuristic between two points (x1, y1) and (x2, y2).
    """
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    return 1.5 * min(delta_x, delta_y) + abs(delta_x - delta_y)

def astar_search(start, goal, map_instance):
    open_list = []  # Priority queue for open states
    closed_set = {}  # Dictionary to store visited states
    expanded_nodes = 0  # Counter for the number of expanded nodes

    # Initialize the start state's g-value and cost
    start.set_g(0)
    start.set_cost(octile_distance(start.get_x(), start.get_y(), goal.get_x(), goal.get_y()))

    # Create a custom hashable representation of the start state
    start_key = (start.get_x(), start.get_y())

    # Push the start state into the open list
    heapq.heappush(open_list, (start.get_cost(), start_key, start))

    while open_list:
        _, _, current_state = heapq.heappop(open_list)
        expanded_nodes += 1

        # Check if the current state is the goal state
        if current_state == goal:
            return current_state.get_g(), expanded_nodes

        # Add the current state to the closed set
        closed_set[(current_state.get_x(), current_state.get_y())] = current_state

        for successor in map_instance.successors(current_state):
            successor_key = (successor.get_x(), successor.get_y())

            # Check if the successor is in the closed set
            if successor_key in closed_set:
                continue

            tentative_g = current_state.get_g() + map_instance.cost(successor.get_x() - current_state.get_x(), successor.get_y() - current_state.get_y())
            h_value = octile_distance(successor.get_x(), successor.get_y(), goal.get_x(), goal.get_y())

            # Calculate the new cost of the successor
            successor_cost = tentative_g + h_value

            # Check if the successor is in the open list with a higher cost
            found = False
            for i, (_, _, s) in enumerate(open_list):
                if s == successor and successor_cost >= s.get_cost():
                    found = True
                    break

            if not found:
                successor.set_g(tentative_g)
                successor.set_cost(successor_cost)
                heapq.heappush(open_list, (successor_cost, successor_key, successor))
            

    return -1, expanded_nodes
