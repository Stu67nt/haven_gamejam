
import pygame
import sys
import Options

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Set the font for the header text
HeaderFont = pygame.font.SysFont("snapitc", 50)

# Set the font for the buttons
ButtonFont = pygame.font.SysFont("snapitc", 30)

pygame.display.set_caption("Gambler's Fallacy")

# Load the background image
Background = pygame.image.load("HomePage.png").convert_alpha()

Play = True
UserBalance = -500


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

        pygame.Surface.fill(screen, 'grey', button_rect)

        pygame.draw.rect(screen, 'black', button_rect, 2, 5)

        # Centre text inside button
        text_rect = button_text.get_rect(center=button_rect.center)

        screen.blit(button_text, text_rect)


# MAIN MENU LOOP
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

    Improvements = Button("High Score", centre_x, start_y + button_height + spacing, True)


      # Header image
    HeaderImage = pygame.image.load("GamblersFallacy.png").convert()

    # Resize header image
    HeaderImage = pygame.transform.smoothscale(HeaderImage, (400, 150))

    # Centre header image at the top of the screen
    HeaderRect = HeaderImage.get_rect(center=(screen.get_width() // 2, 60))

    screen.blit(HeaderImage, HeaderRect)

    # Get mouse position
    MouseX, MouseY = pygame.mouse.get_pos()

    # Detect mouse hovering over buttons
    if (
        StartGame.button_rect.collidepoint(MouseX, MouseY)
        or Improvements.button_rect.collidepoint(MouseX, MouseY)
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

                Options.run(screen, Background)

            # HIGH SCORE BUTTON
            elif Improvements.button_rect.collidepoint(event.pos):

                pass

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
