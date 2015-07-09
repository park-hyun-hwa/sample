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
	print "*****************************"
	print "1. 끄기"
	print "2. 켜기"
	print "3. 색 랜덤하게 바꾸기"
	print "4. 빛 밝기 바꾸기"
	print "5. 빛 채도 바꾸기"
	print "6. Hue 상태 보기"
	print "****************************"
	
	menu = input("메뉴를 선택하시오.")
	hue_num = input("제어 할 Hue 번호를 입력하시오.")
	
	state = getState(hue_num)
	
	if menu==1:
		off(1)
		print str(state[0])+" is off"
	elif menu==2:
		on(1)
		print str(state[0])+" is on"
	elif menu==3:
		random = random.randrange(0,65535) #0~65535 사이의 정수 랜덤으로 출력
		putHue(hue_num,random)
		print str(state[0])+"'s color is randomly changed"
	elif menu==4:
		print "Current brightness is "+str(state[2])
		bri_val = input("밝기를 입력하시오.")
		if (bri_val is ' '):
			return -1
		putBri(hue_num, bri_val)
		print str(state[0])+"'s brightness is changed"	
	elif menu==5:
		print "Current saturation is "+str(state[4])
		sat_val = input("채도를 입력하시오.")
		if (sat_val is ' '):
			return -1
		putSat(hue_num, sat_val)
		print str(state[0])+"'s brightness is changed"
	else:
		print_state(hue_num)	
if __name__ == '__main__':
	whle True:
		select_menu()
	
	

	
