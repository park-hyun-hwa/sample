# -*- coding: utf-8 -*-

import httplib
import time
import json
import random

conn = httplib.HTTPConnection("10.255.255.65")

#Hue 켜기
def on(light):
	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", '{"on":true}')
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue 끄기
def off(light):
	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", '{"on":false}')
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False

#Hue의 saturation변화 0~255 0 흰색
def putSat(light, sat):
	saturation = {}
	saturation['sat'] = sat
	saturation = json.dumps(saturation)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", saturation)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue의 밝기 변화 0~255 
def putBri(light, bri):
	bright = {}
	bright['bri'] = bri
	bright = json.dumps(bright)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", bright)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue의 hue값 변화  0~65535
def putHue(light, hue):
	color = {}
	color['hue'] = hue
	color = json.dumps(color)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", color)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False



#Hue 상태 가져오기 json객체 작성중
def getState(light):
	conn.request("GET","/api/newdeveloper/lights/"+str(light))
	response = conn.getresponse()
	raw_data = json.loads(response.read())
	data = raw_data

	ret =[]
	ret.append(data['name'])
	ret.append(data['state']['on'])
	ret.append(data['state']['bri'])
	ret.append(data['state']['hue'])
	ret.append(data['state']['sat'])
	ret.append(data['state']['xy'])
	return ret

def print_state(light):
	state = getState(light)
	print "name : "+str(state[0])
	print "on : "+str(state[1])
	print "brightness : "+str(state[2])
	print "color : "+str(state[3])
	print "saturation : "+str(state[4])
	print "xy : "+str(state[5])
	print ""

def select_menu():
	print " "
	print "*****************************"
	print "1. turn off"
	print "2. turn on"
	print "3. Change the color random"
	print "4. change the brightness of the light"
	print "5. change the saturation of the light"
	print "6. Hue state"
	print "7. close"
	print "****************************"
	print " "
	
	menu = input("Please select the menu.")
	hue_num = input("Please enter the Hue number that you want to control.")
	
	state = getState(hue_num)
	
	if menu==1:
		off(1)
		print str(state[0])+" is off"
		time.sleep(2)
	elif menu==2:
		on(1)
		print str(state[0])+" is on"
		time.sleep(2)
	elif menu==3:
		random_bri = random.randrange(0,65535) #0~65535 사이의 정수 랜덤으로 출력
		putHue(hue_num,random_bri)
		print str(state[0])+"'s color is randomly changed"
		time.sleep(2)
	elif menu==4:
		print "Current brightness is "+str(state[2])
		bri_val = raw_input("Please enter the brightness.")
		if (bri_val is ' '):
			pass
		putBri(hue_num, bri_val)
		print str(state[0])+"'s brightness is changed"	
		time.sleep(2)
	elif menu==5:
		print "Current saturation is "+str(state[4])
		sat_val = raw_input("Please enter the saturation.")
		if (sat_val is ' '):
			pass
		putSat(hue_num, sat_val)
		print str(state[0])+"'s brightness is changed"
		time.sleep(2)
	elif menu==6:
		print_state(hue_num)
		time.sleep(2)
	else :
		pass
		
if __name__ == '__main__':
	try:
		while True:
			select_menu()
  	except KeyboardInterrupt:
  		pass
	
	
	

	
