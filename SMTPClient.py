from socket import *
import time
import httplib
import json

#https://docs.python.org/3/library/http.client.html 

msg1 = "\r\n I love computer networks!"
msg2 = "\r\n We love Christine!"
msg3 = "\r\n Hello World"
msg_list = [msg1, msg2, msg3]
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "127.0.0.1"
port = 12001

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
print "send HELO"
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
print "send MAIL FROM"
mailFromCommand = 'MAIL FROM: <fake.email@gmail.com>\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print recv2

# Send RCPT TO command and print server response.
print "send RCPT TO"
rcptToCommand = 'RCPT TO: <fake.email@gmail.com>\r\n'
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print recv3

# Send DATA command and print server response.
print "send DATA"
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print recv4

# Send multiple emails at once
for msg in msg_list:
    # Send message data.
    print "send msg"
    clientSocket.send(msg)

    # prevent msg + endmsg from being combined into 1 req
    time.sleep(1)

    # Message ends with a single period.
    print "send endmsg"
    clientSocket.send(endmsg)
    recv5 = clientSocket.recv(1024).decode()
    print recv5


conn = httplib.HTTPConnection("SERVERHOSTNAME", 12001) # what is the hostname? localhost?
conn.request("GET", "/emailstorage.json") # placeholder file name
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
r1 = conn.getresponse()
data1 = r1.read()
mail_dict = json.loads(data1)
for i in data1['emails']: 
    print(i) //prints emails
r1.close()

'''
output:
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '0'}
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '1'}
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '2'}

'''
# Send QUIT command and get server response.
print "send QUIT"
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand)
recv6 = clientSocket.recv(1024).decode()
print recv6
