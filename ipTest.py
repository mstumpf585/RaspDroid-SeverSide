import urllib2 

def public_ip():
	data = urllib2.urlopen('https://api.ipify.org').read()
	return data

print(public_ip())

import socket
data = socket.gethostbyname(socket.gethostname())
print data

import socket, subprocess

hostname =  socket.gethostname()

shell_cmd = "ifconfig | awk '/inet addr/{print substr($2,6)}'"
proc = subprocess.Popen([shell_cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

ip_addresses = out.split('\n')
ip_address = ip_addresses[0]

for x in xrange(0, len(ip_addresses)):
    try:
        if ip_addresses[x] != "127.0.0.1" and ip_addresses[x].split(".")[3] != "1":
            ip_address = ip_addresses[x]
	    print ip_address
    except:
        pass
