from typing import Iterable, Callable
from dataclasses import dataclass


class _ConditionalErrorCauser:
    def __init__(self, condition: Callable, error: Exception):
        self.condition = condition
        self.error = error

    def __call__(self, *args, **kwargs) -> None:
        if self.condition(*args, **kwargs):
            raise self.error


class GraphNode:
    __not_graph_error_causer = _ConditionalErrorCauser(
        lambda graph_node: not isinstance(graph_node, GraphNode),
        AttributeError("It is not a graph node")
    )

    def __init__(self, data: any, next_nodes: Iterable = tuple()) -> None:
        self.data = data
        self.__next_nodes = set(next_nodes)

    def __repr__(self) -> str:
        return f"{self.data}{'.' if not self.__next_nodes else ''}{self.__next_nodes}"

    def __getitem__(self, data_of_next_node: any):
        for node in self.__next_nodes:
            if node.data == data_of_next_node:
                return node

        raise KeyError(data_of_next_node)

    @property
    def nodes(self) -> set:
        return set(self.__next_nodes)

    def add_node(self, graph_node) -> None:
        self.__not_graph_error_causer(graph_node)
        self.__next_nodes.add(graph_node)

    def cut_node(self, graph_node) -> None:
        self.__not_graph_error_causer(graph_node)
        self.__next_nodes.remove(graph_node)


@dataclass(frozen=True)
class GraphNodePath:
    starting_node: GraphNode
    keys_to_final_node: Iterable

    def __post_init__(self) -> None:
        active_node = self.starting_node

        for intermediate_key in self.keys_to_final_node:
            if not any(map(lambda node: node.data == intermediate_key, active_node.nodes)):
                raise AttributeError(f"{active_node} has no key {intermediate_key}")

            active_node = active_node[intermediate_key]


    def __repr__(self) -> str:
        return f"{self.starting_node.data} -> {' -> '.join(map(lambda key: str(key), self.keys_to_final_node))}"

    @property
    def nodes(self):
        active_node = self.starting_node

        yield active_node

        for intermediate_key in self.keys_to_final_node:
            active_node = active_node[intermediate_key]
            yield active_node

    @property
    def final_node(self) -> GraphNode:
        return tuple(self.nodes)[-1]
