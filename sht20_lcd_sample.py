#!/usr/bin/python
# Author : ipmstyle, https://github.com/ipmstyle
#        : jeonghoonkang, https://github.com/jeonghoonkang

# for the detail of HW connection, see lcd_connect.py

import sys
import smbus
import time
import requests
import json
import string
import serial,os
import RPi.GPIO as GPIO
import logging
import logging.handlers
import fcntl,socket,struct
import urllib2
import httplib
import datetime
import pygame

sys.path.append("../../devel/BerePi/apps/lcd_berepi/lib")
from lcd import *
sys.path.append("../../devel/BerePi/apps/BereCO2/lib")
from co2led import *

##### SHT20 define####
SHT20_ADDR = 0x40       # SHT20 register address => 1000 0000
SHT20_CMD_R_T = 0xF3    # no hold Master Mode (Temperature) => 1111 0011
SHT20_CMD_R_RH = 0xF5   # no hold Master Mode (Humidity) => 1111 0101
SHT20_CMD_RESET = 0xFE  # soft reset => 1111 1110

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

##### CO2 define#####
ppm = 0

DEBUG_PRINT = 1
SERIAL_READ_BYTE = 12
FILEMAXBYTE = 1024 * 1024 * 100 #100MB
LOG_PATH = '/home/pi/log_tos.log'

#CO2LED_BLUE_PIN = 17
#CO2LED_GREEN_PIN = 22
#CO2LED_RED_PIN = 27

# important, sensorname shuould be pre-defined, unique sensorname
sensorname = "co2.test"
logger = logging.getLogger(sensorname)

#####dust variable#####################
#conn = httplib.HTTPConnection("192.168.0.16")
data =''
co2 = ''
##### open RASPI serial device, 38400#########
try: 
    serial_in_device = serial.Serial('/dev/ttyAMA0',38400) ##38400bps 
except serial.SerialException, e:
    logger.error("Serial port open error") 
    ledall_off()

#########flow lcd##############
def flow_lcd(line1_str,line2_str,flow_str_num):
    if flow_str_num==1:
    	if len(line1_str) > 16:
    		dif = len(line1_str)-16
    	  	for i in range(dif+2) : 
    			fin_line1_str = line1_str[i:i+15]
    			lcd_string('%s' %(fin_line1_str),LCD_LINE_1,1)
    			lcd_string('%s' % (line2_str),LCD_LINE_2,1)
    			time.sleep(1)
    	
    else:
    	if len(line2_str) > 16:
    		dif = len(line2_str)-16
    	  	for i in range(dif+2) : 
    			fin_line2_str = line2_str[i:i+15]
    			lcd_string('%s' %(line1_str),LCD_LINE_1,1)
    			lcd_string('%s' % (fin_line2_str),LCD_LINE_2,1)
    			time.sleep(1)
    		
############temperature, humidity######################### 
def reading(v):
    bus.write_quick(SHT20_ADDR)
    if v == 1:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_T)
    elif v == 2:
        bus.write_byte(SHT20_ADDR, SHT20_CMD_R_RH)
    else:
        return False
        
    time.sleep(.1)
    
    b = (bus.read_byte(SHT20_ADDR)<<8)
    b += bus.read_byte(SHT20_ADDR)
    return b

def calc(temp, humi):
    tmp_temp = -46.85 + 175.72 * float(temp) / pow(2,16)
    tmp_humi = -6 + 125 * float(humi) / pow(2,16)

    return tmp_temp, tmp_humi

def tem_humi():
    temp = reading(1)
    humi = reading(2)
    if not temp or not humi:
        print "register error"
    value = calc(temp, humi)
    lcd_string('temp : %s ' %value[0],LCD_LINE_1,1)
    lcd_string('humi : %s ' %value[1],LCD_LINE_2,1)

    print "temp : %s\thumi : %s" % (value[0], value[1]) 

    if float(value[0])< 22 :
        blueLCDon()
    elif float(value[0]) < 27 : 
        greenLCDon()
    elif float(value[0]) < 29 :
	print "temp_yellow"
        yellowLCDon()
    else :
        redLCDon()
        print "temp_red"
        
    time.sleep(2)
    return value[0],value[1]

####################ip_address######################
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def ip_chk():
    cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    ipAddr = run_cmd(cmd)
    return ipAddr

def wip_chk():
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    wipAddr = run_cmd(cmd)
    return wipAddr

def mac_chk():
    cmd = "ifconfig -a | grep ^eth | awk '{print $5}'"
    macAddr = run_cmd(cmd)
    return macAddr

def wmac_chk():
    cmd = "ifconfig -a | grep ^wlan | awk '{print $5}'"
    wmacAddr = run_cmd(cmd)
    return wmacAddr

def stalk_chk():
    cmd = "hostname"
    return run_cmd(cmd)
	
def ip_addr():
    lcd_string('IP address ', LCD_LINE_1,1)
    lcd_string('MAC eth0, wlan0',LCD_LINE_2,1)
    blue_backlight(False) #turn on, yellow
    time.sleep(2) 
    
    red_backlight(False) #turn on, yellow
    ip_str = ip_chk()
    ip_str = ip_str[:-1]
    mac_str = mac_chk()
    mac_str = mac_str[:-1]
    
    flow_lcd(ip_str,mac_str,2)
    time.sleep(2) 
    
    green_backlight(False) #turn on, yellow
    wip_str = wip_chk()
    wip_str = wip_str[:-1]
    wmac_str = wmac_chk()
    wmac_str = wmac_str[:-1]
    
    flow_lcd(wip_str,wmac_str,2)
    
    time.sleep(2) 
    
    red_backlight(False) #turn on, yellow
    stalk_str = stalk_chk()
    stalk_str = stalk_str[:-1]
    lcd_string('sTalk Channel' ,LCD_LINE_1,1)
    lcd_string('%s           ' % (stalk_str),LCD_LINE_2,1)
    
    time.sleep(2)

#####################CO2########################
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' %ord(char) for char in info[18:24]])

macAddr = getHwAddr('eth0')
macAddr = macAddr.replace(':','.')

level = 0
ppm = 0

# check length, alignment of incoming packet string
def syncfind():
    index = 0
    alignment = 0
    while 1:
        in_byte = serial_in_device.read(1)
# packet[8] should be 'm'
# end of packet is packet[10]
        if in_byte is 'm' :
            #print 'idx =', index, in_byte
            alignment = 8
        if alignment is 10 : 
            alignment = 1
            index = 0
            break
        elif alignment > 0 :
            alignment += 1
        index += 1

def checkAlignment(incoming):
    idxNum = incoming.find('m')
    # idxNum is 9, correct
    offset = idxNum - 9 
    if offset > 0 :
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    if offset < 0 :
        offset = 12 + offset 
        new_str = incoming[offset:]
        new_str = new_str + incoming[:offset]
    return new_str
    
def init_process():
    print " "
    print "MSG - [S100, T110 CO2 Sensor Driver on RASPI2, Please check log file : ", LOG_PATH
    print "MSG - now starting to read SERIAL PORT"
    print " "
    ledall_off()

def CO2():
    ppm = 0 
    try:
        in_byte = serial_in_device.read(SERIAL_READ_BYTE) 
        pos = 0
    except serial.SerialException, e:
        ledall_off()
    if not (len(in_byte) is SERIAL_READ_BYTE) : 
        logger.error("Serial packet size is strange, %d, expected size is %d" % (len(in_byte),SERIAL_READ_BYTE))
        print 'serial byte read count error'
        return -1
    # sometimes, 12 byte alighn is in-correct
    # espacially run on /etc/rc.local
    if not in_byte[9] is 'm':
        shift_byte = checkAlignment(in_byte)
        in_byte = shift_byte
    if ('ppm' in in_byte):
            if not(in_byte[2] is ' ') :
                ppm += (int(in_byte[2])) * 1000
            if not (in_byte[3] is ' ') :
                ppm += (int(in_byte[3])) * 100
            if not (in_byte[4] is ' ') :
                ppm += (int(in_byte[4])) * 10
            if not (in_byte[5] is ' ') :
                ppm += (int(in_byte[5]))  

            logline = sensorname + ' CO2 Level is '+ str(ppm) + ' ppm' 
            ledall_off()
	    
            lcd_string('CO2 : %d ' %ppm,LCD_LINE_1,1)
	    lcd_string('',LCD_LINE_2,1)

            if DEBUG_PRINT :
                print logline

            if ppm > 2100 : 
                logger.error("%s", logline)
                # cancel insert data into DB, skip.... since PPM is too high,
                # it's abnormal in indoor buidling
                ledred_on()
                ### maybe change to BLINK RED, later
                return -1
            else :
                logger.info("%s", logline)

    if ppm < 800 :  
        #ledblue_on()
        print "co2_blue"
        blueLCDon()
    elif ppm < 1000 :  
        #ledbluegreen_on()
        print "co2_skye"
        pinkLCDon()
    elif ppm < 1300 :  
        #ledgreen_on()
        print "co2_green"
        greenLCDon()
    elif ppm < 1600:  
        #ledwhite_on()
        print "co2_white"
        whiteLCDon()
    elif ppm < 1900:  
        #ledyellow_on()
        print "co2_yellow"
        yellowLCDon()
    elif ppm >= 1900 :  
        #ledpurple_on()
        print "co2_red"
    	redLCDon()
    time.sleep(2)
        
    return ppm

##################dust_get###########################
"""def getWebpage(url, referer=''):
    debug = 0
    if debug:
        return file(url.split('/')[-1], 'rt').read()
    else:
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'),
            ('Referer', referer),
        ]
        return opener.open(url).read()

def getDataPage():
    return getWebpage('http://www.airkorea.or.kr/index')
    
def normailize(s):
    return s.replace('<td>','').replace('</td>','').replace(' ','')
    
def printUsing():
    print sys.argv[0], '<output file name>'

def getDatetime(buffers):
    return buffers.split('<p class="now_time">')[1].split('<strong>')[1].split('</strong>')[0]
"""    
def get_page():
    page = urllib2.urlopen("http://www.airkorea.or.kr/index")
    text = page.read()
    return text    
    
def getDatablocks(buffers):
    a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
    b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
    r = ''
    value=[]

    for line in b.split('<td>'):
       if len(line) < 30:
           line = line.strip()
           r = r+line+' '
       else:
           line = line.strip()
           r = r+line+'\n'
	   value.append(line)
    return value

def print_dust(value):
    print "seoul : "+value[1]
    print "busan : "+value[2]
    print "deagu : "+value[3]
    print "incheon : "+value[4]
    print "gwangju : "+value[5]
    print "daejeon : "+value[6]
    
def lcd_dust(value):
    if int(value[1]) < 30:
    	print "dust_blue"
    	blueLCDon()
    elif int(value[1]) < 80:
    	print "dust_green"
    	greenLCDon()
    elif int(value[1]) < 150 :
    	print "dust_yellow"
    	yellowLCDon()
	
    lcd_string('Air',LCD_LINE_1,2)
    lcd_string('Information',LCD_LINE_2,2)
    time.sleep(2)
    
    lcd_string('seoul : %s' % (value[1]),LCD_LINE_1,1)
    lcd_string('busan : %s' % (value[2]),LCD_LINE_2,1)
    time.sleep(2)
    lcd_string('deagu : %s' % (value[3]),LCD_LINE_1,1)
    lcd_string('incheon : %s' % (value[4]),LCD_LINE_2,1)
    time.sleep(2)
    lcd_string('gwangju : %s' % (value[5]),LCD_LINE_1,1)
    lcd_string('daejeon : %s' % (value[6]),LCD_LINE_2,1)
    time.sleep(2)
    

def dust():
	buffers = get_page()
	dust = getDatablocks(buffers)
	print_dust(dust)
	lcd_dust(dust)
	return dust[1]

###########current time####################
def current_time():
    pinkLCDon()
    curr_time = datetime.datetime.today()
    curr_time = str(curr_time)[:19]
    flow_lcd('current time',curr_time,2)
    print "time : "+str(curr_time)
    time.sleep(2)

##################send data to db#####################
def send_data(temp, humi,ppm,dust) :
    url = "http://10.255.252.132:4242/api/put"
    data = {
            "metric": "sht20.temp",
            "timestamp" : time.time(),
            "value" : float(temp),
            "tags":{
                "host": "hyunhwa"
            }
    }
    ret = requests.post(url, data=json.dumps(data))

    print ret.text

    data = {
            "metric": "sht20.humi",
            "timestamp" : time.time(),
            "value" : float(humi),
            "tags":{
                "host": "hyunhwa"
            }
    }
    ret = requests.post(url, data=json.dumps(data))

    print ret.text
  
    data = {
		"metric":"rc1.co2.ppm",
		"timestamp" : time.time(),
		"value" : ppm,
		"tags" : {
			"host" : "hyunhwa"
		}
    }
    ret = requests.post(url, data=json.dumps(data))
    
    print ret.text
    
    data = {
		"metric":"html.dust",
		"timestamp" : time.time(),
		"value" : dust,
		"tags" : {
			"host" : "hyunhwa"
		}
    }
    ret = requests.post(url, data=json.dumps(data))
    
    print ret.text
############## main ############################    
def main():
     # set logger file
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=FILEMAXBYTE,backupCount=10)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # call raspi init...
    init_process()
 
    # Initialise display
    lcd_init()
    print ip_chk(), wip_chk(), mac_chk(), wmac_chk(), stalk_chk()
    buffers = get_page()
    
    #initialise sound
    pygame.mixer.init()
    pygame.mixer.music.load("sound_test.mp3")
    pygame.mixer.music.play()
    
    while True :
    	current_time()
        ip_addr()
  	value=tem_humi()
  	tem=value[0]
  	humi=value[1]
  	ppm=CO2()
  	seoul_dust = dust()
  	print pygame.mixer.music.get_busy()
  	if pygame.mixer.music.get_busy()==0:
    		pygame.mixer.music.play()
    	#send_data(tem,humi,ppm,seoul_dust)
    	#pygame.mixer.music.unpause()
    	
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
