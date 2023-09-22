import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 400
GROUND_HEIGHT = 50
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 20
GLIDE_CONSTANT = 5
GLIDE_VELOCITY_Y = 1

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.original_image.fill(RED)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.jumping = False
        self.gliding = False  # Added gliding state
        self.glide_velocity_y = 1  # Adjust glide speed as needed

    def update(self):
        if self.gliding:
            self.image = pygame.transform.rotate(self.original_image, 90)
        else:
            self.image = self.original_image

        if not self.gliding:
            self.velocity_y += GRAVITY

        # Check if the player is pressing the spacebar to glide
        keys = pygame.key.get_pressed()
        # if self.jumping and keys[pygame.K_SPACE]:
            # self.velocity_y += self.glide_velocity_y  # Add glide velocity

        self.rect.y += self.velocity_y

        # Ground collision
        if self.rect.y > HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
            self.jumping = False
            self.gliding = False  # Reset gliding state when touching the ground

    def jump(self):
        if not self.jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True
        else:
            self.gliding = True
            self.velocity_y = GLIDE_VELOCITY_Y
    def unjump(self):
        self.gliding = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_WIDTH, OBSTACLE_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT

    def update(self):
        self.rect.x -= SPEED
        if self.rect.x < -OBSTACLE_WIDTH:
            self.kill()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Game")

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    obstacle_timer = 0
    space_held = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed_time = pygame.time.get_ticks()  # Record the time when space is pressed
                    space_held = True
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.unjump()  # Space button is released after a hold
                    space_held = False
            if space_held and pygame.time.get_ticks() - space_pressed_time > 10:  # Check if space was held for less than 10 ms
                player.jump()
        all_sprites.update()
        obstacles.update()

        # Add obstacles
        obstacle_timer += 1
        if obstacle_timer > 100:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            obstacle_timer = 0

        # Check for collisions
        if pygame.sprite.spritecollide(player, obstacles, False):
            running = False

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, (0, 0, 0), [0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT])
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


#File created using ChatGPT
# base ChatGPT Prompt:
#We are creating a platform game with obstacles where the individual can run and jump. Please code a simple platformer with object oriented python where the user is perpetually running when they're not jumping. It should use pygame. 