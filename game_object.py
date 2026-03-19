import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    """Abstract base class for all game objects"""
    
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
    
    @abstractmethod
    def update(self):
        """Update the game object state"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """Draw the game object on the screen"""
        pass
    
    def get_rect(self):
        """Return the pygame Rect object for collision detection"""
        self.rect.x = self.x
        self.rect.y = self.y
        return self.rect
    
    def get_position(self):
        """Return the (x, y) position of the object"""
        return (self.x, self.y)