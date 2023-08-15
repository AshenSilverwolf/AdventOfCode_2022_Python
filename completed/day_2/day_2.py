play_indeces = {
    'A': 0,
    'B': 1,
    'C': 2,
    'X': 0,
    'Y': 1,
    'Z': 2
}

outcome_matrix = [
    ['Z', 'X', 'Y'],
    ['X', 'Y', 'Z'],
    ['Y', 'Z', 'X']
]

points_matrix = [
    [(3,3), (0,6), (6,0)],
    [(6,0), (3,3), (0,6)],
    [(0,6), (6,0), (3,3)]
]

def parse_input(filepath):

    out = []
    
    f = open(filepath, 'r')
    
    while True:
        line = f.readline()
        if line == '': # EOF
            break
        out.append(line.split())

    f.close()

    return out


def choose_play(pair):

    p1 = play_indeces[pair[0]]
    outcome = play_indeces[pair[1]]

    return outcome_matrix[p1][outcome]


def calculate_total_score(guide):

    sum_points = 0

    for game in guide:
        play = choose_play(game)
        sum_points += calculate_single_score([game[0], play])

    return sum_points


def calculate_single_score(game):

    p1 = play_indeces[game[0]]
    p2 = play_indeces[game[1]]
    
    game_points = points_matrix[p1][p2][1]
    play_points = 1 + play_indeces[game[1]]

    return game_points + play_points

def main():

    guide = parse_input('input.txt')

    print(calculate_total_score(guide))


main()