# importing Libraries
import socket
import pickle
import time

# socket size and server addresses
data = input("Enter the socket ftp-server address: ")
IP_ADD = data
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 2048

# returns a dictionary for pickle to serialize
def constructdata(type, ip, port, data):
    dict = {"command": type, "ip": ip, "port": port, "data": data}
    return dict


# INFO: Pickle is used to serialize data, loads will de-serialize and dumps will serialize

# main function
def main():
    # establishing connection to remote server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADD_T)

    while True:
        # waiting for input
        data = pickle.loads(client.recv(SIZE))
        cmd = data["command"]

        # if cmd == msg, print the data sent by server
        if cmd == "msg":
            print(data["data"])

        cmd = input("> ")

        # if cmd == list, a list request is sent to server whch returns active clients
        if cmd == "list":
            dict = {"command": "list", "ip": "", "port": "", "data": ""}
            client.send(pickle.dumps(dict))

        # if cmd == upload, file is uploaded to the desired client
        if cmd == "upload":
            reciever = input("Enter Client IP > ")
            port = input("Enter Client Port > ")
            file_path = input("Enter file path > ")

            filename = file_path.split("/")[-1]

            # pickle is used to serialize the data, and a handshake with file name is done
            client.send(pickle.dumps(constructdata("upload", reciever, port, filename)))

            client.recv(SIZE)
            # after server responds ok, the file starts uploading
            with open(file_path, "r") as f:
                while True:
                    data_stream = f.read(SIZE)
                    if not data_stream:
                        break
                    client.send(data_stream.encode("utf-8"))

                # after file is sent a command done is sent to mark the end of the upload
                time.sleep(0.001)
                dict = {
                    "command": "done",
                    "ip": reciever,
                    "port": port,
                    "data": "",
                }
                client.send(pickle.dumps(dict))

        # if cmd == receive, the client is set to receive mode to download data sent by another client
        if cmd == "receive":
            # file with <filename> is created
            filename = pickle.loads(client.recv(SIZE))["data"]
            with open(filename, "a") as f:
                while True:
                    data = client.recv(SIZE)
                    try:
                        x = data.decode("utf-8")
                        f.write(x)
                    except:
                        break

        # close the client
        if cmd == "stop":
            break

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()
