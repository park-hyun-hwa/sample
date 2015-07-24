#<150720 스터디>#
##1.sht20 온습도 센서 값 데이터베이스에 넘기기##

- /var/www/sht_db_test.php 참고

- 센서값이 파일에 저장되면 분리하여 Database에 저장시키는 방식


##2.센서값 간단하게 웹상에 나타내기##

- /var/www/sht_test.php 참고

- 현재까지는 그냥 파일을 실행시켰을 때 텍스트 파일에 값이 저장된 것을 읽어오는 것만 수행.

- 차후에 python 코드 상에서 db와 연동시켜서 바로 연동되도록 해야할 듯.

- 구체적인 프로그래밍 구상을 더 해야할 듯.

#####참고 url#####
- http://ilikesan.com/category/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4
- http://zetawiki.com/wiki/%EB%A6%AC%EB%88%85%EC%8A%A4_%EB%B0%98%EB%B3%B5_%EC%98%88%EC%95%BD%EC%9E%91%EC%97%85_cron,_crond,_crontab
- http://icbanq.tistory.com/entry/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-%ED%99%9C%EC%9A%A9-%EA%B0%95%EC%A2%8C-15-%EC%8A%A4%EB%A7%88%ED%8A%B8%ED%8F%B0%EC%97%90%EC%84%9C-DB%EC%97%90-%EA%B8%B0%EB%A1%9D%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%83%80-%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0
- http://ji-ggu.tistory.com/9


#<150722 스터디>#
##1.센서 값을 python 코드 상에서 바로 데이터베이스에 저장##

- /test/sht20_db.py 참고

	    con = mdb.connect('localhost','root','tinyos','keti')
        cur = con.cursor()
        
        now = datetime.datetime.now()
        temp = reading(1)
        humi = reading(2)
        if not temp or not humi:
            print "register error"
            #break
        value = calc(temp, humi)
        result="temp:"+str(value[0])+"\t humi:"+str(value[1])
        
        sql = "INSERT INTO onenode (time,temperature,humidity,co2) VALUES(%s,%s,%s,%s)"
        sql_data=(now,value[0],value[1],0)
        cur.execute(sql,sql_data)
        con.commit()
        cur.close()
        con.close()
        print "%s" %(result)
        
#####참고 url#####
- https://github.com/jervine/rpi-temp-humid-monitor/blob/master/python_code/updateMysql.py


#<150724 스터디>#
##1.Web에서 센서 제어하기##
- GPIO 이용

- WebIOPi 이용

#####참고 url#####
- https://github.com/rasplay/RemoteOnOff
- http://fishpoint.tistory.com/1376
- http://www.rasplay.org/?p=5061
- http://kocoafab.cc/tutorial/view/310
- http://www.highcharts.com/
- http://cafe.naver.com/openrt/1846
- http://www.rasplay.org/?p=5773
- http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=4
