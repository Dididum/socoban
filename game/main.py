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
    clock = pygame.time.Clock()
    level = open(f"levels/lvl{level_number}.csv")
    boxes, player_position, massive_blocks, wins_position = level_structure(level)

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
                    boxes, player_position, massive_blocks, wins_position = (
                        level_structure(level)
                    )

                if e.key == pygame.K_SPACE:
                    level_number += 1
                    level = open(f"levels/lvl{level_number}.csv")
                    boxes, player_position, massive_blocks, wins_position = (
                        level_structure(level)
                    )

                if e.key == pygame.K_MINUS:
                    level_number -= 1
                    level = open(f"levels/lvl{level_number}.csv")
                    boxes, player_position, massive_blocks, wins_position = (
                        level_structure(level)
                    )

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
                            boxes, player_position, massive_blocks, wins_position = (
                                level_structure(level)
                            )
                        except:
                            print("You win")
                            print("Press any key to exit    ")
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
