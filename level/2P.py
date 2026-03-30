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
p1_path = os.path.join(img_folder, "P1.png")
p2_path = os.path.join(img_folder, "P2.png")
p1_won_path = os.path.join(img_folder, "P1Won.png")  
p2_won_path = os.path.join(img_folder, "P2Won.png") 
lost_path = os.path.join(img_folder, "Lost.png")
snake_path = os.path.join(img_folder,"Snake.png")
snake_path = os.path.join(img_folder,"Snake.png")
pygame.display.set_caption("Duck's Adventure")


grass_img = pygame.image.load(os.path.join(img_folder, "Grass.png"))
grass_img = pygame.transform.scale(grass_img, (50, 50))

rock_img = pygame.image.load(os.path.join(img_folder, "Rock.png"))
rock_img = pygame.transform.scale(rock_img, (50, 50))

p1_img = pygame.image.load(p1_path)
p1_img = pygame.transform.scale(p1_img, (50, 50))

p2_img = pygame.image.load(p2_path)
p2_img = pygame.transform.scale(p2_img, (50, 50))

egg_img = pygame.image.load(egg_path)
egg_img = pygame.transform.scale(egg_img, (30, 30))

p1_won_img = pygame.image.load(p1_won_path) 
p1_won_img = pygame.transform.scale(p1_won_img, window_size)

p2_won_img = pygame.image.load(p2_won_path) 
p2_won_img = pygame.transform.scale(p2_won_img, window_size)

lost_img = pygame.image.load(lost_path)
lost_img = pygame.transform.scale(lost_img, window_size)

snake_img = pygame.image.load(snake_path)
snake_img = pygame.transform.scale(snake_img, (30,30))

p1_speed = 5
p2_speed = 5
tile_size = 50
clock = pygame.time.Clock()

grass_tiles = [(x, y) for y, row in enumerate(map[:-1]) for x, col in enumerate(row) if col == "0"]

p1_x, p1_y = random.choice(grass_tiles)
p1_x *= tile_size
p1_y *= tile_size

p2_x, p2_y = random.choice(grass_tiles)
p2_x *= tile_size
p2_y *= tile_size

egg_positions = random.sample(grass_tiles, 15)
egg_positions = [(x * tile_size, y * tile_size) for x, y in egg_positions]

p1_eggs_collected = 0
p2_eggs_collected = 0
win_flag = False


while not win_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    
    new_p1_x = p1_x + p1_dx * p1_speed
    new_p1_y = p1_y + p1_dy * p1_speed

    if map[new_p1_y // tile_size][new_p1_x // tile_size] in ["0", "3"]:
        p1_x = new_p1_x
        p1_y = new_p1_y

    
    new_p2_x = p2_x + p2_dx * p2_speed
    new_p2_y = p2_y + p2_dy * p2_speed

    if map[new_p2_y // tile_size][new_p2_x // tile_size] in ["0", "3"]:
        p2_x = new_p2_x
        p2_y = new_p2_y

    p1_rect = pygame.Rect(p1_x, p1_y, 50, 50)
    p2_rect = pygame.Rect(p2_x, p2_y, 50, 50)

    for egg_pos in egg_positions[:]:
        egg_rect = pygame.Rect(egg_pos[0], egg_pos[1], 30, 30)
        if p1_rect.colliderect(egg_rect):
            egg_positions.remove(egg_pos)
            p1_eggs_collected += 1
        elif p2_rect.colliderect(egg_rect):
            egg_positions.remove(egg_pos)
            p2_eggs_collected += 1


    if len(egg_positions) == 0:
        win_flag = True

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

    window.blit(p1_img, (p1_x, p1_y))
    window.blit(p2_img, (p2_x, p2_y))

    pygame.display.update()
    clock.tick(60)

if p1_eggs_collected > p2_eggs_collected: 
    window.blit(p1_won_img, (0, 0))
elif p2_eggs_collected > p1_eggs_collected: 
    window.blit(p2_won_img, (0, 0))
else: 
    window.blit((0, 0))  

pygame.display.update()
pygame.time.delay(2000)
exec(open("main.py").read())
pygame.quit()
sys.exit()
