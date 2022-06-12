import re

TURN_TABLE = {
    'O': 'X',
    'X': 'O'
}


def create_board():
    return \
        {
            'a': [' '] * 3,
            'b': [' '] * 3,
            'c': [' '] * 3,
        }


def print_board(board: dict):
    print(f'   {" ".join(map(lambda x: str(x), range(1, 4)))}')
    for key, row in board.items():
        print(f'{key}: ', end='')
        print('|'.join(row))
        if key != 'c':
            print(f'  {7 * "—"}')


def input_location():
    location = input("Enter board location: ").lower()
    while not re.match('[abc]:[123]', location):
        print('Invalid location format!')
        print('The valid form for location is -> RowName:ColumnNumber. E.g: a:3, b:1, c:2')
        location = input("Enter board location: ").lower()
    row = location.split(':')[0]
    column = int(location.split(':')[1])
    return row, column - 1


def is_board_full(board: dict):
    for row in board.values():
        if ' ' in row:
            return False
    return True


def get_vertical_winner(board: dict):
    for column_index in range(3):
        column_set = {board[row_key][column_index] for row_key in board.keys()}
        if len(column_set) == 1 and ' ' not in column_set:
            return board['a'][column_index], [f'{row_key}{column_index + 1}' for row_key in board.keys()]
    return None


def get_horizontal_winner(board: dict):
    for row_key, row in board.items():
        row_set = {column for column in board[row_key]}
        if len(row_set) == 1 and ' ' not in row_set:
            return board[row_key][0], [f'{row_key}{column_index + 1}' for column_index in range(3)]
    return None


def get_oblique_winner(board: dict):
    if board['a'][0] == board['b'][1] == board['c'][2]:
        return board['a'][0], ['a1', 'b2', 'c3']
    if board['a'][2] == board['b'][1] == board['c'][0]:
        return board['a'][0], ['a3', 'b1', 'c1']
    return None


def get_winner(board: dict):
    winner_functions = [get_vertical_winner, get_horizontal_winner, get_oblique_winner]
    for winner_function in winner_functions:
        res = winner_function(board)
        if res:
            return res
    return None, None


def play_game():
    board = create_board()
    turn = 'O'
    winner = None
    win_reason = None
    while not winner and not is_board_full(board):
        print_board(board)
        print(f"{turn}'s turn!")
        row, column = input_location()
        while board[row][column] != ' ':
            print('This location was already chosen! Please choose another location.')
            row, column = input_location()
        board[row][column] = turn
        turn = TURN_TABLE[turn]
        winner, win_reason = get_winner(board)
    if winner:
        print_board(board)
        print(f"{winner} is the winner because of: {', '.join(win_reason)}")
    else:
        print("No body won!")


main_menu = [
    ('Play game.', play_game),
    ('Exit.', exit)
]


def print_menu(options):
    for index, option in enumerate(options):
        print(f'{index + 1}. {option[0]}')


if __name__ == '__main__':
    while True:
        print_menu(main_menu)
        selected_option = input('Enter an option number: ')
        if selected_option.isdecimal() and 0 <= int(selected_option) - 1 < len(main_menu):
            main_menu[int(selected_option) - 1][1]()
        else:
            print('Invalid input.')
