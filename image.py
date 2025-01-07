import numpy as np
import cv2
from easyocr import Reader
import os

def preprocess_cell(cell):

    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    gamma_correction = 1.2
    table = np.array([(i / 255.0) ** gamma_correction * 255 for i in range(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(gray, table)

    resized = cv2.resize(gamma_corrected, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_LINEAR)

    return resized

def detect_sudoku_cells(image_path, side_padding=5, bottom_padding=2):

    image = cv2.imread(image_path)
    if image is None:
        print("Hiba: Nem sikerült betölteni a képet.")
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    approx = cv2.approxPolyDP(largest_contour, 0.02 * cv2.arcLength(largest_contour, True), True)
    if len(approx) == 4:
        points = approx.reshape(4, 2)
        rectified_grid = transform_perspective(image, points)

        cell_width = rectified_grid.shape[1] // 9
        cell_height = rectified_grid.shape[0] // 9

        reader = Reader(['en'], gpu=False)
        sudoku_grid = []

        for row in range(9):
            row_data = []
            for col in range(9):
                x_start = col * cell_width + side_padding
                y_start = row * cell_height + side_padding
                x_end = (col + 1) * cell_width - side_padding
                y_end = (row + 1) * cell_height - bottom_padding

                cell = rectified_grid[y_start:y_end, x_start:x_end]
                processed_cell = preprocess_cell(cell)
                detection = reader.readtext(processed_cell, detail=0)
                number = int(detection[0]) if detection and detection[0].isdigit() else 0
                row_data.append(number)

            sudoku_grid.append(row_data)

        print("\nFelismert Sudoku rács:")
        for row in sudoku_grid:
            print(row)

        return sudoku_grid, rectified_grid
    else:
        print("Hiba: Nem található megfelelő négyzet alakú rács.")
        return None, None


def transform_perspective(image, points):
    rect = order_points(points)     #Rectangle
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([        #Destination coordinates
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)      #Matrix
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def overlay_solution_in_grid(rectified_grid, detected_grid, solution_grid, input_image_path):

    cell_width = rectified_grid.shape[1] // 9
    cell_height = rectified_grid.shape[0] // 9

    for row in range(9):
        for col in range(9):
            if detected_grid[row][col] == 0 and solution_grid[row][col] != 0:
                x_start = col * cell_width
                y_start = row * cell_height
                x_center = x_start + cell_width // 2
                y_center = y_start + cell_height // 2

                cv2.putText(rectified_grid, str(solution_grid[row][col]),
                            (x_center - 15, y_center + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    output_path = f"{base_name}_solved.png"

    cv2.imwrite(output_path, rectified_grid)
    print(f"Megoldott Sudoku kép mentve: {output_path}")

    cv2.imshow("Sudoku Megoldás a Körbevágott Táblán", rectified_grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return rectified_grid