# Example file showing a circle moving on screen
import pygame
import math
import random

# pgit ygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("arial", 28, bold=True)
clock = pygame.time.Clock()
running = True
dt = 0

def draw_sliced_circle(surface, centre, radius, num_slices, angle_offset=0):
    cx, cy = centre
    angle_step = (2 * math.pi) / num_slices

    for i in range(num_slices):
        # Alternate between red and black
        if i == 0:
            colour = "green"
        elif i % 2 == 1:
            colour = "red"
        else:
            colour = "black"

        # Add angle_offset to rotate the entire wheel
        start_angle = i * angle_step + angle_offset
        end_angle = (i + 1) * angle_step + angle_offset


        # Start the polygon at the centre of the circle
        points = [centre]

        # Add points along the curved outer edge for a smooth arc
        steps = 20
        for s in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * (s / steps)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(surface, colour, points)

current_angle = 0.0
spin_speed = 0.0
friction = 0.95

balance = 100
bet_amount = 10
selected_colour = "red"  # "red", "black", or "green"
status_message = "Choose a colour, adjust your bet, and press SPACE!"

# Circle attributes
centre = screen.get_width() // 2, screen.get_height() // 2
radius = 120
sample_pix = (screen.get_width() // 2, (screen.get_height() // 2) - radius)


while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and spin_speed == 0:
            # Select colour
            if event.key == pygame.K_1:
                selected_colour = "red"
            elif event.key == pygame.K_2:
                selected_colour = "black"
            elif event.key == pygame.K_3:
                selected_colour = "green"

            # Adjust bet amount
            elif event.key == pygame.K_UP:
                if bet_amount + 10 <= balance:
                    bet_amount += 10
            elif event.key == pygame.K_DOWN:
                if bet_amount - 10 >= 10:
                    bet_amount -= 10
            elif event.key == pygame.K_SPACE:
                # Random initial speed (radians per frame)
                if bet_amount <= balance:
                    balance -= bet_amount
                    spin_speed = random.uniform(0.25, 0.45)
                else:
                    status_message = "Your broke bitch"
        if event.type == pygame.QUIT:
            running = False

    if spin_speed > 0:
        current_angle += spin_speed
        spin_speed *= friction

        # Stop completely when the wheel slows to a crawl
        if spin_speed < 0.0005:
            spin_speed = 0
            pixel_colour = screen.get_at((sample_pix[0], sample_pix[1]+1))
            if pixel_colour == pygame.Color("green"):
                landed = "green"
            if pixel_colour == pygame.Color("red"):
                landed = "red"
            if pixel_colour == pygame.Color("black"):
                landed = "black"

            if landed == selected_colour:
                multiplier = 14 if landed == "green" else 2
                winnings = bet_amount * multiplier
                balance += winnings
                status_message = (
                    f"Landed on {landed.upper()}! You won £{winnings}!"
                )
            else:
                status_message = (
                    f"Landed on {landed.upper()}. You lost £{bet_amount}."
                )

        # Cap bet_amount if balance dropped below current bet
        if bet_amount > balance and balance >= 10:
            bet_amount = balance

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    balance_text = font.render(f"Balance: £{balance}", True, "white")
    bet_text = font.render(
        f"Bet: £{bet_amount}   |   Choice: {selected_colour.upper()}",
        True,
        "yellow",
    )
    status_text = font.render(status_message, True, "white")
    controls_text = font.render(
        "Controls: [1] Red (2x)   [2] Black (2x)   [3] Green (14x)   [UP/DOWN] Bet Size   [SPACE] Spin",
        True,
        "lightgrey",
    )

    screen.blit(balance_text, (40, 30))
    screen.blit(bet_text, (40, 70))
    screen.blit(status_text, (centre[0] - status_text.get_width() // 2, centre[1] + radius + 50))
    screen.blit(controls_text, (    centre[0] - controls_text.get_width() // 2, centre[1] + radius + 100))

    keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, "black",radius = radius+10, center=centre)
    draw_sliced_circle(screen, centre=centre, radius=radius, num_slices=24, angle_offset= current_angle)
    pygame.draw.polygon(screen, "white", [sample_pix, (sample_pix[0]-10, sample_pix[1]-10), (sample_pix[0]+10, sample_pix[1]-10)])
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()