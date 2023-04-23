import numpy as np


def click(xCoord, yCoord, userSteps, matrix, width, height):
    cells_to_delete = []
    check_shape(xCoord, yCoord, cells_to_delete, width, height, matrix)

    if cells_to_delete:
        add_to_steps(userSteps, matrix)
        delete_cells(cells_to_delete, matrix)

    return len(cells_to_delete)


def check_shape(xCoord, yCoord, cells_to_delete, width, height, matrix):
    check_positions = [(xCoord, yCoord + 1), (xCoord, yCoord - 1),
                       (xCoord + 1, yCoord), (xCoord - 1, yCoord)]

    origin_name = matrix[xCoord, yCoord]
    if origin_name != 0:
        for coordinates in check_positions:
            x_pos = coordinates[0]
            y_pos = coordinates[1]
            if 0 <= x_pos <= height - 1 and 0 <= y_pos <= width - 1:
                neighbour_name = matrix[x_pos, y_pos]
                if neighbour_name == origin_name:
                    if (x_pos, y_pos) not in cells_to_delete:
                        cells_to_delete.append((x_pos, y_pos))
                        check_shape(x_pos, y_pos, cells_to_delete, width, height, matrix)


def add_to_steps(userSteps, matrix):
    userSteps.append(matrix.tolist())


def delete_cells(cells_to_delete, matrix):
    for coordinates in cells_to_delete:
        matrix[coordinates[0], coordinates[1]] = 0


def update_matrix(matrix, width, height):
    matrix = drop_down_cells(matrix, width)
    matrix = move_cells_left(matrix, width, height)

    return matrix


def drop_down_cells(matrix, width):
    columns_array = create_columns_list(matrix, width)
    columns_array = drop_columns(columns_array)
    matrix = join_columns(columns_array)

    return matrix


def create_columns_list(matrix, width):
    columns = [matrix[:, i] for i in range(width)]

    return columns


def drop_columns(columns_array):
    result = []
    for i in columns_array:
        i_list = i.tolist()
        zero_nums = i_list.count(0)
        result_item = [0]*zero_nums + [val for val in i_list if val != 0]
        result.append(np.array(result_item))

    return result


def join_columns(columns_array):
    matrix = np.column_stack(columns_array)

    return matrix


def move_cells_left(matrix, width, height):
    columns = create_columns_list(matrix, width)
    columns = [col for col in columns if col[-1] != 0]
    for i in range(width - len(columns)):
        columns.append(np.zeros(height, dtype=int))

    matrix = join_columns(columns)

    return matrix


def undo(matrix, userSteps):
    if len(userSteps) > 0:
        matrix = np.array(userSteps[-1])
        userSteps = userSteps[:-1]

    return matrix, userSteps


def draw_matrix(matrix):

    for line in matrix:
        print(*line)
