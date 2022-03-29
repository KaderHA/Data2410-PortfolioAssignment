import select
import socket
import sys

host, port = '', int(sys.argv[1])                                                           # The ip and port adresees the server will be listening for

suggestions = ["Why don't we sing", "Let's take a walk", 
               "Let's yell!", "I feel like fighting right now",
               "Maybe we could try some bickering?",
               "What do you say about we start hugging?",
               "Let's start working"]                                  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                           # Bind the server to ip and port and listen for clients.
server_socket.bind((host, port))
server_socket.listen()

socket_list = [server_socket]                                                               # Make a list of sockets and clients.
active_clients = {}
names = []

expected_message_count = 0                                                                  # variables for keeping track of how many messages you expect, and the current message count.
message_count = 0

def add_client():                                                                           # A function that adds new client to the socket array.
    c, addr = server_socket.accept()       
    socket_list.append(c)
    name = c.recv(1024).decode()
    names.append(name)                                                                      # Add client to names array to wait until next round of conversations
    print(f"{name} has joined the chat!")


def remove_client(sock):                                                                    # A function that removes a client from socket list and active_clients dictonary
    print(f"{active_clients[sock]} disconnected.")
    socket_list.remove(sock)
    del active_clients[sock]

def handle_client_message(sock):
    global message_count, expected_message_count
    try:                                                                                    # try and except to check if the client is still connected                                                                                      
        msg = sock.recv(1024)
    except ConnectionAbortedError: 
        remove_client(sock)                                                                 # If client has lost connection, remove them from data structures.
        expected_message_count -= 1                                                         # Lower expected messages by one so the server doesn't wait for non existant client
        return
    if not len(msg):                                                                        # If the message is empty it is a clean exit from the client.               
        remove_client(sock)
        return
    print(f"{msg.decode()}")                                                                # Print the message and keep count over how many message has been received       
    message_count += 1
    for client in active_clients:                                                           # Boradcast to all clients  
        if client == sock: continue
        client.send(msg)   


def send_suggestion():
    global message_count, expected_message_count
    print('\n', str(suggestions))                                                       # Show all avaiable suggestions to user
    inpt = input(f"Select a suggestion by index (1-{len(suggestions)}): ")              # Let user choose which suggestion to pick
    if not inpt.isnumeric(): return False                                                    # Allow user to exit by typing a string
    suggestion = "Host: " + suggestions[int(inpt)-1]                                    # Assume user picks valid index, select that message as the suggestion.
        
    print('\n', suggestion, sep="")                                                     # Print the suggestion and send it to all connected clients,
    for client in active_clients:
        try:
            client.send(suggestion.encode())
            expected_message_count += 1
        except:    
            socket_list.remove(client)      
    return True                                            # and keep track of how many answers you expect


print(f'Listening for connections on {host}:{port}...')
while True:                                                                                 # Create a endless loop for back and fourth between server and client.
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], socket_list)

    for sock in read_sockets:                                                               # Looping over all reading socket and preforming an action
        if sock == server_socket:                                                           # If the readable socket is server, we know it is a new connection
            add_client()                                                                    # Add this connection to list of all sockets, and list of clients.
        else:                                                                               # If the readable socket isn't the server we know it is message from one of the clients. Read the message and broadcast it to all clients.
            handle_client_message(sock)
        
    for sock in error_sockets:                                                              # Looping over all error event sockets and removing them
        remove_client(sock)
    
    if message_count == expected_message_count:                                             # Check for if all the messages has been received before sending a suggestion.
        for index, name in enumerate(names):                                                # Loop over all names and add them to the active_clients
            active_clients[socket_list[-len(names) + index]] = name
        names.clear()

        message_count = 0
        expected_message_count = 0
        
        if not send_suggestion(): break