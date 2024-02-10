import socket
import pygame
from constants import *


class Opponent:
    def __init__(self, player_id: int):
        self.state = OFFLINE
        self.movements = []
        self.updates = str(OFFLINE)
        self.color = RED if player_id == PLAYER1 else GREEN
        self.width, self.height = PLAYER_SIZE, PLAYER_SIZE

    def draw(self, screen: pygame.Surface) -> None:
        for move in self.movements:
            pygame.draw.rect(
                screen, self.color, (move[X], move[Y], self.width, self.height)
            )
        self.movements = []

    def process_updates(self) -> None:
        temp = self.updates.split(",")
        self.state = int(temp[STATE])
        if len(temp) > 1:
            for i in range(STATE + 1, len(temp), 2):
                self.movements.append((int(temp[i]), int(temp[i + 1])))

    def reset(self) -> None:
        self.movements = []


class Player:
    def __init__(self, id: int) -> None:
        self.id = id
        self.x, self.y = None, None
        self.vx, self.vy = None, None
        self.width, self.height = PLAYER_SIZE, PLAYER_SIZE
        self.color = GREEN if id == PLAYER1 else RED
        self.state = WAITING
        self.teleports = None
        self.released = True

    def move(self) -> None:
        keys = pygame.key.get_pressed()
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
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collision(self, deathpoints: set) -> None:
        if (
            (self.x, self.y) in deathpoints
            or self.x >= SCREEN_WIDTH - WALL_SIZE
            or self.x <= WALL_SIZE - PLAYER_SIZE
            or self.y >= SCREEN_HEIGHT - WALL_SIZE
            or self.y <= WALL_SIZE - PLAYER_SIZE
        ):
            self.state = LOSE

    def reset(self) -> None:
        self.state = INGAME
        self.teleports = MAX_TELEPORTS
        self.released = False
        self.x, self.y = STARTPOS[self.id][X], STARTPOS[self.id][Y]
        self.vx, self.vy = SPEED if self.id == PLAYER1 else -SPEED, 0


tick_counter = 0


def draw_text(
    screen: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    font_size: int,
    color: tuple[int, int, int],
    centered: bool,
) -> pygame.Rect:
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if centered:
        text_rect = text_surface.get_rect(center=pos)
    else:
        text_rect = text_surface.get_rect(x=pos[X], y=pos[Y])
    screen.blit(text_surface, text_rect.topleft)
    return text_rect


def draw_walls() -> None:
    pygame.draw.rect(screen, BLUE, (0, 0, WALL_SIZE, SCREEN_HEIGHT))
    pygame.draw.rect(
        screen, BLUE, (SCREEN_WIDTH - WALL_SIZE, 0, WALL_SIZE, SCREEN_HEIGHT)
    )
    pygame.draw.rect(screen, BLUE, (0, 0, SCREEN_WIDTH, WALL_SIZE))
    pygame.draw.rect(
        screen, BLUE, (0, SCREEN_HEIGHT - WALL_SIZE, SCREEN_WIDTH, WALL_SIZE)
    )


def reset_game(
    player: Player, opponent: Opponent, deathpoints: set, screen: pygame.Surface
) -> None:
    global tick_counter
    tick_counter = 0
    screen.fill(BLACK)
    draw_walls()
    player.reset()
    opponent.reset()
    deathpoints.clear()
    deathpoints.update(STARTPOS)


def waiting_screen(
    player: Player, opponent: Opponent, deathpoints: set, screen: pygame.Surface
) -> None:
    global tick_counter
    tick_counter += 1
    screen.fill(BLACK)
    text_box = draw_text(
        screen,
        "Waiting for Opponent",
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        FONT_SIZE,
        WHITE,
        True,
    )
    animation_pos = (text_box.x + text_box.width, text_box.y)
    if tick_counter <= WAITING_ANIMATION_TIMER:
        draw_text(screen, ".", animation_pos, FONT_SIZE, WHITE, False)
    elif tick_counter <= WAITING_ANIMATION_TIMER * 2:
        draw_text(screen, "..", animation_pos, FONT_SIZE, WHITE, False)
    elif tick_counter <= WAITING_ANIMATION_TIMER * 3:
        draw_text(screen, "...", animation_pos, FONT_SIZE, WHITE, False)
        if tick_counter == WAITING_ANIMATION_TIMER * 3:
            tick_counter = 0
    if opponent.state == WAITING:
        reset_game(player, opponent, deathpoints, screen)


def end_screen(player: Player, opponent: Opponent, screen: pygame.Surface) -> None:
    global tick_counter
    tick_counter += 1
    if tick_counter >= END_SCREEN_TIMER:
        screen.fill(BLACK)
        draw_text(
            screen,
            "Press to Space to Play Again",
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            FONT_SIZE,
            WHITE,
            True,
        )
    elif player.state == WIN:
        draw_text(
            screen,
            "You Win",
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            FONT_SIZE,
            WHITE,
            True,
        )
    elif player.state == LOSE and opponent.state == LOSE:
        draw_text(
            screen,
            "Its a Tie",
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            FONT_SIZE,
            WHITE,
            True,
        )
    elif player.state == LOSE and opponent.state == WIN:
        draw_text(
            screen,
            "You Lose",
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            FONT_SIZE,
            WHITE,
            True,
        )
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.state = WAITING
        tick_counter = 0


def process(
    player: Player, opponent: Opponent, deathpoints: set, screen: pygame.Surface
) -> None:
    opponent.process_updates()
    if player.state == WAITING:
        waiting_screen(player, opponent, deathpoints, screen)
    elif player.state == INGAME and opponent.state == INGAME:
        player.move()
        deathpoints.update(opponent.movements)
        player.collision(deathpoints)
        deathpoints.add((player.x, player.y))
        player.draw(screen)
        opponent.draw(screen)
    elif (
        opponent.state == LOSE or opponent.state == OFFLINE
    ) and player.state == INGAME:
        player.state = WIN
    elif player.state == WIN or player.state == LOSE:
        end_screen(player, opponent, screen)
    pygame.display.flip()


def update(client_socket: socket.socket, player: Player, opponent: Opponent) -> None:
    if player.state == INGAME and opponent.state == INGAME:
        client_socket.sendall(
            (str(player.state) + "," + str(player.x) + "," + str(player.y)).encode(
                "utf-8"
            )
        )
    else:
        client_socket.sendall(str(player.state).encode("utf-8"))
    opponent.updates = client_socket.recv(1024).decode("utf-8")


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron")
    address = socket.gethostbyname(socket.gethostname())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, PORT))
    player = Player(int(client_socket.recv(1024).decode("utf-8")))
    opponent = Opponent(player.id)
    deathpoints = set()
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        process(player, opponent, deathpoints, screen)
        update(client_socket, player, opponent)
    print("Disconnecting...")
    client_socket.close()
    pygame.quit()
