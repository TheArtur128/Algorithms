from math import inf as infinity


def binary_search_index_of(number: int, sorted_array: list[int]) -> int:
    '''O(log n). Analogs: list.index(number)'''

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


def is_item_in(array: list, item: any) -> bool:
    '''O(n). Analogs: item in list'''

    boxes = []
    for object_ in array:
        if object_ == item:
            return True
        elif type(object_) is list:
            boxes.append(object_)

    return any(map(lambda box: is_item_in(box, item), boxes))


def get_biggest_from(numbers: list[int]) -> int:
    '''O(n). Analogs: max(numbers)'''

    bigest = -infinity
    for number in numbers:
        if bigest < number:
            bigest = number

    return bigest
