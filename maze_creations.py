from maze import Maze, Cell, Cell_Type
import random


def dfs_generation(height, width):  # генерация лабиринта обходом в глубину
    start_pos = (height - 1, 0)
    finish_pos = (0, width - 1)
    labyrinth = Maze(height, width, start_pos, finish_pos)
    visited = [[False for j in range(width)] for i in range(height)]
    stack = [start_pos]

    while len(stack) != 0:  # пока есть, куда двигаться
        y_pos, x_pos = stack[len(stack) - 1]
        visited[y_pos][x_pos] = True
        neighbors = dict()  # находим всех не посещённых соседей
        if x_pos > 0 and not visited[y_pos][x_pos - 1]:
            neighbors[len(neighbors)] = (y_pos, x_pos - 1)
        if y_pos > 0 and not visited[y_pos - 1][x_pos]:
            neighbors[len(neighbors)] = (y_pos - 1, x_pos)
        if x_pos < width - 1 and not visited[y_pos][x_pos + 1]:
            neighbors[len(neighbors)] = (y_pos, x_pos + 1)
        if y_pos < height - 1 and not visited[y_pos + 1][x_pos]:
            neighbors[len(neighbors)] = (y_pos + 1, x_pos)

        if len(neighbors) == 0:  # соседей нет - сгенерировали тупик
            stack.pop()
            continue

        next_cell = neighbors[random.randint(0, len(neighbors) - 1)]  # выбираем случайного соседа
        if x_pos > next_cell[1]:  # убираем нужную стену
            labyrinth[next_cell].right_wall = False
        elif y_pos > next_cell[0]:
            labyrinth[next_cell].bottom_wall = False
        elif x_pos < next_cell[1]:
            labyrinth[(y_pos, x_pos)].right_wall = False
        elif y_pos < next_cell[0]:
            labyrinth[(y_pos, x_pos)].bottom_wall = False
        stack.append(next_cell)

    return labyrinth


def prims_generation(height, width):  # генерация лабиринта рандомизированным алгоритмом Прима
    start_pos = (height - 1, 0)
    finish_pos = (0, width - 1)
    labyrinth = Maze(height, width, start_pos, finish_pos)
    visited = [[False for j in range(width)] for i in range(height)]
    visited[start_pos[0]][start_pos[1]] = True
    walls_list = [(start_pos[0] - 1, start_pos[1], 0), (start_pos[0], start_pos[1], 1)]  # список необработанных стен
    # 0 - если стена "нижняя горизонтальная", 1 - если стена "правая вертикальная"

    while len(walls_list) != 0:  # пока не обработали все стены
        wall_num = random.randint(0, len(walls_list) - 1)  # выбираем случайную стену
        cur_wall = walls_list[wall_num]

        unprocessed_cells = []  # необработанные клетки, которые делит стена
        if not visited[cur_wall[0]][cur_wall[1]]:
            unprocessed_cells.append((cur_wall[0], cur_wall[1]))
        if cur_wall[2] == 0 and not visited[cur_wall[0] + 1][cur_wall[1]]:
            unprocessed_cells.append((cur_wall[0] + 1, cur_wall[1]))
        elif cur_wall[2] == 1 and not visited[cur_wall[0]][cur_wall[1] + 1]:
            unprocessed_cells.append((cur_wall[0], cur_wall[1] + 1))

        if len(unprocessed_cells) == 1:  # если одна из клеток не обработана
            if cur_wall[2] == 0:  # убираем стену
                labyrinth[cur_wall[0]][cur_wall[1]].bottom_wall = False
            else:
                labyrinth[cur_wall[0]][cur_wall[1]].right_wall = False

            y_pos, x_pos = unprocessed_cells[0]
            visited[y_pos][x_pos] = True
            left_wall = (y_pos, x_pos - 1, 1)
            right_wall = (y_pos, x_pos, 1)
            top_wall = (y_pos - 1, x_pos, 0)
            bottom_wall = (y_pos, x_pos, 0)

            if x_pos > 0 and left_wall != cur_wall:  # добавляем стены
                walls_list.append(left_wall)
            if x_pos < width - 1 and right_wall != cur_wall:
                walls_list.append(right_wall)
            if y_pos > 0 and top_wall != cur_wall:
                walls_list.append(top_wall)
            if y_pos < height - 1 and bottom_wall != cur_wall:
                walls_list.append(bottom_wall)

        walls_list.pop(wall_num)  # удаляем обработанную стену

    return labyrinth


def maze_passage(labyrinth: Maze):  # решение лабиринта обходом в глубину
    start_pos = labyrinth.start
    finish_pos = labyrinth.finish
    height, width = labyrinth.size()
    visited = [[False for j in range(width)] for i in range(height)]
    previous = [[None for j in range(width)] for i in range(height)]
    previous[start_pos[0]][start_pos[1]] = (-1, -1)
    stack = [start_pos]
    finish_found = False

    while not len(stack) == 0 and not finish_found:  # пока есть, куда двигаться, и финиш не найден
        y_pos, x_pos = stack[len(stack) - 1]
        visited[y_pos][x_pos] = True
        neighbors = dict()  # находим всех не посещённых соседей
        if x_pos > 0 and not visited[y_pos][x_pos - 1] and not labyrinth[y_pos][x_pos - 1].right_wall:
            neighbors[len(neighbors)] = (y_pos, x_pos - 1)
        if y_pos > 0 and not visited[y_pos - 1][x_pos] and not labyrinth[y_pos - 1][x_pos].bottom_wall:
            neighbors[len(neighbors)] = (y_pos - 1, x_pos)
        if x_pos < width - 1 and not visited[y_pos][x_pos + 1] and not labyrinth[y_pos][x_pos].right_wall:
            neighbors[len(neighbors)] = (y_pos, x_pos + 1)
        if y_pos < height - 1 and not visited[y_pos + 1][x_pos] and not labyrinth[y_pos][x_pos].bottom_wall:
            neighbors[len(neighbors)] = (y_pos + 1, x_pos)

        if len(neighbors) == 0:  # соседей нет - тупик
            stack.pop()
            continue

        next_cell = neighbors[random.randint(0, len(neighbors) - 1)]  # выбираем случайного соседа
        previous[next_cell[0]][next_cell[1]] = (y_pos, x_pos)
        stack.append(next_cell)
        if next_cell == finish_pos:  # финиш найден
            finish_found = True

    if not finish_found:
        print("Выхода из лабиринта нет:(")
        return

    cur_pos = finish_pos
    while cur_pos != (-1, -1):  # изменение типа клеток, принадлежащих решению
        labyrinth[cur_pos].change_state(Cell_Type.IN_PATH)
        cur_pos = previous[cur_pos[0]][cur_pos[1]]
