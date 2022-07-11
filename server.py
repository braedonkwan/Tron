import socket
import util
from _thread import *

clientstate = [(15, 15, 0), (1700, 945, 0)]


def threaded_client(conn, pIndex):
    util.sendData(conn, clientstate[pIndex])
    while True:
        try:
            clientstate[pIndex] = util.recvData(conn)
            if not clientstate[pIndex]:
                break
            else:
                if pIndex == 1:
                    reply = clientstate[0]
                else:
                    reply = clientstate[1]
            util.sendData(conn, reply)
        except:
            break
    conn.close()


def main():
    server = ""
    port = 5555
    currentPlayer = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))
    s.listen(2)
    while True:
        conn, addr = s.accept()
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


main()
