import socket
import pickle

data = input("Enter the server adress: ")

IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 1024


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
            reciever = input("Enter Client IP > ")
            port = input("Enter Client Port > ")
            file_path = input("Enter file path > ")
            with open(file_path, "r") as f:
                while True:
                    data_stream = f.read(SIZE)
                    if not data_stream:
                        break
                    dict = {
                        "command": "upload",
                        "ip": reciever,
                        "port": port,
                        "data": data_stream.encode("utf-8"),
                    }
                    client.send(pickle.dumps(dict))
        if cmd == "recieve":
            with open("ex.txt", "a") as f:
                f.write(data["data"].decode("utf-8"))

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
