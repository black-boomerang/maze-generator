from colorama import Back, init
from enum import Enum

init() # инициализация colorama

class Cell_Type(Enum): # тип клетки лабиринта
    USUAL = 0
    START = 1
    FINISH = 2
    IN_PATH = 3

class Cell: # клетка лабиринта
    def __init__(self, type = Cell_Type.USUAL, right_wall = True, bottom_wall = True):
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        self.type = type

    def change_state(self, new_state = Cell_Type.USUAL): # изменение типа клетки
        if self.type == Cell_Type.USUAL:
            self.type = new_state

class Maze:
    def __init__(self, height = 2, width = 2, start = (0, 0), finish = (0, 0)):
        self.field = [[Cell(Cell_Type.USUAL) for j in range(width)] for i in range(height)]
        self.start = start # стартовая позиция
        self.finish = (height - 1, width - 1) if finish == (0, 0) else finish # финишная позиция
        self.field[start[0]][start[1]].type = Cell_Type.START
        self.field[finish[0]][finish[1]].type = Cell_Type.FINISH
        self.height = height
        self.width = width
        self.is_show_path = False # нужно ли показывать путь

    def __getitem__(self, item): # обращение к клетке лабиринта
        if isinstance(item, int):
            return self.field[item]
        else:
            return self.field[item[0]][item[1]]

    def __repr__(self): # отображение лабиринта в консоли
        repr = ""
        for i in range(self.width * 2 + 1): # первый слой стен
            repr += Back.WHITE + '  ' + Back.RESET
        repr += '\n'

        for row_num in range(self.height): # вывод каждой строки лабирнта
            row = self.field[row_num]
            next_row = self.field[row_num + 1] if row_num < self.height - 1 else None
            repr += Back.WHITE + '  ' + Back.RESET
            for cell_num in range(self.width): # вывод каждой клетки лабиринта
                cell = row[cell_num]
                next_cell = row[cell_num + 1] if cell_num < self.width - 1 else None
                if cell.type == Cell_Type.START: # вывод стартовой клетки
                    repr += Back.GREEN
                elif cell.type == Cell_Type.FINISH: # вывод финишной клетки
                    repr += Back.BLUE
                elif self.is_show_path and cell.type == Cell_Type.IN_PATH: # клетка. включённая в решение лабиринта
                    repr += Back.RED
                repr += '  ' + Back.RESET

                # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
                if self.is_show_path and cell.type != Cell_Type.USUAL and not cell.right_wall\
                        and next_cell.type != Cell_Type.USUAL:
                    repr += Back.RED
                elif cell.right_wall: # "вертикальная" стена между клетками
                    repr += Back.WHITE
                repr += '  '
                repr += Back.RESET

            repr += '\n' + Back.WHITE + '  ' + Back.RESET # вывод левой боковой стены
            for cell_num in range(self.width): # выводим вертикальные стены между клетками, если они есть
                cell = row[cell_num]
                next_cell = next_row[cell_num] if next_row is not None else None

                # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
                if self.is_show_path and cell.type != Cell_Type.USUAL and not cell.bottom_wall\
                        and next_cell.type != Cell_Type.USUAL:
                    repr += Back.RED
                elif cell.bottom_wall: # "горизонтальная" стена между клетками
                    repr += Back.WHITE
                repr += '  ' + Back.WHITE + '  ' + Back.RESET
            repr += '\n'
        return repr

    def size(self): # размер лабиринта
        return (self.height, self.width)

    def show_path(self): # отображение решения
        self.is_show_path = True
