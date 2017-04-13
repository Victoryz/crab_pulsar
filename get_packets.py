import socket
import struct
import time

IP = '10.10.12.35' #bind on all IP addresses
PORT = 10000 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

while PORT != -1:
    data, addr = sock.recvfrom(4096+8)
    #print data[0]
    header = struct.unpack('<Q', data[0:8])[0]
    payload_len = len(data) - 8 # subtract 8 bytes of header
    data1 = struct.unpack('<2048h', data[8:])
    file1 = open("YY.txt","w")
    for i in range(0,100000): 
	 print time.time(), 
   	 print 'received %d bytes' % payload_len,
   	 print 'from', addr,	  
   	 print 'HEADER: %d, TIMESTAMP: %d, CHANNEL %4d, SEQ: %d' % (header, header >> 12, header & 0xfff, header >> 9)
         print 'data 1', data1[:]
#	 print(len(data1))
#	 channel = data1[1::4]
#	 for item in channel:
#		file1.write("%s\n"% item)
#   exit()
file1.close()
