import pygame


class Block():

    def __init__(self, screen):
        self.screen = screen
        self.image = None
        self.x_pos = None
        self.y_pos = None
        self.x_grid_index = None
        self.y_grid_index = None
        self.width = 50

    def set_block_color(self, picture_name):
        self.image = pygame.image.load('images/' + picture_name)
        self.image = pygame.transform.scale(self.image, (self.width, self.width))

    def set_xy_position(self, x_position: int, y_position: int):
        self.x_pos = x_position
        self.y_pos = y_position

    def set_xy_index(self, x_index: int, y_index: int):
        self.x_grid_index = x_index
        self.y_grid_index = y_index

    def output(self):
        self.screen.blit(self.image, (self.x_pos, self.y_pos))
