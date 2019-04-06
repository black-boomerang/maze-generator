import pickle, argparse, os
import maze_gui
from maze_creations import *
from maze import Maze, Cell


def save_maze(labyrinth, file_name):  # сохранение лабиринта в файл
    "Сохранение лабиринта в файл"
    with open(file_name, "wb") as maze_file:
        labyrinth.hide_path()
        pickle.dump(labyrinth, maze_file)


def load_maze(file_name):  # загрузка лабиринта из файла
    "Загрузка лабиринта из файла"
    if os._exists(file_name):
        print("Файл " + file_name + " отсутсствует")
        return None
    with open(file_name, "rb") as maze_file:
        labyrinth = pickle.load(maze_file)
        return labyrinth


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    labyrinth = None

    parser.add_argument("--maze_type",
                        help="вариант генерации лабиринта (по умолчанию генерация обходом в глубину)",
                        choices=["dfs", "prims", "ellers", "recursive"])
    parser.add_argument("-l", "--load", help="загрузка лабиринта из файла")
    parser.add_argument("-s", "--save", help="сохранение лабиринта в файл")
    parser.add_argument("--height", type=int, help="высота лабиринта")
    parser.add_argument("--width", type=int, help="ширина лабиринта")
    parser.add_argument("--show_path", action="store_true", help="отображение решения лабиринта")
    parser.add_argument("-g", "--gui", action="store_true", help="графический интерфейс (прохождение пользователем)")
    args = parser.parse_args()

    if args.load:  # в случае загрузки лабиринта
        labyrinth = load_maze(os.path.join(os.getcwd(), 'mazes', args.load + '.maze'))
    else:
        height = width = 10
        if args.height:  # задаём высоту лабиринта
            height = args.height
        if args.width:  # задаём ширину лабиринта
            width = args.width

        if args.maze_type == "prims":  # генерация лабиринта
            labyrinth = prims_generation(height, width)
        elif args.maze_type == "ellers":
            labyrinth = ellers_generation(height, width)
        elif args.maze_type == "recursive":
            labyrinth = recursive_generation(height, width)
        else:
            labyrinth = dfs_generation(height, width)

        maze_passage(labyrinth)  # решение лабиринта

    if args.save:  # в случае сохранения лабиринта
        save_maze(labyrinth, os.path.join(os.getcwd(), 'mazes', args.save + '.maze'))

    if args.show_path:  # показываем решение лабиринта
        labyrinth.show_path()

    if args.gui:  # графический интерфейс (с прохождением пользователя)
        maze_gui.gui(labyrinth)
    else:  # отображение в консоли
        labyrinth.show()
