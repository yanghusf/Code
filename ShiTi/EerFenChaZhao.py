def binary_search(iter1,data):
    low_first = 0
    last_num = len(iter1) -1
    while low_first <= last_num:
        mid = (low_first + last_num) // 2
        guess = iter1[mid]
        if guess > data:
            last_num = mid - 1
        if guess < data:
            low_first = mid + 1
        if guess == data:
            return mid

    return None
if __name__ == '__main__':
    list_item = [1, 3, 5, 7, 9, 23, 43, 57, 58, 60, 76, 89, 100]
    index = binary_search(list_item, 89)
    print('查找的索引是{0}，对应的数字是{1}'.format(index, list_item[index]))



