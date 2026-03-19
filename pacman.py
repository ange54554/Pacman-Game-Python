import pygame
import math
from game_object import GameObject
from constants import *

class Pacman(GameObject):
    """Pacman player class"""
    
    def __init__(self, x, y):
        super().__init__(x, y, CELL_WIDTH//1.8, CELL_HEIGHT//1.8, YELLOW)
        self.start_x = x
        self.start_y = y
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        self.next_direction = 0
        self.speed = PACMAN_SPEED
        self.mouth_open = True
        self.mouth_timer = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.in_portal = False

    def handle_input(self, key):
        """Handle keyboard input for movement"""
        if key == pygame.K_RIGHT:
            self.next_direction = 0
        if key == pygame.K_DOWN:
            self.next_direction = 1
        if key == pygame.K_LEFT:
            self.next_direction = 2
        if key == pygame.K_UP:
            self.next_direction = 3
            


    def update(self, maze):
        """Update Pacman's position and state"""
        # Update mouth animation
        self.mouth_timer += 1
        if self.mouth_timer >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
        
        # Get next position based on next_direction
        new_x, new_y, hitbox = self.get_next_position()

        # Check if there is collision with a wall
        if not maze.is_wall_collision(hitbox):
            self.direction = self.next_direction
            self.x = new_x
            self.y = new_y

        #partie2

        current_hitbox= pygame.Rect(self.x, self.y, self.width, self.height)
                      

        if self.in_portal:
            if not (current_hitbox.colliderect(maze.orange_portal_rect) or current_hitbox.colliderect(maze.blue_portal_rect)):
                self.in_portal = False
        else:
            dest= maze.get_portal_destination(current_hitbox)
            if dest:
                self.x = dest[0]- self.width//2
                self.y = dest[1] - self.height//2
                self.in_portal = True


        #fin partie2


    def get_next_position(self):
        """
        Get the next position based on direction

        The hitbox will be used to detect collisions before moving.
        Returns new_x, new_y, hitbox
        """
        new_x, new_y = self.x, self.y
        hitbox = None

        # TODO: Écrire votre code ici
        if self.next_direction ==0:
            new_x += self.speed
        elif self.next_direction ==1:
            new_y += self.speed
        elif self.next_direction ==2:
            new_x -= self.speed
        elif self.next_direction ==3:
            new_y -= self.speed

        hitbox= pygame.Rect(new_x, new_y, self.width, self.height)

        #is it CELL_HEIGHT//1.8 or self.height
        
        
        return new_x, new_y, hitbox
    
    def draw(self, screen):
        """Draw Pacman with mouth animation"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        radius = self.width // 2

        # TODO: Écrire votre code ici
        # Draw Pacman body
        if not self.mouth_open:
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        else:
            liste_de_point = [(center_x, center_y)]
            if self.next_direction == 0:
                for i in range(30, 331, 5):
                    x = center_x + radius* math.cos(math.radians(i))
                    y = center_y - radius* math.sin(math.radians(i))
                    liste_de_point.append((x, y))
            elif self.next_direction == 1:
                for i in range(300, 601, 5):
                    x = center_x + radius* math.cos(math.radians(i))
                    y = center_y - radius* math.sin(math.radians(i))
                    liste_de_point.append((x, y))
            elif self.next_direction == 2:
                for i in range(210, 481, 5):
                    x = center_x + radius* math.cos(math.radians(i))
                    y = center_y - radius* math.sin(math.radians(i))
                    liste_de_point.append((x, y))
            elif self.next_direction == 3:
                for i in range(120, 421, 5):
                    x = center_x + radius* math.cos(math.radians(i))
                    y = center_y - radius* math.sin(math.radians(i))
                    liste_de_point.append((x, y))

            
            pygame.draw.polygon(screen, YELLOW, liste_de_point, 0)

          
        # Draw Pacman eye
        if self.next_direction == 0:
            x = center_x + radius//2 
            y = center_y - radius//2
        elif self.next_direction == 1:
            x = center_x + radius//2 
            y = center_y + radius//2
        elif self.next_direction == 2:
            x = center_x - radius//2 
            y = center_y + radius//2
        elif self.next_direction == 3:
            x = center_x - radius//2 
            y = center_y - radius//2

        pygame.draw.circle(screen, BLACK, (x, y), radius//3)
    
    def reset_position(self):
        """Reset Pacman to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.direction = 0
        self.next_direction = 0