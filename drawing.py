import pygame
import math
from consts import SCREEN_SIZE, CELL_SIZE


def drawing_frame(grid):
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_SIZE * CELL_SIZE, SCREEN_SIZE * CELL_SIZE))
    clock = pygame.time.Clock()
    running = True
    drawing = False

    for x in range(SCREEN_SIZE):
        for y in range(SCREEN_SIZE):
            grid[x][y] = 0

    def distance(x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1
        return math.sqrt(x * x + y * y)

    def paint_grid(point, size=1):
        for x in range(SCREEN_SIZE):
            for y in range(SCREEN_SIZE):
                dist = distance(point[0], point[1], x, y)
                if dist < size and dist != 0:
                    grid[x][y] += 255 / dist
                    if grid[x][y] > 255: grid[x][y] = 255
                elif dist == 0:
                    grid[x][y] = 255

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.KEYDOWN:
                running = False

        for x in range(SCREEN_SIZE):
            for y in range(SCREEN_SIZE):
                pygame.draw.rect(screen, (grid[x][y], grid[x][y], grid[x][y]),
                                 pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if drawing:
            paint_grid((int(pygame.mouse.get_pos()[0] / CELL_SIZE), int(pygame.mouse.get_pos()[1] / CELL_SIZE)), 2)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
