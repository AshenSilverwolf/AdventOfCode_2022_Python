FILEPATH = 'd13_input.txt'

def string_to_list(str):

    output = []
    index = 1
    
    while True:
        c = str[index]
        if c == '[':
            offset = 1
            stack = ['[']
            while len(stack) > 0:
                if str[index + offset] == ']':
                    stack.pop()
                elif str[index + offset] == '[':
                    stack.append('[')
                offset += 1
            temp_list = string_to_list(str[index : index + offset])
            output.append(temp_list)
            index += offset
        elif c == ']':
            break
        elif c == ',':
            index += 1
        else:
            offset = 1
            while str[index + offset].isnumeric():
                offset += 1
            num = int(str[index : index + offset])
            output.append(num)
            index += offset

    return output


def parse_input(filepath):

    f = open(filepath, 'r')

    output = []

    while True:
        line1 = f.readline()
        line1 = line1.split('\n')[0]
        line2 = f.readline()
        line2 = line2.split('\n')[0]

        left_list = string_to_list(line1)
        right_list = string_to_list(line2)

        output.append(left_list)
        output.append(right_list)

        check = f.readline()
        if check == '':
            break

    f.close()

    return output


def left_smaller(list1, list2):

    len_1 = len(list1)
    len_2 = len(list2)
    size = min(len_1, len_2)
    if len_1 == len_2:
        smaller = 0
    elif len_1 < len_2:
        smaller = 1
    elif len_1 > len_2:
        smaller = 2
    
    i = 0

    while i < size:

        left = list1[i]
        right = list2[i]
        
        if type(left) == int and type(right) == int:
            if left < right:
                return True
            elif left > right:
                return False
        elif type(left) == int and type(right) == list:
            rec_result = left_smaller([left], right)
            if rec_result is not None:
                return rec_result
        elif type(left) == list and type(right) == int:
            rec_result = left_smaller(left, [right])
            if rec_result is not None:
                return rec_result
        elif type(left) == list and type(right) == list:
            rec_result = left_smaller(left, right)
            if rec_result is not None:
                return rec_result

        i += 1

    if smaller == 0:
        return_value = None
    if smaller == 1:
        return_value = True
    if smaller == 2:
        return_value = False

    return return_value


def my_sort(arr):

    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and not left_smaller(arr[j], key):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def main():

    divider_packets = [[[2]], [[6]]]
    parsed_input = parse_input(FILEPATH)
    parsed_input += divider_packets
    my_sort(parsed_input)

    dividers = []
    for i, x in enumerate(parsed_input):
        if x in divider_packets:
            dividers.append(i+1)

    decoder_key = dividers[0] * dividers[1]
    print(decoder_key)


main()