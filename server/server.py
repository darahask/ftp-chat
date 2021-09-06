import os
import socket
import threading

IP_ADD = "0.0.0.0"
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 1024
FORMAT = "utf-8"
clients = {}
# SERVER_DATA_PATH = "server_data"


def handle_transfer(con, add):
    print(f"Client at {add} is connected")
    con.send("OK@Welcome to File Sharing Platform!!!".encode(FORMAT))

    while True:
        info = con.recv(SIZE).decode(FORMAT)
        info = info.split("@")
        action = info[0]

        if action == "LIST":
            ppl = "OK@Active Users: \n"

            for k, v in clients:
                ppl += f"{k}: {v}\n"

            con.send(ppl.encode(FORMAT))


def start_server():
    tserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tserver.bind(ADD_T)
    tserver.listen()
    print(f"Server started on {IP_ADD}:{PORT}.")

    while True:
        con, add = tserver.accept()
        clients[add] = 1
        thread = threading.Thread(target=handle_transfer, args=(con, add))
        thread.start()


if __name__ == "__main__":
    start_server()
