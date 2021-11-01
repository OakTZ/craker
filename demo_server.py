import socket as soc
import hashlib
import time
md5 = "aaaaabbb"
#md5 = "zaaaaaaa"
hash_object = hashlib.md5(md5.encode())
md5 = hash_object.hexdigest()
socket = soc.socket()
socket.bind(("127.0.0.1",13370))
socket.listen(5)
msg = ""
num = 17#id
while(msg != "Howdy"):
    client_soc, addr = socket.accept()
    msg = client_soc.recv(1024).decode()
    if msg == "Howdy":
        client_soc.send(str(num).encode())
    client_soc.close()
    socket.close()
socket = soc.socket()
socket.connect(("127.0.0.1",13370+num))
socket.send(("aaaaaaaa,aaaazzzz," + md5).encode())
print("sent code")
answer = socket.recv(1024).decode()
print(answer)
