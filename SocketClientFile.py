import socket, struct
from SocketMessageIOFile import SocketMessageIO



if __name__ == '__main__':
    mySocket = socket.socket()
    manager = SocketMessageIO()
    name = input("What is your name? ")

    port = 3000
    mySocket.connect(('127.0.0.1', port))

    # send the user's name to the socket and get the confirmation from the host.
    manager.send_message_to_socket(name, mySocket)
    acknowledgement = manager.receive_message_from_socket(mySocket)
    print(acknowledgement)

    #now run the loop that checks for messages from the host.
    while True:
        msg = input ("What is the message? ")
        manager.send_message_to_socket(msg, mySocket)
        acknowledgement = manager.receive_message_from_socket(mySocket)
        print(acknowledgement)