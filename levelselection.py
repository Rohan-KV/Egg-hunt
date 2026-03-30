import pygame

from utils import FPS, WINDOW_SIZE, load_image


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


def run(window, clock):
    pygame.display.set_caption("Level Selection")

    background = load_image("LevelSelection.png", WINDOW_SIZE, alpha=False)
    button_size = (150, 50)
    level1_button = load_image("Level1Button.jpg", button_size)
    level2_button = load_image("Level2Button.png", button_size)
    level3_button = load_image("Level3Button.png", button_size)
    back_button = load_image("BackButton.png", button_size)

    level1_rect = level1_button.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 100))
    level2_rect = level2_button.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    level3_rect = level3_button.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 100))
    back_rect = back_button.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 200))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(mouse_pos):
                    return "level1"
                if level2_rect.collidepoint(mouse_pos):
                    return "level2"
                if level3_rect.collidepoint(mouse_pos):
                    return "level3"
                if back_rect.collidepoint(mouse_pos):
                    return "main_menu"

        window.blit(background, (0, 0))
        _draw_button(window, level1_button, level1_rect, level1_rect.collidepoint(mouse_pos))
        _draw_button(window, level2_button, level2_rect, level2_rect.collidepoint(mouse_pos))
        _draw_button(window, level3_button, level3_rect, level3_rect.collidepoint(mouse_pos))
        _draw_button(window, back_button, back_rect, back_rect.collidepoint(mouse_pos))

        pygame.display.update()
        clock.tick(FPS)
