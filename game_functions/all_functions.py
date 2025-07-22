import pygame
from pygame import Surface


def level_structure(level):
    count = 0
    pl_pos = []
    mas_bl = []
    win_pos = []
    boxes = []
    for line in level:
        line = line.strip().split(";")
        for i in line:
            count += 1
            if i == "1":
                mas_bl.append(count)
            elif i == "2":
                win_pos.append(count)
            elif i == "3":
                boxes.append(count)
            elif i == "4":
                pl_pos.append(count)
    boxes, player_position = lvl_box_and_player(boxes, pl_pos)
    massive_blocks = lvl_blocks(mas_bl)
    wins_position = win_position(win_pos)
    player_position = player_position[1]
    return boxes, player_position, massive_blocks, wins_position


def texture_loader() -> tuple[Surface, Surface, Surface, Surface, Surface]:
    texture_block = pygame.image.load("texture/block.png")
    texture_box = pygame.image.load("texture/box.png")
    texture_win_position_off = pygame.image.load("texture/texture_win_position_off.png")
    box_act = pygame.image.load("texture/box_act.png")
    bg = pygame.image.load("texture/bg.png")
    return texture_block, texture_box, texture_win_position_off, box_act, bg


def texture_player(last_move):
    if last_move == "left":
        return "player_left"
    elif last_move == "right":
        return "player_right"
    elif last_move == "up":
        return "player_up"
    elif last_move == "down":
        return "player_down"
    else:
        return False


def check_win(boxes, wins_position):
    if all(box in wins_position for box in boxes):
        return True
    else:
        return False


def win_position(wins):
    all_positions = all_blocks()
    m = [x[1] for x in all_positions if (x[0]) in wins]
    return m


def all_blocks():
    m = []
    i = 0
    for y in range(0, 600, 50):
        for x in range(0, 800, 50):
            i += 1
            m.append((i, pygame.Rect(x, y, 50, 50)))
    return m


def lvl_blocks(lvl_block):
    m1 = all_blocks()
    m = [x[1] for x in m1 if (x[0]) in lvl_block]
    return m


def lvl_box_and_player(boxes, player):
    all_blocks_lvl = all_blocks()
    m = [x[1] for x in all_blocks_lvl if (x[0]) in boxes]
    player = player[0]
    player1 = all_blocks_lvl[player - 1]
    return m, player1


def player_on_box(player_position, boxes, last_move, massive_blocks):
    for box in boxes:
        if player_position == box:
            index = new_position(
                box, last_move, massive_blocks + [x for x in boxes if x != box]
            )[1]
            if index == "right":
                player_position.move_ip(-50, 0)
            elif index == "left":
                player_position.move_ip(50, 0)
            elif index == "up":
                player_position.move_ip(0, 50)
            elif index == "down":
                player_position.move_ip(0, -50)


def new_position(position, command, massive_blocks):
    index = "nothing"
    if command == "down":
        position.move_ip(0, 50)
        if check_collision(position, massive_blocks):
            position.move_ip(0, -50)
            index = "down"
    elif command == "up":
        position.move_ip(0, -50)
        if check_collision(position, massive_blocks):
            position.move_ip(0, 50)
            index = "up"
    elif command == "left":
        position.move_ip(-50, 0)
        if check_collision(position, massive_blocks):
            position.move_ip(50, 0)
            index = "left"
    elif command == "right":
        position.move_ip(50, 0)
        if check_collision(position, massive_blocks):
            position.move_ip(-50, 0)
            index = "right"
    return position, index


def check_collision(player_position, massive_blocks):
    for block in massive_blocks:
        if player_position in block:
            return True
    return False


def act(key):
    if key == pygame.K_UP or key == pygame.K_w:
        print("up")
        return "up"
    elif key == pygame.K_DOWN or key == pygame.K_s:
        print("down")
        return "down"
    elif key == pygame.K_LEFT or key == pygame.K_a:
        print("left")
        return "left"
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        print("right")
        return "right"
    elif key == pygame.K_ESCAPE:
        exit(0)
    return None
