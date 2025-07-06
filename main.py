from dataclasses import dataclass
import pygame

@dataclass
class GameContext(object):
    screen: pygame.surface.Surface = None
    clock: pygame.time.Clock = None
    dt: float = 0



@dataclass
class GameObject(object):
    pos: pygame.Vector2 = pygame.Vector2(0,0)
    vel: pygame.Vector2 = pygame.Vector2(0,0)
    acc: pygame.Vector2 = pygame.Vector2(0,0)

@dataclass
class Obstacle(GameObject):

    def update(self, ctx: GameContext):
        pass
    
    def draw(self, ctx: GameContext):
        pygame.draw.rect(ctx.screen, "red", pygame.Rect(self.pos.x, self.pos.y, 100,100))

@dataclass
class Player(GameObject):
    state: str = None
    jump_cooldown: int = 0

    def handle_input(self, ctx: GameContext):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_w]:
            if self.state == None:
                self.vel.y = -5
                self.acc.y -= 30 
                self.state = "JUMP"
                print("jumped")

        if keys[pygame.K_a]:
            self.vel.x = -10
        if keys[pygame.K_d]:
            self.vel.x = 10

    def update(self, ctx: GameContext):
        dt = ctx.dt 
        self.vel.x += self.acc.x*dt
        self.vel.y += self.acc.y*dt

        self.pos.y += self.vel.y
        self.pos.x += self.vel.x

        self.pos.x = min(WIDTH-100, max(0, self.pos.x))
        self.pos.y = min(HEIGHT-100, max(0, self.pos.y))
        

        is_falling = self.pos.y < HEIGHT-100

        if is_falling:
            self.acc.y += 2
        else:
            self.acc.y = 0
            self.vel.y = 0

            if self.state == "JUMP":
                self.state = None

        print(self)
    def draw(self, ctx: GameContext):
       pygame.draw.rect(ctx.screen, "green", pygame.Rect(self.pos.x, self.pos.y, 100,100), 20) 


WIDTH = 1280
HEIGHT = 720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
print(type(screen))
clock = pygame.time.Clock()
running = True
dt = 0
game_ctx = GameContext(screen=screen, clock=clock)
player_pos = pygame.Vector2(300,300)
player = Player(pos=player_pos)

ob = Obstacle(pos=(pygame.Vector2(30,HEIGHT-100)))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
   
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.handle_input(game_ctx)
    if keys[pygame.K_q]:
        running = False

    if not running:
        continue

    # game loop preamble
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")
    
    ob.draw(game_ctx)

    player.update(game_ctx)
    player.draw(game_ctx)
    # game loop post-logic phase
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    game_ctx.dt = clock.tick(60) / 1000

pygame.quit()
