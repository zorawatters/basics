import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


# a sprite is a graphical representation of game objects on the screen. we can use the sprite class by extending it into another class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__() #initializes sprite
        self.surface = pygame.Surface(75, 25) #initialize surface
        self.surface.fill(255,255,255)
        self.rect = self.surf.get_rect() #used to draw objects

    def update(self, pressed_keys):
        if pressed_keys[K_UP]: # move_ip stands for move in place and uses the rect to preform that action. this is why rect needs to be passed as a position in the block transfer
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # there needs to be rules for sprite movement within our board
        # keep player on the screen
        if self.rect.left < 0: # checking to see if sprite has hit the borders of the screen and reset its position to stay there
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Initialize pygame
pygame.init()

# we have to create a screen and display it
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #takes in a tuple representing width and height in px

player = Player() #initialize player

# now we have to set up a game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN: #this is a keypress event
            if event.key == K_ESCAPE: #if the user presses the escape key
                running = False
        elif event.type == QUIT: #if the user clicked the window close button
            running = False


# DRAWING
screen.fill((0,0,0)) #this fills screen with black. takes RGB

# # we can create new surfaces and set their size and shape. each surface is represented by a rectangle. this is done above in player so we will comment out

# new_surface = pygame.Surface((50,50)) #takes (length, width)
# new_surface.fill((0,0,0)) #fill with black
# rect = new_surface.get_rect()

# # to display the new surface we need to transfer it onto the original surface

# getting center coordinates of the screen
surface_center = (
    (SCREEN_WIDTH-surf.get_width())/2,
    (SCREEN_HEIGHT-surf.get_height())/2
)
 
# screen.blit(player.surface, surface_center) # this is a block transfer. takes in surface to place and postion to place it; this will place the block in the middle

screen.blit(player.surface, player.rect) # allows sprite to move  

screen.display.flip() #updates screen

# MOVING

# this retrieves set of keys pressed by user at the start of every frame
pressed_keys = pygame.key.get_pressed()
# we will write a method update that effects the sprite based on these keys and it will be in the player class above
player.update(pressed_keys)

# SPRITE GROUPS allow methods to be used on sprites and groups different ones together.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# this will allow you to add multiple sprites to the screen with a for loop
for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)

# to check if sprites have collided, use...
pygame.sprite.spritecollideany(thing1, player)