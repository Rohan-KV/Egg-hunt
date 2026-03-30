import pygame

import levelselection
from utils import FPS, WINDOW_SIZE, load_image
from level import level1, level2, level3
import importlib.util
import os


def _load_two_player_snake():
    path = os.path.join("level", "2P2.py")
    spec = importlib.util.spec_from_file_location("two_player_snake", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _draw_button(window, image, rect, hover):
    if hover:
        scaled = pygame.transform.smoothscale(
            image, (int(rect.w * 1.06), int(rect.h * 1.06))
        )
        scaled_rect = scaled.get_rect(center=rect.center)
        window.blit(scaled, scaled_rect.topleft)
        pygame.draw.rect(window, (255, 230, 120), scaled_rect, 2)
    else:
        window.blit(image, rect.topleft)


def main_menu(window, clock):
    pygame.display.set_caption("Main Menu")

    background_img = load_image("Mainmenu.png", WINDOW_SIZE, alpha=False)
    single_player_img = load_image("1P.png", (200, 50))
    two_players_img = load_image("2P.png", (200, 50))
    quit_button_img = load_image("QuitButton.png", (200, 50))

    single_player_rect = single_player_img.get_rect(center=(WINDOW_SIZE[0] // 2, 320))
    two_players_rect = two_players_img.get_rect(center=(WINDOW_SIZE[0] // 2, 420))
    quit_button_rect = quit_button_img.get_rect(center=(WINDOW_SIZE[0] // 2, 520))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_rect.collidepoint(mouse_pos):
                    return "level_select"
                if two_players_rect.collidepoint(mouse_pos):
                    return "two_player_snake"
                if quit_button_rect.collidepoint(mouse_pos):
                    return None

        window.blit(background_img, (0, 0))
        _draw_button(window, single_player_img, single_player_rect, single_player_rect.collidepoint(mouse_pos))
        _draw_button(window, two_players_img, two_players_rect, two_players_rect.collidepoint(mouse_pos))
        _draw_button(window, quit_button_img, quit_button_rect, quit_button_rect.collidepoint(mouse_pos))

        pygame.display.update()
        clock.tick(FPS)

    return None


def run():
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    two_player_snake = _load_two_player_snake()

    scene = "main_menu"
    while scene:
        if scene == "main_menu":
            scene = main_menu(window, clock)
        elif scene == "level_select":
            scene = levelselection.run(window, clock)
        elif scene == "level1":
            scene = level1.run(window, clock)
        elif scene == "level2":
            scene = level2.run(window, clock)
        elif scene == "level3":
            scene = level3.run(window, clock)
        elif scene == "two_player_snake":
            scene = two_player_snake.run(window, clock)
        else:
            scene = None

    pygame.quit()


if __name__ == "__main__":
    run()
