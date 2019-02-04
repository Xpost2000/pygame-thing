# importing modules
# pieces of code that I didn't write basically.
import pygame
import random

# all the global variables
score = 0
run_game = True
game_over = False
font = None
window = None

def AABB_Collide( a, b ):
    # 0 = x
    # 1 = y
    # 2 = w
    # 3 = h
    # classic rectangle intersection algorithm. Never fails anyone!
    if ( (a[0] < b[0] + b[2]) & (a[0] + a[2] > b[0]) )  and ( (a[1] < b[1] + b[3]) & (a[1] + a[3] > b[1]) ):
       return True
    return False

class Paddle(object):
    def __init__( self, position, size ):
        self.position = list(position)
        self.size = list(size)

    def update(self, ball):
        if (AABB_Collide(
                list((self.position[0], self.position[1], self.size[0], self.size[1])),
                list((ball.position[0], ball.position[1], ball.radius, ball.radius))
        )) :
            ball.velocity[1] *= -1
            ball.position[1] -= self.size[1];

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 255, 255), (self.position, self.size) )


class Ball(object):
    def __init__( self, position, radius, velocity ):
        self.position = list(position)
        self.radius = radius
        self.velocity = list(velocity)

    def update(self):
        global game_over
        # allow the ball to bounce around the screen basically
        if( self.position[0] + self.radius > 1024 - self.radius ) or ( self.position[0] < 0 ):
            self.velocity[0] *= -1;

        if ( self.position[1] < 0 ):
            self.velocity[1] *= -1;
        # if it falls through the floor it's a game over.
        if ( self.position[1] + self.radius > 768 - self.radius ):
            game_over = True

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255, 255), (self.position), self.radius)

class Basket(object):
    def __init__( self, position, size, speed ):
        self.position = list(position)
        self.size = list(size)
        self.speed = speed

    def update(self, ball):
        global score
        # Reset the basket if it goes away from the screen
        if( self.position[0] + self.size[0] > 1024 - self.size[0] ):
            self.position[0] = 0

        # check ball collision
        # only check it if ball is coming down.
        # as if there was a hole at the top.
        if (AABB_Collide(
                list((self.position[0], self.position[1], self.size[0], self.size[1])),
                list((ball.position[0], ball.position[1], ball.radius, ball.radius))
        ) and (ball.velocity[1] > 0)) :
            score += 1
        # reset ball position
            ball.position[0] = (1024 / 2 - 25)
            ball.position[1] = (768 / 2 - 25)
        self.position[0] += self.speed

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0, 255), (self.position, self.size) )

# creating basic game entity objects.
baskets = []
baskets.append(Basket((0, 120), (50, 50), 2))
baskets.append(Basket((70*4.25, 120), (50, 50), 2))
baskets.append(Basket((140*4.25, 120), (50, 50), 2))

main_ball = Ball((1024 / 2 - 25, 768 / 2 - 25), 20, (random.randint(-7, 7), random.randint(4, 9)) )
main_paddle = Paddle((1024 / 2 - 150, 768-100), (200, 20))

def init():
    global window
    global font
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont( pygame.font.get_default_font(), 40 )

    window = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Ball Catcher")

def run():
    global font
    global window
    global run_game

    window.fill((30, 30, 30, 255))

    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            run_game = False
            print("Game quit")

    keys = pygame.key.get_pressed()

    if game_over == False:
        if keys[pygame.K_LEFT]:
            if( main_paddle.position[0] > 0 ):
                main_paddle.position[0] -= 15;
        if keys[pygame.K_RIGHT]:
            if( main_paddle.position[0] + main_paddle.size[0] < 1024 ):
                main_paddle.position[0] += 15;


        for basket in baskets:
            basket.draw(window)
            basket.update(main_ball)

        main_ball.update()
        main_ball.draw(window)

        main_paddle.update(main_ball)
        main_paddle.draw(window)

        window.blit ( font.render("Ball Catcher Demo", False, (0, 255, 0)), (0, 0) )
        window.blit ( font.render( "Current Score: "+str(score) , False, (0, 255, 0)), (0, 45) )
    else:
        window.blit ( font.render("Game Over", False, (0, 255, 0)), (0, 0) )

    pygame.display.update()

    # This determines how often pygame updates.
    # without it, the library seems to slow to
    # a ridiculous halt.
    pygame.time.Clock().tick(60)

def main():
    init()

    while run_game:
        run()

if __name__ == "__main__":
    main()
