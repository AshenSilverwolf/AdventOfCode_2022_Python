class Monkey:

    def __init__(self, starting_items, operator, operand, div_by, true_target,
                 false_target):
        """
        :param starting_items: list of integers
        :param stress_func: function
        :param test_func: function
        :param true_target: integer
        :param false_target: integer
        """
        self.items = starting_items
        self.stress_func = generate_operation(operator, operand)
        self.test_func = lambda x: x % div_by == 0
        self.true_target = true_target
        self.false_target = false_target
        self.inspection_counter = 0

    def __repr__(self):
        return str(self.items)

    def update_stress(self, stress_level):
        """
        :param stress_level: integer
        """
        stress_level = self.stress_func(stress_level)
        stress_level //= 3
        self.inspection_counter += 1
        
        return stress_level

    def select_target(self, stress_level):
        """
        :param stress_level: integer
        """
        if self.test_func(stress_level):
            return self.true_target
        else:
            return self.false_target

    def add_item(self, item):
        """
        :param item: integer
        """
        self.items.append(item)

    def pop_front(self):
        """
        Returns the front element of the items list.
        """
        return self.items.pop(0)

    def get_inspections(self):
        """
        Returns the number of inspections performed by this monkey
        """
        return self.inspection_counter


def generate_operation(operator, operand):

    if operand == 'old':
        if operator == '+':
            operation = lambda x: x + x
        elif operator == '*':
            operation = lambda x: x * x
    else:
        if operator == '+':
            operation = lambda x: x + int(operand)
        elif operator == '*':
            operation = lambda x: x * int(operand)

    return operation


def parse_input(filepath):

    f = open(filepath, 'r')

    # Lets do this one with a Monkey Class

    monkeys = []

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]

        # Starting Items
        line = f.readline()
        line = line.split('\n')[0]
        items = line.split(': ')[1].split(', ')
        starting_items = list(map(lambda x: int(x), items))

        # Stress Operation
        line = f.readline()
        line = line.split('\n')[0]
        function = line.split('Operation: ')[1]
        operands = function.split('new = old ')[1].split(' ')
        operator = operands[0]
        operand = operands[1]

        # Test Function
        line = f.readline()
        line = line.split('\n')[0]
        div_by = int(line.split('Test: divisible by ')[1])

        # True/False Targets
        line = f.readline()
        line = line.split('\n')[0]
        true_target = int(line.split('If true: throw to monkey ')[1])

        line = f.readline()
        line = line.split('\n')[0]
        false_target = int(line.split('If false: throw to monkey ')[1])

        curr_monkey = Monkey(starting_items, operator, operand, div_by, true_target,
                             false_target)

        monkeys.append(curr_monkey)

        f.readline()

    f.close()

    return monkeys


def play_game(monkeys_list):
    
    for i in range(20): # 20 Rounds
        for monkey in monkeys_list: # Each Monkey
            throwing_list = []
            while len(monkey.items) > 0:
                monkey.items[0] = monkey.update_stress(monkey.items[0])
                target = monkey.select_target(monkey.items[0])
                throwing_list.append((target, monkey.pop_front()))
            for target, item in throwing_list:
                monkeys_list[target].add_item(item)

        print('After round ' + str(i+1) + ', the monkeys are holding items with these worry levels:')
        for idx, monkey in enumerate(monkeys_list):
            print('Monkey ' + str(idx) + ': ' + str(monkey.items))
        print()

    inspections = []
    for monkey in monkeys_list:
        inspections.append(monkey.get_inspections())

    inspections.sort()
    top1 = inspections[-1]
    top2 = inspections[-2]
    print(top1, top2)

    level_of_monkey_business = top1 * top2

    return level_of_monkey_business


def main():

    monkeys_list = parse_input('d11_input.txt')

    level_of_monkey_business = play_game(monkeys_list)
    print(level_of_monkey_business)


main()
