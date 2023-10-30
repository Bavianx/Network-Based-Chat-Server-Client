import socket 
import threading 
import time

# This is a list named 'clients' and a dictionary named 'nicknames' are defined to store the connected clients and their nicknames, respectively.
clients = []
nicknames = {}

def handle_client(socket, address):
    print(f"New connection from {address}")
    socket.send("Welcome to the chatroom! ".encode('utf-8'))
    nickname = socket.recv(2048).decode('utf-8')
    nicknames[address] = nickname
    print(f"User at {address} is {nickname}")
    while True:
        try:
            message = socket.recv(2048).decode('utf-8')
            # If a users message starts with / it will be checked 
            if message.startswith('/'):
                #if it follows up with /quit the socket will then close
                if message.startswith('/quit'):
                    socket.send('/quit'.encode('utf-8'))
                    socket.close()
                # Once the socket is closed the users nickname will be removed from the dictionary
                if socket in clients:
                    del clients[socket]
                    nickname = nicknames[address]
                    print(f"{nickname} has left the chat")
                    nicknames.pop(address)
                    break
            else:
                # Will create a time stamp that the server will see which will contain the users nickname and the time the message was sent 
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                message = f"{timestamp} {nicknames[address]}: {message}"
                print(message)
                for client_socket in clients:
                    if client_socket != socket:
                        client_socket.send(message.encode('utf-8'))
        except:
            print(f"Connection from {address} has been closed")
            if socket in clients:
                clients.remove(socket)
                if address in nicknames:
                    nicknames.pop(address)
            break


# This will create an IP socket which will allow us later on to create a connection from the server to the users client so they can communicate together.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Creating a personal address and a port which will link between both servers allowing for communication to be made.
server_address = ('127.0.0.1', 4444)
server_socket.bind(server_address)
# This allows the server to listen in for connections between the the server and client linking the Address and Port together.
server_socket.listen()
#This will print to the command line what the server address is listening on e.g. "127.0.0.1" , 4444
print(f"Server is listening on {server_address}...")


def message_send():
    while True:
        #prompt allowing the user to enter a message 
        message = input("Enter a message on the server: ")
        for client_socket in clients:
            client_socket.send(message.encode('utf-8'))

# Create thread for message sending
send_thread = threading.Thread(target=message_send)
send_thread.start()


while True:
    client_socket, client_address = server_socket.accept()
    # This will add the new client to the list of clients
    clients.append(client_socket)
    # This will create a new thread which will handle the client. args will pass the 'handle_client' function which will run the handle_client allowing a new thread to start running.
    clients_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    clients_thread.start()