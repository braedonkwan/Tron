import socket
import threading
import time
from constants import (
    ADDRESS,
    PORT,
    MAX_PLAYERS,
    DISCONNECTED,
    PLAYER1,
    PLAYER2,
    QUEUE_SIZE
)

lock = threading.Lock()
player_properties = [str(DISCONNECTED), str(DISCONNECTED)]
player_ID = -1


def start_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen(QUEUE_SIZE)
    while True:
        print("Waiting for client...")
        client_socket, address = server_socket.accept()

        print("Accepted connection from {}:{}".format(*address))
        thread = threading.Thread(
            target=client_handler,
            args=(client_socket, set_player_ID(1)),
        )
        thread.start()


def client_handler(client_socket, playerID) -> None:
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
    set_player_count(-1)
    set_player_property(playerID, str(DISCONNECTED))
    client_socket.close()


def set_player_ID(factor) -> int:
    with lock:
        global player_ID
        player_ID += factor
        return player_ID


def set_player_property(player, value) -> None:
    with lock:
        global player_properties
        player_properties[player] = value


if __name__ == "__main__":
    start_server()
