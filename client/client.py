import socket
import pickle
import time

data = input("Enter the server adress: ")

IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 2048


def constructdata(type, ip, data):
    dict = {"command": type, "ip": ip, "port": "", data: data}
    return dict


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADD_T)

    while True:
        data = pickle.loads(client.recv(SIZE))
        cmd = data["command"]
        print(data)

        if cmd == "msg":
            print(data["data"])

        cmd = input("> ")

        if cmd == "list":
            dict = {"command": "list", "ip": "", "port": "", "data": ""}
            client.send(pickle.dumps(dict))
        if cmd == "upload":
            reciever = "127.0.0.1"  # input("Enter Client IP > ")
            port = input("Enter Client Port > ")
            file_path = input("Enter file path > ")
            with open(file_path, "r") as f:
                while True:
                    data_stream = f.read(1024)
                    if not data_stream:
                        break
                    dict = {
                        "command": "upload",
                        "ip": reciever,
                        "port": port,
                        "data": data_stream,
                    }
                    client.send(pickle.dumps(dict))
                    time.sleep(0.001)
                dict = {
                    "command": "done",
                    "ip": reciever,
                    "port": port,
                    "data": "",
                }
                client.send(pickle.dumps(dict))

        if cmd == "recieve":
            with open("ex.txt", "a") as f:
                while True:
                    data = pickle.loads(client.recv(SIZE))
                    if data["command"] == "done":
                        break
                    f.write(data["data"])
        if cmd == "stop":
            break

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
