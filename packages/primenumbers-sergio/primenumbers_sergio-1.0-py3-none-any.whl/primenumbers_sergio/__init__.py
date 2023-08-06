def primeNumbersUpTo(number):
    primeNumbers = []
    for i in range(2, number + 1):

        totalDividers = 0

        for j in range(1, i):
            if (i % j == 0):
                totalDividers += 1
            if (totalDividers > 1):
                break

        if(totalDividers < 2):
            primeNumbers.append(i)

    return primeNumbers
