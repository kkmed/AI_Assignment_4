def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid(board, row, col, num):
    for j in range(9):
        if board[row][j] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    box_x = (col // 3) * 3
    box_y = (row // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num:
                return False

    return True


def get_domain(board, row, col):
    domain = set(range(1, 10))
    for i in range(9):
        if board[row][i] in domain:
            domain.remove(board[row][i])
        if board[i][col] in domain:
            domain.remove(board[i][col])

    box_x = (col // 3) * 3
    box_y = (row // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] in domain:
                domain.remove(board[i][j])

    return domain


def select_unassigned_variable(board):
    min_domain = 10
    best_cell = None

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                domain = get_domain(board, i, j)
                if len(domain) < min_domain:
                    min_domain = len(domain)
                    best_cell = (i, j)

    return best_cell


def forward_check(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                if len(get_domain(board, i, j)) == 0:
                    return False
    return True


def solve(board):
    cell = select_unassigned_variable(board)
    if not cell:
        return True

    row, col = cell
    domain = get_domain(board, row, col)

    for num in domain:
        if is_valid(board, row, col, num):
            board[row][col] = num

            if forward_check(board) and solve(board):
                return True

            board[row][col] = 0

    return False


# Example puzzle (0 = empty)
board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

print("Original:")
print_board(board)

solve(board)

print("\nSolved:")
print_board(board)