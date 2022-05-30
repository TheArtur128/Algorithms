from math import inf as infinity
from typing import Iterable

from structures.graphs import GraphNode, GraphNodePath
from structures.collections_ import Queue


def binary_search_index_of(number: int, sorted_array: Iterable[int,]) -> int:
    """
    Binary search for the index of a number in a sorted collection. At each iteration,
    determines the approximate habitat zone of the number in the list by comparing
    the number with the average number in the collection and choosing a larger or
    smaller zone depending on the comparison answer, until the search zone narrows
    down to one number. Throws an error if the number is not in the collection.
    O(log n) speed. Analogs: list.index(number).
    """

    min, max = 0, len(sorted_array) - 1

    while min != max and min + 1 != max:
        midle = (min + max) // 2

        if max - 1 == min:
            break

        if number == sorted_array[midle]:
            return midle

        elif number > sorted_array[midle]:
            min = midle

        elif number < sorted_array[midle]:
            max = midle

    raise ValueError (f"{number} is not in list")


def is_item_in(array: Iterable, item: any) -> bool:
    """
    Looking for an answer to the question about the presence of an element in
    the collection and its subcollections. O(n) speed. Analogs: item in list.
    """

    boxes = []
    for object_ in array:
        if object_ == item:
            return True
        elif type(object_) is list:
            boxes.append(object_)

    return any(map(lambda box: is_item_in(box, item), boxes))


def get_biggest_from(numbers: Iterable[int,]) -> int:
    """Finder of the biggest number in the collection. O(n) speed. Analogs: max(numbers)."""

    bigest = -infinity
    for number in numbers:
        if bigest < number:
            bigest = number

    return bigest


def breadth_first_search(starting_node_graph: GraphNode, final_node_graph: GraphNode) -> GraphNodePath | None:
    """
    Searches for a path from one graph node to another, spending the minimum number of steps.
    Returns None if no path exists, otherwise abstract graph of the path. O(n) speed.
    """

    paths_to_nodes = Queue(map(lambda node: GraphNodePath(starting_node_graph, [node.data]), starting_node_graph.nodes))

    while paths_to_nodes:
        active_path = paths_to_nodes.get()

        if active_path.final_node is final_node_graph:
            return active_path
        else:
            paths_to_nodes.add_from(
                map(
                    lambda next_node: GraphNodePath(starting_node_graph, [*active_path.intermediate_keys, next_node.data]),
                    active_path.final_node.nodes
                )
            )
