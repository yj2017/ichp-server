from flask import Flask, request, jsonify, redirect, url_for, abort
from werkzeug.utils import secure_filename
from flask import Response, render_template
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import json
import mysql.connector
import redis
import uuid
import traceback
import os
from record import Record
from activity import Activity
from entry import Entry

app = Flask(__name__)
uploadDir = 'D:/uploads/'

status = {0: 'successfully',
          1: 'password error',
          2: 'no such account name or password',
          3: 'username or password can not be empty',
          4: 'the username has already existed',
          5: 'register failed',
          6: 'add entry failed',
          7: 'the file type  is wrong ',
          8: 'unlogined,please login firstly',
          9: 'modify entry failed',
          10: 'mysql error ',
          11: 'issue activity failed in mysql',
          12: 'issue record failed',
          13: 'store personal info  failed',
          14: 'collect activity failed',
          15: 'you have not the authority',
          16: 'get records failed',
          17: 'search records failed ',
          18: 'search activity failed',
          19: 'search entry failed',
          20: 'search user failed',
          21: 'collect activity failed',
          22: 'there have not the activity',
          23: 'collect record failed',
          24: 'there have not the record',
          25: 'collect entry failed',
          26: 'there have not the entry',
          27: 'delete record failed'
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
    username = req['username']  # account_name账号名
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
                r.set(the_uuid, user_id, ex=3600*24)
                cursor.close()
                return json.dumps({"msg": "login successfully", "token": str(the_uuid), "uid": user_id})
            else:
                cursor.close()
                return decodeStatus(1)
        else:
            cursor.close()
            return decodeStatus(2)


# store the users' information


@app.route('/storeInfo', methods=['Get', 'POST', 'PUT'])
def StoreInfo():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    telephone = req['telephone']
    name = req['name']
    sign = req['sign']  # 个性签名
    image_src = req['image_src']  # 头像图片链接
    user_id = int(r.get(token))
    if user_id == None:
        cursor.close()
        return decodeStatus(8)
    else:
        sql = 'update user set telephone="%s",name="%s",sign="%s" ,image_src="%s" where user_id=%d' % (
            telephone, name, sign, user_id, image_src)
        app.logger.debug(sql)
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            cursor.close()
            return decodeStatus(10)
        if cursor.rowcount > 0:
            cursor.close()
            return decodeStatus(0)


# allowed file type
ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc',
     'WMV', 'ASF', 'AVI',  'AVS', 'FLV', 'MKV', 'MOV', '3GP', 'MP4', 'MPG', 'MPEG', 'DAT', 'OGM', 'VOB', 'RM', 'RMVB', 'TS', 'TP', 'IFO', 'NSV'
     'mp3', 'AAC', 'WAV', 'WMA', 'CDA', 'FLAC', 'M4A', 'MID', 'MKA', 'MP2', 'MPA', 'MPC', 'APE', 'OFR', 'OGG', 'RA', 'WV', 'TTA', 'AC3', 'DTS'
     ]
)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', 'Get', 'PUT'])
def Upload():
    try:
        token = request.form['token']  # client 传来的token属性.token为键，uid为值
        app.logger.debug(str(token))
        if r.exists(token):  # 登录状态
            f = request.files['the_file']
            app.logger.debug(str(f.filename))
            app.logger.debug(dir(f))
            if f and allowed_file(f.filename):
                app.logger.debug(f.filename)
                local_file = uploadDir+f.filename
                app.logger.debug(local_file)
                f.save(local_file)
                access_key = 'c4X-etSkzHTpZsHoPBvjshXtTbKOtGeGVgmMrVbR'
                secret_key = 'mCmzTs1PTu8oYsHhi8Tm84_gA6ZOd2gej5Vd8aeH'
                q = Auth(access_key, secret_key)
                bucket_name = 'ichp-bucket'
                up_filename = str(uuid.uuid1())+f.filename
                app.logger.debug(up_filename)
                key = str(up_filename)  # 七牛云上文件名
                up_token = q.upload_token(bucket_name, key, 3600*24)
                ret, info = put_file(up_token, key, local_file)
                os.remove(local_file)
                return json.dumps({"msg": "upload successfully", "addr": 'http://p5o94s90i.bkt.clouddn.com/%s' % up_filename, "code": 0}, ensure_ascii=False)
            else:
                return decodeStatus(7)
        else:  # 未登录
            return decodeStatus(8)
    except Exception as e:
        app.logger.debug(e)
        return decodeStatus(13)

# add label,entry


@app.route('/addEntry', methods=['POST'])
def AddEntry():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    editor = int(r.get(token))
    if r.exists(token):
        name = req['name']
        content = req['content']
        sql = 'insert into entry (name,content,editor) values ("%s","%s",%d)' % (
            name, content, editor)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(6)
        else:
            cursor.close()
            return decodeStatus(0)
    else:
        return decodeStatus(8)

# modify label or entry


@app.route('/modifyEntry', methods=['POST'])
def modifyEntry():
    cursor = conn.cursor()
    req = json.loads(request.data)
    name = req['name']
    token = req['token']
    editor = int(r.get(token))
    if r.exists(token):
        content = req['content']
        sql = 'update entry set content=("%s"),editor=(%d) where name=("%s")' % (
            content, editor, name)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(9)
        else:
            cursor.close()
            return decodeStatus(0)
    else:
        return decodeStatus(8)
    # store record

# search entry


@app.route('/searchEntry', methods=["POST"])
def SearchEntry():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    searchEntry = req['searchEntry']
    if r.exists(token):
        sql = 'select entry_id,name,content,editor from entry  where name like "%s" ' % (
            '%'+searchEntry+'%',)
        try:
            cursor.execute(sql)
            listEnt = cursor.fetchall()
            entL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    entry = Entry(listEnt[row][0], listEnt[row]
                                  [1], listEnt[row][2], listEnt[row][3])
                    entL.append(entry)
                    app.logger.debug(entL)
            return json.dumps({"msg": "successfully", "code": 0, "data": entL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(19)
    else:
        return decodeStatus(8)


@app.route('/collEntry', methods=["POST"])
def CollEntry():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    entry_id = int(req['entry_id'])
    if r.exists(token):
        sql_ent = 'select * from entry where entry_id= %d' % (entry_id,)
        cursor.execute(sql_ent)
        cursor.fetchall()
        if cursor.rowcount > 0:
            collector = int(r.get(token))
            sql = 'insert into coll_entry (collector,entry_id) values (%d,%d)' % (
                collector, entry_id)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as de:
                app.logger.debug(str(de))
                conn.rollback()
                cursor.close()
                return decodeStatus(25)
            else:
                cursor.close()
                return decodeStatus(0)
        else:
            return decodeStatus(26)
    else:
        return decodeStatus(8)

# get  an entry content


@app.route('/getEntry', methods=["POST", "GET"])
def GetEntry():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    entry_id = int(req['entry_id'])
    if r.exists(token):
        sql = 'select entry_id,name,content,editor from entry where entry_id=%d' % (
            entry_id,)
        try:
            cursor.execute(sql)
            entry = cursor.fetchall()
            entryL = []
            if cursor.rowcount > 0:
                entry = Entry(entry[0][0], entry[0][1],
                              entry[0][2], entry[0][3])
                entryL.append(entry)
                return json.dumps({"msg": "successfully", "code": 0, "data": entryL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
            else:
                return decodeStatus(26)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        return decodeStatus(8)


# issue record


@app.route('/addRec', methods=['POST'])
def AddRec():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    if r.exists(token):
        recorder = int(r.get(token))
        title = req['title']
        discribe = req['discribe']
        url = req['url']
        type = req['type']
        addr = req['addr']  # 地址
        sql = 'insert into record (recorder,title,discribe,url,type,addr) values ("%d","%s","%s","%s","%s","%s")' % (
            recorder, title, discribe, url, type, addr)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(10)
        else:
            cursor.close()
            return decodeStatus(0)
    else:
        return decodeStatus(8)

# delete record


@app.route('/delRec', methods=["POST"])
def DelRec():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    rec_id = int(req['rec_id'])
    if r.exists(token):
        sql_isExist = 'select * from record where rec_id=%d' % (rec_id,)
        cursor.execute(sql_isExist)
        cursor.fetchall()
        if cursor.rowcount > 0:
            operator = int(r.get(token))
            sql_temp = 'select recorder from record where rec_id=%d' % (
                rec_id,)
            cursor.execute(sql_temp)
            recorder = cursor.fetchall()
            if operator == recorder[0][0]:
                sql = 'delete from record where rec_id=%d' % (rec_id,)
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as de:
                    app.logger.debug(str(de))
                    conn.rollback()
                    cursor.close()
                    return decodeStatus(27)
                else:
                    cursor.close()
                    return decodeStatus(0)
            else:
                return decodeStatus(15)  # 不是发布者删除record
        else:
            return decodeStatus(24)
    else:
        return decodeStatus(8)
# get record list


@app.route('/getALLRec', methods=['POST', 'GET'])
def GetAllRec():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    if r.exists(token):
        sql = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe from record'
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            app.logger.debug(listRec)
            recL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                    [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9])
                    recL.append(record)
                    app.logger.debug(recL)
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        return decodeStatus(8)

 # search record


@app.route('/searchRec', methods=["POST"])
def SearchRec():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    searchRec = req['searchRec']
    if r.exists(token):
        sql = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe from record where title like "%s" ' % (
            '%'+searchRec+'%',)
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                    [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9])
                    recL.append(record)
                    app.logger.debug(recL)
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(17)
    else:
        return decodeStatus(8)


@app.route('/collRec', methods=["POST"])
def CollRec():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    rec_id = int(req['rec_id'])
    if r.exists(token):
        sql_rec = 'select * from record where rec_id= %d' % (rec_id,)
        cursor.execute(sql_rec)
        cursor.fetchall()
        if cursor.rowcount > 0:
            collector = int(r.get(token))
            sql = 'insert into coll_record (collector,rec_id) values (%d,%d)' % (
                collector, rec_id)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as de:
                app.logger.debug(str(de))
                conn.rollback()
                cursor.close()
                return decodeStatus(23)
            else:
                cursor.close()
                return decodeStatus(0)
        else:
            return decodeStatus(24)
    else:
        return decodeStatus(8)

# issue activity


@app.route('/issueAct', methods=["POST"])
def IssueAct():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    if r.exists(token):
        publisher = int(r.get(token))
        role_sql = 'select role from user where user_id= %d' % (publisher,)
        cursor.execute(role_sql)
        role_id = cursor.fetchall()
        if role_id[0][0] == 1:  # 角色为官方
            title = req['title']
            content = req['content']
            hold_date = req['hold_date']
            hold_addr = req['hold_addr']
            act_src = req['act_src']
            sql = 'insert into record (publisher,title,content,hold_date,hold_addr,act_src) values (%d,"%s","%s","%s","%s","%s")' % (
                publisher, title, content, hold_date, hold_addr, act_src)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as de:
                app.logger.debug(str(de))
                conn.rollback()
                cursor.close()
                return decodeStatus(11)
            else:
                cursor.close()
                return decodeStatus(0)
        else:
            return decodeStatus(15)
    else:
        return decodeStatus(8)

# delete activity


@app.route('/delAct', methods=["POST"])
def DelAct():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    act_id = int(req['act_id'])
    if r.exists(token):
        sql_isExist = 'select * from activity where act_id=%d' % (act_id,)
        cursor.execute(sql_isExist)
        cursor.fetchall()
        if cursor.rowcount > 0:
            operator = int(r.get(token))
            sql_temp = 'select publisher from activity where act_id=%d' % (
                act_id,)
            cursor.execute(sql_temp)
            publisher = cursor.fetchall()
            if operator == publisher[0][0]:
                sql = 'delete from activity where act_id=%d' % (act_id,)
                try:
                    cursor.execute(sql)
                    conn.commit()
                except Exception as de:
                    app.logger.debug(str(de))
                    conn.rollback()
                    cursor.close()
                    return decodeStatus(27)
                else:
                    cursor.close()
                    return decodeStatus(0)
            else:
                return decodeStatus(15)  # 不是发布者删除
        else:
            return decodeStatus(22)
    else:
        return decodeStatus(8)

# search activity


@app.route('/searchAct', methods=["POST", "GET"])
def SearchAct():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    searchAct = req['searchAct']
    if r.exists(token):
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date from activity  where title like "%s" ' % (
            '%'+searchAct+'%',)
        try:
            cursor.execute(sql)
            listAct = cursor.fetchall()
            actL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                        [4], listAct[row][5], listAct[row][6], listAct[row][7])
                    actL.append(activity)
                    app.logger.debug(actL)
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(18)
    else:
        return decodeStatus(8)

# get an activity 
@app.route('/getAct', methods=["POST", "GET"])
def GetAct():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    entry_id = int(req['entry_id'])
    if r.exists(token):
        sql = 'select entry_id,name,content,editor from entry where entry_id=%d' % (
            entry_id,)
        try:
            cursor.execute(sql)
            entry = cursor.fetchall()
            entryL = []
            if cursor.rowcount > 0:
                entry = Entry(entry[0][0], entry[0][1],
                              entry[0][2], entry[0][3])
                entryL.append(entry)
                return json.dumps({"msg": "successfully", "code": 0, "data": entryL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
            else:
                return decodeStatus(26)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        return decodeStatus(8)
# collect activity


@app.route('/collAct', methods=["POST", "GET"])
def CollAct():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    act_id = int(req['act_id'])
    if r.exists(token):
        sql_act = 'select * from activity where act_id= %d' % (act_id,)
        cursor.execute(sql_act)
        temp = cursor.fetchall()
        app.logger.debug(temp)
        if cursor.rowcount > 0:
            collector = int(r.get(token))
            sql = 'insert into coll_activity (collector,act_id) values (%d,%d)' % (
                collector, act_id)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as de:
                app.logger.debug(str(de))
                conn.rollback()
                cursor.close()
                return decodeStatus(21)
            else:
                cursor.close()
                return decodeStatus(0)
        else:
            return decodeStatus(22)
    else:
        return decodeStatus(8)


# search user


@app.route('/searchUser', methods=["POST", "GET"])
def searchUser():
    cursor = conn.cursor()
    req = json.loads(request.data)
    token = req['token']
    searchEntry = req['searchEntry']
    if r.exists(token):
        sql = 'select entry_id,name,content,editor from entry  where name like "%s" ' % (
            '%'+searchEntry+'%',)
        try:
            cursor.execute(sql)
            listEnt = cursor.fetchall()
            entL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    entry = Entry(listEnt[row][0], listEnt[row]
                                  [1], listEnt[row][2], listEnt[row][3])
                    entL.append(entry)
                    app.logger.debug(entL)
            return json.dumps({"msg": "successfully", "code": 0, "data": entL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(19)
    else:
        return decodeStatus(8)


if __name__ == '__main__':
    app.run(debug=True)
