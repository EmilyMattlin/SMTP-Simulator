from socket import *
import json
import ssl
import pprint

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 12008
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')


# Set up a new connection from the client
connectionSocket, addr = serverSocket.accept()

# Establish secure connection using TLS
secure_sock = ssl.wrap_socket(connectionSocket, server_side=True, ca_certs = "client.pem", certfile="server.pem", keyfile="server.key", cert_reqs=ssl.CERT_REQUIRED,
                           ssl_version=ssl.PROTOCOL_TLSv1_2)

print repr(secure_sock.getpeername())
print secure_sock.cipher()
print pprint.pformat(secure_sock.getpeercert())
cert = secure_sock.getpeercert()
print cert                        

# verify client
if not cert or ('organizationName', 'Wellesley') not in cert['subject'][3]: raise Exception("ERROR")

secure_sock.send('220')
# receive HELO
helo = secure_sock.recv(1024)
print("Expected HELO, received: " + helo)
# for now, assume commands are correct
secure_sock.send('250')

# receive MAIL FROM
mail_from = secure_sock.recv(1024)
mail_from_addr = mail_from.split("<")[1].split(">")[0]
print("Expected MAIL FROM, received:" + mail_from)
print("mail from address: " + mail_from_addr)
secure_sock.send('250')

# receive RCPT TO
rcpt_to = secure_sock.recv(1024)
rcpt_to_addr = rcpt_to.split("<")[1].split(">")[0]
print("Expected RCPT TO, received:" + rcpt_to)
print("rcpt to address: " + rcpt_to_addr)
secure_sock.send('250')

# receive DATA command
data_command = secure_sock.recv(1024)
print("expected DATA, received: ", data_command)
secure_sock.send('250')

# for json file for data storage
data = {}
counter = 0

messages = {}
server_alive = True

while server_alive:
    # receive msg
    msg = secure_sock.recv(1024)
    if 'QUIT' in msg:
        print("expected QUIT, received: ", quit)
        secure_sock.send('250')
        break
    print("expected msg, received: ", msg)
    messages[counter] = msg
    counter = counter + 1

    # receive endmsg
    end_msg = secure_sock.recv(1024)
    print("expected endmsg, received: ", end_msg)
    secure_sock.send('250')

# Close the secure socket for SMTP
secure_sock.close()

# Save the emails into json files
emails_list = []
for key in messages:
    print messages[key]
    emails_list.append({
        'mail_from': mail_from_addr,
        'rct_to': rcpt_to_addr,
        'message' : messages[key],
        'ID' : key
    })
data['emails'] = emails_list
with open('emailstorage.txt', 'w') as outfile:
    json.dump(data, outfile)

# Listen for HTTP GET request from client
# Set up a new connection from the client
connectionSocket, addr = serverSocket.accept()

# If an exception occurs during the execution of try clause
# the rest of the clause is skipped
# If the exception type matches the word after except
# the except clause is executed
try:
    print "the server is ready to receive"
    # Receives the request message from the client
    message = connectionSocket.recv(1024)

    # Extract the path of the requested object from the message
    # The path is the second part of HTTP header, identified by [1]
    filename = message.split()[1]

    # Because the extracted path of the HTTP request includes
    # a character '\', we read the path from the second character
    f = open(filename[1:])

    print f
    # Store the entire content of the requested file in a temporary buffer
    outputdata = f.read()

    print "output: " + outputdata

    #Send one HTTP header line into socket
    connectionSocket.send('HTTP/1.1 200 OK\r\n')

    connectionSocket.send('{"emails": [{"mail_from": "fake.email@gmail.com", "message": "t", "rct_to": "fake.email@gmail.com", "ID": 0}]}')
    #connectionSocket.send(outputdata.encode())
    #Send the content of the requested file to the client
    # for i in range(0, len(outputdata)):
    #     connectionSocket.send(outputdata[i])
    connectionSocket.close()

except IOError:
    #Send response message for file not found
    connectionSocket.send('HTTP/1.1 404 Not Found\r\n')

    #Close client socket
    connectionSocket.close()

# Client's Order of SMTP Operations:
# HELO
# MAIL FROM
# RCPT TO
# DATA
# msg1
# end_msg
# msg2
# end_msg
# msg3
# end_msg
# QUIT

'''
{
    "emails": [
        {
        "rcpt_to": "EMAIL ADDRESS",
        "mail_from": "EMAIL ADDRESS",
        "message": "email contents",
        "id": "0"
        },
        {
        "rcpt_to": "EMAIL ADDRESS",
        "mail_from": "EMAIL ADDRESS",
        "message": "email contents",
        "id": "1"
        },
        {
        "rcpt_to": "EMAIL ADDRESS",
        "mail_from": "EMAIL ADDRESS",
        "message": "email contents",
        "id": "2"
        }
    ]
}
'''
