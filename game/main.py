import pygame


def launch(true=True):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    texture = pygame.image.load("texture_player3.jpg")
    texture_potato = pygame.image.load("potato.jpg")

    player_position = pygame.Rect(150, 250, 50, 50)
    box = pygame.Rect(250, 350, 50, 50)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    massive_blocks = blocks()
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
                )
                player_on_box(player_position, box, last_move)

        screen.fill(BLACK)
        for i in massive_blocks:
            pygame.draw.rect(screen, WHITE, i)

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


def blocks():
    block1 = pygame.Rect(50, 100, 150, 50)
    block2 = pygame.Rect(150, 50, 250, 50)
    block3 = pygame.Rect(350, 100, 50, 250)
    block4 = pygame.Rect(50, 100, 50, 400)
    block5 = pygame.Rect(50, 450, 350, 50)
    block6 = pygame.Rect(400, 300, 50, 200)
    m = [block1, block2, block3, block4, block5, block6]
    return m


def player_on_box(player_position, box, last_move):
    if player_position == box:
        new_position(box, last_move)


def new_position(position, command, massive_blocks):
    if command == "down":
        position.move_ip(0, 50)
        if check_collision(position, massive_blocks):
            position.move_ip(0, -50)
    elif command == "up":
        position.move_ip(0, -50)
        if check_collision(position, massive_blocks):
            position.move_ip(0, 50)
    elif command == "left":
        position.move_ip(-50, 0)
        if check_collision(position, massive_blocks):
            position.move_ip(50, 0)
    elif command == "right":
        position.move_ip(50, 0)
        if check_collision(position, massive_blocks):
            position.move_ip(-50, 0)
    return position


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


def barriers(block_position, player_position, last_move):
    if block_position == player_position:
        if last_move == "up":
            player_position.move_ip(0, 50)
    return player_position


if __name__ == "__main__":
    print(launch())
