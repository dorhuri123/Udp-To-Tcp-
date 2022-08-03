import socket
import sys

"""
The server receive from the user a text which is divided into packets (the data size of each packet is 100 bytes).
Each packet is build like that: packetID; data.
When a packet is received, the server return a confirmation message to the user that include the packet number.

The first packet that the server receive contains the number of packets that the client will send.
This number (called counter) is used to understand when the file is fully printed on the screen.
When the file is completely printed, the server again from the beginning.
"""


def server(s):
    counter = 0
    i = 1
    sys.stdout.flush()
    while True:
        data, addr = s.recvfrom(1024)

        # If the data is bigger than 100 bytes the server drop the packet
        if len(data) <= 100:
            # Using the delimiter ';' the server split the message into: index (the packet number) and the text
            index, text = data.decode('utf-8').split(';')
            # If the index is 0 its signify that is the first packet that contain the total number of packets
            if int(index) == 0:
                counter = int(text)
            # index == i => signify that is the right packet to print by the order
            if int(index) == i:
                print(text, end="")
                i += 1
            # Send a confirmation to the client
            s.sendto(data, addr)
            # i == counter => It's the end of the file, so the process is terminated
            if i == counter:
                break


if __name__ == '__main__':
    # Open a socket a listen on the port 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 12345))

    while True:
        server(s)
