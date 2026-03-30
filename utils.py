import os
import pygame

IMG_DIR = "img"
WINDOW_SIZE = (1366, 768)
FPS = 60
TILE_SIZE = 50


def load_image(name, size=None, alpha=True):
    path = os.path.join(IMG_DIR, name)
    image = pygame.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image


def is_walkable(grid, new_x, new_y, tile_size):
    if new_x < 0 or new_y < 0:
        return False
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    grid_x = new_x // tile_size
    grid_y = new_y // tile_size
    if grid_x < 0 or grid_y < 0 or grid_x >= cols or grid_y >= rows:
        return False
    return grid[grid_y][grid_x] in ("0", "3")


def format_time(seconds):
    return f"{int(seconds // 60):02}:{int(seconds % 60):02}"


def show_splash(window, image, clock, duration_ms):
    end_time = pygame.time.get_ticks() + duration_ms
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        window.blit(image, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return True
