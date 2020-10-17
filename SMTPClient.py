from socket import *
import time
import httplib
import json
import ssl

#https://docs.python.org/3/library/http.client.html 

endmsg = "\r\n.\r\n"
portnum = 12001

def setup_server():
    # Choose a mail server (e.g. Google mail server) and call it mailserver
    mailserver = "127.0.0.1"

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setblocking(1)
    clientSocket.connect((mailserver, portnum))

    # Establish secure connection using TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('server.pem')
    context.load_cert_chain(certfile="client.pem", keyfile="client.key")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(clientSocket, server_side=False, server_hostname=mailserver)
    else:
        secure_sock = context.wrap_socket(clientSocket, server_side=False)

    cert = secure_sock.getpeercert()
    print cert

    # verify server
    if not cert or ('organizationName', 'Wellesley') not in cert['subject'][3]: raise Exception("ERROR")

    recv = secure_sock.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    print "send HELO"
    heloCommand = 'HELO Alice\r\n'
    secure_sock.send(heloCommand.encode())
    recv1 = secure_sock.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
        
    send_mail_from(secure_sock)
    send_rcpt_to(secure_sock)
    prep_data(secure_sock)
    
    return secure_sock

# Send MAIL FROM command and print server response.
def send_mail_from(secure_sock):
    print "send MAIL FROM"
    mailFromCommand = 'MAIL FROM: <fake.email@gmail.com>\r\n'
    secure_sock.send(mailFromCommand.encode())
    recv2 = secure_sock.recv(1024).decode()
    print recv2

# Send RCPT TO command and print server response.
def send_rcpt_to(secure_sock):
    print "send RCPT TO"
    rcptToCommand = 'RCPT TO: <fake.email@gmail.com>\r\n'
    secure_sock.send(rcptToCommand.encode())
    recv3 = secure_sock.recv(1024).decode()
    print recv3

# Send DATA command and print server response.
def prep_data(secure_sock):
    print "send DATA"
    dataCommand = 'DATA\r\n'
    secure_sock.send(dataCommand.encode())
    recv4 = secure_sock.recv(1024).decode()
    print recv4

def send_message(secure_sock, msg):
    # Send message data.
    print "send msg"
    secure_sock.send(msg.encode())
    
    # prevent msg + endmsg from being combined into 1 req
    time.sleep(1)

    # Message ends with a single period.
    print "send endmsg"
    secure_sock.send(endmsg.encode())
    recv5 = secure_sock.recv(1024).decode()
    print recv5

# Send QUIT command and get server response.
def end_message_sending(secure_sock):
    print "send QUIT"
    quitCommand = 'QUIT\r\n'
    secure_sock.send(quitCommand)
    recv6 = secure_sock.recv(1024).decode()
    secure_sock.close()
    print recv6

# Pull protocol
def pull_messages(secure_sock):
    conn = httplib.HTTPConnection("localhost", portnum)
    conn.request("GET", "/emailstorage.txt") 
    r1 = conn.getresponse()
    conn.close()
    headers = r1.getheaders()
    r1.close()
    data1 = headers[0][0] + ":" + headers[0][1]
    mail_dict = json.loads(data1)
    # prints emails
    if not mail_dict['emails']:
        print "Inbox empty"
        return
    for i in mail_dict['emails']:
        print "email #" + str(i['ID'])
        print "to: " + i['rcpt_to'] 
        print "from: " + i['mail_from']
        print "from: " + i['message']  + "\r\n"
    '''
    sample input:
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

'''
output:
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '0'}
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '1'}
{'rcpt_to': 'EMAIL ADDRESS', 'mail_from': 'EMAIL ADDRESS', 'message': 'email contents', 'id': '2'}
'''
#######################################################################################################


def main():
    sec_sock = setup_server()
    msg = ''
    while msg != 'quit':
        msg = raw_input("Type your message and hit enter to send. Type 'quit' to send your message and refresh your inbox. ")
        if msg == 'quit':
            end_message_sending(sec_sock)
        else:
            send_message(sec_sock, msg)
    time.sleep(1)
    pull_messages(sec_sock)
    
if __name__ == "__main__":
    main()




