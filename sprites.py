import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite): # Background sprite
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        bg_image =  pygame.image.load('Assets/Background/darkPurple.png')
        bg_image = pygame.transform.scale(bg_image,(bg_image.get_width()*2,bg_image.get_height())) # Double background width

        # Scale background based on scale factor
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height)) # Create full sized background image

        # Create 2 background images for smoother scrolling later        
        self.image = pygame.Surface((full_width * 2,full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt): # Scroll background
        self.pos.x -= 150 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        # Image
        ground_surf=pygame.image.load('Assets/Obstacles/ground.png').convert_alpha()
        ground_surf = pygame.transform.scale(ground_surf,(ground_surf.get_width(),ground_surf.get_height()/2))
        self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size())*scale_factor)
        
        # Positions
        self.rect = self.image.get_rect(bottomleft=(0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt): # Scroll ground
        self.pos.x -= 200*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
        
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        # Image
        player_image = pygame.image.load('Assets/Player/shipYellow_manned.png')
        player_width = player_image.get_width()
        player_height = player_image.get_height()
        self.image = pygame.transform.scale(player_image,(player_width/1.5,player_height/1.5))
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20,WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Load sound
        self.jump_sound = pygame.mixer.Sound('Assets/Sounds/laserRetro_002.ogg')
        self.jump_sound.set_volume(0.5)

        # Movement
        self.gravity = 550
        self.direction = 0

        # Mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
    
    def jump(self):
        self.direction = -200
        self.jump_sound.play()

    def update(self, dt):
        self.apply_gravity(dt)
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        # Image
        surf = pygame.image.load('Assets/Obstacles/spike.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
		
        # Orientation
        x = WINDOW_WIDTH + randint(40,100)
        orientation = choice(('up','down')) 
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 200 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()