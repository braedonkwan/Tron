import socket
import pygame
from constants import *

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.color = color
        self.state = DISCONNECTED
        self.deathpoints = [STARTPOS[0], STARTPOS[1]]
        self.teleports = 3
        self.released = True

    def move(self, keys):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    if keys[pygame.K_SPACE] and self.teleports != 0 and self.released:
        if self.vx == SPEED:
            self.x += TELEDIST
        elif self.vx == -SPEED:
            self.x -= TELEDIST
        elif self.vy == SPEED:
            self.y += TELEDIST
        else:
            self.y -= TELEDIST
        self.teleports -= 1
        self.released = False
    elif (
        self.vx == 0 and keys[pygame.K_UP] == False and keys[pygame.K_DOWN] == False
    ):
        if keys[pygame.K_RIGHT]:
            self.vx = SPEED
            self.vy = 0
        elif keys[pygame.K_LEFT]:
            self.vx = -SPEED
            self.vy = 0
    elif (
        self.vy == 0
        and keys[pygame.K_RIGHT] == False
        and keys[pygame.K_LEFT] == False
    ):
        if keys[pygame.K_DOWN]:
            self.vy = SPEED
            self.vx = 0
        elif keys[pygame.K_UP]:
            self.vy = -SPEED
            self.vx = 0
    if self.released == False and keys[pygame.K_SPACE] == False:
        self.released = True

    def process(p):
        global options
        keys = pygame.key.get_pressed()
        if p.state == MENU:
            if keys[pygame.K_UP]:
                options = 0
            elif keys[pygame.K_DOWN]:
                options = 1
            elif keys[pygame.K_SPACE]:
                if options == 0:
                    p.state = INGAME
                else:
                    running = False
        elif p.state == ENDSCREEN:
            if keys[pygame.K_UP]:
                options = 0
            elif keys[pygame.K_DOWN]:
                options = 1
            if keys[pygame.K_SPACE]:
                if options == 0:
                else:
                    running = False
        elif self.p.state == util.INGAME and self.p2.state == util.INGAME:
            self.p.move(keys)
            self.p.update()
            self.p2.update()
            if (
                (self.p.x, self.p.y) not in self.deathpoints
                and self.p.x >= util.WALL
                and self.p.x <= util.WIDTH - self.p.width - util.WALL
                and self.p.y >= util.WALL
                and self.p.y <= util.HEIGHT - self.p.height - util.WALL
            ):
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

    def reset_game(PLAYERID):
        p = Player(STARTPOS[PLAYERID][0], STARTPOS[PLAYERID][1], GREEN)
        p2 = Player(STARTPOS[1 - PLAYERID][0], STARTPOS[1 - PLAYERID][1], RED)
        p.vx = -SPEED if PLAYERID else SPEED
        return p, p2

    def update(self):
        util.sendData(self.conn, (self.p.x, self.p.y, self.p.state))
        data = util.recvData(self.conn)
        self.p2.state = data[2]
        if self.p.state == util.INGAME and self.p2.state == util.INGAME:
            self.p2.x = data[0]
            self.p2.y = data[1]


    def render(self):
    if self.p.state == util.STARTSCREEN:
        pygame.draw.rect(self.screen, util.BLACK, (0, 0, util.WIDTH, util.HEIGHT))
        self.screen.blit(self.startscreen, (0, 0))
        if self.options == 0:
            pygame.draw.rect(self.screen, util.WHITE, (315, 218, 245, 100), 2)
        else:
            pygame.draw.rect(self.screen, util.WHITE, (315, 338, 245, 100), 2)
    elif self.p.state == util.INGAME or self.p.state == util.WAITING:
        self.p.draw(self.screen)
        self.p2.draw(self.screen)
        pygame.draw.rect(self.screen, util.BLUE, (0, 0, util.WALL, util.HEIGHT))
        pygame.draw.rect(
            self.screen,
            util.BLUE,
            (util.WIDTH - util.WALL, 0, util.WALL, util.HEIGHT),
        )
        pygame.draw.rect(
            self.screen,
            util.BLUE,
            (util.WALL, 0, util.WIDTH - util.WALL, util.WALL),
        )
        pygame.draw.rect(
            self.screen,
            util.BLUE,
            (util.WALL, util.HEIGHT - util.WALL, util.WIDTH - util.WALL, util.WALL),
        )
        self.drawText(
            "arial", "Teleports: " + str(self.p.teleports), util.WHITE, (0, 0), 12
        )
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


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ADDRESS, PORT))
    PLAYERID = int(client_socket.recv(1024).decode()) 
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update()
        render()
    print("Client is disconnecting...")
    client_socket.close()
    pygame.quit()
