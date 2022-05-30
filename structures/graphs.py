from typing import Iterable, Callable

from errors import NoGraphNodeReference, NoNextGraphNode


class _StaticallyTypedSet(set):
    """
    Set that only stores certain types of data. Throws exceptions when attempting
    to add unsupported types.
    """

    def __init__(self, supported_types: Iterable[type,], items: Iterable = tuple(), *args, **kwargs):
        self.supported_types = supported_types
        self.check_objects_for_types(items)

        super().__init__(items, *args, **kwargs)

    def __repr__(self) -> str:
        return f"staticset{set(self) if self else '()'}"

    def add(self, object_: any, *args, **kwargs) -> None:
        self.check_object_for_types(object_)
        return super().add(object_, *args, **kwargs)

    def check_object_for_types(self, object_: any) -> None:
        if not any(map(lambda type_: isinstance(object_, type_), self.supported_types)):
            beautiful_types = ', '.join(map(lambda type_: type_.__name__, self.supported_types))
            raise TypeError(f"This set can only store objects of type {beautiful_types}, not {object_.__class__.__name__}")

    def check_objects_for_types(self, objects: Iterable) -> None:
        for object_ in objects:
            self.check_object_for_types(object_)


class GraphNode:
    """Part of an imaginary graph. Stores any data and links to other parts of the graph."""

    def __init__(self, data: any, next_nodes: Iterable = tuple()) -> None:
        self.data = data
        self.__nodes = _StaticallyTypedSet((self.__class__,), next_nodes)

    def __repr__(self) -> str:
        return f"{self.data}.{self.__nodes}"

    def __getitem__(self, data_of_next_node: any):
        for node in self.__nodes:
            if node.data == data_of_next_node:
                return node

        raise NoGraphNodeReference(node=self, data=data_of_next_node)

    @property
    def nodes(self) -> set:
        return set(self.__nodes)

    def add_node(self, graph_node) -> None:
        self.__nodes.add(graph_node)

    def cut_node(self, graph_node) -> None:
        self.__nodes.remove(graph_node)


class GraphNodePath:
    """Abstract graph without branch."""

    def __init__(self, *args, **kwargs) -> None:
        self.update(*args, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(map(lambda key: str(key), self.intermediate_keys))})"

    def update(self, first_node: GraphNode, intermediate_keys: Iterable) -> None:
        self.__intermediate_keys = tuple(intermediate_keys)
        self.update_nodes(first_node)

    def update_nodes(self, starting_node: GraphNode) -> None:
        self.__nodes = [starting_node]
        active_node = starting_node

        for key_index, intermediate_key in enumerate(self.intermediate_keys):
            self._check_serial_node(active_node, intermediate_key, key_index + 1)
            active_node = active_node[intermediate_key]

            self.__nodes.append(active_node)

        self.__starting_node = starting_node
        self.__final_node = self.nodes[-1]

    def _check_serial_node(self, node: GraphNode, next_intermediate_key: any, node_index: int) -> None:
        if not any(map(lambda node: node.data == next_intermediate_key, node.nodes)):
            raise NoNextGraphNode(node=self, node_index=node_index, data=next_intermediate_key)

    @property
    def intermediate_keys(self) -> tuple:
        return tuple(self.__intermediate_keys)

    @property
    def nodes(self) -> tuple[GraphNode,]:
        return tuple(self.__nodes)

    @property
    def starting_node(self) -> GraphNode:
        return self.__starting_node

    @property
    def final_node(self) -> GraphNode:
        return self.__final_node
