def qsort(numbers: list[int]) -> list:
    '''O(n). Analogs: numbers.copy().sort()'''

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
