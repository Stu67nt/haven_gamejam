
import pygame
import sys
import Options
import state
import asyncio

pygame.init()

pygame.mixer.music.load("bgm.ogg")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Set the font for the header text
HeaderFont = pygame.font.SysFont("snapitc", 50)

# Set the font for the buttons
ButtonFont = pygame.font.SysFont("snapitc", 30)

pygame.display.set_caption("Gambler's Fallacy")

# Load the background image
Background = pygame.image.load("HomePage.png").convert_alpha()



# Class for all the buttons in the game
class Button:

    def __init__(self, text, x_pos, y_pos, enabled):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled

        self.button_rect = pygame.Rect(self.x_pos, self.y_pos, 250, 70)

        self.draw()

    def draw(self):

        button_text = ButtonFont.render(self.text, True, (214, 160, 24))

        button_rect = pygame.Rect(self.x_pos, self.y_pos, 250, 70)

        pygame.Surface.fill(screen, 'black', button_rect)

        pygame.draw.rect(screen, 'black', button_rect, 2, 5)

        # Centre text inside button
        text_rect = button_text.get_rect(center=button_rect.center)

        screen.blit(button_text, text_rect)


# MAIN MENU LOOP
async def main():
    Play = True
    while Play:

        # Scale background to fit screen
        CurrentBackground = pygame.transform.smoothscale(Background, screen.get_size())

        screen.blit(CurrentBackground, (0, 0))

        # Calculate centre position
        button_width = 250
        button_height = 70
        spacing = 25

        centre_x = screen.get_width() // 2 - button_width // 2

        total_height = (button_height * 2) + spacing

        start_y = (screen.get_height() // 2 - total_height // 2)

        # Buttons
        StartGame = Button("Start Game", centre_x, start_y, True)

        HeaderImage = pygame.image.load("GamblersFallacy.png").convert_alpha()

        # Crop away the empty transparent space around the text
        HeaderImage = HeaderImage.subsurface(HeaderImage.get_bounding_rect()).copy()

        # Resize header image (keeping its original proportions)
        HeaderWidth = 500
        HeaderHeight = int(HeaderImage.get_height() * HeaderWidth / HeaderImage.get_width())
        HeaderImage = pygame.transform.smoothscale(HeaderImage, (HeaderWidth, HeaderHeight))

        # Centre header image at the top of the screen
        HeaderRect = HeaderImage.get_rect(center=(screen.get_width() // 2, 60))

        screen.blit(HeaderImage, HeaderRect)

        # Show the current balance (shared with the games)
        BalanceText = ButtonFont.render(f"Balance: £{state.balance}", True, (214, 160, 24))
        BalanceBox = BalanceText.get_rect(topleft=(40, 30)).inflate(30, 16)
        pygame.draw.rect(screen, (0, 0, 0), BalanceBox, 0, 8)
        pygame.draw.rect(screen, (214, 160, 24), BalanceBox, 2, 8)
        screen.blit(BalanceText, BalanceText.get_rect(center=BalanceBox.center))

        # Get mouse position
        MouseX, MouseY = pygame.mouse.get_pos()

        # Detect mouse hovering over buttons
        if (
            StartGame.button_rect.collidepoint(MouseX, MouseY)
        ):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # EVENT HANDLERS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                Play = False

            # Detect mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # START GAME BUTTON
                if (
                    MouseX >= StartGame.x_pos
                    and MouseX <= StartGame.x_pos + 250
                    and MouseY >= StartGame.y_pos
                    and MouseY <= StartGame.y_pos + 70
                    and StartGame.button_rect.collidepoint(event.pos)
                ):

                    await Options.run(screen, Background)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())