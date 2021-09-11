import socket
import base64

data = input("Enter the server adress: ")

IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 1024*4
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

        if cmd == "list":
            client.send(cmd.encode(FORMAT))

        if cmd == "upload":
            reciever = input("Enter Client IP> ")
            file_path = input("Enter file path > ")
            with open(file_path,'r') as f:
                data_stream = f.read(1024)
                temp = ("upload@"+reciever+"@")
                client.send((temp+base64.b64encode(data_stream)).encode(FORMAT))
                while data_stream:
                    data_stream = f.read(1024)
                    client.send((temp+base64.b64encode(data_stream)).encode(FORMAT))

        if cmd == "recieve":
            with open("experiment.jpg",'a') as f:
                f.write(base64.b64decode(msg))


    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
