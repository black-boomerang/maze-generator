from colorama import Back, init
from enum import Enum


class Cell_Type(Enum):  # тип клетки лабиринта
    USUAL = 0
    START = 1
    FINISH = 2
    IN_PATH = 3


class Cell:  # клетка лабиринта
    def __init__(self, cl_type=Cell_Type.USUAL, right_wall=True, bottom_wall=True):
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        self.cell_type = cl_type

    def change_state(self, new_state=Cell_Type.USUAL):  # изменение типа клетки
        if self.cell_type == Cell_Type.USUAL:
            self.cell_type = new_state


class Maze:
    def __init__(self, height=2, width=2, start=None, finish=None):
        self.field = [[Cell(Cell_Type.USUAL) for j in range(width)] for i in range(height)]
        self.start = start if start else (0, 0)  # стартовая позиция
        self.finish = finish if finish else (height - 1, width - 1)  # финишная позиция
        self.field[start[0]][start[1]].cell_type = Cell_Type.START
        self.field[finish[0]][finish[1]].cell_type = Cell_Type.FINISH
        self.height = height
        self.width = width
        self.is_show_path = False  # нужно ли показывать путь

    def __getitem__(self, item):  # обращение к клетке лабиринта
        if isinstance(item, int):
            return self.field[item]
        else:
            return self.field[item[0]][item[1]]

    def show(self):  # отображение лабиринта в консоли
        init()  # инициализация colorama
        for i in range(self.width * 2 + 1):  # первый слой стен
            print(Back.WHITE, '  ', Back.RESET, sep='', end='')
        print()

        for row_num in range(self.height):  # вывод каждой строки лабирнта
            row = self.field[row_num]
            next_row = self.field[row_num + 1] if row_num < self.height - 1 else None
            print(Back.WHITE, '  ', Back.RESET, sep='', end='')
            for cell_num in range(self.width):  # вывод каждой клетки лабиринта
                cell = row[cell_num]
                next_cell = row[cell_num + 1] if cell_num < self.width - 1 else None
                if cell.cell_type == Cell_Type.START:  # вывод стартовой клетки
                    print(Back.GREEN, end='')
                elif cell.cell_type == Cell_Type.FINISH:  # вывод финишной клетки
                    print(Back.BLUE, end='')
                elif self.is_show_path and cell.cell_type == Cell_Type.IN_PATH:  # клетка. включённая в решение лабиринта
                    print(Back.RED, end='')
                print('  ', Back.RESET, sep='', end='')

                # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
                if self.is_show_path and cell.cell_type != Cell_Type.USUAL and not cell.right_wall \
                        and next_cell.cell_type != Cell_Type.USUAL:
                    print(Back.RED, end='')
                elif cell.right_wall:  # "вертикальная" стена между клетками
                    print(Back.WHITE, end='')
                print('  ', Back.RESET, sep='', end='')

            print('\n', Back.WHITE, '  ', Back.RESET, sep='', end='')  # вывод левой боковой стены
            for cell_num in range(self.width):  # выводим "горизонтальные" стены между клетками, если они есть
                cell = row[cell_num]
                next_cell = next_row[cell_num] if next_row is not None else None

                # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
                if self.is_show_path and cell.cell_type != Cell_Type.USUAL and not cell.bottom_wall \
                        and next_cell.cell_type != Cell_Type.USUAL:
                    print(Back.RED, end='')
                elif cell.bottom_wall:  # "горизонтальная" стена между клетками
                    print(Back.WHITE, end='')
                print('  ', Back.WHITE, '  ', Back.RESET, sep='', end='')
            print()

    def size(self):  # размер лабиринта
        return (self.height, self.width)

    def show_path(self):  # отображение решения
        self.is_show_path = True

    def hide_path(self):  # скрытие решения
        self.is_show_path = False
