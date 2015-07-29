#150727 스터디#
##1.Web2py 설치 및 실행##

- 설치 
		 git clone --recursive https://github.com/web2py/web2py.git
         git submodule update --init --recursive
- 설치한 뒤 실행 명령 
		 sudo screen -dmS web2py sudo python web2py.py --ip [자신의 ip]
         (인증서 포함 실행은 아래)
		 sudo python web2py.py -i (ip) -p (port) -a '(password)' -c server.crt -k server.key
         
####(참고 URL)####
- https://github.com/web2py/web2py
- http://web2py.readthedocs.org/en/latest/
- https://github.com/mjhea0/web2py
- http://www.web2py.com/examples/default/examples#simple_examples

#150728 스터디#
- 참고 : https://github.com/mjhea0/web2py

##1. Web2py 작동과정 이해##
- MVC 구조(Model View Control)
	 	 Model : 어플리케이션 데이터
         View : 최종 사용자가 볼 수 있도록 허용 된 응용 프로그램 데이터의 일부
         Controller : 최종 사용자에게 데이터를 표시하는 데 사용되는 응용 프로그램 워크 플로우 및 로직을 제어
         
         즉, 사용자는 conroller를 이용하여 model을 조작하고,
         model이 view를 업데이트하고, view는 사용자가 본다.
         
         
####[예제 1 : `ip주소:포트번호/test/default/display_form.html` 참고]####
- Model : Database의 테이블과 스키마를 정의
	- db.py 를 열어서 Database 스키마를 정의하는 아래의 코드를 추가한다.
	- 세개의 필드가 있고 web2py에 의해 자동으로 생성된 unique ID를 더한다.
	
    	 	db = DAL('sqlite://webform.sqlite')
		 	db.define_table('register',
    		Field('first_name', requires=IS_NOT_EMPTY()),
    		Field('last_name', requires=IS_NOT_EMPTY()),
    		Field('email', requires=IS_NOT_EMPTY()))
            
- View : form을 호출
	- default/dispaly_form.html을 생성 하고 아래의 코드를 추가한다.
	
			<center>
			<br /><br /><br />
			<h1>Web Form</h1>
			<br />
			<h2>Inputs:</h2>
			{{=form}}
			<h2>Submitted variables:</h2>
			{{=BEAUTIFY(request.vars)}}
			</center>

- Controller : 호출 할 form을 구축
	- default.py에 아래 코드를 추가하여 새로운 기능을 정의한다.
	
			def display_your_form():
    			form = SQLFORM(db.register)
    			return dict(form=form)

####[예제 2 : `ip주소:포트번호/test/default/check_form.html` 참고]####

- Model에서 `requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]`으로 설정하면
	빈칸이거나 조건에 맞지 않을 때 오류메시지를 띄운다.
    
####[예제 3 : `ip주소:포트번호/test/default/check_form.html` 참고]####

- Model에서 아래와 같이 추가한다면 두 form의 정보가 다를 경우 DB에 입력하지 않는다.

		  Field('email_validate',requires=IS_EQUAL_TO(request.vars.email)))
		  db.register.email.requires=IS_NOT_IN_DB(db,'register.email')
        
- Controller에 아래와 같은 함수를 구현하면 DB의 모든 레코드를 보여준다.

		def all_records():
      	grid = SQLFORM.grid(db.register,user_signature=False)
    	  return locals()
        
- Controller에서  `request.args()` 는 특정 ID와 관련된 레코드를 가져온다.
		아직 구현 안됨.

#150729 스터디#

####[예제 4 : `ip주소:포트번호/test/default/index.html` 참고]####
- plugin으로 업로드 시켜서 레이아웃을 변경하는 작업을 수행
- 앞으로의 진행을 메뉴에 추가 시켜가면서 기록한다.

1.
