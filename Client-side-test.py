import socket
import threading
import datetime
encode = "ascii"

def receive_messages(clients_socket):
    while True:
        try:
            #Will receive message from server
            data = clients_socket.recv(2084)
            if not data:    
                break
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = data.decode()
            print(f"[{current_time}] {message}")
        except:
            print("There was an ERROR retrieving data from the server!!")
            break                                       

# This will create an IP socket which will allow us later on to create a connection from the server to the users client so they can communicate together.
clients_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This will connect the client socket to the server socket linking them for an established.
try:
    server_address = ('127.0.0.1', 4444)
    clients_socket.connect(server_address)
    # This message will be sent to the server when the client has established connection to the server through the correct server_address.
    nickname = input("Enter a nickname: ")
    message = f"{nickname}"
    clients_socket.send(message.encode())
except:
    print("There was an ERROR connecting to the server, please retry.")
    clients_socket.close()
    exit()

# This will start a new thread to receive messages.
receive_thread = threading.Thread(target=receive_messages, args=(clients_socket,))
receive_thread.start()

def message_send():
    while True:
        try:
            #The /quit command will close the server so no one will be able message which will display a printed error message
            message = input(f"{nickname}: ")
            if message == "/quit":
                clients_socket.send('/quit'.encode('utf-8'))
                clients_socket.close()
                break
            clients_socket.send(message.encode(encode))
        except:
            print("There was an ERROR sending data.")
            break

message_thread = threading.Thread(target=message_send)
message_thread.start()