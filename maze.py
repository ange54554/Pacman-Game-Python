import pygame
from constants import *
import numpy as np
#import random pour pouvoir utiliser random....
import random

class Maze:
    """Maze class that handles the game board and collision detection"""
    
    def __init__(self):
        self.width = MAZE_WIDTH
        self.height = MAZE_HEIGHT
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT

        # Create a simple maze layout (1 = wall, 0 = empty)
        self.layout = np.array([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])

        # partie1
        valid_positions = self.get_valid_positions()

        self.orange_portal_pos, self.blue_portal_pos = random.sample(valid_positions, 2)

        self.orange_portal_rect = pygame.Rect(
            self.orange_portal_pos[0] - self.cell_width//2,
            self.orange_portal_pos[1] - self.cell_height//2,
            self.cell_width,
            self.cell_height
        )

        self.blue_portal_rect = pygame.Rect(
            self.blue_portal_pos[0] - self.cell_width//2,
            self.blue_portal_pos[1] - self.cell_height//2,
            self.cell_width,
            self.cell_height
        )


        #fin partie1

    def is_wall_collision(self, hitbox):
        """Check if the given rectangle collides with any walls"""
        # TODO: Écrire votre code ici


        cx = hitbox.centerx
        cy = hitbox.centery

        col_center = int(cx//self.cell_width)
        row_center = int(cy//self.cell_height)

        #offsets pour une grille 3x3
        offsets = [-1, 0, 1]

        for dy in offsets:
            for dx in offsets:
                row = row_center + dy
                col = col_center + dx

                if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
                    if self.layout[row][col] == 1:
                        wall_rect = pygame.Rect(
                            col*self.cell_width,
                            row*self.cell_height,
                            self.cell_width,
                            self.cell_height                          

                        )

                        if hitbox.colliderect(wall_rect):
                            
                            return True

        return False
    
    def draw(self, screen):
        """Draw the maze on the screen"""
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 1:  # Wall
                    x = col * self.cell_width
                    y = row * self.cell_height
                    wall_rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                    pygame.draw.rect(screen, BLUE, wall_rect)
                    
                    # Add border for better visibility
                    pygame.draw.rect(screen, WHITE, wall_rect, 1)

    #partie1.2
        pygame.draw.rect(screen, ORANGE, self.orange_portal_rect)
        pygame.draw.rect(screen, BLUE, self.blue_portal_rect)
    # fin partie 1.2




    def get_valid_positions(self):
        """Get all valid (non-wall) positions for placing objects"""
        valid_positions = []
        
        for row in range(self.height):
            for col in range(self.width):
                if self.layout[row,col] == 0:  # Empty space
                    x = col * self.cell_width + self.cell_width // 2
                    y = row * self.cell_height + self.cell_height // 2
                    valid_positions.append((x, y))

        return valid_positions
    
        # partie 1.3
    def get_portal_destination(self, hitbox):
        if hitbox.colliderect(self.orange_portal_rect):
            return self.blue_portal_rect.center
        if hitbox.colliderect(self.blue_portal_rect):
            return self.orange_portal_rect.center
        return None
    #fin partie 1.3