from socket import *
import json

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 12001
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

# create json file for data storage
data = {}
counter = 0

# Set up a new connection from the client
connectionSocket, addr = serverSocket.accept()
    
connectionSocket.send('220')
# receive HELO
helo = connectionSocket.recv(1024)
print("Expected HELO, received: " + helo)
# for now, assume commands are correct
connectionSocket.send('250')

# receive MAIL FROM
mail_from = connectionSocket.recv(1024)
mail_from_addr = mail_from.split("<")[1].split(">")[0]
print("Expected MAIL FROM, received:" + mail_from)
print("mail from address: " + mail_from_addr)
connectionSocket.send('250')

# receive RCPT TO
rcpt_to = connectionSocket.recv(1024)
rcpt_to_addr = rcpt_to.split("<")[1].split(">")[0]
print("Expected RCPT TO, received:" + rcpt_to)
print("rcpt to address: " + rcpt_to_addr)
connectionSocket.send('250')

# receive DATA command
data_command = connectionSocket.recv(1024)
print("expected DATA, received: ", data_command)
connectionSocket.send('250')

messages = {}
while 1:
    # receive msg
    msg = connectionSocket.recv(1024)
    if 'QUIT' in msg:
        print("expected QUIT, received: ", quit)
        connectionSocket.send('250')
        break
    print("expected msg, received: ", msg)
    messages[counter] = msg
    counter = counter + 1

    # receive endmsg
    end_msg = connectionSocket.recv(1024)
    print("expected endmsg, received: ", end_msg)
    connectionSocket.send('250')

connectionSocket.close()

# save the email into data
data["mail_from"] = mail_from_addr
data["rcpt_to"] = rcpt_to_addr
data['messages'] = messages

json_data = json.dumps(data)
print(json_data)

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

# Expected JSON:
# 
# {
#     "rcpt_to": "fake.email@gmail.com", 
#     "mail_from": "fake.email@gmail.com", 
#     "messages": {
#         "0": "\r\n I love computer networks!", 
#         "1": "\r\n We love Christine!", 
#         "2": "\r\n Hello World"
#         }
# }