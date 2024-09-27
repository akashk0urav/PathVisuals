import heapq
from django.http import JsonResponse
from django.shortcuts import render

# Dijkstra's algorithm for 2D grid
def dijkstra(grid, start, end):
    # print("hello this is the dijkstra algo")
    rows, cols = len(grid), len(grid[0])
    pq = [(0, tuple(start))]  # Priority queue stores (distance, node) using tuples
    distances = {tuple(start): 0}  # Use tuple for start as key
    predecessors = {tuple(start): None}  # Track the path using tuples

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        current_x, current_y = current_node

        if current_node == tuple(end):  # End point also as tuple
            # Trace the path back using predecessors
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]
            path.reverse()
            return path

        for direction in directions:
            neighbor_x = current_x + direction[0]
            neighbor_y = current_y + direction[1]

            if 0 <= neighbor_x < rows and 0 <= neighbor_y < cols and grid[neighbor_x][neighbor_y] == 0:  # Not an obstacle
                neighbor = (neighbor_x, neighbor_y)  # Store neighbors as tuples
                new_distance = current_distance + 1

                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

    return []  # No path found

# A* algorithm for 2D grid
def a_star(grid, start, end):
    # print("hello this is a_star algo")
    rows, cols = len(grid), len(grid[0])
    pq = [(0, tuple(start))]  # Priority queue stores (f_score, node)
    g_scores = {tuple(start): 0}  # Actual cost from start to node
    f_scores = {tuple(start): heuristic(start, end)}  # Estimated total cost from start to end
    predecessors = {tuple(start): None}  # Track the path using tuples

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    while pq:
        current_f_score, current_node = heapq.heappop(pq)
        current_x, current_y = current_node

        if current_node == tuple(end):  # End point also as tuple
            # Trace the path back using predecessors
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]
            path.reverse()
            return path

        for direction in directions:
            neighbor_x = current_x + direction[0]
            neighbor_y = current_y + direction[1]

            if 0 <= neighbor_x < rows and 0 <= neighbor_y < cols and grid[neighbor_x][neighbor_y] == 0:  # Not an obstacle
                neighbor = (neighbor_x, neighbor_y)  # Store neighbors as tuples
                tentative_g_score = g_scores[current_node] + 1  # Assuming uniform cost for each step

                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    predecessors[neighbor] = current_node
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + heuristic(neighbor, end)

                    if neighbor not in [i[1] for i in pq]:  # If neighbor is not already in the priority queue
                        heapq.heappush(pq, (f_scores[neighbor], neighbor))

    return []  # No path found

# Heuristic function for A*
def heuristic(node, end):
    # Using Manhattan distance as heuristic
    return abs(node[0] - end[0]) + abs(node[1] - end[1])

# API view for handling pathfinding requests
def find_path(request):
    if request.method == 'POST':
        print("POST Request received")
        grid = eval(request.POST.get('grid'))  # 2D grid as a list of lists
        start = eval(request.POST.get('start'))  # Start coordinate (x, y)
        end = eval(request.POST.get('end'))  # End coordinate (x, y)
        algorithm = request.POST.get('algorithm')  # Get selected algorithm

        if algorithm == 'dijkstra':
            path = dijkstra(grid, start, end)
        elif algorithm == 'a-star':
            path = a_star(grid, start, end)
        else:
            return JsonResponse({'error': 'Invalid algorithm selected'}, status=400)

        return JsonResponse({'path': path})

    return render(request, 'grid.html')
