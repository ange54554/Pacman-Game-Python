import pygame
import random
from game_object import GameObject
from constants import *

class Ghost(GameObject):
    """Base Ghost class"""
    
    def __init__(self, x, y, color):
        super().__init__(x, y, int(CELL_WIDTH//2), int(CELL_HEIGHT//1.2), color)
        self.start_x = x
        self.start_y = y
        self.direction = random.randint(0, 3)
        self.speed = GHOST_SPEED
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.vulnerable_duration = 300  # frames
        self.step = "left"
        self.step_timer = 0
        self.last_RL_direction = 0
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.in_portal = False

    def update(self, maze, pacman):
        """Update ghost position and state"""
        # Update vulnerable state
        if self.vulnerable:
            self.vulnerable_timer += 1
            if self.vulnerable_timer >= self.vulnerable_duration:
                self.vulnerable = False
                self.vulnerable_timer = 0
        
        # Update ghost animation
        self.step_timer += 1
        if self.step_timer >= 10:
            self.step = "right" if self.step == "left" else "left"
            self.step_timer = 0
        
        # Move ghost
        self.move(maze, pacman)
    
    def move(self, maze, pacman):
        """Basic ghost movement (random direction on collision)"""
        new_x, new_y, hitbox = self.get_next_position()
        
        # Check for collision with walls
        if maze.is_wall_collision(hitbox):
            # Change direction randomly
            self.direction = random.randint(0, 3)
        else:
            self.x = new_x
            self.y = new_y

#partie 3
   
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


#fin partie 3




    
    def get_next_position(self):
        """Get next position based on current direction"""
        new_x, new_y = self.x, self.y
        hitbox = None

        if self.direction in [0, 2]:  # Right or Left
            self.last_RL_direction = self.direction
        
        # TODO: Écrire votre code ici
        if self.direction == 0:
            new_x += self.speed
        elif self.direction ==1:
            new_y += self.speed
        elif self.direction ==2:
            new_x -= self.speed
        elif self.direction ==3:
            new_y -= self.speed

        hitbox= pygame.Rect(new_x, new_y, self.width, self.height)
        

        return new_x, new_y, hitbox
      
    def draw(self, screen):
        """Load ghost image"""
        # TODO: Écrire votre code ici
        if self.vulnerable:
            image_g = pygame.image.load(f"imgs/weak_ghost.png").convert_alpha()
        else:
            image_g= pygame.image.load(f"imgs/{self.color}_ghost.png").convert_alpha()

        image_g= pygame.transform.scale(image_g, (self.width, self.height))
        screen.blit(image_g, (self.x, self.y))

        if self.step=="left":
            image_g = pygame.transform.rotate(image_g, 10)
        else:
            image_g = pygame.transform.rotate(image_g, -10)

        if self.last_RL_direction ==2:
            image_g = pygame.transform.flip(image_g, True, False)

      
    

       
    def make_vulnerable(self):
        """Make the ghost vulnerable to being eaten"""
        self.vulnerable = True
        self.vulnerable_timer = 0
    
    def reset_position(self):
        """Reset ghost to starting position"""
        self.x = self.start_x - self.width // 2
        self.y = self.start_y - self.height // 2
        self.vulnerable = False
        self.vulnerable_timer = 0

class RedGhost(Ghost):
    """Red ghost - aggressive, chases Pacman directly"""
    
    def __init__(self, x, y, color="red"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Aggressive movement - chase Pacman directly"""
        if self.vulnerable:
            # Run away from Pacman when vulnerable
            self.flee_from_pacman(maze, pacman)
        else:
            # Chase Pacman
            self.chase_pacman(maze, pacman)
    
    def chase_pacman(self, maze, pacman):
        """Move towards Pacman"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        curent_x, curent_y = self.x, self.y
        default_direction= self.direction
        dx= abs(pacman_x - curent_x)
        dy= abs(pacman_y - curent_y)

        if dx > dy:
            if pacman_x > curent_x:
                self.direction=0
            else:
                self.direction=2

        else:
            if pacman_y> curent_y:
                self.direction= 1
            else:
                self.direction=3
        new_x, new_y, hitbox = self.get_next_position()
        
    #check colision

        if maze.is_wall_collision(hitbox):
            self.direction = default_direction
            return super().move(maze, pacman)
        else:
            self.x=new_x
            self.y=new_y



    def flee_from_pacman(self, maze, pacman):
        """Run away from Pacman when vulnerable"""
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        curent_x, curent_y = self.x, self.y
        dx= abs(pacman_x - curent_x)
        dy= abs(pacman_y - curent_y)
        if dx > dy:
            if pacman_x > curent_x:
                self.direction=2
            else:
                self.direction=0

        else:
            if pacman_y> curent_y:
                self.direction= 3
            else:
                self.direction=1
        

class PinkGhost(Ghost):
    """Pink ghost - tries to ambush Pacman"""

    def __init__(self, x, y, color="pink"):
        super().__init__(x, y, color)

    def move(self, maze, pacman):
        """Ambush movement - try to get ahead of Pacman"""
        if self.vulnerable:
            super().move(maze, pacman)  # Random movement when vulnerable
        else:
            self.ambush_pacman(maze, pacman)

    def ambush_pacman(self, maze, pacman):
        """Try to position ahead of Pacman"""
        # Try to position ahead of Pacman
        pacman_x, pacman_y = pacman.get_position()
        
        # TODO: Écrire votre code ici
        ghost_x, ghost_y = self.x, self.y

        vx= pacman_x - ghost_x
        vy= pacman_y - ghost_y

        target_x = int(round(pacman_x + vx/2))
        target_y = int(round(pacman_y + vy/2))

       
        dx = abs(target_x - ghost_x)
        dy= abs(target_y - ghost_y)

        if dx > dy:
            self.direction = 0 if target_x > ghost_x else 2
        else:
            self.direction = 3 if target_y > ghost_y else 1
        return super().move(maze, pacman)


        


        

        

class BlueGhost(Ghost):
    """Blue ghost - patrol behavior"""

    def __init__(self, x, y, color="blue"):
        super().__init__(x, y, color)
        self.patrol_timer = 0
        self.patrol_duration = 120
    
    def move(self, maze, pacman):
        """Patrol movement - changes direction periodically"""
        self.patrol_timer += 1
        
        # TODO: Écrire votre code ici
        new_x, new_y, hitbox = self.get_next_position()

        if maze.is_wall_collision(hitbox) or self.patrol_timer >= self.patrol_duration:
            self.direction= random.choice([0, 1, 2, 3])
            self.patrol_timer = 0
        return super().move(maze, pacman)

        dest = maze.get_portal_destination(self.hitbox)
        if dest:
            self.x, self.y = dest
            self.hitbox.center = dest


class OrangeGhost(RedGhost):
    """Orange ghost - mixed behavior"""

    def __init__(self, x, y, color="orange"):
        super().__init__(x, y, color)
        self.behavior_timer = 0
        self.chase_mode = True
        self.behavior_duration = 180  # frames
    
    def move(self, maze, pacman):
        """Mixed behavior - alternates between chasing and fleeing"""
        self.behavior_timer += 1
        
        # TODO: Écrire votre code ici
        
        if self.vulnerable:
            self.flee_from_pacman(maze, pacman)

        else:           
            if self.chase_mode:
                self.chase_pacman(maze, pacman)
            else: 
                new_x, new_y, hitbox= self.get_next_position()
                if maze.is_wall_collision(hitbox):
                    self.direction= random.choice([0, 1, 2, 3])
            
                super().move(maze, pacman)

        if self.behavior_timer >= self.behavior_duration:
            self.behavior_timer = 0
            self.chase_mode = not self.chase_mode

        
ghosts_dict = {
            "red": RedGhost,
            "pink": PinkGhost,
            "blue": BlueGhost,
            "orange": OrangeGhost
        }