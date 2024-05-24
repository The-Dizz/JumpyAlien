import pygame
import sys
import time
from settings import *
from sprites import *

class Game: 
    # Set up
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True # Set initial game state

        # Controller Support
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            self.joystick = None

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group() 
        self.collision_sprites = pygame.sprite.Group() 

        # Scale Factor for dynamic game resizing 
        bg_height = pygame.image.load('darkPurple.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / float(bg_height) # Scale factor is a ratio of window height and background height
        
        # Sprite set up
        BG(self.all_sprites, self.scale_factor) # Set what sprite group they belong to and scale factor so it can be resized
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.player = Player(self.all_sprites) # Player gets self.player so we can control it
        
        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1 
        pygame.time.set_timer(self.obstacle_timer, 1400) # Spawn rate for obstacles

        # Score
        self.font = pygame.font.Font('BD_Cartoon_Shout.ttf', 24)
        self.score = 0 
        self.start_offset = 0 # Starting score for first run

        # Menu
        self.menu_surf = pygame.image.load('shipYellow_damage2.png')
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    def collisions(self):
        collision_sound = pygame.mixer.Sound('explosionCrunch_004.ogg')
        collision_sound.set_volume(0.5)
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top <= 0: # When player hits obstacle/ground or goes too high
            collision_sound.play()
            # Rumble Support (Untested)
            # if self.joystick and hasattr(self.joystick, 'rumble'):  # Ensure the joystick supports rumble
            #     try:
            #         self.joystick.rumble(1.0, 1.0, 500)  # Rumble at 100% intensity on both motors for 500 ms
            #     except AttributeError:
            #         print("Rumble not supported on this joystick")

            for sprite in self.collision_sprites.sprites(): # If lost by hitting an obstacle, kill that obstacle
                if sprite.sprite_type == 'obstacle': 
                    sprite.kill()
            self.active = False # Deactivate game state
            self.player.kill()
    
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height # Drop final score below menu after losing
        score_surf = self.font.render(self.score, True, (255, 255, 255))
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH/2, y))
        self.display_surface.blit(score_surf, score_rect)
        
    def run(self):
        last_time = time.time()
        while True:
            # Delta time
            dt = time.time() - last_time
            last_time = time.time() 

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN: # Keyboard controls
                    if event.key == pygame.K_SPACE: # Space bar
                        if self.active: # Jumps when the game is active
                            self.player.jump() 
                        else: # When the game is inactive: spawns the player, activates the game, and starts counting score
                            self.player = Player(self.all_sprites) 
                            self.active = True
                            self.start_offset = pygame.time.get_ticks()
                    if event.key == pygame.K_ESCAPE: # ESC key
                        pygame.quit() # Quit game
                        sys.exit()

                if self.joystick: # Joystick controls
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0: # A button
                            if self.active: # Jumps when the game is active
                                self.player.jump() 
                            else: # When the game is inactive: spawns the player, activates the game, and starts counting score
                                self.player = Player(self.all_sprites) 
                                self.active = True
                                self.start_offset = pygame.time.get_ticks() 
                        if event.button == 1: # B button
                            pygame.quit() # Quit game
                            sys.exit()
                if event.type == self.obstacle_timer: # Spawn obstacles at their spawn rate with a size set in settings
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * DIFFICULTY_LEVEL)

            # Game Logic - turn on all the stuff set up above
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)

if __name__ == '__main__':
    game = Game()
    game.run()