import socket
import base64
import pickle

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

        if cmd == "msg":
            print(data["data"])
            cmd = input("> ")

        if cmd == "list":
            dict = {"command": "list", "ip": "", "port": "", "data": ""}
            client.send(pickle.dumps(dict))

        if cmd == "upload":
            reciever = input("Enter Client IP > ")
            port = input("Enter Client Port > ")
            file_path = input("Enter file path > ")
            with open(file_path, "r") as f:
                data_stream = f.read()
                dict = {
                    "command": "upload",
                    "ip": reciever,
                    "port": port,
                    "data": data_stream.encode("utf-8"),
                }
                client.send(pickle.dumps(dict))
                # while data_stream:
                #     data_stream = f.read(1024)
                #     client.send((temp+base64.b64encode(data_stream)).encode(FORMAT))

        if cmd == "recieve":
            # with open("experiment.", "a") as f:
            print(data["data"])
            # f.write(base64.b64decode(msg))

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
