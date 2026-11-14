import random
import pygame

pygame.init()

screen = pygame.display.set_mode((900, 400))
pygame.display.set_caption("Snail Race")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

start_x = 60
finish_x = 800
lane_y_positions = [55, 130, 205, 280]
snail_colors = [
    ((80, 170, 90), (190, 120, 55)),
    ((80, 130, 210), (220, 150, 70)),
    ((220, 100, 100), (160, 100, 180)),
    ((220, 180, 60), (100, 150, 100)),
]


def new_race():
    return [
        {"x": start_x, "y": y}
        for y in lane_y_positions
    ]


snails = new_race()
winner = None
balance = 100
bet_amount = 10
selected_snail = 0
game_state = "betting"
result_message = ""
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == "betting":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    selected_snail = event.key - pygame.K_1
                elif event.key == pygame.K_UP:
                    bet_amount = min(balance, bet_amount + 10)
                elif event.key == pygame.K_DOWN:
                    bet_amount = max(1, bet_amount - 10)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if 0 < bet_amount <= balance:
                        balance -= bet_amount
                        snails = new_race()
                        winner = None
                        game_state = "racing"
            elif game_state == "result":
                if event.key == pygame.K_r and balance > 0:
                    selected_snail = 0
                    bet_amount = min(10, balance)
                    snails = new_race()
                    game_state = "betting"
                elif event.key == pygame.K_n:
                    balance = 100
                    bet_amount = 10
                    selected_snail = 0
                    snails = new_race()
                    game_state = "betting"

    if game_state == "racing":
        finishers = []
        for index, snail in enumerate(snails):
            old_x = snail["x"]
            speed = random.uniform(0.5, 4.0)
            snail["x"] += speed
            if snail["x"] + 54 >= finish_x:
                distance = finish_x - 54 - old_x
                finishers.append((distance / speed, index))

        if finishers:
            winner = min(finishers)[1]
            if winner == selected_snail:
                winnings = bet_amount * 4
                balance += winnings
                result_message = f"You won! {winnings} coins returned (4x your bet)."
            else:
                result_message = (
                    f"You lost {bet_amount} coins. Snail {winner + 1} won."
                )
            game_state = "result"

    screen.fill((238, 232, 205))
    for y in lane_y_positions:
        pygame.draw.line(screen, (190, 185, 165), (0, y + 55), (900, y + 55), 2)

    pygame.draw.line(screen, (40, 150, 70), (start_x, 35), (start_x, 365), 4)
    pygame.draw.line(screen, (210, 45, 45), (finish_x, 35), (finish_x, 365), 5)

    if game_state == "betting":
        status = f"Coins: {balance}    Bet: {bet_amount}    Selected: Snail {selected_snail + 1}"
        instructions = "Press 1-4 to choose | Up/Down changes bet | Enter to race"
    elif game_state == "racing":
        status = f"Racing! You bet {bet_amount} coins on Snail {selected_snail + 1}"
        instructions = "Each snail's speed changes as it races."
    else:
        status = result_message
        instructions = (
            "Press R to bet again | N for a new game | Esc to quit"
            if balance > 0
            else "You're out of coins. Press N for a new game."
        )

    screen.blit(font.render(status, True, (20, 20, 20)), (12, 8))
    screen.blit(small_font.render(instructions, True, (50, 50, 50)), (12, 38))

    for snail, colors in zip(snails, snail_colors):
        x = snail["x"]
        y = snail["y"]
        body_color, shell_color = colors

        if game_state == "betting" and snail == snails[selected_snail]:
            pygame.draw.rect(screen, (40, 100, 220), (start_x - 10, y + 5, 70, 42), 2)

        pygame.draw.ellipse(screen, body_color, (x, y + 20, 42, 18))
        pygame.draw.circle(screen, shell_color, (x + 25, y + 22), 13)
        pygame.draw.circle(screen, (245, 220, 150), (x + 25, y + 22), 8, 2)
        pygame.draw.circle(screen, body_color, (x + 43, y + 18), 8)
        pygame.draw.circle(screen, (255, 255, 255), (x + 45, y + 15), 3)
        pygame.draw.circle(screen, (20, 20, 20), (x + 46, y + 15), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

