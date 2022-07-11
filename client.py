import pygame
import socket
import util


WIDTH = 1725
HEIGHT = 970
gamestate = [-1, -1]
deathpoints = []
win = pygame.display.set_mode((WIDTH, HEIGHT))
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    pygame.display.set_caption("Tron")
    server = socket.gethostbyname(socket.gethostname())
    port = 5555
    addr = (server, port)
    conn.connect(addr)
    data = util.recvData(conn)
    global p
    p = Player(data[0], data[1], 10, 10, (0, 255, 0))
    deathpoints.append((p.x, p.y))
    global pIndex
    if (p.x) == 15:
        p.vx = 5
        pIndex = 0
    else:
        p.vx = -5
        pIndex = 1
    gamestate[pIndex] = data[2]
    global p2
    p2 = Player(-30, -30, 10, 10, (255, 0, 0))
    gameloop()


def gameloop():
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        if gamestate[0] == 0 and gamestate[1] == 0:
            update()
            collisions()
            render()
        else:
            print("waiting for player 2")


def update():
    util.sendData(conn, (p.x, p.y, gamestate[pIndex]))
    data = util.recvData(conn)
    p2.x = data[0]
    p2.y = data[1]
    p2.update()
    p.move()


def collisions():
    return


def render():
    p.draw(win)
    p2.draw(win)
    pygame.display.update()


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.vx == 0 and keys[pygame.K_UP] == False and keys[pygame.K_DOWN] == False:
            if keys[pygame.K_RIGHT]:
                self.vx = 5
                self.vy = 0
            elif keys[pygame.K_LEFT]:
                self.vx = -5
                self.vy = 0
        elif self.vy == 0 and keys[pygame.K_RIGHT] == False and keys[pygame.K_LEFT] == False:
            if keys[pygame.K_DOWN]:
                self.vy = 5
                self.vx = 0
            elif keys[pygame.K_UP]:
                self.vy = -5
                self.vx = 0
        self.x += self.vx
        self.y += self.vy
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def main():
    init()


main()
