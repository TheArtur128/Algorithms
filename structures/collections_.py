from typing import Iterable


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
