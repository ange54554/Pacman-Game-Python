import pygame
import sys
from constants import *
from pacman import Pacman
from ghost import ghosts_dict
from maze import Maze
from collectibles import Dot, PowerPellet
import random

class Game:
    """Main game class that handles the game loop and overall game state"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = MENU
        self.score = 0
        self.lives = 3
        self.level = 1
        
        # Initialize game objects
        self.maze = Maze()
        self.pacman = Pacman(PACMAN_START_X, PACMAN_START_Y)  # Start position
        self.ghosts = []
        self.dots = []
        self.power_pellets = []
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.init_game_objects()
    
    def init_game_objects(self):
        """Initialize game objects like dots, power pellets, and ghosts"""
        self.dots = []
        self.power_pellets = []
        self.ghosts = []
        
        # Get valid positions from maze
        valid_positions = self.maze.get_valid_positions()

        # Place ghosts in the maze
        for color, ghost_class in ghosts_dict.items():
            # Make sure that ghost are not placed too close to Pacman
            valid_positions = [pos for pos in valid_positions if not (PACMAN_START_X - 4 * CELL_WIDTH <= pos[0] <= PACMAN_START_X + 4 * CELL_WIDTH and PACMAN_START_Y - 4 * CELL_HEIGHT <= pos[1] <= PACMAN_START_Y + 4 * CELL_HEIGHT)]
            
            # Pick a random position for the ghost
            x, y = random.choice(valid_positions)
            ghost = ghost_class(x, y)
            self.ghosts.append(ghost)

        # Place dots and power pellets
        for i, (x, y) in enumerate(valid_positions):
            # Place power pellets at specific strategic positions
            if (i % 50 == 0 and len(self.power_pellets) < 4):
                self.power_pellets.append(PowerPellet(x, y))
            else:
                # Don't place dots too close to starting positions
                if not (PACMAN_START_X - 2 * CELL_WIDTH <= x <= PACMAN_START_X + 2 * CELL_WIDTH and PACMAN_START_Y - 2 * CELL_HEIGHT <= y <= PACMAN_START_Y + 2 * CELL_HEIGHT):
                    self.dots.append(Dot(x, y))
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        self.game_state = PLAYING
                elif self.game_state == PLAYING:
                    self.pacman.handle_input(event.key)
                elif self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.restart_game()
    
    def update(self):
        """Update game state"""
        if self.game_state == PLAYING:
            # Update pacman
            self.pacman.update(self.maze)
            
            # Update ghosts
            for ghost in self.ghosts:
                ghost.update(self.maze, self.pacman)
            
            # Check collisions
            self.check_collisions()
            
            # Check win condition
            if len(self.dots) == 0:
                self.game_state = VICTORY
    
    def check_collisions(self):
        """Check collisions between game objects"""
        pacman_rect = self.pacman.get_rect()
        
        # Check dot collection
        for dot in self.dots[:]:
            if pacman_rect.colliderect(dot.get_rect()):
                self.dots.remove(dot)
                self.score += DOT_POINTS
        
        # Check power pellet collection
        for pellet in self.power_pellets[:]:
            if pacman_rect.colliderect(pellet.get_rect()):
                self.power_pellets.remove(pellet)
                self.score += POWER_PELLET_POINTS
                # Make ghosts vulnerable
                for ghost in self.ghosts:
                    ghost.make_vulnerable()
        
        # Check ghost collision
        for ghost in self.ghosts:
            if pacman_rect.colliderect(ghost.get_rect()):
                if ghost.vulnerable:
                    ghost.reset_position()
                    self.score += GHOST_POINTS
                else:
                    self.lives -= 1
                    self.pacman.reset_position()
                    if self.lives <= 0:
                        self.game_state = GAME_OVER
    
    def draw(self):
        """Draw all game objects"""
        self.screen.fill(BLACK)
        
        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        elif self.game_state == VICTORY:
            self.draw_victory()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu"""
        title = self.font.render("PACMAN", True, YELLOW)
        instruction = self.small_font.render("Press SPACE to start", True, WHITE)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(instruction, instruction_rect)
    
    def draw_game(self):
        """Draw the main game"""
        # Draw maze
        self.maze.draw(self.screen)
        
        # Draw dots
        for dot in self.dots:
            dot.draw(self.screen)
        
        # Draw power pellets
        for pellet in self.power_pellets:
            pellet.update()  # Update animation
            pellet.draw(self.screen)
        
        # Draw pacman
        self.pacman.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
    
    def draw_ui(self):
        """Draw the user interface"""
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 35))
        self.screen.blit(level_text, (10, 60))
    
    def draw_game_over(self):
        """Draw the game over screen"""
        game_over = self.font.render("GAME OVER", True, RED)
        final_score = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
        restart = self.small_font.render("Press R to restart", True, WHITE)
        
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(final_score, score_rect)
        self.screen.blit(restart, restart_rect)
    
    def draw_victory(self):
        """Draw the victory screen"""
        victory = self.font.render("VICTORY!", True, YELLOW)
        final_score = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
        
        victory_rect = victory.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25))
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        
        self.screen.blit(victory, victory_rect)
        self.screen.blit(final_score, score_rect)
    
    def restart_game(self):
        """Restart the game"""
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_state = PLAYING
        self.init_game_objects()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()