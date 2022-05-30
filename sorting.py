    '''O(n). Analogs: numbers.sort()'''
from typing import Iterable
def qsort(numbers: Iterable[int]) -> list:

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


    """O(n^2). Analogs: numbers.sort()"""
def bubble_sort(numbers: Iterable) -> None:

    is_sorted = False

    while not is_sorted:
        is_sorted = True

        for i in range(len(numbers) - 1):
            if numbers[i] > numbers[i + 1]:
                is_sorted = False

                difference = numbers[i] - numbers[i + 1]
                numbers[i] -= difference
                numbers[i + 1] += difference
