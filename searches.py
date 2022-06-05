from math import inf as infinity
from typing import Iterable, Callable

from structures.graphs import AbstractGraphNode, GraphNode, HashGraphNode, GraphPath
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


def breadth_first_search(starting_node_graph: AbstractGraphNode, final_node_graph: AbstractGraphNode) -> GraphPath | None:
    """
    Searches for a path from one graph node to another, spending the minimum number of steps.
    Returns None if no path exists, otherwise abstract graph of the path. O(n) speed.
    """

    paths_to_nodes = Queue(map(lambda node: GraphPath(starting_node_graph, [node.data]), starting_node_graph.nodes))

    while paths_to_nodes:
        active_path = paths_to_nodes.get()

        if active_path.final_node is final_node_graph:
            return active_path
        else:
            paths_to_nodes.add_from(
                map(
                    lambda next_node: GraphPath(starting_node_graph, [*active_path.intermediate_keys, next_node.data]),
                    active_path.final_node.nodes
                )
            )


def get_optinal_paths_to_graph_nodes(
    starting_graph_node: GraphNode,
    path_comparison_function: Callable | None = None,
) -> dict[HashGraphNode, GraphPath]:
    """
    Finds and returns optimal paths for all nodes of the abstract graph. Determines
    the optimal path by input function path_comparison_function, which has two
    input arguments leading to the same graph node. By default,
    path_comparison_function operates on paths consisting of HashGraphNodes that
    store numbers as intermediate data and when comparing two paths, returns the
    path that had a smaller sum stored in the intermediate values of its nodes,
    than the other path. Uses Dijkstra's algorithm as a finder. O(n) speed.
    """

    if not path_comparison_function:
        path_comparison_function = (
            lambda first_path, second_path:
                first_path if sum(first_path.get_all_intermediate_data()) < sum(second_path.get_all_intermediate_data()) else second_path
            )

    shortest_path_to_node = dict()
    paths_to_check = Queue([GraphPath(starting_graph_node, tuple())])

    while paths_to_check:
        update_branch = True
        active_path = paths_to_check.get()

        if active_path.final_node in shortest_path_to_node.keys():
            chosen_path = path_comparison_function(
                shortest_path_to_node[active_path.final_node],
                active_path
            )

            update_branch = chosen_path is active_path
            shortest_path_to_node[active_path.final_node] = chosen_path
        else:
            shortest_path_to_node[active_path.final_node] = active_path

        if update_branch:
            paths_to_check.add_from(
                map(
                    lambda next_node: GraphPath(starting_graph_node, [*active_path.intermediate_keys, next_node.data]),
                    active_path.final_node.nodes
                )
            )

    return shortest_path_to_node


def choose_items_from(
    items: Iterable,
    sorted_function: Callable,
    is_choice_correct: Callable
) -> list:
    """
    Returns a filtered list of the input iterable objects and uses the greedy
    algorithm as a filterer. Sorts the input collection using the input function
    sorted_function returning the sorted collection, and selects the appropriate
    objects starting from the first one, looking at the binary return result of
    the input is_choice_correct function, which takes as input a tuple of already
    selected objects and a new object. O(n*c + s) speed, where "n" is the number
    of elements, "c" is the speed of the input function is_choice_correct and "s"
    is the speed of the also input function sorted_function.
    """

    items_to_choose = Queue(sorted_function(items))
    chosen_items = list()

    while items_to_choose:
        select_item = items_to_choose.get()

        if is_choice_correct((*chosen_items, select_item)):
            chosen_items.append(select_item)

    return chosen_items
