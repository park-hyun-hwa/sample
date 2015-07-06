
#150629 스터디#
###1. 무선 랜 설정(네이버 검색 : http://m.blog.naver.com/shumin/220309949028)###
	-아이콘이 존재하지는 않는 관계로 수동 설정이 필요했음.
	
	lsusb
	ifconfig
	sudo nano /etc/wpa_supplicant/wpa_supplicant.conf에 작성

  wpa_supplicant 파일은 와이파이 인터페이스 설정과 AP 목록을 관리한다.
  wpa_supplicant.conf는 wpa_supplicant를위한 구성 파일, WPA 및 WiFi 네트워크를 구현하는 다른 보안 프로토콜을 구현하는 데 사용되는 소프트웨어입니다.
  
  	network = {
  		ssid="keti_tinyos_01"
  		key_mgmt=WPA-PSK
  		psk="allberkeley"
  	}
  	
  key_mgmt 는 key_management로 암호화방식?을 의미
  psk는 비밀번호를 의미

	sudo nano /etc/network/interfaces에 작성

  	auto lO
  	iface lo inet loopback
  	iface eth0 inet dhcp
  
  	auto wlan0
  	allow-hotplug wlan0
  	iface wlan0 inet dhcp
  	wpa-ssid "keti_tinyos_01"
  	wpa-psk "allberkeley"

  
###2. java 설정###
	java -version
	which java

	vi /etc/profile

  	제일 마지막 줄에 아래 3출 추가
 	JAVA_HOME=/usr/
 	export JAVA_HOME
  	export PATH=$PATH:$JAVA_HOME/bin

	source /etc/profile


#################################################

#150630 스터디#
	=< kowonsik.com >에서 '라즈베리파이 opentsd?'에서 과정 익히기
###1. hbase 설치 및 설정###
  	=홈페이지 다운으로 진행하지 못함.

##################################################

#150701 스터디#
###1. 라즈베리 파이 파티션 용량 수동으로 늘리기###

	참고사이트 : http://zelits.tistory.com/65

	df -h : 파티션 확인
	sudo fdisk -l : 파티션 리스트 확인
	sudo fdisk -u -c /dev/mmcblk0 : -u(unit 단위로 디스플레이),
						-c(호환 모드)
	p : 파티션 리스트 출력
	d 다음 2 : 2번째 디바이스 접근
	n : 파티션 생성
	p : 파티션 타입 설정
	2 : 파티션 번호 설정
	122880 : 첫 섹터
	default : 마지막 섹터
	w : 커맨드 종료
	sudo reboot : 리부팅

	sudo resize2fs /dev/mmcblk0p2 : 리사이징


###2. 라즈베리 파이 내부에서 github 연동하기(windows도 연동하기)###
	GitHub을 통해서 소스를 편리하게 공유하고 버젼 관리 가능.
	
	처음에 시작할 때 
	git pull origin[나 주소] master
	항상 수정한다음에
	git add [파일명]
	git commit -m "[update문구]"
	git push -u origin[나 주소] master
	하기


###3.hbase 설정###
	-설정 중 압축이 덜 풀려서 xml 파일 설정에 오류가 남.

#################################################

#150702 스터디#
###1. 제품 3가지 설정(용랑, 이름, 버전업그레이드)###

###2.hbase 설치 완료###
	cd /usr/local
    	mkdir data
    	wget http://www.apache.org/dist/hbase/stable/hbase-1.0.1.1-bin.tar.gz
    	tar xvfz hbase-1.0.1.1-bin.tar.gz
    	cd hbase-1.0.1.1

    	hbase_rootdir=${TMPDIR-'/usr/local/data'}/tsdhbase
   	iface=lo`uname | sed -n s/Darwin/0/p`

    	vi conf/hbase-site.xml

    	configuration 태그 사이의 내용을 넣어주면 됨

     	<?xml version="1.0"?>
     	<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
     	<configuration>
       	<property>
         		<name>hbase.rootdir</name>
         		<value>file:///DIRECTORY/hbase</value>
       	</property>
       	<property>
         		<name>hbase.zookeeper.property.dataDir</name>
         		<value>/DIRECTORY/zookeeper</value>
        	</property>
     	</configuration>

	./bin/start-hbase.sh =>hbase 실행

###3. GnuPlot 설치 완료###
	=>경로는 ~/.bashrc에 추가하기
	cd /usr/local
     	apt-get install gcc
     	apt-get install libgd2-xpm-dev
     	wget 				http://sourceforge.net/projects/gnuplot/files/gnuplot/4.6.3/gnuplot-4.6.3.tar.gz
     	tar zxvf gnuplot-4.6.3.tar.gz
     	cd gnuplot-4.6.3
     	./configure
     	make install
     	apt-get install gnuplot

    	apt-get install dh-autoreconf

###4. openTSDB 설치 완료###
	
	
	cd /usr/local
     	git clone git://github.com/OpenTSDB/opentsdb.git

     	cd opentsdb
     	./build.sh
		=>java heap error가 나면
		./.bashrc에 
		export JABA_OPTS="-Xms512m -Xmx2048m -XX:MaxPermSize=512m" 을 추가하기
		=>
     	env COMPRESSION=NONE 	HBASE_HOME=/usr/local/hbase-1.0.1.1 ./src/create_table.sh

    	tsdtmp=${TMPDIR-'/usr/local/data'}/tsd
     	mkdir -p "$tsdtmp"

     	여기서 screen 으로 
     	screen -dmS tsdb
     	screen -list
    	tsdb로 -r tsdb

     	./build/tsdb tsd --port=4242 --staticroot=build/staticroot --cachedir=/usr/local/data --auto-metric

     	실행 후에는 Ctl + a + d 로 빠져나옴

###5. Tcollector 설치 완료###
	cd /usr/local
     	git clone git://github.com/OpenTSDB/tcollector.git
     	cd tcollector
     	vi startstop

    	#TSD_HOST=dns.name.of.tsd 이부분에서 주석해제하고 IP를 적어주면 됨	(아래처럼)
     	TSD_HOST=127.0.0.1 (ip주소)

##################################################

#150703 스터디#

###1. openTSDB 실행 순서###
	cd hyunhwa/workspace/openTSDB
	./openTSDB.sh =>스크립트 생성함.
	
	./startTSDB.sh =>스크립트 생성함.


###2. screen 명령어###
	- screen이라는 리눅스 프로세스를 사용하여 연결이 끊어져도 서버에 session이 유지되기 때문에 프로세스가 멈추지 않고 계속 작동.

	- screen -dmS : 데몬으로 시작(detached 모드)
   	screen -list : 리스트 출력
   	screen -r [session] : detach된 프로세스를 reattach하기

###3. openTSDB 다시 설치해보기###
	./build.sh를 수행하는 과정에서 java heap 에러 발생
		=>해결방법 찾기

###4. LCD 예제 실행###
- ip_addr.py
	1	GND
	2	5V
	3 	GND
	4	6
	5	GND
	6	13
	7
	8
	9	
	10
	11	19
	12	26
	13	21
	14	20
	15	5V
	16	16
	17	12
	18	7

- 16x2_LCD_RGB.py
	1	GND
	2	5V
	3 	GND
	4	27
	5	GND
	6	22
	7
	8
	9	
	10
	11	25
	12	24
	13	23
	14	12
	15	5V
	16	4
	17	17
	18	7

###5. 집에서 해볼 것###
	공유기에 무선으로 연결
	온습도 센서를 이용해서 구성한 라즈베리 파이에 LCD로 mac 주소 확인
	완성된 라즈베리파이를 냉장고에 넣고 센서 테스트
	
	
