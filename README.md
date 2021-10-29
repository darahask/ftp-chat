# ftp-chat

Transfer files between devices connected to same hosted server.

File structure:

- client/client.py
- server/server.py

## client.py

Contains the commands from client side and also defines the functionalities of the client through console input.

## server.py

This contains the server sided funtionalitites. It is the point of contact for all clients and it provides a gateway to the clients to send files without storing within itself.

## Steps to run

### Running a server

```bash
> python3 server/server.py
```

### Running the client

```bash
> python3 client/client.py
> Enter the socket IP address: (server IP address expected which can be found ifconfig/ipconfig in linux and windows respectively)
```

- Running of clients in different computers connected to same router is preffered, if clients are run on same computer, they should run in different folders.

Commands available for clients: `list`, `upload`, `receive`, `stop`.

Detailed description is available [here](Report.pdf)
