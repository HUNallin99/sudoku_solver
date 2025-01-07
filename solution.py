def is_valid(table, row, col, num):
    if num in table[row]:
        return False

    if num in [table[i][col] for i in range(9)]:
        return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if table[i][j] == num:
                return False

    return True


def solve_sudoku(table):
    for row in range(9):
        for col in range(9):
            if table[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(table, row, col, num):
                        table[row][col] = num

                        if solve_sudoku(table):
                            return True

                        table[row][col] = 0

                return False

    return True


def print_table(table):
    for row in table:
        print(" ".join(str(num) if num != 0 else '.' for num in row))