import pygame

class Wall(pygame.Rect):
    def __init__(self, x, y, width, height, grid_size) -> None:
        super(Wall, self).__init__(x*grid_size, y*grid_size, width*grid_size, height*grid_size)

        self.color = (80, 80, 80)
    
