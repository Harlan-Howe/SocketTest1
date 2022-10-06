import socket, struct, typing

class SocketMessageIO:
    """
    A utility class that makes it easy to send and receive messages from a socket in the format of a packed length of
    the message, followed by the message.
    """
    def receive_message_from_socket(self, connection: socket) -> str:
        """
        Waits until the socket provides a message in the form of a packed length of the message and the message itself.
        The message could conceivably be quite long, so it will do multiple reads of the socket until all the data arrives
        before returning the message.
        :param connection: the socket that it is listening to
        :return: a string containing the content of the message that was sent.
        Throws a ConnectionAbortedError exception if this socket has been discontinued.
        """
        message_length_str = connection.recv(4)
        if message_length_str == b'':
            print("no data - disconnected?")
            raise ConnectionAbortedError("Disconnected.")
        message_length = struct.unpack('>I', message_length_str)[0]
        received_length = 0
        message = ""
        # we're going to ask to receive data from the socket, but it may arrive in separate sections of data. For
        # instance, we might be expecting a message of length 512, but it could come in two "chunks" of 200 and 312.
        # Moreover, we're only asking for data from the socket up to size 1024, so a longer message might require
        # several reads of the socket.
        # But the goal is to get the entire message.
        while received_length < message_length:
            request_length = min(1024, message_length-received_length)
            chunk_o_data = connection.recv(request_length).decode()
            message += chunk_o_data
            received_length += len(chunk_o_data)
        return message

    def send_message_to_socket(self,message: str, connection: socket) -> None:
        """
        Sends the given message to the given socket in the format of the packed length of the message, followed by
        the encoded message, itself.
        :param message: the message to send
        :param connection: the socket to send it to
        :return: None.
        """
        connection.sendall(struct.pack('>I', len(message)))
        connection.sendall(message.encode())