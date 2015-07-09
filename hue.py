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
	print "bri : "+str(state[2])
	print "hue : "+str(state[3])
	print "sat : "+str(state[4])
	print "xy : "+str(state[5])
	
if __name__ == '__main__':
	state = getState(1)
	print_state(1)
	
	print str(state[0])+" is off"
	off(1)
	time.sleep(5)
	
	print str(state[0])+" is on"
	on(1)
	time.sleep(5)
	
	print str(state[0])+"'s color is randomly changed"
	random = random.random()
	print random
	putHue(1,random.random())
	
