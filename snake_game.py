import pygame as pg
from random import randrange

WINDOW = 600
TILE_SIZE = 20
GRID_SIZE = WINDOW // TILE_SIZE
RANGE = (1, GRID_SIZE - 1)
get_random_position = lambda: randrange(*RANGE) * TILE_SIZE

snake = [pg.Rect(get_random_position(), get_random_position(), TILE_SIZE, TILE_SIZE)]
food = pg.Rect(get_random_position(), get_random_position(), TILE_SIZE, TILE_SIZE)
direction = pg.Vector2(1, 0)
new_segment = False

score = 0

pg.init()
screen = pg.display.set_mode((WINDOW, WINDOW))
clock = pg.time.Clock()

font = pg.font.Font(None, 36)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_UP] and direction.y != 1:
        direction.xy = 0, -1
    elif keys[pg.K_DOWN] and direction.y != -1:
        direction.xy = 0, 1
    elif keys[pg.K_LEFT] and direction.x != 1:
        direction.xy = -1, 0
    elif keys[pg.K_RIGHT] and direction.x != -1:
        direction.xy = 1, 0

    snake_head = snake[0].move(direction.x * TILE_SIZE, direction.y * TILE_SIZE)

    if not pg.Rect(0, 0, WINDOW, WINDOW).colliderect(snake_head):
        pg.quit()
        exit()

    if snake_head.colliderect(food):
        food.topleft = get_random_position(), get_random_position()
        new_segment = True
        score += 1

    snake.insert(0, snake_head)
    if not new_segment:
        snake.pop()

    new_segment = False

    for segment in snake[1:]:
        if segment.colliderect(snake_head):
            pg.quit()
            exit()

    screen.fill('black')
    [pg.draw.rect(screen, 'green', segment) for segment in snake]
    pg.draw.rect(screen, 'red', food)

    score_text = font.render(f"Score: {score}", True, 'white')
    screen.blit(score_text, (10, 10))

    pg.display.flip()
    clock.tick(10)