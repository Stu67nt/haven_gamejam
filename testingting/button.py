# Example file showing a circle moving on screen
import pygame
import math
import random
import state
import gameover
import asyncio

async def run(screen):
    font = pygame.font.SysFont("arial", 28, bold=True)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    status_message = ""
    balance = state.balance  # pick up the shared balance
    bet_amount = 10
    if bet_amount > balance and balance >= 10:
        bet_amount = balance

    # Circle attributes
    centre = screen.get_width() // 2, screen.get_height() // 2
    radius = 120


    while running:
        for event in pygame.event.get():
            # Adjust bet amount
            if event.type == pygame.KEYDOWN:
                # Exit back to the menu
                if event.key == pygame.K_ESCAPE:
                    state.balance = balance  # hand the balance back
                    return
                elif event.key == pygame.K_UP:
                    if bet_amount + 10 <= balance:
                        bet_amount += 10
                elif event.key == pygame.K_DOWN:
                    if bet_amount - 10 >= 10:
                        bet_amount -= 10
                elif event.key == pygame.K_SPACE:
                    if bet_amount <= balance:
                        balance -= bet_amount
                        roll = random.randint(1, 10)
                        if roll == 1:
                            balance += 10
                            status_message = "you won!"
                        else:
                            status_message = "you lost!"
                    else:
                        status_message = "Your broke bitch"
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


            # Cap bet_amount if balance dropped below current bet
            if bet_amount > balance and balance >= 10:
                bet_amount = balance

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        balance_text = font.render(f"Balance: £{balance}", True, "white")
        bet_text = font.render(
            f"Bet: £{bet_amount}",
            True,
            "yellow",
        )
        status_text = font.render(status_message, True, "white")
        controls_text = font.render(
            "Controls:[UP/DOWN] Bet Size   [SPACE] Press the button   [ESC] Menu",
            True,
            "lightgrey",
        )

        screen.blit(balance_text, (40, 30))
        screen.blit(bet_text, (40, 70))
        screen.blit(status_text, (centre[0] - status_text.get_width() // 2, centre[1] + radius + 50))
        screen.blit(controls_text, (centre[0] - controls_text.get_width() // 2, centre[1] + radius + 100))

        keys = pygame.key.get_pressed()

        pygame.draw.circle(screen, "grey", radius=radius + 10, center=centre)
        pygame.draw.circle(screen, "red",radius = radius, center=centre)

        if balance <= 0:
            await asyncio.sleep(1)
            await gameover.run(screen)
            return

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

        state.balance = balance
        state.update_highscore()

        if balance <= 0:
            await asyncio.sleep(1)
            await gameover.run(screen)
            return
