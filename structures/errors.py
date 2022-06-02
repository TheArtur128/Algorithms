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
