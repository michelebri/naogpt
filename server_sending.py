import socket
import time
# Crea un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connettiti al server
server_address = ('192.168.1.61', 4352)  # Usa lo stesso indirizzo IP e porta del server
sock.connect(server_address)

try:
    # Invia dati
    message = 'start listening'
    print(f"Invio: {message}")
    sock.sendall(message.encode('utf-8'))

    # Aspetta la risposta
    response = sock.recv(16)
    print(f"Ricevuto: {response.decode('utf-8')}")
    time.sleep(200)
    message = 'stop listening'
    sock.sendall(message.encode('utf-8'))
    response = sock.recv(16)
finally:
    # Chiudi il socket per pulire
    sock.close()
