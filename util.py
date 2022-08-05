BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 500
STARTSCREEN, WAITING, INGAME, WIN, LOSE = 0, 1, 2, 3, 4
WALL, SPEED_LENGTH, START_DIST = 15, 5, 15
STARTPOS = ((START_DIST + WALL, START_DIST + WALL), (WIDTH - START_DIST -
            SPEED_LENGTH - WALL, HEIGHT - START_DIST - SPEED_LENGTH - WALL))


def sendData(conn, data):
    data = str(data[0]) + "," + str(data[1]) + "," + str(data[2])
    conn.sendall(str.encode(data))


def recvData(conn):
    data = conn.recv(1024).decode()
    data = data.split(",")
    return (int(data[0]), int(data[1]), int(data[2]))
