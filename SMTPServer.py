from socket import *

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 12000
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

while 1:
    print('new connection from client')
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    
    connectionSocket.send('220')
    # receive HELO
    sentence = connectionSocket.recv(1024)
    connectionSocket.send('250')

    # receive MAIL FROM

    # receive RCPT TO

    # receive DATA

    # receive endmsg

    # receive QUIT
    connectionSocket.close()