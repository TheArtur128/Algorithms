from typing import Iterable
from dataclasses import dataclass
from functools import reduce
from math import inf
from copy import copy


class Queue:
    def __init__(self, data: Iterable = tuple()):
        self.__objects = list(data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(len={len(self)})"

    def __len__(self) -> int:
        return len(self.__objects)

    def __iter__(self) -> iter:
        return iter(self.__objects)

    def __bool__(self) -> bool:
        return bool(self.__objects)

    def get(self) -> any:
        return self.__objects.pop(0)

    def add(self, data: any) -> None:
        self.__objects.append(data)

    def add_from(self, data: tuple) -> None:
        for object_ in data:
            self.add(object_)


@dataclass(frozen=True)
class ItemDescription():
    items: tuple
    cost: int
    importance_index: int

    def __add__(self, other):
        if self is self.__class__.get_worst_example() and other is self.__class__.get_worst_example():
            return self.__class__.get_worst_example()

        elif self is self.__class__.get_worst_example():
            return copy(other)

        elif other is self.__class__.get_worst_example():
            return copy(self)

        else:
            return self.__class__(
                (*self.items, *other.items),
                self.cost + other.cost,
                self.importance_index + other.importance_index
            )

    @classmethod
    def get_worst_example(cls):
        if not hasattr(cls, "_worst_example"):
            cls._worst_example = cls(tuple(), inf, -inf)

        return cls._worst_example

    @staticmethod
    def choise_optimal_description(
        descriptions: Iterable,
        cost_limit: int = inf,
        bad_result: any = None
    ) -> any:
        clean_descriptions = tuple(
            filter(lambda description: description.cost <= cost_limit, descriptions)
        )

        if not clean_descriptions:
            return bad_result

        return reduce(
            lambda first, second: (
                first if first.importance_index >= second.importance_index else second
            ),
            clean_descriptions
        )
