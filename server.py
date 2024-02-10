import socket
import threading
from constants import (
    WAITING,
    OFFLINE,
    PLAYER1,
    PLAYER2,
    QUEUE_SIZE,
    MAX_PLAYERS,
    PORT,
    STATE,
)

connection_count = 0
player_properties = [str(OFFLINE), str(OFFLINE)]
lock = threading.Lock()


def server_loop(server_socket: socket.socket) -> None:
    global connection_count
    while True:
        print("Waiting for client...")
        client_socket, address = server_socket.accept()
        if connection_count < MAX_PLAYERS:
            with lock:
                connection_count += 1
            print("Accepted connection from {}:{}".format(*address))
            thread = threading.Thread(target=client_handler, args=(client_socket,))
            thread.start()
        else:
            print("Declined connection from {}:{}".format(*address))


def set_player_ID() -> int:
    with lock:
        if player_properties[PLAYER1] == str(OFFLINE):
            player_properties[PLAYER1] = str(WAITING)
            return PLAYER1
        else:
            player_properties[PLAYER2] = str(WAITING)
            return PLAYER2


def client_handler(client_socket: socket.socket) -> None:
    global connection_count
    player_id = set_player_ID()
    client_socket.sendall(str(player_id).encode("utf-8"))
    while True:
        try:
            data_recv = client_socket.recv(1024).decode("utf-8")
            if not data_recv:
                break
            update_properties(player_id, data_recv)
            update_client(player_id, client_socket)
        except:
            break
    print("Player " + str(player_id + 1) + " has disconnected.")
    with lock:
        connection_count -= 1
        player_properties[player_id] = str(OFFLINE)
    client_socket.close()


def update_properties(player_id: int, data_recv: str) -> None:
    with lock:
        player_properties[player_id] = (
            data_recv[STATE]
            + player_properties[player_id][STATE + 1 :]
            + data_recv[STATE + 1 :]
        )


def update_client(player_id: int, client_socket: socket.socket) -> None:
    with lock:
        if player_id == PLAYER1:
            client_socket.sendall(player_properties[PLAYER2].encode("utf-8"))
            player_properties[PLAYER2] = player_properties[PLAYER2][STATE]
        else:
            client_socket.sendall(player_properties[PLAYER1].encode("utf-8"))
            player_properties[PLAYER1] = player_properties[PLAYER1][STATE]


if __name__ == "__main__":
    address = socket.gethostbyname(socket.gethostname())
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, PORT))
    server_socket.listen(QUEUE_SIZE)
    server_loop(server_socket)
