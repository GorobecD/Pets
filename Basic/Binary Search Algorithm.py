def binary_search(searchNumber, sortedList):
    l = 0
    u = len(sortedList) - 1

    while l <= u:
        mid = (l + u) // 2

        if searchNumber == sortedList[mid]:
            return mid
        elif searchNumber > sortedList[mid]:
            l = mid
        else:
            u = mid


sor = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(binary_search(4, sor))
