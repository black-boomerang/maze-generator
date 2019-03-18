import sys, pickle
from maze_creations import dfs_generation, prims_generation, ellers_generation, recursive_generation, maze_passage
from maze import Maze, Cell


def show_help():  # помощь по аргументам командной строки
    print("Аргумены указываются в следующем порядке:")
    print("1) Вариант генерации лабиринта (по умолчанию генерация обходом в глубину):")
    print("   dfs_generation - генерация обходом в глубину,")
    print("   prims_generation - генерация алгоритмом Прима;")
    print("   ellers_generation - генерация алгоритмом Эллера;")
    print("   recursive_generation - генерация методом рекурсивного деления;")
    print("2) Размер лабиринта: высота и ширина (в случае, если лабиринт не загружается из файла);")
    print("3) save - в случае, если лабиринт нужно загрузить, load - в случае, если лабиринт нужно загрузить;")
    print("4) название файла (без указания расширения);")
    print("5) show_path - в случае, если нужно отобразить решение лабиринта.")
    print()


def save_maze(labyrinth, file_name):  # сохранение лабиринта в файл
    "Сохранение лабиринта в файл"
    with open(file_name, "wb") as file:
        pickle.dump(labyrinth.size(), file)
        pickle.dump(labyrinth.start, file)
        pickle.dump(labyrinth.finish, file)
        for row in labyrinth.field:
            for cell in row:
                pickle.dump(cell.bottom_wall, file)
                pickle.dump(cell.right_wall, file)


def load_maze(file_name):  # загрузка лабиринта из файла
    "Загрузка лабиринта из файла"
    with open(file_name, "rb") as file:
        height, width = pickle.load(file)
        start = pickle.load(file)
        finish = pickle.load(file)
        labyrinth = Maze(height, width, start, finish)
        for i in range(height):
            for j in range(width):
                labyrinth.field[i][j].bottom_wall = pickle.load(file)
                labyrinth.field[i][j].right_wall = pickle.load(file)
        return labyrinth


if __name__ == "__main__":
    is_show = True
    labyrinth = None
    cur_arg = 1

    if len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'help':  # помощь по аргументам командной строки
        show_help()
        is_show = False
    elif len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'load':  # в случае загрузки лабиринта
        cur_arg += 1
        if len(sys.argv) == cur_arg:
            print("Укажите название файла, из которого будет загружен лабиринт\n")
            is_show = False
        else:
            labyrinth = load_maze(sys.argv[cur_arg] + ".maze")
            cur_arg += 1
    else:
        mode = 0  # вид генерации
        if len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'dfs_generation':
            mode = 0
            cur_arg += 1
        elif len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'prims_generation':
            mode = 1
            cur_arg += 1
        elif len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'ellers_generation':
            mode = 2
            cur_arg += 1
        elif len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'recursive_generation':
            mode = 3
            cur_arg += 1

        if len(sys.argv) == cur_arg or not sys.argv[cur_arg].isdigit():  # задаём высоту лабиринта
            height = 10
        else:
            height = int(sys.argv[cur_arg])
            cur_arg += 1
        if len(sys.argv) == cur_arg or not sys.argv[cur_arg].isdigit():  # задаём ширину лабиринта
            width = 10
        else:
            width = int(sys.argv[cur_arg])
            cur_arg += 1

        if mode == 0:  # генерация лабиринта
            labyrinth = dfs_generation(height, width)
        elif mode == 1:
            labyrinth = prims_generation(height, width)
        elif mode == 2:
            labyrinth = ellers_generation(height, width)
        elif mode == 3:
            labyrinth = recursive_generation(height, width)
        else:
            labyrinth = None
            print("Ошибка")

        if len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'save':  # в случае сохранения лабиринта
            cur_arg += 1
            if len(sys.argv) == cur_arg:
                print("Укажите название файла, в который будет сохранён лабиринт\n")
            else:
                save_maze(labyrinth, sys.argv[cur_arg] + ".maze")
                cur_arg += 1

    if len(sys.argv) > cur_arg and sys.argv[cur_arg] == 'show_path':  # показываем решение лабиринта
        maze_passage(labyrinth)
        labyrinth.show_path()
    if is_show:  # выводим лабирнт на экран
        print(labyrinth)
