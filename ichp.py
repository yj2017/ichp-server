from flask import Flask, request, jsonify, redirect, url_for, abort
from werkzeug.utils import secure_filename
import json
import mysql.connector
import redis
import uuid
import traceback

app = Flask(__name__)
uploadDir = 'D:/uploads/'

status = {0: 'login successfully',
          1: 'password error',
          2: 'no such account name or password',
          3: 'username or password can not be empty',
          4: 'the username has already existed',
          5: 'register failed',
          6: 'upload sucessfully',
          7: 'the file type  is wrong ',
          8: 'unlogined,please login firstly',
          9: 'store successfully',
          10: 'mysql error '
          }
# redis
pool = redis.ConnectionPool(
    host='localhost', port='6379', decode_responses=True)
r = redis.Redis(connection_pool=pool)
# mysql
conn = mysql.connector.connect(
    user='root', password='273841', database='ichp')


def decodeStatus(code):
    return json.dumps({"msg": status[code], "code": code})

# This is register


@app.route('/register', methods=['POST'])
def Register():
    cursor = conn.cursor()
    req = json.loads(request.data)
    username = req['username']
    psw = req['psw']
    role = int(req['role'])
    if username == ''or psw == '' or role == '':
        return decodeStatus(3)
    else:
        cursor.execute(
            'select * from user where account_name="%s"' % (username,))
        cursor.fetchall()
        if cursor.rowcount > 0:
            cursor.close()
            return decodeStatus(4)
        else:
            sql = 'insert into user (account_name,psw,role) values ("%s","%s",%d)' % (
                username, psw, role)
            try:
                cursor.execute(sql)
                conn.commit()
            except:  # mysql error
                conn.rollback()
                cursor.close()
                return decodeStatus(10)
            if cursor.rowcount == 1:
                cursor.execute(
                    'select user_id from user where account_name="%s" and psw="%s"' % (username, psw))
                user_id = cursor.fetchall()[0][0]
                cursor.close()
                # return the unique user id
                return json.dumps({"the user id": user_id})
            else:
                cursor.close()
                return decodeStatus(5)


# This is login
@app.route('/login', methods=['POST', 'Get'])
def Login_info():
    cursor = conn.cursor()
    req = json.loads(request.data)
    username = req['username']
    psw = req['psw']
    if username == '' or psw == '':
        cursor.close()
        return decodeStatus(2)
    else:
        cursor.execute(
            'select psw,user_id from user where account_name="%s"' % (username,))
        psw_id = cursor.fetchall()
        if cursor.rowcount == 1:
            if psw == psw_id[0][0]:
                the_uuid = uuid.uuid1()  # the key
                user_id = psw_id[0][1]  # the value
                # key-value is stored by redis,3600s后过期
                r.set(the_uuid, user_id, ex=3600)
                cursor.close()
                return json.dumps({"msg": "login successfully", "the uuid": str(the_uuid), "user id": user_id})
            else:
                cursor.close()
                return decodeStatus(1)
        else:
            cursor.close()
            return decodeStatus(2)

# store the users' information


@app.route('/storeInfo', methods=['Get', 'POST', 'PUT'])
def storeInfo():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    telephone = req['telephone']
    name = req['name']
    sign = req['sign']  # 个性签名
    user_id = int(r.get(token))
    if user_id == None:
        cursor.close()
        return decodeStatus(8)
    else:
        sql = 'update user set telephone="%s",name="%s",sign="%s" where user_id=%d' % (
            telephone, name, sign, user_id)
        app.logger.debug(sql)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            conn.rollback()
            cursor.close()
            return decodeStatus(10)
        if cursor.rowcount > 0:
            cursor.close()
            return decodeStatus(9)


# allowed file type
ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
     'WMV', 'ASF', 'AVI',  'AVS', 'FLV', 'MKV', 'MOV', '3GP', 'MP4', 'MPG', 'MPEG', 'DAT', 'OGM', 'VOB', 'RM', 'RMVB', 'TS', 'TP', 'IFO', 'NSV'
     'mp3', 'AAC', 'WAV', 'WMA', 'CDA', 'FLAC', 'M4A', 'MID', 'MKA', 'MP2', 'MPA', 'MPC', 'APE', 'OFR', 'OGG', 'RA', 'WV', 'TTA', 'AC3', 'DTS'
     ]
)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#there are some bugs 
@app.route('/upload', methods=['POST', 'Get', 'PUT'])
def upload():
    try:
        req = json.loads(request.data)
        token = req['token']  # client 传来的token属性.token为键，uid为值
        app.logger.debug(str(token))
        if r.exists(token):  # 登录状态
            f = req['the_file']
            app.logger.debug(str(f.filename))
            
            if f and allowed_file(f.filename):
                f.save(uploadDir+secure_filename(f.filename))  # 七牛云存储
                return decodeStatus(6)
            else:
                return decodeStatus(7)
        else:  # 未登录
            return decodeStatus(8)
    except Exception as e:
        app.logger.debug(str(e))

@app.route('/',methods=['POST','Get'])




if __name__ == '__main__':
    app.run(debug=True)
