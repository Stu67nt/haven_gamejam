import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()

Play = True
while Play:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Play = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
