import pygame


def launch(true=True):
    pygame.init()
    screen = pygame.display.set_mode((500, 600))

    texture = pygame.image.load("texture_player3.jpg")
    texture_potato = pygame.image.load("potato.jpg")

    player_position = lvl_box_and_player()[1]

    boxes = lvl_box_and_player()[0]
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    massive_blocks = lvl_blocks()
    wins_position = win_position()
    run = true
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                pygame.draw.rect(screen, BLACK, player_position)
                last_move = act(e.key)
                player_position = new_position(
                    player_position, last_move, massive_blocks
                )[0]
                player_on_box(player_position, boxes, last_move, massive_blocks)
                check_win(boxes, wins_position)
        screen.fill(BLACK)
        for i in massive_blocks:
            pygame.draw.rect(screen, (0, 0, 255), i)

        for win in wins_position:
            pygame.draw.rect(screen, (255, 0, 0), win)

        for box in boxes:
            for x in range(box.left, box.right, texture.get_width()):
                for y in range(box.top, box.bottom, texture.get_height()):
                    screen.blit(texture_potato, (x, y))

        for x in range(
            player_position.left, player_position.right, texture.get_width()
        ):
            for y in range(
                player_position.top, player_position.bottom, texture.get_height()
            ):
                screen.blit(texture, (x, y))
        pygame.display.flip()
    pygame.quit()


def check_win(boxes, wins_position):
    if all(box in wins_position for box in boxes):
        print("You won!")


def win_position():
    all_positions = all_blocks()
    wins = [34, 54, 66, 85, 100, 103, 117]
    m = [x[1] for x in all_positions if (x[0] - 17) in wins]
    return m


def all_blocks():
    m = []
    i = 0
    for y in range(0, 600, 50):
        for x in range(0, 800, 50):
            i += 1
            m.append((i, pygame.Rect(x, y, 50, 50)))
    return m


def lvl_blocks():
    m1 = all_blocks()
    lvl_1 = [
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
    ]
    m = [x[1] for x in m1 if (x[0] - 17) in lvl_1]
    return m


def lvl_box_and_player():
    m1 = all_blocks()
    boxes = [36, 53, 69, 98, 100, 101, 102]
    m = [x[1] for x in m1 if (x[0] - 17) in boxes]
    player = all_blocks()[51][1]
    return [m, player]


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
    if key == pygame.K_UP:
        print("up")
        return "up"
    elif key == pygame.K_DOWN:
        print("down")
        return "down"
    elif key == pygame.K_LEFT:
        print("left")
        return "left"
    elif key == pygame.K_RIGHT:
        print("right")
        return "right"
    elif key == pygame.K_ESCAPE:
        exit(0)
    return None


if __name__ == "__main__":
    print(launch())
