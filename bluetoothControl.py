from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Adafruit_LED_Backpack import Matrix8x8
from Matrix16x8 import Matrix16x8
from fonts import custom_font
from bluetooth import *

import os
import time
import atexit
import socket, subprocess


#create objects 
mh = Adafruit_MotorHAT(addr=0x60)
display16x8 = Matrix16x8(address=0x72, busnum=1)
display8x8  = Matrix8x8.Matrix8x8(address=0x72, busnum=1) 

#run the 8x8 first because 16x8 wont work at this time still figureing out 
display8x8 = Matrix8x8.Matrix8x8(address=0x72, busnum=1)
display8x8.begin()
display8x8.clear()
display8x8.set_pixel(0,0,1)

#configure 16x8 lights 
display16x8.set_brightness(8)
display16x8.display_16x8_buffer(custom_font.shapes['all_on']+custom_font.shapes['all_on'])
time.sleep(1)
display16x8.display_16x8_buffer(custom_font.shapes['all_off']+custom_font.shapes['all_off'])

#say hello
message = "suh dude"
display16x8.scroll_message(message.upper(), custom_font.textFont2)
display16x8.scroll_message(message.upper(), custom_font.textFont2)

#show IP
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
	    # print the ip in terminal 
            print ip_address
	    # show ip in the matrix 
	    display16x8.scroll_message(ip_address.upper(), custom_font.textFont2)
    except:
        pass

#auto disable motors 
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
Motor3 = mh.getMotor(3)
Motor4 = mh.getMotor(4)
 
#set the speed to start, from 0 (off) to 255 (max speed)
Motor3.setSpeed(150)
Motor3.run(Adafruit_MotorHAT.FORWARD);
Motor4.setSpeed(150)
Motor4.run(Adafruit_MotorHAT.FORWARD);

#turn off motor
Motor3.run(Adafruit_MotorHAT.RELEASE);
Motor4.run(Adafruit_MotorHAT.RELEASE);


#create bt server socket 
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "motorPiControl",
                   service_id = uuid,
                   service_classes = [ uuid,SERIAL_PORT_CLASS ],
                   profiles = [SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
#tell me whats going on
print "Waiting for connection on RFCOMM channel %d" % port

#confirm the connection on this end 
client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

#show bunnys
display8x8.clear()
display8x8.set_pixel(0,0,1) 
display16x8.display_16x8_buffer(custom_font.shapes['bunny1']+custom_font.shapes['bunny2'])

#do this untill keyboard interupt or disconnect 
while True:           

    print "top"
    try:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print "received [%s]" % data

            if data == 'fwd':
		#confirm what was recived 
                data = 'fwd!'
                print "Forward! "

		#run the motors 
                Motor3.run(Adafruit_MotorHAT.FORWARD)
                Motor4.run(Adafruit_MotorHAT.FORWARD)

            elif data == 'left':
            	#confirm what was recived 
                data = 'left!'
		print "left!"
		
		#run the motors 
		Motor3.run(Adafruit_MotorHAT.FORWARD)
		Motor4.run(Adafruit_MotorHAT.RELEASE)
            
            elif data == 'right':
            	#confirm what was recived 
                data = 'right!'
		print "right!"
		
		#run the motors 
		Motor3.run(Adafruit_MotorHAT.RELEASE)
		Motor4.run(Adafruit_MotorHAT.FORWARD)

            elif data == 'rev':
		#confirm what was recived 
                data = 'rev!'
                print "Backward! "

		#run the motors 
                Motor3.run(Adafruit_MotorHAT.BACKWARD)
		Motor4.run(Adafruit_MotorHAT.BACKWARD)
        
            else:
                data = 'something is up!'
                print "Release"
                Motor3.run(Adafruit_MotorHAT.RELEASE)
		Motor4.run(Adafruit_MotorHAT.RELEASE)
                time.sleep(1.0)
                        
               # client_sock.send(data)
               # print "sending [%s]" % data

    except IOError:
        print "hit except"
        pass

    except KeyboardInterrupt:

        print "disconnected"
        Motor3.run(Adafruit_MotorHAT.RELEASE)
	Motor4.run(Adafruit_MotorHAT.RELEASE)
        client_sock.close()
        server_sock.close()
        print "all done"

        break
