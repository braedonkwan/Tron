import socket

# Screen Size
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500

# Game Settings
SPEED = 5
PLAYER_SIZE, WALL_SIZE = SPEED, 15
STARTDIST, TELEDIST = 15, 50
STARTPOS = (
    (STARTDIST + WALL_SIZE, STARTDIST + WALL_SIZE),
    (
        SCREEN_WIDTH - STARTDIST - PLAYER_SIZE - WALL_SIZE,
        SCREEN_HEIGHT - STARTDIST - PLAYER_SIZE - WALL_SIZE,
    ),
)

# Network Settings
ADDRESS, PORT = socket.gethostbyname(socket.gethostname()), 5675
MAX_PLAYERS = 2
QUEUE_SIZE = 8

# Client States
DISCONNECTED, MENU, INGAME, ENDSCREEN = 0, 1, 2, 3
PLAYER1, PLAYER2 = 0, 1

# Colors
BLUE, GREEN, RED, BLACK, WHITE = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 0),
    (255, 255, 255),
)
