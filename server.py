import socket
import util
import threading

data = [(-15, -15, -1), (-15, -15, -1)]


def serverloop(conn, pIndex):
    conn.sendall(str.encode(str(pIndex)))
    while True:
        data[pIndex] = util.recvData(conn)
        if data[pIndex] == (-15, -15, -1):
            break
        else:
            if pIndex == 1:
                reply = data[0]
            else:
                reply = data[1]
            util.sendData(conn, reply)
    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ""
    port = 5555
    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))
    s.listen(2)
    currentPlayer = 0
    while currentPlayer < 2:
        conn, addr = s.accept()
        thread = threading.Thread(
            target=serverloop, args=(conn, currentPlayer))
        thread.start()
        currentPlayer += 1


main()
