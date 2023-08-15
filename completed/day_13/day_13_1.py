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

        output.append((left_list, right_list))

        check = f.readline()
        if check == '':
            break

    f.close()

    return output


def compare(list1, list2):

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
            rec_result = compare([left], right)
            if rec_result is not None:
                return rec_result
        elif type(left) == list and type(right) == int:
            rec_result = compare(left, [right])
            if rec_result is not None:
                return rec_result
        elif type(left) == list and type(right) == list:
            rec_result = compare(left, right)
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


def main():

    parsed_input = parse_input(FILEPATH)

    sum = 0
    for i, pair in enumerate(parsed_input):
        left = pair[0]
        right = pair[1]
        print(left)
        print(right)
        print()

        result = compare(left, right)
    
        if result is None:
            print('The lists are equal.')
        elif result == True:
            print('The lists are ordered correctly.')
            sum += i+1
        elif result == False:
            print('The lists are NOT ordered correctly.')

        print()
        print()

    print('Sum of indices of correctly ordered lists: ' + str(sum))


main()