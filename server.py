import socket
import threading
import time
from constants import (
    ADDRESS,
    PORT,
    MAXCLIENTS,
    WAITTIME,
    DISCONNECTED,
    PLAYER1,
    PLAYER2,
)

lock = threading.Lock()
player_properties = [str(DISCONNECTED), str(DISCONNECTED)]
player_count = 0


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen(MAXCLIENTS)
    while True:
        if read_player_count() < MAXCLIENTS:
            print("Waiting for client...")
            client_socket, address = server_socket.accept()
            print("Accepted connection from {}:{}".format(*address))
            thread = threading.Thread(
                target=client_handler,
                args=(client_socket, read_player_count()),
            )
            thread.start()
            temp = read_player_count() + 1
            set_player_count(temp)
        else:
            print("Server is full...")
            time.sleep(WAITTIME)


def client_handler(client_socket, playerID) -> None:
    global player_count
    client_socket.sendall(str(playerID).encode("utf-8"))
    while True:
        data_recv = client_socket.recv(1024).decode("utf-8")
        if not data_recv:
            break
        with lock:
            player_properties[playerID] += data_recv
            if playerID == PLAYER1:
                client_socket.sendall(player_properties[PLAYER2].encode("utf-8"))
                player_properties[PLAYER2] = player_properties[PLAYER2][0]
            else:
                client_socket.sendall(player_properties[PLAYER1].encode("utf-8"))
                player_properties[PLAYER1] = player_properties[PLAYER1][0]
    print("Player " + str(playerID + 1) + " has disconnected.")
    with lock:
        player_count -= 1
        player_properties[playerID] = str(DISCONNECTED)
    client_socket.close()


def set_player_count(value) -> None:
    with lock:
        global player_count
        player_count = value


def read_player_count() -> int:
    with lock:
        global player_count
        return player_count


def set_player_property(player, value) -> None:
    with lock:
        global player_properties
        player_properties[player] = value


def read_player_property(player) -> str:
    with lock:
        global player_properties
        return player_properties[player]


if __name__ == "__main__":
    start_server()
