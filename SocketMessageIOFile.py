import socket, struct, typing

class SocketMessageIO:
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
        while received_length < message_length:
            chunk_o_data = connection.recv(1024).decode()
            message += chunk_o_data
            received_length += len(chunk_o_data)
        return message

    def send_message_to_socket(self,message: str, connection: socket) -> None:

        connection.sendall(struct.pack('>I', len(message)))
        connection.sendall(message.encode())