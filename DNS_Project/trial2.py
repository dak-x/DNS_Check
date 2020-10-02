import socket
an_address = "8.8.8.8"

domain_name = socket.gethostbyaddr(an_address)

print(domain_name)
