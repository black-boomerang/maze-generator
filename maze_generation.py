import os, sys, pickle
from maze_creations import dfs_generation, prims_generation, maze_passage
from maze import Maze, Cell


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
    if os._exists(file_name):
        print("Файл " + file_name + " отсутсствует")
        return None
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
    print("Введите вариант генерации лабиринта:")
    print("   dfs_generation - генерация обходом в глубину,")
    print("   prims_generation - генерация алгоритмом Прима;")
    print("   load - загрузить лабиринт из файла.")

    labyrinth = None
    type_of_gen = input().strip().lower()

    if type_of_gen == 'load':
        print("Введите название файла лабиринта (без расширения):")
        file_name = input().strip().lower()
        labyrinth = load_maze(os.path.join(os.getcwd(), 'mazes', file_name + '.maze'))
    else:
        correct = False
        height, width = 0, 0

        while not correct:
            print("Введите размер лабиринта (высота и ширина через пробел):")
            height, width = input().strip().split()

            if not height.isdigit() or not width.isdigit():
                print("Размеры должны быть числами!")
            else:
                correct = True

        height, width = int(height), int(width)
        if type_of_gen == 'dfs_generation':
            labyrinth = dfs_generation(height, width)
        elif type_of_gen == 'prims_generation':
            labyrinth = prims_generation(height, width)
        else:
            print("Генерация алгоритмом по умолчанию (dfs_generation)")
            labyrinth = dfs_generation(height, width)

    print("Нужно ли выводить решение лабиринта (yes, no):")
    show_path = (input().strip().lower() == 'yes')

    if labyrinth is not None and show_path:
        maze_passage(labyrinth)
        labyrinth.show_path()

    if labyrinth is not None:
        print(labyrinth)

        print("Нужно ли сохранить лабиринт (yes, no):")
        is_save = (input().strip().lower() == 'yes')

        if is_save:
            print("Введите название файла, в который нужно сохранить лабиринт (без расширения):")
            file_name = input().strip().lower()
            save_maze(labyrinth, os.path.join(os.getcwd(), 'mazes', file_name + '.maze'))
