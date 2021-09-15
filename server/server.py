# importing libraries
import socket
import threading
import pickle
import time

# configuring ip address of server
IP_ADD = "0.0.0.0"
PORT = 2222
ADD_T = (IP_ADD, PORT)
SIZE = 2048

# a dictionary for storing (address,client) key-value pairs
clients = {}

# returns a dictionary for pickle to serialize
def constructdata(type, ip, port, data):
    dict = {"command": type, "ip": ip, "port": port, "data": data}
    return dict


# forwards data to a client at an address
def sendto(data, address):
    sendcon = clients[address]
    sendcon.send(data)


# a thread function which handles the logic of file transfer
def handle_transfer(con, add):
    # sending welcome message to client
    print(f"Client at {add} is connected")
    con.send(pickle.dumps(constructdata("msg", "", "", "Welcome to file transfer !!!")))

    try:
        # accept and decode requests by client
        while True:
            info = pickle.loads(con.recv(SIZE))
            action = info["command"]

            # sends list of active users to client
            if action == "list":
                ppl = "Active Users: \n"

                for k, v in clients:
                    ppl += f"{k}: {v}\n"

                con.send(pickle.dumps(constructdata("msg", "", "", ppl)))

            # transfering data from one client to another
            if action == "upload":
                # storing the ip address and port number of the client to send and sending headers
                ip = info["ip"]
                port = info["port"]
                filename = info["data"]

                # sending file-name to the recevier client
                sendto(
                    pickle.dumps(constructdata("", "", "", filename)), (ip, int(port))
                )
                # sending a confirmation to sender client
                con.send("OK".encode("utf-8"))

                # forwarding data content packets to receiver client
                while True:
                    co = con.recv(SIZE)
                    try:
                        # if the data is of header type(JSON) then close the connection
                        x = pickle.loads(co)

                        if x["command"] == "done":
                            # sending close instruction to receiver client
                            sendto(
                                pickle.dumps(constructdata("", "", "", "")),
                                (ip, int(port)),
                            )
                            time.sleep(1)

                            # notifyting sender and receiver that the file transfer is complete
                            # here con is instance of sender client, receiver clients instance is
                            # fetched using the dictionary
                            sendto(
                                pickle.dumps(
                                    constructdata("msg", "", "", "file transfer done")
                                ),
                                (ip, int(port)),
                            )

                            con.send(
                                pickle.dumps(constructdata("msg", "", "", "file sent"))
                            )
                            break
                    except:
                        # id data is content type(utf-8) forward it to receiver client
                        sendto(
                            co,
                            (info["ip"], int(info["port"])),
                        )
    except:
        # client is disconnected
        clients.pop(add)
        print(f"Client at {add} is disconnected")


# starting the lifecycle of the socket server, create->bind->listen->accept
def start_server():
    tserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tserver.bind(ADD_T)
    tserver.listen()
    print(f"Server started")
    # accepts multiple incoming connections
    while True:
        con, add = tserver.accept()
        # add all client objects to dictionary
        clients[add] = con
        # enable seperate thread for each connection
        thread = threading.Thread(target=handle_transfer, args=(con, add))
        # starting thread
        thread.start()


if __name__ == "__main__":
    start_server()
