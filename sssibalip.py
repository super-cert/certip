from socket import inet_aton
from socket import inet_ntoa
from struct import unpack
from struct import pack

def ip2long(ip_addr): ## ip값을 int형으로 변한해주는 함수

	try : return unpack("!I", inet_aton(ip_addr))[0]

	except IOError : return None

def int2ip(addr):
    return inet_ntoa(pack("!I", addr))


print(int2ip(356486455))

print(ip2long('3.195.191.62'))