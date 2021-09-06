import socket

data = input("Enter the server adress: ")

IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 1024
FORMAT = "utf-8"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADD_T)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print("DISCONNECTED")
        elif cmd == "OK":
            print(msg)

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "LIST":
            client.send(cmd.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
