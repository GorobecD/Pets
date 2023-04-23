import copy

import pygame
import sys
from block import Block
import gameLogic
import numpy as np


def prepare_blocks(screen):
    """blocks:
    0 - sandy
    1 - yellow
    2 - red
    3 - blue
    4 - green
    """
    blocks = [Block(screen) for i in range(5)]
    blocks[0].set_block_color("sandy_block.png")
    blocks[1].set_block_color("yellow_block.png")
    blocks[2].set_block_color("red_block.png")
    blocks[3].set_block_color("blue_block.png")
    blocks[4].set_block_color("green_block.png")

    return blocks


def draw_grid(matrix, blocks):
    blocks_grid = []
    matrix = matrix.tolist()

    for i in range(16):
        for j in range(10):
            value = matrix[i][j]

            if value != 0:
                new_block = copy.copy(blocks[value - 1])
                new_block.set_xy_position(50 * j, 50 * (i + 1))
                new_block.set_xy_index(i, j)

                new_block.output()

                blocks_grid.append(new_block)

    return blocks_grid


def get_box_indexes(grid):
    pos = pygame.mouse.get_pos()
    for i in grid:
        if i.x_pos <= pos[0] <= i.x_pos + i.width:
            if i.y_pos <= pos[1] <= i.y_pos + i.width:
                return [i.x_grid_index, i.y_grid_index]

    return -1


def is_finished(matrix):
    shapes = []
    for i in range(16):
        for j in range(10):
            gameLogic.check_shape(i, j, shapes, 10, 16, matrix)

    if sum(matrix[-1]) == 0:
        return True
    else:
        if not shapes:
            return False

    return -1


def show_finish_panel(screen, isWon, restart_button, undo_button, score):
    panel = pygame.Surface((300, 400))
    panel.fill((255, 255, 255))
    screen.blit(panel, (100, 250))

    screen.blit(restart_button, (175, 500))
    screen.blit(undo_button, (175, 575))

    basicfont = pygame.font.SysFont(None, 60)
    basicfont2 = pygame.font.SysFont(None, 30)

    if not isWon:
        text = basicfont.render("You Lose", True, (0, 0, 0))
        screen.blit(text, (155, 350))
    else:
        text = basicfont.render("You Won", True, (0, 0, 0))
        screen.blit(text, (160, 350))

    text = basicfont2.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (195, 400))



def run():

    pygame.init()
    screen = pygame.display.set_mode((500, 850))
    pygame.display.set_caption("Clickomania")
    bg_color = (176, 164, 164)

    blocks = prepare_blocks(screen)
    matrix = np.random.randint(1, 6, size=(16, 10))

    undo_button = pygame.image.load("images/undo.png")
    undo_button = pygame.transform.scale(undo_button, (150, 50))

    restart_button = pygame.image.load("images/restart.png")
    restart_button = pygame.transform.scale(restart_button, (150, 50))

    userSteps = []
    score = 0

    isFinished = False

    while True:
        screen.fill(bg_color)

        screen.blit(undo_button, (0, 0))
        screen.blit(restart_button, (350, 0))

        grid = draw_grid(matrix, blocks)

        if isFinished:
            show_finish_panel(screen, isWon, restart_button, undo_button, score)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    indexes = get_box_indexes(grid)
                    if not isFinished:
                        if indexes != -1:
                            scoreNum = gameLogic.click(indexes[0], indexes[1], userSteps, matrix=matrix, width=10, height=16)
                            score += scoreNum
                        else:
                            pos = pygame.mouse.get_pos()
                            if 0 < pos[0] < 150 and 0 < pos[1] < 50:
                                isFinished = False
                                matrix, userSteps = gameLogic.undo(matrix, userSteps)
                                score -= 10
                            elif 350 < pos[0] < 500 and 0 < pos[1] < 50:
                                userSteps = []
                                isFinished = False
                                matrix = np.random.randint(1, 6, size=(16, 10))
                                score = 0
                    else:
                        pos = pygame.mouse.get_pos()
                        if 175 < pos[0] < 325 and 575 < pos[1] < 625:
                            isFinished = False
                            matrix, userSteps = gameLogic.undo(matrix, userSteps)
                            score -= 10
                        elif 175 < pos[0] < 325 and 500 < pos[1] < 550:
                            userSteps = []
                            isFinished = False
                            matrix = np.random.randint(1, 6, size=(16, 10))
                            score = 0

                    matrix = gameLogic.update_matrix(matrix, 10, 16)

                    isWon = is_finished(matrix)

                    if isWon != -1 and not isFinished:
                        isFinished = True


run()
