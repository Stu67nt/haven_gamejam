import asyncio
import pygame
import roulette
import button
import state


async def run(screen, Background):

    OptionsRunning = True

    # Set fonts
    OptionsFont = pygame.font.SysFont("snapitc", 50)
    ButtonFont = pygame.font.SysFont("snapitc", 30)
    ReturnFont = pygame.font.SysFont("arial", 22)

    clock = pygame.time.Clock()

    pygame.display.set_caption("Gambler's Fallacy - Options")

    # Class for all the buttons
    class Button:

        def __init__(self, text, x_pos, y_pos, enabled):
            self.text = text
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.enabled = enabled

            self.button_rect = pygame.Rect(
                self.x_pos, self.y_pos, 250, 70
            )

            self.draw()

        def draw(self):

            button_text = ButtonFont.render(
                self.text, True, (214, 160, 24)
            )

            button_rect = pygame.Rect(
                self.x_pos, self.y_pos, 250, 70
            )

            pygame.Surface.fill(screen, "black", button_rect)

            pygame.draw.rect(
                screen, "black", button_rect, 2, 5
            )

            # Centre text inside button
            text_rect = button_text.get_rect(
                center=button_rect.center
            )

            screen.blit(button_text, text_rect)


    # OPTIONS PAGE LOOP
    while OptionsRunning:

        # Draw original main.py background
        CurrentBackground = pygame.transform.smoothscale(
            Background, screen.get_size()
        )

        screen.blit(CurrentBackground, (0, 0))

        # Calculate centre position
        button_width = 250
        button_height = 70
        spacing = 25

        centre_x = screen.get_width() // 2 - button_width // 2

        total_height = (button_height * 2) + spacing

        start_y = (
            screen.get_height() // 2 - total_height // 2
        )

        # Create buttons
        Game1 = Button(
            "Game 1", centre_x, start_y, True
        )

        Game2 = Button(
            "Game 2",
            centre_x,
            start_y + button_height + spacing,
            True
        )

        # Options heading
        OptionsTitle = OptionsFont.render(
            "Options", True, (214, 160, 24)
        )

        OptionsRect = OptionsTitle.get_rect(
            center=(screen.get_width() // 2, 100)
        )

        screen.blit(OptionsTitle, OptionsRect)

        # Show the current balance (shared with the games)
        BalanceText = ButtonFont.render(f"Balance: £{state.balance}", True, (214, 160, 24))
        BestText = ButtonFont.render(f"Best: £{state.high_score}", True, (214, 160, 24))
        BalanceBox = pygame.Rect(
            40, 30,
            max(BalanceText.get_width(), BestText.get_width()) + 30,
            BalanceText.get_height() + BestText.get_height() + 24,
        )
        pygame.draw.rect(screen, (0, 0, 0), BalanceBox, 0, 8)
        pygame.draw.rect(screen, (214, 160, 24), BalanceBox, 2, 8)
        screen.blit(BalanceText, (BalanceBox.x + 15, BalanceBox.y + 8))
        screen.blit(BestText, (BalanceBox.x + 15, BalanceBox.y + 16 + BalanceText.get_height()))

        # Return instruction
        ReturnText = ReturnFont.render(
            "Press ESC to return to the main menu",
            True, "white"
        )

        ReturnRect = ReturnText.get_rect(
            center=(screen.get_width() // 2, 650)
        )

        screen.blit(ReturnText, ReturnRect)

        # Mouse position
        MouseX, MouseY = pygame.mouse.get_pos()

        # EVENT HANDLERS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    OptionsRunning = False

            # Detects mouse hovering over Game 1
            if (
                (MouseX >= Game1.x_pos and MouseX <= Game1.x_pos + 250)
                and
                (MouseY >= Game1.y_pos and MouseY <= Game1.y_pos + 70)
            ):

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if Game1.button_rect.collidepoint(event.pos):
                        await roulette.run(screen)
                        OptionsRunning = False  # back to main menu when the game exits

            # Detects mouse hovering over Game 2
            elif (
                (MouseX >= Game2.x_pos and MouseX <= Game2.x_pos + 250)
                and
                (MouseY >= Game2.y_pos and MouseY <= Game2.y_pos + 70)
            ):

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if Game2.button_rect.collidepoint(event.pos):
                        await button.run(screen)
                        OptionsRunning = False  # back to main menu when the game exits

            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    # Return to main menu
    pygame.display.set_caption("Gambler's Fallacy")
