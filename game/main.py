import pygame
from player.player import Vector
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

texture_block = pygame.image.load("texture/block.png")
texture_box = pygame.image.load("texture/box.png")
texture_win_position_off = pygame.image.load("texture/texture_win_position_off.png")
box_act = pygame.image.load("texture/box_act.png")
bg = pygame.image.load("texture/bg.png")

CELL_SIZE = 50

direction_step = {
    pygame.K_RIGHT: Vector((1, 0)),
    pygame.K_LEFT: Vector((-1, 0)),
    pygame.K_DOWN: Vector((0, 1)),
    pygame.K_UP: Vector((0, -1))
}

def launch():
    pygame.init()
    screen = pygame.display.set_mode((500, 600))

    level_number = 0

    player_position = lvl_box_and_player(level_number)[1]
    massive_blocks = lvl_blocks(level_number)
    wins_position = win_position(level_number)
    boxes = lvl_box_and_player(level_number)[0]

    all_blocks1 = all_blocks()
    last_move = ""

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, WHITE, player_position)
                last_move = act(e.key)
                player_position = new_position(
                    player_position, last_move, massive_blocks
                )[0]
                player_on_box(player_position, boxes, last_move, massive_blocks)
                if check_win(boxes, wins_position):
                    level_number += 1
                    player_position = lvl_box_and_player(level_number)[1]
                    massive_blocks = lvl_blocks(level_number)
                    wins_position = win_position(level_number)
                    boxes = lvl_box_and_player(level_number)[0]
        screen.fill(BLACK)

        for i in all_blocks1:
            block = i[1]
            for x in range(block.left, block.right, bg.get_width()):
                for y in range(block.top, block.bottom, bg.get_height()):
                    screen.blit(bg, (x, y))

        if last_move in ["up", "down", "left", "right"]:
            texture = pygame.image.load(f"texture/{texture_player(last_move)}.png")
        else:
            texture = pygame.image.load("texture/player_down.png")

        for block in massive_blocks:
            for x in range(block.left, block.right, texture_block.get_width()):
                for y in range(block.top, block.bottom, texture_block.get_height()):
                    screen.blit(texture_block, (x, y))

        for win in wins_position:
            for x in range(win.left, win.right, texture_win_position_off.get_width()):
                for y in range(
                    win.top, win.bottom, texture_win_position_off.get_height()
                ):
                    screen.blit(texture_win_position_off, (x, y))

        for box in boxes:
            if box not in wins_position:
                for x in range(box.left, box.right, texture_box.get_width()):
                    for y in range(box.top, box.bottom, texture_box.get_height()):
                        screen.blit(texture_box, (x, y))
            else:
                for x in range(box.left, box.right, box_act.get_width()):
                    for y in range(box.top, box.bottom, box_act.get_height()):
                        screen.blit(box_act, (x, y))
        for x in range(
            player_position.left, player_position.right, texture.get_width()
        ):
            for y in range(
                player_position.top, player_position.bottom, texture.get_height()
            ):
                screen.blit(texture, (x, y))
        pygame.display.flip()
    pygame.quit()


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


def win_position(lvl):
    all_positions = all_blocks()
    wins = [[34, 54, 66, 85, 100, 103, 117], [69, 37]]
    m = [x[1] for x in all_positions if (x[0] - 17) in wins[lvl]]
    return m


def all_blocks():
    m = []
    i = 0
    for y in range(0, 600, 50):
        for x in range(0, 800, 50):
            i += 1
            m.append((i, pygame.Rect(x, y, 50, 50)))
    return m


def lvl_blocks(lvl):
    m1 = all_blocks()
    lvl_block = [
        [
            3,
            4,
            5,
            6,
            7,
            17,
            18,
            19,
            23,
            33,
            39,
            49,
            50,
            51,
            55,
            65,
            67,
            68,
            71,
            81,
            83,
            87,
            88,
            97,
            104,
            113,
            120,
            129,
            130,
            131,
            132,
            133,
            134,
            135,
            136,
        ],
        [
            33,
            34,
            98,
            2,
            3,
            4,
            5,
            6,
            22,
            38,
            54,
            55,
            71,
            87,
            103,
            119,
            118,
            117,
            116,
            100,
            99,
            98,
            82,
            81,
            65,
            49,
            68,
            36,
            18,
        ],
    ]
    m = [x[1] for x in m1 if (x[0] - 17) in lvl_block[lvl]]
    return m


def lvl_box_and_player(lvl):
    all_blocks_lvl = all_blocks()
    m1 = [[36, 53, 69, 98, 100, 101, 102], [67, 35]]
    boxes = m1[lvl]
    m = [x[1] for x in all_blocks_lvl if (x[0] - 17) in boxes]
    player = [all_blocks()[51][1], all_blocks_lvl[35][1]]
    return [m, player[lvl]]


def player_on_box(player_position, boxes, last_move, massive_blocks):
    for box in boxes:
        if player_position == box:
            index = new_position(
                box, last_move, massive_blocks + [x for x in boxes if x != box]
            )[1]
            if index in direction_step:
                step = direction_step[index] * -50
                player_position.move_ip(*step)

def new_position(position, command, massive_blocks):
    index = "nothing"
    if command in direction_step:
        step = direction_step[command] * 50
        position.move_ip(*step)
        if check_collision(position, massive_blocks):
            position.move_ip(*(-1 * step))
            index = command
    return position, index


def check_collision(player_position, massive_blocks):
    for block in massive_blocks:
        if player_position in block:
            return True
    return False


def act(key):
    if key == pygame.K_ESCAPE:
        exit(0)
    elif key in direction_step:
        return key
    return None


if __name__ == "__main__":
    print(launch())
