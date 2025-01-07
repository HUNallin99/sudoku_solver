from gui import create_gui
from image import detect_sudoku_cells, overlay_solution_in_grid
from solution import solve_sudoku, print_table

def process_sudoku_image(image_path):
    print("\nSudoku tábla feldolgozása...")
    detected_grid, rectified_grid = detect_sudoku_cells(image_path)

    if detected_grid and rectified_grid is not None:
        print("\nFelismert Sudoku rács:")
        print_table(detected_grid)

        print("\nSudoku megoldása...")
        solution_grid = [row[:] for row in detected_grid]
        if solve_sudoku(solution_grid):
            print("\nMegoldott Sudoku rács:")
            print_table(solution_grid)

            print("\nMegoldás ráillesztése a körbevágott Sudoku táblára...")
            overlay_solution_in_grid(rectified_grid, detected_grid, solution_grid, image_path)
        else:
            print("\nHiba: A Sudoku rács nem megoldható.")
    else:
        print("\nHiba: A Sudoku rács feldolgozása sikertelen.")

def main():
    create_gui(process_sudoku_image)

if __name__ == "__main__":
    main()
