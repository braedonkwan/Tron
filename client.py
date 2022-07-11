import pygame
import socket
import util


WIDTH = 1725
HEIGHT = 970
deathpoints = []
win = pygame.display.set_mode((WIDTH, HEIGHT))
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    pygame.display.set_caption("Tron")
    pygame.font.init()
    server = socket.gethostbyname(socket.gethostname())
    port = 5555
    addr = (server, port)
    conn.connect(addr)
    data = util.recvData(conn)
    global p
    p = Player(data[0], data[1], 10, 10, (0, 255, 0))
    deathpoints.append((p.x, p.y))
    if (p.x) == 15:
        p.vx = 5
    else:
        p.vx = -5
    p.gamestate = 1
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
        if p.gamestate == 1 and p2.gamestate == 1:
            p.move()
            update()
            collisions()
            render()
        else:
            update()
            render()


def update():
    p.update()
    util.sendData(conn, (p.x, p.y, p.gamestate))
    data = util.recvData(conn)
    p2.x = data[0]
    p2.y = data[1]
    p2.gamestate = data[2]
    p2.update()


def collisions():
    if (p.x, p.y) not in deathpoints and p.x >= 0 and p.x <= WIDTH - p.width and p.y >= 0 and p.y <= HEIGHT - p.height:
        deathpoints.append((p.x, p.y))
        deathpoints.append((p2.x, p2.y))
    else:
        p.gamestate = 2


def render():
    p.draw(win)
    p2.draw(win)
    if p.gamestate == 2:
        drawText("impact", (255, 255, 255), "You Lose!!!",
                 (WIDTH / 2, HEIGHT / 2), 60)
    elif p2.gamestate == 2:
        drawText("impact", (255, 255, 255), "You Win!!!",
                 (WIDTH / 2, HEIGHT / 2), 60)
    pygame.display.update()


def drawText(font, color, text, pos, size):
    f = pygame.font.SysFont(font, size)
    s = f.render(text, True, color)
    t = s.get_rect()
    t.center = pos
    win.blit(s, t)


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.gamestate = 0
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

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def main():
    init()


main()
