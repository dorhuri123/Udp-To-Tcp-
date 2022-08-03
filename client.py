import socket
import sys

# Global variables
SERVER_PORT = ""
SERVER_IP = ""
FILE_NAME = ""
SERVER_ADDR = ""
TIMEOUT = 11
READSIZE = 94


"""
The client open a file (using the name received by the user) and sent it to the server.
Each packet (contain 92 Bytes, that include 4 bytes for the number of the packet and 88 bytes of data) is sent to the
server and the server return a confirmation using the the packet index.
When the last packet is sent, the client sent a an EOF signal to signify the end of the file. 
"""


def client(count):
    # Open the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(TIMEOUT)

    # Send the number of packets to the server
    packet = (str(0) + ";" + str(count)).encode('utf-8')
    while True:
        if 1 == send_rec(s, packet, 0, str(count)):
            break
            
    # Open the file
    file = open(FILE_NAME, "r")
    data = file.read(READSIZE)

    # The variable i significant the number of the packet
    eof = 0
    i = 1
    while data:
        # The packet include: packetID; text
        packet = (str(i) + ";" + data).encode('utf-8')

        # If the function return 1, then keep going to the next packet
        # Else, resend it to the server
        if 1 == send_rec(s, packet, i, data):
            data = file.read(READSIZE)
            i += 1
            if i == count:
                break
        if i == count:
            eof += 1
        if eof == 2:
            break

    # Close socket and file read mode
    s.close()
    file.close()


# This function count the numberof packet that the user will send.
def packet_counter():
    res = 0
    try:
        file = open(FILE_NAME, "r")
        data = file.read(READSIZE)
        res += 1
        while data:
            data = file.read(READSIZE)
            res += 1
        file.close()
    except IOError:
        return 0
    return res


"""
This function send the packet to the server and receive a confirmationfrom the server.
If after 11 sec the client dont get an answer,  the function return 0.
"""


def send_rec(s, packet, index, text):
    try:
        s.sendto(packet, SERVER_ADDR)
        res, addr = s.recvfrom(100)
        i, data = res.decode('utf-8').split(';')
        if index != int(i) or data != text:
            return 0
    except socket.timeout:
        return 0
    return 1


# The function check the validity of the ip and port
def valid_ip_port(ip, port):
    if (port > 65535) or (port < 0):
        return 0
    ip = ip.split('.')
    if len(ip) == 4:
        for i in ip:
            if (i.isdigit() == 0) or (int(i) < 0) or (int(i) > 255):
                return 0
        return 1
    return 0
    
    
if __name__ == '__main__':
    # Check if the user arg contain: Port, IP and file name
    if (3 == (len(sys.argv) - 1)) and valid_ip_port(sys.argv[2], int(sys.argv[1])):
        SERVER_PORT = int(sys.argv[1])
        SERVER_IP = sys.argv[2]
        FILE_NAME = sys.argv[3]
        SERVER_ADDR = (SERVER_IP, SERVER_PORT)

        # Get the number of packet that the client will sent, and launch the client process
        counter = packet_counter()
        if counter > 0:
            client(counter)
