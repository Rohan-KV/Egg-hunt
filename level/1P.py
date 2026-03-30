import pygame
import sys
import os
import random
from maps.levelmap import map

pygame.init()
window_size = (1366, 768)
window = pygame.display.set_mode(window_size)
img_folder = "img"
egg_path = os.path.join(img_folder, "Egg.png")
duck_path = os.path.join(img_folder, "P1.png")
snake_path = os.path.join(img_folder, "Snake.png")
won_path = os.path.join(img_folder, "Won.png")
lost_path = os.path.join(img_folder, "Lost.png")
pygame.display.set_caption("Duck's Adventure")

grass_img = pygame.image.load(os.path.join(img_folder, "Grass.png"))
grass_img = pygame.transform.scale(grass_img, (50, 50))

rock_img = pygame.image.load(os.path.join(img_folder, "Rock.png"))
rock_img = pygame.transform.scale(rock_img, (50, 50))

duck_img = pygame.image.load(duck_path) 
duck_img = pygame.transform.scale(duck_img, (50, 50))

egg_img = pygame.image.load(egg_path)
egg_img = pygame.transform.scale(egg_img, (30, 30))

won_img = pygame.image.load(won_path)
won_img = pygame.transform.scale(won_img, window_size)

lost_img = pygame.image.load(lost_path)
lost_img = pygame.transform.scale(lost_img, window_size)

snake_img = pygame.image.load(snake_path)
snake_img = pygame.transform.scale(snake_img, (30,30))

duck_speed = 5
tile_size = 50
clock = pygame.time.Clock()

grass_tiles = [(x, y) for y, row in enumerate(map[:-1]) for x, col in enumerate(row) if col == "0"]

duck_x, duck_y = random.choice(grass_tiles)
duck_x *= tile_size
duck_y *= tile_size

egg_positions = random.sample(grass_tiles, 19)
egg_positions = [(x * tile_size, y * tile_size) for x, y in egg_positions]

snake_positions = random.sample(grass_tiles, 11)
snake_positions = [(x * tile_size, y * tile_size) for x, y in snake_positions]

collected_eggs = 0
win_flag = False

time_limit = 60
start_time = pygame.time.get_ticks() // 1000

while not win_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    elif keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    elif keys[pygame.K_q]:
        pygame.quit()
        exec(open("main.py").read())
        sys.exit()


    new_x = duck_x + dx * duck_speed
    new_y = duck_y + dy * duck_speed

    if map[new_y // tile_size][new_x // tile_size] in ["0", "3"]:
        duck_x = new_x
        duck_y = new_y

    duck_rect = pygame.Rect(duck_x, duck_y, 50, 50)
    for egg_pos in egg_positions[:]:
        egg_rect = pygame.Rect(egg_pos[0], egg_pos[1], 30, 30)
        if duck_rect.colliderect(egg_rect):
            egg_positions.remove(egg_pos)
            collected_eggs += 1
    for snake_pos in snake_positions[:]:
        snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], 30, 30)
        if duck_rect.colliderect(snake_rect):
             window.blit(lost_img, (0, 0))
             pygame.display.update()
             pygame.time.delay(2000)
             pygame.quit()
             exec(open("main.py").read())
             sys.exit()

    current_time = pygame.time.get_ticks() // 1000
    elapsed_time = current_time - start_time
    time_remaining = max(time_limit - elapsed_time, 0)

    if elapsed_time >= time_limit:
        window.blit(lost_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        exec(open("main.py").read())
        sys.exit()

    if collected_eggs == 19:
        window.blit(won_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        exec(open("main.py").read())
        sys.exit()
        

    window.fill((0, 0, 0))
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            tile_x = x * tile_size
            tile_y = y * tile_size

            if col == "0":
                window.blit(grass_img, (tile_x, tile_y))
            elif col == "1":
                window.blit(rock_img, (tile_x, tile_y))

    for egg_pos in egg_positions:
        window.blit(egg_img, egg_pos)
    for snake_pos in snake_positions:
        window.blit(snake_img, snake_pos)

    window.blit(duck_img, (duck_x, duck_y))

    time_text = f"Time remaining: {int(time_remaining // 60):02}:{int(time_remaining % 60):02}"
    back_text = f"Press Q to go Back"
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    text_surface = font.render(time_text, True, text_color)
    text_surface2 = font.render(back_text, True, text_color)
    window.blit(text_surface2, (40, 40))
    window.blit(text_surface, (10, 10))

    pygame.display.update()
    clock.tick(60)
