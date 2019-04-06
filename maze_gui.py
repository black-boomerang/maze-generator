from tkinter import *
from maze import Maze, Cell_Type
from maze_creations import *
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)


# восстановление цвета клетки после того, как пользователь её покидает
def cell_repair(labyrinth, sc, user_pos, user_rect, usr_in_wall):
    cell = labyrinth[user_pos]
    cell_color = BLACK
    if usr_in_wall == 2:  # пользователь в "горизонтальном" проходе между клеткамими
        next_cell = labyrinth[user_pos[0] + 1][user_pos[1]]
        if labyrinth.is_show_path and cell.cell_type != Cell_Type.USUAL and next_cell.cell_type != Cell_Type.USUAL:
            cell_color = RED
    elif usr_in_wall == 1:  # пользователь в "вертикальном" проходе между клетками
        next_cell = labyrinth[user_pos[0]][user_pos[1] + 1]
        if labyrinth.is_show_path and cell.cell_type != Cell_Type.USUAL and next_cell.cell_type != Cell_Type.USUAL:
            cell_color = RED
    else:
        if cell.cell_type == Cell_Type.START:
            cell_color = YELLOW
        elif cell.cell_type == Cell_Type.FINISH:
            cell_color = BLUE
        elif labyrinth.is_show_path and cell.cell_type == Cell_Type.IN_PATH:
            cell_color = RED
    pygame.draw.rect(sc, cell_color, user_rect)


def gui(labyrinth: Maze):
    pygame.init()  # инициализация pygame

    CELL_SZ = 20  # размер клетки
    HEIGHT = (labyrinth.height * 2 + 1) * CELL_SZ
    WIDTH = (labyrinth.width * 2 + 1) * CELL_SZ
    FPS = 10

    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")
    sc.fill(BLACK)
    clock = pygame.time.Clock()

    user_pos = (labyrinth.start)
    user_rect = ((labyrinth.start[1] * 2 + 1) * CELL_SZ, (labyrinth.start[0] * 2 + 1) * CELL_SZ, CELL_SZ, CELL_SZ)
    user_in_right_wall = 0
    user_in_bottom_wall = 0

    pygame.draw.rect(sc, GREEN, (0, 0, WIDTH, CELL_SZ))  # первый слой стен

    cur_height = 0
    for row_num in range(labyrinth.height):  # вывод каждой строки лабирнта
        cur_height += CELL_SZ
        row = labyrinth.field[row_num]
        next_row = labyrinth.field[row_num + 1] if row_num < labyrinth.height - 1 else None

        # вывод левой боковой стены
        pygame.draw.rect(sc, GREEN, (0, cur_height, CELL_SZ, CELL_SZ))

        cur_width = CELL_SZ
        for cell_num in range(labyrinth.width):  # вывод каждой клетки лабиринта
            cell = row[cell_num]
            next_cell = row[cell_num + 1] if cell_num < labyrinth.width - 1 else None
            cell_color = BLACK
            if cell.cell_type == Cell_Type.START:  # вывод стартовой клетки
                cell_color = YELLOW
            elif cell.cell_type == Cell_Type.FINISH:  # вывод финишной клетки
                cell_color = BLUE
            elif labyrinth.is_show_path and cell.cell_type == Cell_Type.IN_PATH:  # клетка. включённая в решение лабиринта
                cell_color = RED
            pygame.draw.rect(sc, cell_color, (cur_width, cur_height, CELL_SZ, CELL_SZ))
            cur_width += CELL_SZ

            # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
            cell_color = BLACK
            if labyrinth.is_show_path and cell.cell_type != Cell_Type.USUAL and not cell.right_wall \
                    and next_cell.cell_type != Cell_Type.USUAL:
                cell_color = RED
            elif cell.right_wall:  # "вертикальная" стена между клетками
                cell_color = GREEN
            pygame.draw.rect(sc, cell_color, (cur_width, cur_height, CELL_SZ, CELL_SZ))
            cur_width += CELL_SZ

        # вывод левой боковой стены
        cur_height += CELL_SZ
        pygame.draw.rect(sc, GREEN, (0, cur_height, CELL_SZ, CELL_SZ))

        cur_width = CELL_SZ
        for cell_num in range(labyrinth.width):  # выводим "горизонтальные" стены между клетками, если они есть
            cell = row[cell_num]
            next_cell = next_row[cell_num] if next_row is not None else None

            # если две соседние клетки принадлежат решению и между ними нет стены, окрашиваем переход между ними
            cell_color = BLACK
            if labyrinth.is_show_path and cell.cell_type != Cell_Type.USUAL and not cell.bottom_wall \
                    and next_cell.cell_type != Cell_Type.USUAL:
                cell_color = RED
            elif cell.bottom_wall:  # "горизонтальная" стена между клетками
                cell_color = GREEN
            pygame.draw.rect(sc, cell_color, (cur_width, cur_height, CELL_SZ, CELL_SZ))
            cur_width += CELL_SZ
            pygame.draw.rect(sc, GREEN, (cur_width, cur_height, CELL_SZ, CELL_SZ))
            cur_width += CELL_SZ

    pygame.display.update()

    key_left = key_right = key_up = key_bottom = False
    is_finish = False
    while True:  # обновления окна
        for i in pygame.event.get():  # обработка действий пользователя
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:  # нажатие на клавишу
                if i.key == pygame.K_LEFT:
                    key_left = True
                elif i.key == pygame.K_RIGHT:
                    key_right = True
                elif i.key == pygame.K_UP:
                    key_up = True
                elif i.key == pygame.K_DOWN:
                    key_bottom = True
            elif i.type == pygame.KEYUP:  # отпускание клавиши
                if i.key == pygame.K_LEFT:
                    key_left = False
                elif i.key == pygame.K_RIGHT:
                    key_right = False
                elif i.key == pygame.K_UP:
                    key_up = False
                elif i.key == pygame.K_DOWN:
                    key_bottom = False

        if key_left:  # пользователь двигается влево
            if user_in_bottom_wall:
                continue
            elif user_in_right_wall:  # пользователь в "вертикальном" проходе между клетками
                cell_repair(labyrinth, sc, user_pos, user_rect, 1)
                user_in_right_wall = 0
            elif user_pos[1] > 0 and labyrinth[user_pos[0], user_pos[1] - 1].right_wall == False:
                cell_repair(labyrinth, sc, user_pos, user_rect, 0)
                user_pos = (user_pos[0], user_pos[1] - 1)
                user_in_right_wall = 1
        elif key_right:  # пользователь двигается вправо
            if user_in_bottom_wall:
                continue
            elif user_in_right_wall:  # пользователь в "вертикальном" проходе между клетками
                cell_repair(labyrinth, sc, user_pos, user_rect, 1)
                user_pos = (user_pos[0], user_pos[1] + 1)
                user_in_right_wall = 0
            elif user_pos[1] < labyrinth.width - 1 and labyrinth[user_pos[0], user_pos[1]].right_wall == False:
                cell_repair(labyrinth, sc, user_pos, user_rect, 0)
                user_in_right_wall = 1
        elif key_up:  # пользователь двигается вверх
            if user_in_right_wall:
                continue
            elif user_in_bottom_wall:  # пользователь в "горизонтальном" проходе между клетками
                cell_repair(labyrinth, sc, user_pos, user_rect, 2)
                user_in_bottom_wall = 0
            elif user_pos[0] > 0 and labyrinth[user_pos[0] - 1, user_pos[1]].bottom_wall == False:
                cell_repair(labyrinth, sc, user_pos, user_rect, 0)
                user_pos = (user_pos[0] - 1, user_pos[1])
                user_in_bottom_wall = 1
        elif key_bottom:  # пользователь двигается вниз
            if user_in_right_wall:
                continue
            elif user_in_bottom_wall:  # пользователь в "горизонтальном" проходе между клетками
                cell_repair(labyrinth, sc, user_pos, user_rect, 2)
                user_pos = (user_pos[0] + 1, user_pos[1])
                user_in_bottom_wall = 0
            elif user_pos[0] < labyrinth.height - 1 and labyrinth[user_pos[0], user_pos[1]].bottom_wall == False:
                cell_repair(labyrinth, sc, user_pos, user_rect, 0)
                user_in_bottom_wall = 1

        user_rect = ((user_pos[1] * 2 + 1 + user_in_right_wall) * CELL_SZ,
                     (user_pos[0] * 2 + 1 + user_in_bottom_wall) * CELL_SZ, CELL_SZ, CELL_SZ)

        pygame.draw.rect(sc, WHITE, user_rect)
        if user_pos == labyrinth.finish and not user_in_bottom_wall:
            is_finish = True
            break
        pygame.display.update()

        clock.tick(FPS)

    if is_finish:
        sc.fill(GREEN)
        fnt = pygame.font.Font(None, 46)
        txt = fnt.render("The maze is passed", 1, RED)
        place = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sc.blit(txt, place)
        pygame.display.update()
        while True:  # экран окончания игры
            for i in pygame.event.get():  # ждём выхода из программы
                if i.type == pygame.QUIT or i.type == pygame.KEYDOWN:
                    exit()
