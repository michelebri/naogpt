import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.61', 4352))

serversocket.listen(5)

def start_listening():
   print("code for start the listening")

def stop_listening():
   print("code for stop the listening and send audio")


while True:
    print("Waiting for a connection...")
    connection, client_address = serversocket.accept()

    try:
        print("Connection from", client_address)
        data = connection.recv(16)
        print("Received:", data.decode('utf-8'))
        message_received = data.decode('utf-8')
        if "start" in message_received:
           start_listening()
        if "stop" in message_received:
           stop_listening()
        if data:
            message = "received"
            connection.sendall(message.encode('utf-8'))
        else:
            print("No data from", client_address)
    finally:
        connection.close()

