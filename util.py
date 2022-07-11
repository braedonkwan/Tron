def sendData(conn, data):
    data = str(data[0]) + "," + str(data[1]) + "," + str(data[2])
    conn.sendall(str.encode(data))


def recvData(conn):
    data = conn.recv(1024).decode().split(",")
    return (int(data[0]), int(data[1]), int(data[2]))
