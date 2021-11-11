import pygame

class Jelly(pygame.Rect):

    def __init__(self, x, y, width, height, grid_size, color) -> None:
        super(Jelly, self).__init__(x*grid_size, y*grid_size, width*grid_size, height*grid_size)
        self.color = color
