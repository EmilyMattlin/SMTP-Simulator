# SMTP-Simulator
End-to-end SMTP simulator utilizing TLS security

# Usage
In the project directory, generate a certificate and private key for the client and server
```
openssl req -new -x509 -nodes -out server.pem -keyout server.key
openssl req -new -x509 -nodes -out client.pem -keyout client.key
```
In one terminal, start the SMTP Server
```
python SMTPServer.py
```

In another terminal, start the SMTP Client
```
python SMTPClient.py
```
Follow prompts in the SMTP Client terminal to enter text for each email.
