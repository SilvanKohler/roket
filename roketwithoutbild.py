import numpy as np
class Ball:
    def __init__(self, r, pos):
        self.rad = r
        self.pos = pos
    # def __round__(self):
    #     self.pos = round(self.pos)
class Rocket:
    def __init__(self, friction=0.99, gravity=0.15, angularfriction=0.97):
        
        self.fric = friction
        self.grav = gravity
        self.afri = angularfriction
        self.avel = 0.0
        self.xvel = 0.0
        self.yvel = 0.0
        self.dire = 29.75
        self.xpos = 200.0
        self.ypos = 200.0

    def accelerate(self, speedincrement, leftright):
        if leftright == 3:
            self.xvel += np.math.cos(self.dire / (2 * np.pi)) * speedincrement
            self.yvel += np.math.sin(self.dire / (2 * np.pi)) * speedincrement
            self.vel = abs(self.yvel) + abs(self.xvel)
            self.avel *= 0.9
        elif leftright <= 2:
            self.xvel += np.math.cos(self.dire / (2 * np.pi)) * speedincrement / 1.5
            self.yvel += np.math.sin(self.dire / (2 * np.pi)) * speedincrement / 1.5
            if leftright == 2:
                self.avel -= 0.1
            elif leftright == 1:
                self.avel += 0.1
    def move(self):
        self.dire += self.avel
        self.avel *= self.afri
        self.xvel *= self.fric
        self.yvel *= self.fric
        self.yvel += self.grav
        self.vel = abs(self.yvel) + abs(self.xvel)
        self.xpos += self.xvel
        self.ypos += self.yvel


def geschwindigkeit(zahl, pos=(200, 350), size=45):
    font = pygame.font.SysFont("dejavusansmonooblique", size)
    text = str(zahl) + "P/F"
    if not len(str(zahl)) > 3:
        text = ' ' + text
    for line in text.splitlines():
        
        for char in range(1, len(line)+1):
            text = font.render(line[:char], 1, (105, 0, 30))
            screen.blit(text, pos)





import pygame
pygame.init()



display = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.FULLSCREEN)
screen = pygame.display.get_surface()
width,height = screen.get_width(), screen.get_height()
# width = 400
# height = 400
ballposr = np.array([])

for bubble in np.arange(20):
    postuple = (np.random.randint(1, width), np.random.randint(1, height))
    rtuple = np.random.randint(40, 80)
    ballposr = np.append(ballposr, ((postuple), rtuple))
    # ballposr = [((width / 2, height / 2), 50), ((width / 2 - 50, height / 2 + 20), 20)]

balls = []
for posn in np.arange(0, len(ballposr), 2):
    pos = ballposr[posn]
    r = ballposr[posn + 1]
    balls.append(Ball(r, pos))

quittin = False
raketli = Rocket()
turbo = False
left = False
right = False
clock = pygame.time.Clock()
while True:
    dt = clock.tick(30)
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quittin = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.scancode == 33:
                left = True
            elif event.scancode == 36:
                right = True
            elif event.scancode == 57:
                turbo = True
            print(event)
        elif event.type == pygame.KEYUP:
            if event.scancode == 33:
                left = False
            elif event.scancode == 36:
                right = False
            elif event.scancode == 57:
                turbo = False
    if quittin == True:
        break
    if left and not right:
        raketli.accelerate(0.35, 1)
    if right and not left:
        raketli.accelerate(0.35, 2)
    if right and left:
        raketli.accelerate(0.35, 3)
    if turbo:
        raketli.accelerate(0.5, 3)
    if raketli.xpos <= 6:
        # raketli.xvel = raketli.xvel / 3 * -1 
        raketli.xvel = 0 
        raketli.yvel /= 2 
        raketli.xpos = 7
    elif raketli.xpos >= width - 6:
        # raketli.xvel = raketli.xvel / 3 * -1
        raketli.xvel = 0
        raketli.yvel /= 2
        raketli.xpos = width - 7
    if raketli.ypos <= 6:
        # raketli.yvel = raketli.yvel / 3 * -1
        raketli.yvel = 0
        raketli.xvel /= 2
        raketli.ypos = 7
    elif raketli.ypos >= height - 6:
        # raketli.yvel = raketli.yvel / 3 * -1
        raketli.yvel = 0
        raketli.xvel /= 2
        raketli.ypos = height - 7

    
    for ball in np.arange(len(balls)):
        pygame.draw.circle(display, (50, 50, 50), (int(round(balls[ball].pos[0])), int(round(balls[ball].pos[1]))), balls[ball].rad, 1)
    
    raketli.move()
    # keys = [gas, left, right, back]
    # print(keys)
    # carpoints = [[], [], [], []]
    # pygame.draw.lines(display, (255, 100, 50), True, carpoints)
    # print(raketli.xvel)
    ppf = round(raketli.vel * 10) / 10
    geschwindigkeit(ppf, (raketli.xpos, raketli.ypos), int(raketli.vel * 3) + 20)
    # geschwindigkeit(dt)
    # tachometer:
    shake = np.random.rand((1)) * np.math.log10(raketli.vel + 1) / 10
    pygame.draw.line(display, (155, 0, 0), (width / 3, height - 20), (np.math.cos(np.math.log2(raketli.vel + 1) - np.pi - 0.5 + shake) * 40 + width / 3, np.math.sin(np.math.log2(raketli.vel + 1) - np.pi - 0.5 + shake) * 40 + height - 20))
    pygame.draw.arc(display, (100, 100, 100), (width / 3 - 41, height - 61, 82, 82), np.pi * 2 - 0.6, np.pi + 0.6, 3)
    # raketli:
    if turbo:
        pygame.draw.line(display, (255, 220, 50), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) - np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) - np.pi / 2) * 20), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) - np.pi / 2 - 0.3) * 21, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) - np.pi / 2 - 0.3) * 21), 3)
        pygame.draw.line(display, (255, 220, 50), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) + np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) + np.pi / 2) * 20), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) + np.pi / 2 + 0.3) * 21, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) + np.pi / 2 + 0.3) * 21), 3)
    if left:
        pygame.draw.line(display, (255, 150, 50), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) - np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) - np.pi / 2) * 20), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) - np.pi / 2 - 0.2) * 21, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) - np.pi / 2 - 0.2) * 21), 2)
    if right:
        pygame.draw.line(display, (255, 150, 50), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) + np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) + np.pi / 2) * 20), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) + np.pi / 2 + 0.2) * 21, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) + np.pi / 2 + 0.2) * 21), 2)
    pygame.draw.line(display, (255, 0, 50), (raketli.xpos, raketli.ypos), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi)) * 10, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi)) * 10), 2)
    pygame.draw.line(display, (255, 0, 50), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) - np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) - np.pi / 2) * 20), (raketli.xpos + np.math.cos(raketli.dire / (2 * np.pi) + np.pi / 2) * 20, raketli.ypos + np.math.sin(raketli.dire / (2 * np.pi) + np.pi / 2) * 20), 2)
    pygame.draw.circle(display, (255, 255, 255), (int(round(raketli.xpos)), int(round(raketli.ypos))), 5)
    pygame.display.update()