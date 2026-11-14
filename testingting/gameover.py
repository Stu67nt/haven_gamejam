import os
import pygame
import state
import asyncio

async def run(screen):
    TitleFont = pygame.font.SysFont("snapitc", 80)
    ButtonFont = pygame.font.SysFont("snapitc", 30)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Gambler's Fallacy - Game Over")

    # Play the sound effect (skipped quietly if the file or audio device is missing)
    try:
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oof.ogg")
        pygame.mixer.Sound(sound_path).play()
    except (pygame.error, FileNotFoundError):
        pass

    while True:
        screen.fill((40, 0, 0))

        # Game over title
        title = TitleFont.render("GAME OVER", True, (214, 160, 24))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100)))

        # Reset button
        button_rect = pygame.Rect(0, 0, 250, 70)
        button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 40)

        pygame.Surface.fill(screen, "grey", button_rect)
        pygame.draw.rect(screen, "black", button_rect, 2, 5)

        button_text = ButtonFont.render("Reset Game", True, (214, 160, 24))
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Hand cursor when hovering the button
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    state.reset()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    pygame.display.set_caption("Gambler's Fallacy")
                    return

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
