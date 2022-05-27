class ConditionalErrorCauser:
    def __init__(self, condition, error: Exception):
        self.condition = condition
        self.error = error

    def __call__(self, *args, **kwargs) -> None:
        if self.condition(*args, **kwargs):
            raise self.error


class GraphNode:
    __not_graph_error_causer = ConditionalErrorCauser(
        lambda graph_node: not isinstance(graph_node, GraphNode),
        AttributeError("It is not a graph node")
    )

    def __init__(self, data: any, next_nodes: tuple | list | set = tuple()) -> None:
        self.data = data
        self.__next_nodes = set(next_nodes)

    def __repr__(self) -> str:
        return f"{self.data}{'.' if not self.__next_nodes else ''}{self.__next_nodes}"

    def __getitem__(self, data_of_next_node: any):
        for node in self.__next_nodes:
            if node.data == data_of_next_node:
                return node

    @property
    def nodes(self) -> set:
        return set(self.__next_nodes)

    def add_node(self, graph_node) -> None:
        self.__not_graph_error_causer(graph_node)
        self.__next_nodes.add(graph_node)

    def cut_node(self, graph_node) -> None:
        self.__not_graph_error_causer(graph_node)
        self.__next_nodes.remove(graph_node)


class Queue:
    def __init__(self, data: tuple | list | set = tuple()):
        self.__objects = list(data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(len={len(self)})"

    def __len__(self) -> int:
        return len(self.__objects)

    def __bool__(self) -> bool:
        return bool(self.__objects)

    def get(self) -> any:
        return self.__objects.pop(0)

    def add(self, data: any) -> None:
        self.__objects.append(data)

    def add_all(self, data: tuple) -> None:
        for object_ in data:
            self.add(object_)
