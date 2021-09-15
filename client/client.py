import socket
import pickle
import time

data = input("Enter the server adress: ")

IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 2048


def constructdata(type, ip, port, data):
    dict = {"command": type, "ip": ip, "port": port, "data": data}
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

            filename = file_path.split("/")[-1]

            client.send(pickle.dumps(constructdata("upload", reciever, port, filename)))
            print("1")
            client.recv(SIZE)
            print("3")
            with open(file_path, "r") as f:
                while True:
                    data_stream = f.read(SIZE)
                    if not data_stream:
                        break
                    client.send(data_stream.encode("utf-8"))
                time.sleep(0.001)
                dict = {
                    "command": "done",
                    "ip": reciever,
                    "port": port,
                    "data": "",
                }
                client.send(pickle.dumps(dict))

        if cmd == "recieve":
            filename = pickle.loads(client.recv(SIZE))["data"]
            with open(filename, "a") as f:
                while True:
                    data = client.recv(SIZE)
                    try:
                        x = data.decode("utf-8")
                        f.write(x)
                    except:
                        break
        if cmd == "stop":
            break

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
