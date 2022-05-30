class ConditionalErrorCauser:
    def __init__(self, condition: callable, error_factory: callable):
        self.condition = condition
        self.error_factory = error_factory

    def __call__(self, *args, **kwargs) -> None:
        if self.condition(*args, **kwargs):
            raise self.error_factory(*args, **kwargs)

    @staticmethod
    def create_wrapper_error_factory(error: Exception) -> callable:
        return lambda *args, **kwargs: error

    @staticmethod
    def create_structured_error_factory(error_type: callable, *new_error_args, **new_error_kwargs) -> callable:
        return lambda *args, **kwargs: error_type(*new_error_args, **new_error_kwargs)


class _StructuredException(Exception):
    """Exception having a text template that accepts this template on initialization"""

    default_text: str

    def __init__(self, *args, **kwargs):
        super().__init__(self.default_text.format(*args, **kwargs))


class GraphError(Exception):
    """Category of Errors related to graphs."""


class GraphNodeError(GraphError):
    """Category of Errors related to graph nodes."""


class NoGraphNodeReference(_StructuredException, GraphNodeError):
    """
    Error caused by the transition from one node of the graph to a non-existent
    other by its non-existent data.
    """

    default_text = "Graph node {node} has no nodes with data {data}"


class NoNextGraphNode(_StructuredException, GraphNodeError):
    """Error caused by the incorrect sequence of keys of the abstract graph (path)."""
    
    default_text = "Graph node {node} ({node_index} index) has no node with data {data}"
