from typing import Iterable, Callable, Union
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


class AbstractBinaryGraphNode(AbstractGraphNode):
    """
    Stores only two nodes: right and left. Determines the position of the node
    with the determinant_function, which compares the data of the next node and
    the current node and returns "left" or "rigth" for the corresponding location.
    When trying to add a node to an already existing place, it forces you to add
    this node to the node lying in the occupied place. Leaves the implementation
    of getting the function determinant_function.
    """

    def __init__(self, data: any) -> None:
        super().__init__(data)
        self.__right_node = self.__left_node = None

    @property
    def right_node(self) -> AbstractGraphNode:
        return self.__right_node

    @property
    def left_node(self) -> AbstractGraphNode:
        return self.__left_node

    @property
    @abstractmethod
    def determinant_function(self) -> Callable[[any, any], str]:
        pass

    @property
    def nodes(self) -> frozenset[AbstractGraphNode]:
        return frozenset(filter(lambda node: not node is None, (self.left_node, self.right_node)))

    def add_node(self, graph_node: AbstractGraphNode) -> None:
        match self.determinant_function(graph_node.data, self.data):
            case "left":
                if self.__left_node is None:
                    self.__left_node = graph_node
                else:
                    self.__left_node.add_node(graph_node)
            case "right":
                if self.__right_node is None:
                    self.__right_node = graph_node
                else:
                    self.__right_node.add_node(graph_node)
            case _ as result:
                raise ValueError(f'determinant function {determinant_function} returned {result}, not "right" or "left"')


    def cut_node(self, graph_node: AbstractGraphNode) -> None:
        match graph_node:
            case self.__left_node:
                self.__left_node = None
            case self.__right_node:
                self.__right_node = None
            case _:
                raise KeyError(graph_node)


class UserBinaryGraphNode(AbstractBinaryGraphNode):
    """Class taking determinant_function from the client."""

    def __init__(self, data: any, determinant_function: Callable) -> None:
        super().__init__(data)
        self.__determinant_function = determinant_function

    @property
    def determinant_function(self) -> Callable:
        return self.__determinant_function


class SystematizedBinaryGraphNode(AbstractBinaryGraphNode):
    """determinant_function is defined inside the class."""


class NumericBinaryGraphNode(SystematizedBinaryGraphNode):
    """
    Binary node that determines the place of data by numerical comparison: less -
    left, more - right.
    """

    @property
    def determinant_function(self) -> Callable:
        return lambda new_data, old_data: 'left' if new_data < old_data else 'right'


class IBinaryTree(ABC):
    """Describes the behavior of a binary tree."""

    def __repr__(self):
        return "{class_name}(top_data={top_data}, data_amount={data_amount})".format(
            class_name=self.__class__.__name__,
            top_data=self.top_data,
            data_amount=self.data_amount
        )

    @property
    @abstractmethod
    def data_amount(self) -> int:
        pass

    @property
    @abstractmethod
    def top_data(self) -> any:
        pass

    @abstractmethod
    def __getitem__(self, data_key: any) -> tuple:
        pass

    def add_from(self, items: Iterable) -> None:
        for item in items:
            self.add(item)

    @abstractmethod
    def add(self, data: any) -> None:
        pass

    @abstractmethod
    def cut(self, data: any) -> None:
        pass


class BinaryTree(IBinaryTree):
    """
    Binary tree using binary nodes, the class of which must be given during
    initialization.
    """

    def __init__(self, node_type: SystematizedBinaryGraphNode, items: Iterable = tuple()):
        self.__node_type = node_type
        self.__top_node = self.__node_type(None)
        self.add_from(items)

    @property
    def data_amount(self) -> int:
        return sum((
            len(self.__recursive_get_all_nodes_from(self.__top_node)),
            -1 if self.__top_node.data is None else 0
        ))

    @property
    def top_data(self) -> any:
        return self.__top_node.data

    def __getitem__(self, node_data: any) -> tuple:
        found_node = self.__recursive_found_nodes_to_node_with_data(node_data)[-1]

        if found_node is None:
            raise KeyError(node_data)

        return tuple(map(lambda node: node.data, found_node.nodes))

    def add_from(self, items: Iterable) -> None:
        for item in items:
            self.add(item)

    def add(self, data: any) -> None:
        if self.__top_node.data is None:
            self.__top_node.data = data
        else:
            self.__top_node.add_node(self.__node_type(data))

    def cut(self, data: any) -> None:
        previous_node, desired_node = self.__recursive_found_nodes_to_node_with_data(
            data,
            self.__top_node
        )[-2:]

        if desired_node is None:
            raise ValueError("{self} doesn't have node with data {data}")
        elif previous_node is None:
            self.__top_node.data = None
            map(self.__top_node.cut_node, self.__top_node.nodes)
        else:
            previous_node.cut_node(desired_node)

    def __recursive_found_nodes_to_node_with_data(
        self,
        data: any,
        active_node: AbstractBinaryGraphNode | None,
        previous_nodes: tuple[AbstractBinaryGraphNode,] = tuple(),
    ) -> tuple[Union[AbstractBinaryGraphNode, None],]:
        if active_node is None or active_node.data == data:
            return *previous_nodes, active_node

        match active_node.determinant_function(data, active_node.data):
            case "right":
                select_next_node = active_node.right_node
            case "left":
                select_next_node = active_node.left_node

        return self.__recursive_found_nodes_to_node_with_data(
            data,
            select_next_node,
            (*previous_nodes, active_node)
        )

    def __recursive_get_all_nodes_from(
        self,
        node: AbstractBinaryGraphNode
    ) -> list[AbstractBinaryGraphNode,]:
        nodes = [node]

        for bottom_node in node.nodes:
            nodes.extend(self.__recursive_get_all_nodes_from(bottom_node))

        return nodes


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
