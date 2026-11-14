import os


# Shared game state. Lives in memory only, so it resets every time the game launches.
balance = 100
def reset():
    global balance
    balance = 100

HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")


def load_highscore():
    try:
        with open(HIGHSCORE_FILE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


high_score = max(load_highscore(), balance)


def update_highscore():
    global high_score
    if balance > high_score:
        high_score = balance
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(high_score))
        except OSError:
            pass