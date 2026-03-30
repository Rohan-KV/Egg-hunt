import pygame
import random

from maps.level3map import m3
from utils import (
    FPS,
    TILE_SIZE,
    WINDOW_SIZE,
    format_time,
    is_walkable,
    load_image,
    show_splash,
)


def run(window, clock):
    pygame.display.set_caption("Duck's Adventure - Level 3")

    grass_img = load_image("Grass.png", (TILE_SIZE, TILE_SIZE), alpha=False)
    rock_img = load_image("Rock.png", (TILE_SIZE, TILE_SIZE), alpha=False)
    duck_img = load_image("P1.png", (TILE_SIZE, TILE_SIZE))
    egg_img = load_image("Egg.png", (30, 30))
    snake_img = load_image("Snake.png", (30, 30))
    won_img = load_image("Won.png", WINDOW_SIZE, alpha=False)
    lost_img = load_image("Lost.png", WINDOW_SIZE, alpha=False)

    duck_speed = 5

    grass_tiles = [
        (x, y) for y, row in enumerate(m3) for x, col in enumerate(row) if col == "0"
    ]
    duck_x, duck_y = random.choice(grass_tiles)
    duck_x *= TILE_SIZE
    duck_y *= TILE_SIZE

    available_tiles = [tile for tile in grass_tiles if tile != (duck_x // TILE_SIZE, duck_y // TILE_SIZE)]
    egg_tiles = random.sample(available_tiles, 20)
    egg_positions = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in egg_tiles]

    snake_candidates = [tile for tile in available_tiles if tile not in egg_tiles]
    snake_tiles = random.sample(snake_candidates, 9)
    snake_positions = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in snake_tiles]

    collected_eggs = 0
    time_limit = 40
    start_time = pygame.time.get_ticks() // 1000
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        speed = duck_speed * (1.4 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1)
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            return "level_select"

        new_x = duck_x + dx * speed
        new_y = duck_y + dy * speed

        if is_walkable(m3, new_x, new_y, TILE_SIZE):
            duck_x = new_x
            duck_y = new_y

        duck_rect = pygame.Rect(duck_x, duck_y, TILE_SIZE, TILE_SIZE)
        for egg_pos in egg_positions[:]:
            egg_rect = pygame.Rect(egg_pos[0], egg_pos[1], 30, 30)
            if duck_rect.colliderect(egg_rect):
                egg_positions.remove(egg_pos)
                collected_eggs += 1
        for snake_pos in snake_positions:
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], 30, 30)
            if duck_rect.colliderect(snake_rect):
                if not show_splash(window, lost_img, clock, 2000):
                    return None
                return "level_select"

        current_time = pygame.time.get_ticks() // 1000
        elapsed_time = current_time - start_time
        time_remaining = max(time_limit - elapsed_time, 0)

        if elapsed_time >= time_limit:
            if not show_splash(window, lost_img, clock, 2000):
                return None
            return "level_select"

        if collected_eggs == 20:
            if not show_splash(window, won_img, clock, 2000):
                return None
            return "level_select"

        window.fill((0, 0, 0))
        for y, row in enumerate(m3):
            for x, col in enumerate(row):
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE

                if col == "0":
                    window.blit(grass_img, (tile_x, tile_y))
                elif col == "1":
                    window.blit(rock_img, (tile_x, tile_y))

        for egg_pos in egg_positions:
            window.blit(egg_img, egg_pos)
        for snake_pos in snake_positions:
            window.blit(snake_img, snake_pos)

        window.blit(duck_img, (duck_x, duck_y))

        time_text = f"Time: {format_time(time_remaining)}"
        eggs_text = f"Eggs: {collected_eggs}/20"
        back_text = "Press Q or Esc to go back"
        text_color = (255, 255, 255)
        window.blit(font.render(time_text, True, text_color), (20, 10))
        window.blit(font.render(back_text, True, text_color), (20, 40))
        window.blit(font.render(eggs_text, True, text_color), (20, 70))

        pygame.display.update()
        clock.tick(FPS)
