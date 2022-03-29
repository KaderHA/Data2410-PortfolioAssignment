import socket
import sys, os, threading
from Bot import *                                                                               # Import all bot functions from Bot.py.

actions = ["work", "play", "eat", "cry", "sleep",                                               # List of known actions
           "fight", "sing", "hug", "bicker", "yell", 
           "complain", "walk"]


bots = {"bob": bob, "alice": alice, "dora": dora, "chuck": chuck, "user": user}                 # List to turn string to function poiunter.
host, port, bot = sys.argv[1], int(sys.argv[2]), sys.argv[3]
if (bot not in bots): bots[bot] = user                                                          # Make all unkown bots to user.

print(f"Welcome, you selected {bot.capitalize()}!")
print(f"Connecting to server at {host}:{port}...")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                               # Connect to the given ip and port
client_socket.connect((host, port))

client_socket.setblocking(False)
client_socket.send((bot.capitalize()).encode())                                                 # Send your name to the server

print("Connected! Waiting for messages from server...")

def receive_message():                                                                          # Function that returns a tuple of actions from server and actions from client
    server_action, client_action = "", None
    msg = client_socket.recv(1024)
    if not len(msg):                                                                            # if the message is an empty string, assume server is disconnecting
        print('Connection closed by server')
        os._exit(0)
            
    if (msg.decode().find("Host") != -1):                                                       # Check the message for the "Host"
        print(f"\nSuggestion from server!")
        print(f"{msg.decode()}")
        server_action = [action for action in actions if msg.decode().find(action) != -1][0]    # Loop over all actions and check if that action can be found in the message
        return (server_action, client_action)                                           
    else:
        client_action = [action for action in actions if msg.decode().find(action) != -1][0]    # Loop over all actions and check if that action can be found in the message
        print(f"{msg.decode()}\n(I don't have a response to that)\n")
        return (server_action, client_action)

def send_message(server_action, client_action):                                                 # Send a message to the server
    if client_action == server_action: client_action = None
    msg = (f"{bot.capitalize()}: " + bots[bot](server_action, client_action)).encode()
    print(f"{msg.decode()}\n")
    client_socket.send(msg)

def command_line_input_thread():
    while True:
        inpt = input()
        if inpt == 'q' or inpt == 'quit':
            client_socket.close()
            os._exit(0)

threading.Thread(target=command_line_input_thread).start()

action_server, action_client = "", None                                                         # Current actions
while True:                                                                                     # Endless loop to receive and send messages
    if action_server:                                                                           # If an suggestion is given by server, respond
        send_message(action_server, action_client)
    action_server, action_client = "", None

    try:                                                                                        # Since the clients receive is non blocking an error will be thrown if there is no message, ignore this.
        while True:
            action_server, action_client = receive_message()
    except Exception as e:
        if e is SystemExit:                                                                     # But do not ignore the system exit flag.
            break