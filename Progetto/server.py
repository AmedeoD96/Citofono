import socket
import sys

HOST = "192.168.1.50"
PORT = 8888

# socket.socket mi serve per creare un socket
# socket.AF_INET formato dell'indirizzo, Internet = IP
# socket.SOCK_STREAM usato per la connessione a due vie

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket creato")

# Collego il socket all'host e alla porta
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print("Errore di collegamento: " + str(err[0]) + "Messaggio di errore: " + err[1])
    sys.exit()

print("Collegamento creato")

# Creo TCP listener
s.listen(10)
print("In ascolto")

while 1:
    conn, addr = s.accept()
    print("Connesso con: " + addr[0] + ":" + str(addr[1]))
    buf = conn.recv(64)
    print(buf)

s.close()