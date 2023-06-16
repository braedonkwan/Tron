import socket
import threading
import time
from constants import HOST, PORT, DISCONNECTED, CONNECTED, STARTPOS

connection_status = [DISCONNECTED, DISCONNECTED]
# player_attr[i] = "state,x1,y1,x2,y2,...,xn,yn"
player_attr = [str(STARTSCREEN) + "," + str(STARTPOS[0]), str(STARTSCREEN) + "," + str(STARTPOS[1])]
lock = threading.Lock()


# starts the server
def start_server():
    # sets up a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    running = True
    try:
        while running:
            # finds an open playerID
            playerID = -1
            if connection_status[0] == DISCONNECTED:
                playerID = 0
                connection_status[0] = CONNECTED
            elif connection_status[1] == DISCONNECTED:
                playerID = 1
                connection_status[1] = CONNECTED

            # if there is an open playerID
            if playerID != -1:
                print("Listening for clients...")
                client_socket, address = server_socket.accept()
                print("Accepted connection from {}:{}".format(*address))
                thread = threading.Thread(
                    target=client_handler, args=(client_socket, playerID)
                )
                thread.start()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()
        running = False


# handles client communication
def client_handler(client_socket, playerID):
    # send playerID to client
    client_socket.sendall(str(playerID).encode("utf-8"))

    while True:
        # receive data from client
        data_recv = client_socket.recv(1024).decode("utf-8")
        if not data_recv:
            break
        
        # update shared player data
        lock.acquire()
        try:
            player_attr[playerID] = player_attr[playerID] + data_recv
        finally:
            lock.release()

        # send shared opponent and delete it from memory
        lock.acquire()
        try:
            if playerID == 0:
                client_socket.sendall(str(player_attr[1]).encode("utf-8"))
            else:
                client_socket.sendall(str(player_attr[1]).encode("utf-8"))
        finally:
            lock.release()

    print("Player " + (playerID + 1) + " has disconnected.")
    client_socket.close()


if __name__ == "__main__":
    start_server()
