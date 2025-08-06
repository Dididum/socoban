from copy import deepcopy
import game_functions.all_functions as af
import pygame
from numpy import genfromtxt

all_textures = af.texture_loader()
texture_block, texture_box, texture_win_position_off, box_act, bg = (
    all_textures[0],
    all_textures[1],
    all_textures[2],
    all_textures[3],
    all_textures[4],
)


def launch(true=True):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    level_number = 0
    clock = pygame.time.Clock()
    level = genfromtxt(f"levels/lvl{level_number}.csv", delimiter=";", dtype=int)
    boxes, player_position, massive_blocks, wins_position = af.level_structure(level)
    state_log = [
        [
            player_position.copy(),
            wins_position.copy(),
            deepcopy(boxes),
            massive_blocks.copy(),
        ]
    ]
    WHITE = (255, 255, 255)
    BLACK = (255, 255, 255)
    last_move = ""
    run = true
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, WHITE, player_position)
                last_move = af.act(e.key)
                if e.key == pygame.K_r:
                    level = genfromtxt(
                        f"levels/lvl{level_number}.csv", delimiter=";", dtype=int
                    )
                    boxes, player_position, massive_blocks, wins_position = (
                        af.level_structure(level)
                    )

                if e.key == pygame.K_SPACE:
                    level_number += 1
                    level = genfromtxt(
                        f"levels/lvl{level_number}.csv", delimiter=";", dtype=int
                    )
                    boxes, player_position, massive_blocks, wins_position = (
                        af.level_structure(level)
                    )

                if e.key == pygame.K_MINUS:
                    level_number -= 1
                    level = genfromtxt(
                        f"levels/lvl{level_number}.csv", delimiter=";", dtype=int
                    )
                    boxes, player_position, massive_blocks, wins_position = (
                        af.level_structure(level)
                    )

                if e.key == pygame.K_BACKSPACE:
                    if len(state_log) >= 2:
                        player_position, boxes = af.return_last_position(
                            state_log.pop(-2)
                        )
                        state_log.pop(-1)

                player_position = af.new_position(
                    player_position, last_move, massive_blocks
                )[0]
                af.player_on_box(player_position, boxes, last_move, massive_blocks)
                if level_number >= 4:
                    exit()
                print(level_number)
                if af.check_win(boxes, wins_position):
                    if level_number < 4:
                        try:
                            level_number += 1
                            level = genfromtxt(
                                f"levels/lvl{level_number}.csv",
                                delimiter=";",
                                dtype=int,
                            )
                            boxes, player_position, massive_blocks, wins_position = (
                                af.level_structure(level)
                            )
                            state_log = [
                                [
                                    player_position.copy(),
                                    wins_position.copy(),
                                    deepcopy(boxes),
                                    massive_blocks.copy(),
                                ]
                            ]
                        except FileNotFoundError:
                            print("You win")
                            print("Press any key to exit    ")
                state_log.append(
                    [
                        player_position.copy(),
                        wins_position.copy(),
                        deepcopy(boxes),
                        massive_blocks.copy(),
                    ]
                )

        screen.fill(BLACK)

        for i in af.all_blocks():
            block = i[1]
            for x in range(block.left, block.right, bg.get_width()):
                for y in range(block.top, block.bottom, bg.get_height()):
                    screen.blit(bg, (x, y))

        if last_move in ["up", "down", "left", "right"]:
            texture = pygame.image.load(f"texture/{af.texture_player(last_move)}.png")
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
