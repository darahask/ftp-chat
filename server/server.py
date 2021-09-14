import socket
import threading
import pickle
import time

IP_ADD = "0.0.0.0"
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 2048
clients = {}


def constructdata(type, ip, port, data):
    dict = {"command": type, "ip": ip, "port": port, "data": data}
    return dict


def sendto(data, address):
    sendcon = clients[address]
    sendcon.send(data)


def handle_transfer(con, add, socket):
    print(f"Client at {add} is connected")

    con.send(pickle.dumps(constructdata("msg", "", "", "Welcome to file transfer !!!")))

    while True:
        info = pickle.loads(con.recv(SIZE))
        action = info["command"]

        if action == "list":
            ppl = "Active Users: \n"

            for k, v in clients:
                ppl += f"{k}: {v}\n"

            con.send(pickle.dumps(constructdata("msg", "", "", ppl)))

        if action == "upload":
            sendto(
                pickle.dumps(constructdata("recieve", "", "", info["data"])),
                (info["ip"], int(info["port"])),
            )

        if action == "done":
            sendto(
                pickle.dumps(constructdata("done", "", "", "")),
                (info["ip"], int(info["port"])),
            )
            time.sleep(0.001)
            sendto(
                pickle.dumps(constructdata("msg", "", "", "file transfer done")),
                (info["ip"], int(info["port"])),
            )
            con.send(pickle.dumps(constructdata("msg", "", "", "file sent")))


def start_server():
    tserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tserver.bind(ADD_T)
    tserver.listen()
    print(f"Server started")

    while True:
        con, add = tserver.accept()
        clients[add] = con
        thread = threading.Thread(target=handle_transfer, args=(con, add))
        thread.start()


if __name__ == "__main__":
    start_server()
