from typing import Iterable


def qsort(numbers: Iterable[int]) -> list:
    """
    Recursive function returning a sorted list. Sorts the collection into two
    parts: greater than and less than the central number and recursively applies
    to these parts until the array is completely sorted. O(n) speed. Analogs:
    numbers.sort().
    """

    if len(numbers) > 2:
        reliance = numbers[len(numbers)//2 - 1]
        lesser, larger, analogues = [], [], []

        for number in numbers:
            if number == reliance:
                analogues.append(number)

            elif number > reliance:
                larger.append(number)

            elif number < reliance:
                lesser.append(number)

        return qsort(lesser) + analogues + qsort(larger)
    else:
        if len(numbers) == 2:
            if numbers[0] > numbers[1]:
                numbers.reverse()

        return numbers


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
