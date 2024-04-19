import socket
import struct
#ex:"192.168.1.**"
TFTP_IP_ADDRS = "replace with tftp server address"
#ex:"image.efi"
TFTP_NAME_FILE = "replace with of the name of the file that the PXE client must download from the TFTP server"


'''  the program captures the "offer" data that
     is coming from the dhcp server as a response 
     to the client's "discover" '''

with socket.socket(socket.AF_INET,socket.SOCK_DEGRAM) as captureSocket:
  captureSocket.bind(('0.0.0.0',68))
  data , addr = captureSocket.recvfrom(1024)



#the program modifies this offer by adding options 66 and 67
'''
  Don't confuse the options we are adding to the datagram with the ports, 
  options 66 (IP address of the TFTP server) and 67 (This option contains 
  the name of the file that the PXE client must download from the TFTP server), 
  now talking about the ports... the client sends the dates on port 67 to the 
  server that responds on 68
'''
newData = addDataOptions(data)

#the program returns the datagram in broadcast

with socket.socket(socket.AF_INET,socket.SOCK_DEGRAM) as returnerSocket:
#Option required to send in broadcast
  returnerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  returnerSocket.sendto(("<broadcast>",68))

#pxe machine configured is easy... now just configure a tftp server

def addDataOptions(data):
     option66 = struct.pack("!BBBBBB",66,4,*TFTP_IP_ADDRS.split("."))
     option67 = struct.pack("!BB",67,len(TFTP_NAME_FILE))+TFTP_NAME_FILE.encode("ascii")
          '''
     the magic cookie is used to 
     find where the dhcp options start
     '''
     #magic cookie == 0x63 0x82 0x53 0x63
     magicCookie = b"\x63\x82\x53\x63"
     newdata = b""
     for byte in data:
          newdata += struct.pack(!B,byte)
          if newdata[-4:] == magicCookie:
               newdata += option66
               newdata += option67
     return newdata
