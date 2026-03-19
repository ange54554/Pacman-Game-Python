import pygame
from game_object import GameObject
from constants import *

class Dot(GameObject):
    """Small dots that Pacman collects for points"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 4, 4, WHITE)
        self.radius = 2
    
    def update(self):
        """Dots don't need to update"""
        pass
    
    def draw(self, screen):
        """Draw a small white dot"""
        center_x = self.x - self.radius + self.width // 2
        center_y = self.y - self.radius + self.height // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)

class PowerPellet(GameObject):
    """Large pellets that make ghosts vulnerable"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 12, 12, WHITE)
        self.radius = 6
        self.blink_timer = 0
        self.visible = True
    
    def update(self):
        """Animate the power pellet blinking"""
        self.blink_timer += 1
        if self.blink_timer >= 30:  # Blink every 30 frames
            self.visible = not self.visible
            self.blink_timer = 0
    
    def draw(self, screen):
        """Draw a blinking large pellet"""
        if self.visible:
            center_x = self.x - self.radius + self.width // 2
            center_y = self.y - self.radius + self.height // 2
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)

class ScoreText(GameObject):
    """Floating score text when points are earned"""
    
    def __init__(self, x, y, points):
        super().__init__(x, y, 50, 20, WHITE)
        self.points = points
        self.lifetime = 60  # frames
        self.timer = 0
        self.font = pygame.font.Font(None, 24)
        self.velocity_y = -1  # Float upward
    
    def update(self):
        """Update floating text"""
        self.timer += 1
        self.y += self.velocity_y
        return self.timer < self.lifetime
    
    def draw(self, screen):
        """Draw the floating score text"""
        alpha = max(0, 255 - (self.timer * 255 // self.lifetime))
        text_surface = self.font.render(str(self.points), True, YELLOW)
        
        # Create a surface with alpha for fading effect
        fade_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()))
        fade_surface.set_alpha(alpha)
        fade_surface.blit(text_surface, (0, 0))
        
        screen.blit(fade_surface, (self.x, self.y))