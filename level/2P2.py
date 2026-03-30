import pygame
import random

from maps.levelmap import map as level_map
from utils import (
    FPS,
    TILE_SIZE,
    WINDOW_SIZE,
    is_walkable,
    load_image,
    show_splash,
)


def run(window, clock):
    pygame.display.set_caption("Egg Hunt - Two Player")

    grass_img = load_image("Grass.png", (TILE_SIZE, TILE_SIZE), alpha=False)
    rock_img = load_image("Rock.png", (TILE_SIZE, TILE_SIZE), alpha=False)
    p1_img = load_image("P1.png", (TILE_SIZE, TILE_SIZE))
    p2_img = load_image("P2.png", (TILE_SIZE, TILE_SIZE))
    egg_img = load_image("Egg.png", (30, 30))
    snake_img = load_image("Snake.png", (30, 30))
    p1_won_img = load_image("P1Won.png", WINDOW_SIZE, alpha=False)
    p2_won_img = load_image("P2Won.png", WINDOW_SIZE, alpha=False)
    lost_img = load_image("Lost.png", WINDOW_SIZE, alpha=False)

    p1_speed = 5
    p2_speed = 5

    grass_tiles = [
        (x, y) for y, row in enumerate(level_map) for x, col in enumerate(row) if col == "0"
    ]

    p1_x, p1_y = random.choice(grass_tiles)
    p1_x *= TILE_SIZE
    p1_y *= TILE_SIZE

    p2_x, p2_y = random.choice(grass_tiles)
    p2_x *= TILE_SIZE
    p2_y *= TILE_SIZE

    available_tiles = [tile for tile in grass_tiles if tile not in [(p1_x // TILE_SIZE, p1_y // TILE_SIZE), (p2_x // TILE_SIZE, p2_y // TILE_SIZE)]]
    egg_tiles = random.sample(available_tiles, 15)
    egg_positions = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in egg_tiles]

    snake_candidates = [tile for tile in available_tiles if tile not in egg_tiles]
    snake_tiles = random.sample(snake_candidates, 11)
    snake_positions = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in snake_tiles]

    p1_eggs_collected = 0
    p2_eggs_collected = 0
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        keys = pygame.key.get_pressed()

        p1_dx, p1_dy = 0, 0
        if keys[pygame.K_LEFT]:
            p1_dx = -1
        elif keys[pygame.K_RIGHT]:
            p1_dx = 1
        elif keys[pygame.K_UP]:
            p1_dy = -1
        elif keys[pygame.K_DOWN]:
            p1_dy = 1

        p2_dx, p2_dy = 0, 0
        if keys[pygame.K_a]:
            p2_dx = -1
        elif keys[pygame.K_d]:
            p2_dx = 1
        elif keys[pygame.K_w]:
            p2_dy = -1
        elif keys[pygame.K_s]:
            p2_dy = 1

        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            return "main_menu"

        new_p1_x = p1_x + p1_dx * p1_speed
        new_p1_y = p1_y + p1_dy * p1_speed
        if is_walkable(level_map, new_p1_x, new_p1_y, TILE_SIZE):
            p1_x = new_p1_x
            p1_y = new_p1_y

        new_p2_x = p2_x + p2_dx * p2_speed
        new_p2_y = p2_y + p2_dy * p2_speed
        if is_walkable(level_map, new_p2_x, new_p2_y, TILE_SIZE):
            p2_x = new_p2_x
            p2_y = new_p2_y

        p1_rect = pygame.Rect(p1_x, p1_y, TILE_SIZE, TILE_SIZE)
        p2_rect = pygame.Rect(p2_x, p2_y, TILE_SIZE, TILE_SIZE)

        for egg_pos in egg_positions[:]:
            egg_rect = pygame.Rect(egg_pos[0], egg_pos[1], 30, 30)
            if p1_rect.colliderect(egg_rect):
                egg_positions.remove(egg_pos)
                p1_eggs_collected += 1
            elif p2_rect.colliderect(egg_rect):
                egg_positions.remove(egg_pos)
                p2_eggs_collected += 1

        for snake_pos in snake_positions:
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], 30, 30)
            if p1_rect.colliderect(snake_rect):
                if not show_splash(window, p2_won_img, clock, 2000):
                    return None
                return "main_menu"
            if p2_rect.colliderect(snake_rect):
                if not show_splash(window, p1_won_img, clock, 2000):
                    return None
                return "main_menu"

        if len(egg_positions) == 0:
            if p1_eggs_collected > p2_eggs_collected:
                if not show_splash(window, p1_won_img, clock, 2000):
                    return None
            elif p2_eggs_collected > p1_eggs_collected:
                if not show_splash(window, p2_won_img, clock, 2000):
                    return None
            else:
                if not show_splash(window, lost_img, clock, 2000):
                    return None
            return "main_menu"

        window.fill((0, 0, 0))
        for y, row in enumerate(level_map):
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

        window.blit(p1_img, (p1_x, p1_y))
        window.blit(p2_img, (p2_x, p2_y))

        text_color = (255, 255, 255)
        window.blit(font.render("P1: arrows", True, text_color), (20, 10))
        window.blit(font.render("P2: WASD", True, text_color), (20, 35))
        window.blit(font.render(f"P1 Eggs: {p1_eggs_collected}", True, text_color), (20, 60))
        window.blit(font.render(f"P2 Eggs: {p2_eggs_collected}", True, text_color), (20, 85))
        window.blit(font.render("Press Q or Esc to go back", True, text_color), (20, 110))

        pygame.display.update()
        clock.tick(FPS)
