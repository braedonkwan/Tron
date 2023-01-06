import util
import socket
import pygame
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, QUIT)


class Client():
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tron")
        self.connectToServer()
        self.loadimages()
        self.options = 0
        self.p = Player(util.GREEN)
        self.p2 = Player(util.RED)
        self.p.state = util.STARTSCREEN
        self.pIndex = int(self.conn.recv(1024).decode())
        self.running = True
        self.gameloop()

    def connectToServer(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = socket.gethostbyname(socket.gethostname())
        port = 5555
        addr = (server, port)
        self.conn.connect(addr)

    def loadimages(self):
        self.startscreen = pygame.image.load("start_page.jpg")
        self.endscreen1 = pygame.image.load("end_page1.png")
        self.endscreen2 = pygame.image.load("end_page2.png")
        self.endscreen3 = pygame.image.load("end_page3.png")
        self.endscreen4 = pygame.image.load("end_page4.png")

    def gameloop(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
            self.process()
            self.update()
            self.render()
        util.sendData(self.conn, (-15, -15, -1))
        pygame.quit()

    def process(self):
        keys = pygame.key.get_pressed()
        if self.p.state == util.STARTSCREEN:
            if keys[K_UP]:
                self.options = 0
            elif keys[K_DOWN]:
                self.options = 1
            if keys[K_SPACE]:
                if self.options == 0:
                    self.reset()
                else:
                    self.running = False
        elif self.p.state == util.WIN or self.p.state == util.LOSE:
            if keys[K_LEFT]:
                self.options = 0
            elif keys[K_RIGHT]:
                self.options = 1
            if keys[K_SPACE]:
                if self.options == 0:
                    self.reset()
                else:
                    self.running = False
        elif self.p.state == util.INGAME and self.p2.state == util.INGAME:
            self.p.move(keys)
            self.p.update()
            self.p2.update()
            if ((self.p.x, self.p.y) not in self.deathpoints and self.p.x >= util.WALL and self.p.x <= util.WIDTH - self.p.width - util.WALL
                    and self.p.y >= util.WALL and self.p.y <= util.HEIGHT - self.p.height - util.WALL):
                self.deathpoints.append((self.p.x, self.p.y))
                self.deathpoints.append((self.p2.x, self.p2.y))
            else:
                self.p.state = util.LOSE
        elif self.p.state == util.INGAME and self.p2.state == util.LOSE:
            self.p.state = util.WIN
        elif self.p.state == util.WAITING and self.p2.state == util.WAITING:
            self.p.state = util.INGAME
            self.p.x = util.STARTPOS[self.pIndex][0]
            self.p.y = util.STARTPOS[self.pIndex][1]
            pygame.time.delay(500)

    def update(self):
        util.sendData(self.conn, (self.p.x, self.p.y, self.p.state))
        data = util.recvData(self.conn)
        self.p2.state = data[2]
        if self.p.state == util.INGAME and self.p2.state == util.INGAME:
            self.p2.x = data[0]
            self.p2.y = data[1]

    def render(self):
        if self.p.state == util.STARTSCREEN:
            pygame.draw.rect(self.screen, util.BLACK,
                             (0, 0, util.WIDTH, util.HEIGHT))
            self.screen.blit(self.startscreen, (0, 0))
            if self.options == 0:
                pygame.draw.rect(self.screen, util.WHITE,
                                 (315, 218, 245, 100), 2)
            else:
                pygame.draw.rect(self.screen, util.WHITE,
                                 (315, 338, 245, 100), 2)
        elif self.p.state == util.INGAME or self.p.state == util.WAITING:
            self.p.draw(self.screen)
            self.p2.draw(self.screen)
            pygame.draw.rect(self.screen, util.BLUE,
                             (0, 0, util.WALL, util.HEIGHT))
            pygame.draw.rect(self.screen, util.BLUE,
                             (util.WIDTH - util.WALL, 0, util.WALL, util.HEIGHT))
            pygame.draw.rect(self.screen, util.BLUE,
                             (util.WALL, 0, util.WIDTH - util.WALL, util.WALL))
            pygame.draw.rect(self.screen, util.BLUE,
                             (util.WALL, util.HEIGHT - util.WALL, util.WIDTH - util.WALL, util.WALL))
            self.drawText("arial", "Teleports: " +
                          str(self.p.teleports), util.WHITE, (0, 0), 12)
        elif self.p.state == util.WIN:
            if self.options == 0:
                self.screen.blit(self.endscreen1, (0, 0))
            else:
                self.screen.blit(self.endscreen2, (0, 0))
        elif self.p.state == util.LOSE:
            if self.options == 0:
                self.screen.blit(self.endscreen3, (0, 0))
            else:
                self.screen.blit(self.endscreen4, (0, 0))
        pygame.display.update()

    def drawText(self, font, msg, color, pos, size):
        font = pygame.font.SysFont(font, size)
        img = font.render(msg, True, color)
        self.screen.blit(img, pos)

    def reset(self):
        pygame.draw.rect(self.screen, util.BLACK,
                         (0, 0, util.WIDTH, util.HEIGHT))
        self.deathpoints = [util.STARTPOS[0], util.STARTPOS[1]]
        if self.pIndex:
            self.p.vx = -util.SPEED_LENGTH
        else:
            self.p.vx = util.SPEED_LENGTH
        self.p.vy = 0
        self.p.x = -15
        self.p.y = -15
        self.p.teleports = 3
        self.p.update()
        self.p2.x = -15
        self.p2.y = -15
        self.p2.update()
        self.p.state = util.WAITING


class Player():
    def __init__(self, color):
        self.x = -15
        self.y = -15
        self.vx = 0
        self.vy = 0
        self.width = util.SPEED_LENGTH
        self.height = util.SPEED_LENGTH
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)
        self.state = -1
        self.teleports = 3
        self.released = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, keys):
        if keys[K_SPACE] and self.teleports != 0 and self.released:
            if self.vx == util.SPEED_LENGTH:
                self.x += util.TELE_DIST
            elif self.vx == -util.SPEED_LENGTH:
                self.x -= util.TELE_DIST
            elif self.vy == util.SPEED_LENGTH:
                self.y += util.TELE_DIST
            else:
                self.y -= util.TELE_DIST
            self.teleports -= 1
            self.released = False
        elif self.vx == 0 and keys[K_UP] == False and keys[K_DOWN] == False:
            if keys[K_RIGHT]:
                self.vx = util.SPEED_LENGTH
                self.vy = 0
            elif keys[K_LEFT]:
                self.vx = -util.SPEED_LENGTH
                self.vy = 0
        elif self.vy == 0 and keys[K_RIGHT] == False and keys[K_LEFT] == False:
            if keys[K_DOWN]:
                self.vy = util.SPEED_LENGTH
                self.vx = 0
            elif keys[K_UP]:
                self.vy = -util.SPEED_LENGTH
                self.vx = 0
        if self.released == False and keys[K_SPACE] == False:
            self.released = True
        self.x += self.vx
        self.y += self.vy

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def main():
    client = Client(util.WIDTH, util.HEIGHT)


main()
