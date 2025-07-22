from game_functions.all_functions import *
import pygame

all_textures = texture_loader()
texture_block, texture_box, texture_win_position_off, box_act, bg = (
    all_textures[0],
    all_textures[1],
    all_textures[2],
    all_textures[3],
    all_textures[4],
)


def launch(true=True):
    pygame.init()
    screen = pygame.display.set_mode((500, 600))

    level_number = 0
    texture_point = 0
    clock = pygame.time.Clock()
    level = open(f"levels/lvl{level_number}.csv")
    count = 0
    number_player_position = []
    number_massive_blocks = []
    number_wins_position = []
    number_boxes = []
    for line in level:
        line = line.strip().split(";")
        for i in line:
            count += 1
            if i == "1":
                number_massive_blocks.append(count)
            elif i == "2":
                number_wins_position.append(count)
            elif i == "3":
                number_boxes.append(count)
            elif i == "4":
                number_player_position.append(count)
    boxes, player_position = lvl_box_and_player(number_boxes, number_player_position)
    massive_blocks = lvl_blocks(number_massive_blocks)
    wins_position = win_position(number_wins_position)
    player_position = player_position[1]

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    last_move = ""
    run = true
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, WHITE, player_position)
                last_move = act(e.key)
                if e.key == pygame.K_r:
                    level = open(f"levels/lvl{level_number}.csv")
                    count = 0
                    number_player_position = []
                    number_massive_blocks = []
                    number_wins_position = []
                    number_boxes = []
                    for line in level:
                        line = line.strip().split(";")
                        for i in line:
                            count += 1
                            if i == "1":
                                number_massive_blocks.append(count)
                            elif i == "2":
                                number_wins_position.append(count)
                            elif i == "3":
                                number_boxes.append(count)
                            elif i == "4":
                                number_player_position.append(count)
                    boxes, player_position = lvl_box_and_player(
                        number_boxes, number_player_position
                    )
                    massive_blocks = lvl_blocks(number_massive_blocks)
                    wins_position = win_position(number_wins_position)
                    player_position = player_position[1]

                if e.key == pygame.K_SPACE:
                    level_number += 1
                    player_position = lvl_box_and_player(level_number)[1]
                    massive_blocks = lvl_blocks(level_number)
                    wins_position = win_position(level_number)
                    boxes = lvl_box_and_player(level_number)[0]

                if e.key == pygame.K_MINUS:
                    level_number -= 1
                    player_position = lvl_box_and_player(level_number)[1]
                    massive_blocks = lvl_blocks(level_number)
                    wins_position = win_position(level_number)
                    boxes = lvl_box_and_player(level_number)[0]

                player_position = new_position(
                    player_position, last_move, massive_blocks
                )[0]
                player_on_box(player_position, boxes, last_move, massive_blocks)
                if level_number >= 2:
                    exit()
                if check_win(boxes, wins_position):
                    if level_number < 2:
                        try:
                            level_number += 1
                            level = open(f"levels/lvl{level_number}.csv")
                            count = 0
                            number_player_position = []
                            number_massive_blocks = []
                            number_wins_position = []
                            number_boxes = []
                            for line in level:
                                line = line.strip().split(";")
                                for i in line:
                                    count += 1
                                    if i == "1":
                                        number_massive_blocks.append(count)
                                    elif i == "2":
                                        number_wins_position.append(count)
                                    elif i == "3":
                                        number_boxes.append(count)
                                    elif i == "4":
                                        number_player_position.append(count)
                            boxes, player_position = lvl_box_and_player(
                                number_boxes, number_player_position
                            )
                            massive_blocks = lvl_blocks(number_massive_blocks)
                            wins_position = win_position(number_wins_position)
                            player_position = player_position[1]
                        except:
                            print("You win")
        screen.fill(BLACK)

        for i in all_blocks():
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
        clock.tick(165)
    pygame.quit()


if __name__ == "__main__":
    print(launch())
