import time
import os
import sys
import serial

sys.path.append("../../../devel/BerePi/apps/lcd_berepi/lib")
from lcd import *

state = 0
packet =''
available = " "

def bigEndian(s):
	res = 0
	while len(s):
		s2 = s[0:2]
		s = s[2:]

		res <<=8
		res += eval('0x' + s2)
	return res

def littleEndian(s):
	res = 0
	while len(s):
		s2 = s[-2:]
		s = s[:-2]

		res <<= 8
		res += eval('0x' + s2)
	return res

def sese(s):
	
    head = s[:20]
    type = s[36:40]
        
    serialID = s[40:52]
    nodeID = s[52:56]
    #seq = s[40:44]
    
    print "head : "+head
    print "type : "+type
    print "serialID : "+serialID
    print "nodeID : "+nodeID
    #print "seq : "+seq
    
    if type == "0070" : # TH : Total Sensor
        temperature = bigEndian( s[64:68] ) 
        humidity = bigEndian( s[68:72] ) 
        light = bigEndian( s[72:76] ) 
        #v1 = -46.85 + 0.01 * temperature
        #tmp = -6 + 125 * humidity / 4095
        #v2 = tmp
        tmp = (light * 1.017)
        v3 = tmp
        
        v1 = -46.85 + 175.72 * float(temperature) / pow(2,14) # 14 (14bit) for temperature.
    	v2 = -6 + 125 * float(humidity) / pow(2,12) #and 12 (12bit) for relative humidity 
        

        t = int(time.time())
        print "gyu_RC1_thl.temperature %d %.6f nodeid=%d" % ( t, v1, bigEndian( nodeID ) )
        print "gyu_RC1_thl.humidity %d %.6f nodeid=%d" % ( t, v2, bigEndian( nodeID ) )
        print "gyu_RC1_thl.light %d %f nodeid=%d" % ( t, v3, bigEndian( nodeID ) )
        
        return v1,v2,t
        
    else:
	print >> sys.stderr, "Invalid type : " + type
	pass
			
if __name__ == '__main__':

	test = serial.Serial("/dev/ttyUSB0",115200)
	tmpPkt = []
	flag =0

#	if list_serial_ports() !="":
#		port = list_serial_ports()
#		print port
	
	lcd_init()
	
	while 1:
		Data_in = test.read().encode('hex')

		if(Data_in == '7e'):
			if(flag == 2) :
				flag =0
				tmpPkt.append(Data_in)
				packet = ''.join(tmpPkt)
				data = sese(packet)
				
				temp = data[0]
				humi = data[1]
				light = data[2]
				
				lcd_string('Temperature ', LCD_LINE_1,1)
    				lcd_string('%.5s `C' % (temp),LCD_LINE_2,1)
    				time.sleep(1.5)
    				lcd_string('Humidity ', LCD_LINE_1,1)
    				lcd_string('%.5s `C' % (humi),LCD_LINE_2,1)
    				time.sleep(1.5)
    				lcd_string('Light ', LCD_LINE_1,1)
    				lcd_string('%.5s `C' % (light),LCD_LINE_2,1)
    				time.sleep(1.5)
				tmpPkt = []
				sys.stdout.flush()
			else :
				flag = flag + 1
				tmpPkt.append(Data_in)
		else :
			if(flag == 1 and Data_in =='45') :
				flag =2
			tmpPkt.append(Data_in)

