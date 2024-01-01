from flask import Flask, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
from flask_pymysql import MySQL
from datetime import timedelta
import json


                                                                    
app = Flask(__name__)
#데이터베이스 설정(pymysql)
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'qlalf',
    'db': 'fam',
    'charset': 'utf8'
    'cursorclass=pymysql.cursors.DictCursor'
}# ^연결자^

'''  데이터베이스 설정(plask_mysqldb) 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'qlalf'
app.config['MYSQL_DB'] = 'family'
# # #세션 변수 설정 
# # app.config['SECRET_KEY'] = '2893589345891894859485693748832958475938758498234'
# # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) 
'''

mysql = MySQL(app)

@app.route('/home', methods=['GET','POST'])
def home():
  return render_template('home.html')

@app.route('/signup_page', methods=['GET','POST'])
def signup_page():
    return render_template('signup.html')
    

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        userName = request.form['UserName']
        passwd = request.form['Password']
        passwdConf = request.form['PasswordConfirm']
        PhoneNumber = request.form['PhoneNumber']

'''
        #사용자 추가 쿼리
        add_user_query = "INSERT INTO users (username, password) VALUES (%s, %s,%s)"
        cursor = mysql.connection.cursor()
        cursor.execute(add_user_query, (userName, passwd, PhoneNumber))
        mysql.connection.commit()
        cursor.close()
        message = '회원가입이 성공적으로 완료되었습니다.'
        #return render_template('home.html', message=message) #주로 데이터 출력할 때 사용
        return redirect(url_for('home', message=message)) #주로 어떤 결과를 입력받고 결과를 보여주는 데 사용 
''' 
def insert_user(userName, passwd, passwdConf,phoneNumber):
  if request.method == 'POST ':
    if userName=="" or passwd=="" or passwdConf=="" or phoneNumber=="":
      error = '모든 항목을 입력해주세요'
      return redirect(url_for(home, param1=error))  # signup form page로 redirect 시킴 (method를 post로 지정하지 않았기 때문에 GET 방식임)

  #입력한 비밀번호와 비밀번호 확인 필드가 서로 다르면...
  if passwd!=passwdConf:
    error = '비밀번호 입력을 확인해주세요'
    return redirect(url_for(signup_page, param1=error))  # signup form page로 redirect 시킴 (method를 post로 지정하지 않았기 때문에 GET 방식임)

  #정상적인 입력이 확인되면  user 테이블에 위 항목들을 입력한다
  conn=mysql.connect(db_config)
  sql = 'insert into user(name, password, phoneNumber) values(%s,%s,%s)'
  values = (userName, passwd, phoneNumber) # 위 %s에 포맷팅될 각각의 값을 순서대로 튜플형태로 만든다
  cur = conn.cursor() # 데이터베이스 핸들러 객체를 가져온다
  cur.execute(sql, values)  # sql문을 변수들과 함께 실행한다
  mysql.connection.commit() # insert문을 실행한뒤에는 반드시 commit을 해주어야 한다
  cur.close()
  return '회원가입해 주셔서 감사합니다 : <a href="/home">로그인 페이지로 돌아가 로그인을 해주세요.</a>'

@app.route('/login', methods=['POST'])
def login():
  if request.method=='POST':
    UserName = request.form['InputUserName']     # home.html의 form에서 넘겨받은 username ---> name : InputEmail
    Password = request.form['InputPassword']  # home.html의 form에서 넘겨받은 password ---> name : InputPassword

    conn=mysql.connect(db_config)
    cursor = conn.cursor()
    sql = 'select * from user where name=%s and password=%s'
    val = (UserName, Password)
    cursor.execute(sql, val)
    result = cursor.fetchall()  # mysql에서 실행한 결과의 모든 행을 받아온다
    cursor.close()

    if len(result) > 1 :
       return '회원 정보에 중복된 값이 있습니다, 관리자에게 문의하세요'

    if len(result)==1:
       return redirect('main.html')

    else:
       return '<p>이름이나 비밀번호가 일치하지 않습니다</p>'



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('이름')
        birth = request.form.get('생년월일')
        gender = request.form.get('성별')
        contact = request.form.get('연락처')
        dad = request.form.get('부')
        mom = request.form.get('모')
        bro = request.form.get('bro')
        sis = request.form.get('sis')
        rank =request.form.get('rank')
        from_= request.form.get('from')
        rank_ = {'bro': bro,'sis':sis,'rank':rank}  #json형태로 합치기
        json_rank = json.dumps(rank_)
        
        conn = mysql.connect(db_config)
        #cursor = mysql.connection.cursor()
        cursor = conn.cursor()
        sql = 'INSERT INTO input(name, birth,contact,dad,mom,ranking,droughty,gender) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
        val = (name, birth,contact,dad,mom,json_rank,from_,gender)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return '입력이 완료되었습니다'

@app.route('/chinga.html', methods=['GET','POST'])
def chinga():

        #데이터베이스 연결
        conn=mysql.connect(db_config)
        cursor = conn.cursor()

        #데이터베이스에서 데이터 가져오기
        sql = 'SELECT * FROM input where droughty ="친가"'
        cursor.execute(sql) #sql변수의 쿼리 실행
        chn_result = cursor.fetchall() #쿼리 실행 결과 받아옴

        data = []
        for row in chn_result:
          d ={
          'name':row[1],
          'birth':row[2],
          'contact':row[3],
          'dad':row[4],
          'mom':row[5],
          'ranking':row[6],
          'droughty ':row[7],
          'gender':row[8]
          }
          data.append(d)
        cursor.close()

        #가져온 데이터 HTML 템플릿에 전달
        return render_template('chinga.html',chn_result=data)

@app.route('/wega.html', methods=['GET','POST'])
def wega():

        #데이터베이스 연결
        conn=mysql.connect(db_config)
        cursor = conn.cursor()

        #데이터베이스에서 데이터 가져오기
        sql = 'SELECT * FROM input where droughty ="외가"'
        cursor.execute(sql) #sql변수의 쿼리 실행
        we_result = cursor.fetchall() #쿼리 실행 결과 받아옴

        data = []
        for row in we_result:
          d ={
          'name':row[1],
          'birth':row[2],
          'contact':row[3],
          'dad':row[4],
          'mom':row[5],
          'ranking':row[6],
          'droughty ':row[7],
          'gender':row[8]
          }
          data.append(d)
        cursor.close()


        #가져온 데이터 HTML 템플릿에 전달
        return render_template('wega.html',we_result=data)


@app.route('/chuga.html', methods=['GET','POST'])
def chuga():

        #데이터베이스 연결
        conn=mysql.connect(db_config)
        cursor = conn.cursor()

        #데이터베이스에서 데이터 가져오기
        sql = 'SELECT * FROM input where droughty ="처가"'
        cursor.execute(sql) #sql변수의 쿼리 실행
        we_result = cursor.fetchall() #쿼리 실행 결과 받아옴

        data = []
        for row in we_result:
          d ={
          'name':row[1],
          'birth':row[2],
          'contact':row[3],
          'dad':row[4],
          'mom':row[5],
          'ranking':row[6],
          'droughty ':row[7],
          'gender':row[8]
          }
          data.append(d)
        cursor.close()
        
        #가져온 데이터 HTML 템플릿에 전달
        return render_template('chuga.html',chu_result=data)


@app.route('/chuwega.html', methods=['GET','POST'])
def chuwega():

        #데이터베이스 연결
        conn=mysql.connect(db_config)
        cursor = conn.cursor()

        #데이터베이스에서 데이터 가져오기
        sql = 'SELECT * FROM input where droughty ="처외가"'
        cursor.execute(sql) #sql변수의 쿼리 실행
        chw_result = cursor.fetchall() #쿼리 실행 결과 받아옴

        data = []
        for row in chw_result:
          d ={
          'name':row[1],
          'birth':row[2],
          'contact':row[3],
          'dad':row[4],
          'mom':row[5],
          'ranking':row[6],
          'droughty':row[7],
          'gender':row[8]
          }
          data.append(d)
        cursor.close()


        #가져온 데이터 HTML 템플릿에 전달
        return render_template('chuwega.html',chw_result=data)



if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True,port=8080)

