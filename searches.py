from math import inf as infinity, ceil, sqrt
from typing import Iterable, Callable
from collections import OrderedDict

from structures.graphs import AbstractGraphNode, GraphNode, HashGraphNode, GraphPath
from structures.collections_ import Queue, ItemDescription, DistanceToItem
from sorting import qsort


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


def choose_maximum_items_from(
    items: set,
    cost_ceiling: int,
    get_cost_by_item: Callable,
    get_importance_index_by_item: Callable
) -> ItemDescription:
    """
    Selects the most valuable sequence of input items argument, not exceeding the
    maximum cost from the input cost_ceiling argument, using dynamic programming.

    Determines each item's cost and importance index using the input hash
    functions get_cost_by_item and get_importance_index_by_item.

    O(n*(c + i + l/m)) speed, where "c" is get_cost_by_item speed, "i" is
    get_importance_index_by_item speed, "l" is cost_ceiling and "m" is minimum
    cost given by get_cost_by_item.
    """

    base_item_decriptions = [
        ItemDescription(
            (item,),
            get_cost_by_item(item),
            get_importance_index_by_item(item)
        )
        for item in items
    ]

    minimal_cost = min(map(lambda decription: decription.cost, base_item_decriptions))
    available_costs = [i * minimal_cost for i in range(1, ceil(cost_ceiling / minimal_cost) + 1)]

    table = OrderedDict()

    for base_decription_index, base_decription in enumerate(base_item_decriptions):
        table[base_decription] = list()

        for available_cost_index, available_cost in enumerate(available_costs):
            missing_cost = available_cost - (base_decription.cost if base_decription.cost != infinity else 0)

            if missing_cost >= 0:
                best_missing_decription = ItemDescription.choise_optimal_description(
                    sum(
                        map(
                            lambda table_item: table_item[1],
                            filter(
                                lambda table_item: not table_item[0] is base_decription,
                                table.items()
                            )
                        ),
                        list()
                    ),
                    missing_cost,
                    ItemDescription.get_worst_example()
                )

                completed_decription = base_decription + best_missing_decription
            else:
                 completed_decription = ItemDescription.get_worst_example()

            previous = (
                tuple(table.items())[base_decription_index - 1][1][available_cost_index]
                if base_decription_index - 1 >= 0 else ItemDescription.get_worst_example()
            )

            table[base_decription].append(
                ItemDescription.choise_optimal_description(
                    (completed_decription, previous),
                    available_cost,
                    ItemDescription.get_worst_example()
                )
            )

    return tuple(table.items())[-1][1][-1]


def get_items_by_coordinates_from(
    items: Iterable,
    get_coordinates_by_item: Callable,
    maximum_number_of_items: int = infinity,
) -> list[DistanceToItem,]:
    """
    Sets the coordinates for the input items by the input get_coordinates_by_item
    function and returns the items with their distance away from zero.
    max_number_of_items is an argument that sets the number of items returned.

    O(n*g*q) speed, where g is speed of the input function get_coordinates_by_item,
    q is the speed of the qsort function (O(n) speed).

    Can be used as K-Nearest Neighbor algorithm (Used only for it).
    """

    items_by_distance = qsort(
        tuple(map(
            lambda item:
                DistanceToItem(
                    item,
                    sqrt(sum(map(lambda coordinate: coordinate**2, get_coordinates_by_item(item))))
                ),
            items
        )),
        lambda first, second: "middle" if first.distance == second.distance else first.distance > second.distance
    )

    return items_by_distance[:maximum_number_of_items] if len(items_by_distance) > maximum_number_of_items else items_by_distance
