import pygame
from typing import List, Dict, Tuple, Optional
from pygame import*
from queue import PriorityQueue
from cell import Cell
import heapq
from constants import*


class PathfindingRes:
    def __init__(self):
        self.path: List[Cell] = []
        self.affected_nodes: set[Cell] = set({})


def heuristic(node: Cell, goal: Cell) -> int:
    # Calculate the Manhattan distance between two nodes
    return abs(node.col - goal.col) + abs(node.row - goal.row)


def astar(start: Cell, goal: Cell) -> PathfindingRes:
    # Initialize the open and closed sets
    open_set: List[Tuple[int, Cell]] = []
    closed_set: set[Cell] = set()

    # store pathfinding result
    res = PathfindingRes()

    # Create a dictionary to store the g-score for each node
    g_scores: Dict[Cell, int] = {start: 0}

    # Create a dictionary to store the parent node for each node
    parents: Dict[Cell, Optional[Cell]] = {start: None}

    # Push the start node into the open set with a priority of 0
    heapq.heappush(open_set, (0, start))

    while open_set:
        # Pop the node with the lowest f-score from the open set
        current = heapq.heappop(open_set)[1]

        # Check if the current node is the goal node
        if current == goal:
            # Reconstruct the path from the goal node to the start node
            path = []
            while current:
                path.append(current)
                current = parents[current]
            res.affected_nodes = g_scores.keys()  # Return the reversed path
            res.path = path
            return res

        # Add the current node to the closed set
        closed_set.add(current)

        # Explore the neighboring nodes
        for neighbor in current.neighbors:
            # Calculate the g-score for the neighbor
            g_score = g_scores[current] + 1

            if neighbor not in g_scores or g_score < g_scores[neighbor]:
                # Update the g-score and parent for the neighbor
                g_scores[neighbor] = g_score
                parents[neighbor] = current

                # Calculate the f-score for the neighbor
                f_score = g_score + heuristic(neighbor, goal)

                # Push the neighbor into the open set with the calculated f-score
                heapq.heappush(open_set, (f_score, neighbor))

    # If the open set is empty and the goal has not been found, there is no path
    return res


def dfs_path(start: Cell, goal: Cell) -> PathfindingRes:
    res = PathfindingRes()
    stack: List[Tuple[Cell, List[Cell]]] = [(start, [start])]  # Stack elements are tuples of (current node, path)

    while stack:
        node, path = stack.pop()

        if node not in res.affected_nodes:
            res.affected_nodes.add(node)

            if node == goal:
                res.path = path
                return res  # Return the path if the goal is reached

            for neighbor in node.neighbors:
                if neighbor not in res.affected_nodes:
                    stack.append((neighbor, path + [neighbor]))

    return res


def bfs_path(start: Cell, goal: Cell) -> PathfindingRes:
    res = PathfindingRes()
    paths: dict[Cell, list[Cell]] = {start: [start]}
    while paths:
        new_paths: dict[Cell, list[Cell]] = {}
        for node in paths:
            path = paths[node]
            res.affected_nodes.add(node)
            if node == goal:
                res.path = path
                return res
            for neighbor in node.neighbors:
                if neighbor in res.affected_nodes:
                    continue
                neighbor_path = path + [neighbor]
                new_paths[neighbor] = neighbor_path
        paths = new_paths
    return res
