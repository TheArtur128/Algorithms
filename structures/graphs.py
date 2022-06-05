from typing import Iterable, Callable
from abc import ABC, abstractmethod

from errors import NoGraphNodeReference, NoNextGraphNode


class AbstractGraphNode(ABC):
    """
    Abstract class of a part of an imaginary graph. Stores any data and links to
    other parts of the graph and they can be obtained by referring to the node
    with the key as their data. Preserves neighboring graph nodes and leaves
    persistence implementation to descendants.
    """

    def __init__(self, data: any) -> None:
        self.data = data

    def __repr__(self) -> str:
        return "{class_name}(main_data={main_data}, nodes_data={nodes_data})".format(
            class_name=self.__class__.__name__,
            main_data=self.data,
            nodes_data=tuple(map(lambda node: node.data, self.nodes))
        )

    def __getitem__(self, node_data: any):
        for node in self.nodes:
            if node.data == node_data:
                return node

        raise NoGraphNodeReference(node=self, data=node_data)

    @property
    @abstractmethod
    def nodes(self) -> frozenset:
        pass

    @abstractmethod
    def add_node(self, graph_node) -> None:
        pass

    @abstractmethod
    def cut_node(self, graph_node) -> None:
        pass


class GraphNode(AbstractGraphNode):
    """Class of a typical node of a typical graph."""

    def __init__(self, data: any, next_nodes: Iterable[AbstractGraphNode,] = tuple()) -> None:
        super().__init__(data)
        self.__nodes = set(next_nodes)

    @property
    def nodes(self) -> frozenset:
        return frozenset(self.__nodes)

    def add_node(self, graph_node: AbstractGraphNode) -> None:
        self.__nodes.add(graph_node)

    def cut_node(self, graph_node: AbstractGraphNode) -> None:
        self.__nodes.remove(graph_node)


class HashGraphNode(AbstractGraphNode):
    """
    When saving a node, it also saves additional information associated with
    this saved node.
    """

    def __init__(self, data: any, node_data: dict[AbstractGraphNode, any] = dict()) -> None:
        super().__init__(data)
        self.__nodes = dict(node_data)

    @property
    def nodes(self) -> frozenset:
        return frozenset(self.__nodes.keys())

    def get_intermediate_data_from(self, graph_node: AbstractGraphNode) -> any:
        return self.__nodes[graph_node]

    def add_node(self, graph_node: AbstractGraphNode, intermediate_data: any) -> None:
        self.__nodes[graph_node] = intermediate_data

    def cut_node(self, graph_node: AbstractGraphNode) -> None:
        self.__nodes.pop(graph_node)


class GraphPath:
    """Abstract graph without branch."""

    def __init__(self, *args, **kwargs) -> None:
        self.update(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(intermediate_keys={self.intermediate_keys}, starting_node={self.starting_node})"

    def update(self, first_node: AbstractGraphNode, intermediate_keys: Iterable) -> None:
        self.__intermediate_keys = tuple(intermediate_keys)
        self.update_nodes(first_node)

    def update_nodes(self, starting_node: AbstractGraphNode) -> None:
        self.__nodes = [starting_node]
        active_node = starting_node

        for key_index, intermediate_key in enumerate(self.intermediate_keys):
            self._check_serial_node(active_node, intermediate_key, key_index + 1)
            active_node = active_node[intermediate_key]

            self.__nodes.append(active_node)

        self.__starting_node = starting_node
        self.__final_node = self.nodes[-1]

    def _check_serial_node(self, node: AbstractGraphNode, next_intermediate_key: any, node_index: int) -> None:
        if not any(map(lambda node: node.data == next_intermediate_key, node.nodes)):
            raise NoNextGraphNode(node=self, node_index=node_index, data=next_intermediate_key)

    def get_all_intermediate_data(self) -> list:
        all_intermediate_data = list()

        for node_index, node in enumerate(self.nodes[:-1]):
            if isinstance(node, HashGraphNode):
                all_intermediate_data.append(
                    node.get_intermediate_data_from(self.nodes[node_index + 1])
                )

        return all_intermediate_data

    @property
    def intermediate_keys(self) -> tuple:
        return tuple(self.__intermediate_keys)

    @property
    def nodes(self) -> tuple[GraphNode,]:
        return tuple(self.__nodes)

    @property
    def starting_node(self) -> AbstractGraphNode:
        return self.__starting_node

    @property
    def final_node(self) -> AbstractGraphNode:
        return self.__final_node
