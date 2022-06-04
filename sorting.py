from typing import Iterable, Callable


def qsort(
    items: list,
    determinant_function: Callable = lambda first, second: "middle" if first == second else first > second
) -> list:
    """
    Recursively divides the list into parts and chooses which part to
    attribute the element of this list to, according to input function
    determinant_function, which has two arguments, into which these parts fall
    and are compared. Input function determinant_function must return "middle"
    if the element is to be determined in the middle of the new sorted list,
    "left" or False if at the beginning and "rigth" or True if at the end. items
    is the list whose sorted version is to be returned. By default, sorts
    a list of numbers from smallest to largest. O(n) speed.
    """

    match len(items):
        case 2 if not determinant_function(*items):
            items.reverse()
        case _ as length if length < 2:
            return items

    reliance = items[len(items)//2 - 1]
    left_part, middle_part, right_part  = list(), list(), list()

    for item in items:
        match determinant_function(item, reliance):
            case "middle":
                middle_part.append(item)
            case "right" | True:
                right_part.append(item)
            case "left" | False:
                left_part.append(item)
            case _ as result:
                raise ValueError(f'Determinant function must return "middle", "right", "left" or boolean value, not {result}')

    return (
        qsort(left_part, determinant_function) +
        middle_part +
        qsort(right_part, determinant_function)
    )

def bubble_sort(numbers: Iterable) -> None:
    """
    Sorts the collection by continuously iterating over it and replacing two
    adjacent numbers if the left is greater than the right. O(n^2) speed. Analogs:
    numbers.sort().
    """

    is_sorted = False

    while not is_sorted:
        is_sorted = True

        for i in range(len(numbers) - 1):
            if numbers[i] > numbers[i + 1]:
                is_sorted = False

                difference = numbers[i] - numbers[i + 1]
                numbers[i] -= difference
                numbers[i + 1] += difference
