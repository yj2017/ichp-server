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
from user import User
from comment import Comment
import platform
import logging
import mysql

app = Flask(__name__)
app.logger.addHandler(logging.FileHandler('ichp.log'))
app.debug = True


def getUploadDir():
    if platform.system() == 'Windows':
        return 'D:/uploads/'
    else:
        return '/tmp/'


uploadDir = getUploadDir()

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
          10: 'store user information failed ',
          11: 'issue activity failed ',
          12: 'issue record failed',
          13: 'upload file failed',
          14: 'already exist the entry',
          15: 'you have not the authority',
          16: 'get records failed',
          17: 'search records failed ',
          18: 'search activity failed',
          19: 'search entry failed',
          20: 'search user failed',
          21: 'collect activity failed',
          22: 'no such activity',
          23: 'collect record failed',
          24: 'no such record',
          25: 'collect entry failed',
          26: 'no such entry',
          27: 'delete record failed',
          28: 'get activity failed',
          29: 'modify record failed',
          30: 'search user info failed',
          31: 'no such user',
          32: 'get my concerned list failed ',
          33: 'approve record failed',
          34: 'comment record failed',
          35: 'approve comment failed',
          36: 'comment comment failed',
          37: 'get comment of record failed',
          38: 'get comment of comment failed',
          39: 'no such comment record id ',
          40: 'delete comment of comment  failed',
          41: 'delete comment of record failed',
          42: 'no such comment comment id ',
          43: 'recommend record failed',
          44: 'recommend activity failed',
          45: 'get user information failed',
          46: 'delete user failed'
          }
# redis
pool = redis.ConnectionPool(
    host='localhost', port='6379', decode_responses=True)
r = redis.Redis(connection_pool=pool)
# mysql
conn = mysql.connector.connect(
    user='ichp', password='273841', database='ichp')


def decodeStatus(code):
    return json.dumps({"msg": status[code], "code": code})

# This is register


@app.route('/register', methods=['POST'])
def Register():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    username = req['username']  # account_name账号名
    psw = req['psw']
    role = int(req['role'])
    if username == ''or psw == '' or role == '':
        cursor.close()
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
                return decodeStatus(5)
            if cursor.rowcount > 0:
                cursor.execute(
                    'select user_id from user where account_name="%s" and psw="%s"' % (username, psw))
                user_id = cursor.fetchall()[0][0]
                cursor.close()
                # return the unique user id
                return json.dumps({"user_id": user_id})
            else:
                cursor.close()
                return decodeStatus(5)


# This is login
@app.route('/login', methods=['POST'])
def Login():
    cursor = conn.cursor()
    #req = request.get_json(force=True)
    req = request.get_json(force=True)
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
                return json.dumps({"msg": "login successfully", "token": str(the_uuid), "uid": user_id, "code": 0})
            else:
                cursor.close()
                return decodeStatus(1)
        else:
            cursor.close()
            return decodeStatus(2)


# store the users' information
@app.route('/storeInfo', methods=['POST'])
def StoreInfo():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
        try:
            cursor.execute(sql)
            operator = int(r.get(token))
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                operator,)
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            cursor.close()
            return decodeStatus(10)
        if cursor.rowcount > 0:
            cursor.close()
            return decodeStatus(0)


# modify user 's image
@app.route('/modifyImage', methods=["POST"])
def ModifyImage():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    image_src = req['image_src']  # 头像图片链接
    user_id = int(r.get(token))
    if user_id == None:
        cursor.close()
        return decodeStatus(8)
    else:
        sql = 'update user set image_src="%s" where user_id=%d' % (
            image_src, user_id)
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

# modify user's sign


@app.route('/modifySign', methods=["POST"])
def ModifySign():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    sign = req['sign']  # 头像图片链接
    user_id = int(r.get(token))
    if user_id == None:
        cursor.close()
        return decodeStatus(8)
    else:
        sql = 'update user set sign="%s" where user_id=%d' % (
            sign, user_id)
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


@app.route('/upload', methods=['POST'])
def Upload():
    try:
        token = request.form['token']  # client 传来的token属性.token为键，uid为值
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
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        editor = int(r.get(token))
        name = req['name']
        content = req['content']
        url = req['url']
        sql_temp = 'select * from entry where name ="%s"' % (name,)
        cursor.execute(sql_temp)
        cursor.fetchall()
        if cursor.rowcount > 0:
            cursor.close()
            return decodeStatus(14)
        else:
            sql = 'insert into entry (name,content,editor,url) values ("%s","%s",%d,"%s")' % (
                name, content, editor, url)
            try:
                cursor.execute(sql)
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                    operator,)
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
        cursor.close()
        return decodeStatus(8)

# modify label or entry


@app.route('/modifyEntry', methods=['POST'])
def modifyEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    entry_id = int(req['entry_id'])
    token = req['token']
    if r.exists(token):
        editor = int(r.get(token))
        content = req['content']
        sql = 'update entry set content="%s",editor=%d where entry_id=%d' % (
            content, editor, entry_id)
        try:
            cursor.execute(sql)
            operator = int(r.get(token))
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                operator,)
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
        cursor.close()
        return decodeStatus(8)

# search entry


@app.route('/searchEntry', methods=["POST"])
def SearchEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    searchEntry = req['searchEntry']
    if r.exists(token):
        sql = 'select entry_id,name,content,editor,url from entry  where name like "%s" ' % (
            '%'+searchEntry+'%',)
        try:
            cursor.execute(sql)
            listEnt = cursor.fetchall()
            entL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    entry = Entry(listEnt[row][0], listEnt[row]
                                  [1], listEnt[row][2], listEnt[row][3], listEnt[row][4])
                    entL.append(entry)
                    app.logger.debug(entL)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": entL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(19)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/collEntry', methods=["POST"])
def CollEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    operator,)
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
            cursor.close()
            return decodeStatus(26)
    else:
        cursor.close()
        return decodeStatus(8)

# get  an entry content


@app.route('/getEntry', methods=["POST"])
def GetEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    entry_id = int(req['entry_id'])
    if r.exists(token):
        sql = 'select entry_id,name,content,editor,url from entry where entry_id=%d' % (
            entry_id,)
        try:
            cursor.execute(sql)
            entry = cursor.fetchall()
            entryL = []
            if cursor.rowcount > 0:
                entry = Entry(entry[0][0], entry[0][1],
                              entry[0][2], entry[0][3], entry[0][4])
                entryL.append(entry)
                cursor.close()
                return json.dumps({"msg": "successfully", "code": 0, "data": entryL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
            else:
                cursor.close()
                return decodeStatus(26)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        cursor.close()
        return decodeStatus(8)


# issue record
@app.route('/addRec', methods=['POST'])
def AddRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        recorder = int(r.get(token))
        title = req['title']
        discribe = req['discribe']
        url = req['url']
        addr = req['addr']  # 地址]
        labels_id_str = req['labels_id_str']
        sql = 'insert into record (recorder,title,discribe,url,type,addr,appr_num,comm_num,labels_id_str) values (%d,"%s","%s","%s","%s","%s",%d,%d,"%s")' 
        # mysql.insert(sql, [recorder, title, discribe, url, 0, addr, 0, 0, labels_id_str])
        try:
            cursor.execute(sql,[recorder, title, discribe, url, 0, addr, 0, 0, labels_id_str])
            operator = int(r.get(token))
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                operator,)
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(12)
        else:
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0})
    else:
        cursor.close()
        return decodeStatus(8)

# delete record


@app.route('/delRec', methods=["POST"])
def DelRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
                sql1='select comm_rec_id from comm_rec where rec_id=%d'%(rec_id,)
                cursor.execute(sql1)
                comm_rec_id=cursor.fetchall()[0][0]
                if(comm_rec_id!=None):
                    sql2='select comm_comm_id from comm_rec where comm_rec_id=%d'%(comm_rec_id,)
                    cursor.execute(sql2)
                    comm_comm_id=cursor.fetchall()[0][0]
                    if(comm_comm_id!=None):
                        sql3='delete from comm_comm where comm_rec_id=%d'%(comm_rec_id)
                        cursor.execute(sql3)
                        cursor.commit()
                        sql4='delete from comm_rec where rec_id=%d'%(rec_id)
                        cursor.execute(sql4)
                        cursor.commit()
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
                cursor.close()
                return decodeStatus(15)  # 不是发布者删除record
        else:
            cursor.close()
            return decodeStatus(24)
    else:
        cursor.close()
        return decodeStatus(8)

# modify record


@app.route('/modifyRec', methods=["POST"])
def ModifyRecord():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    rec_id = int(req['rec_id'])
    token = req['token']
    if r.exists(token):
        operator = int(r.get(token))
        sql_temp = 'select recorder from record where rec_id=%d' % (rec_id,)
        cursor.execute(sql_temp)
        recorder = cursor.fetchall()
        if operator == recorder[0][0]:
            discribe = req['discribe']
            sql = 'update record set discribe="%s" where rec_id=%d' % (
                discribe, rec_id)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as de:
                app.logger.debug(str(de))
                conn.rollback()
                cursor.close()
                return decodeStatus(29)
            else:
                cursor.close()
                return decodeStatus(0)
        else:
            cursor.close()
            return decodeStatus(15)
    else:
        cursor.close()
        return decodeStatus(8)


# get record list
@app.route('/getAllRec', methods=['POST'])
def GetAllRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        sql = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str from record'
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                    [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                    recL.append(record)
            cursor.close()
            app.logger.debug(str(recL))
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/getUserRec', methods=["POST"])
def GetUserRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    recorder = int(req['recorder'])
    if r.exists(token):
        sql = 'select rec_id, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str  from record where recorder=%d' % recorder
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], recorder, listRec[row][1], listRec[row][2], listRec[row]
                                    [3], listRec[row][4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9])
                    recL.append(record)
                    app.logger.debug(recL)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        cursor.close()
        return decodeStatus(8)

 # search record


@app.route('/getRec', methods=["POST"])
def GetRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    rec_id = int(req['rec_id'])
    if r.exists(token):
        sql = 'select rec_id, recorder,title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str  from record where rec_id=%d' % rec_id
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0],  listRec[row][1], listRec[row][2], listRec[row]
                                    [3], listRec[row][4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                    recL.append(record)
                    app.logger.debug(recL)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/searchRec', methods=["POST"])
def SearchRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    searchW = req['searchW']
    if r.exists(token):
        sql = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str  from record where title like "%s" ' % (
            '%'+searchW+'%',)
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                # 返回列表
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                    [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                    recL.append(record)
                    app.logger.debug(recL)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(17)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/collRec', methods=["POST"])
def CollRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    operator,)
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
            cursor.close()
            return decodeStatus(24)
    else:
        cursor.close()
        return decodeStatus(8)

# issue activity


@app.route('/issueAct', methods=["POST"])
def IssueAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        publisher = int(r.get(token))
        role_sql = 'select role from user where user_id= %d' % (publisher,)
        cursor.execute(role_sql)
        role_id = cursor.fetchall()
        if int(role_id[0][0]) == 1:  # 角色为官方
            title = req['title']
            content = req['content']
            hold_date = req['hold_date']
            hold_addr = req['hold_addr']
            act_src = req['act_src']
            sql = 'insert into activity (publisher,title,content,hold_date,hold_addr,act_src) values (%d,"%s","%s","%s","%s","%s")' % (
                publisher, title, content, hold_date, hold_addr, act_src)
            try:
                cursor.execute(sql)
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                    operator,)
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
            cursor.close()
            return decodeStatus(15)
    else:
        cursor.close()
        return decodeStatus(8)

# delete activity


@app.route('/delAct', methods=["POST"])
def DelAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
                cursor.close()
                return decodeStatus(15)  # 不是发布者删除
        else:
            cursor.close()
            return decodeStatus(22)
    else:
        cursor.close()
        return decodeStatus(8)


# search activity
@app.route('/searchAct', methods=["POST"])
def SearchAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
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
                for row in range(cursor.rowcount):
                    activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                        [4], listAct[row][5], listAct[row][6], listAct[row][7])
                    actL.append(activity)
                cursor.close()
                return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
            cursor.close()
            return decodeStatus(32)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(18)
    else:
        cursor.close()
        return decodeStatus(8)

# get activity


@app.route('/getAllAct', methods=["POST"])
def GetAllAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date from activity'
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            for row in range(cursor.rowcount):
                activity = Activity(act[0][0], act[0][1],
                                    act[0][2], act[0][3], act[0][4], act[0][5], act[0][6], act[0][7])
                actL.append(activity)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(28)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/getUserAct', methods=["POST"])
def GetUserAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        publisher = int(req['publisher'])
        sql = 'select act_id,title,content,hold_date,hold_addr,act_src,issue_date from activity where publisher=%d' % (
            publisher,)
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            activity = Activity(act[0][0], publisher,
                                act[0][1], act[0][2], act[0][3], act[0][4], act[0][5], act[0][6])
            actL.append(activity)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(28)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/getAct', methods=["POST"])
def GetAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        act_id = int(req['act_id'])
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date from activity where act_id=%d' % (
            act_id,)
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            activity = Activity(act[0][0],
                                act[0][1], act[0][2], act[0][3], act[0][4], act[0][5], act[0][6], act[0][7])
            actL.append(activity)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(28)
    else:
        cursor.close()
        return decodeStatus(8)
# collect activity


@app.route('/collAct', methods=["POST"])
def CollAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        act_id = int(req['act_id'])
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
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    operator,)
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
            cursor.close()
            return decodeStatus(22)
    else:
        cursor.close()
        return decodeStatus(8)


# search user information
@app.route('/searchUserInfo', methods=["POST"])
def SearchUserInfo():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    searchW = req['searchW']  # 通过账号模糊搜索
    if r.exists(token):
        sql = 'select user_id,role,telephone,image_src,name,sign,acc_point,account_name,reg_date from user where account_name like "%s"' % (
            '%'+searchW+'%',)
        try:
            cursor.execute(sql)
            listUser = cursor.fetchall()
            userL = []
            for row in range(cursor.rowcount):
                user = User(listUser[row][0], listUser[row][1], listUser[row][2], listUser[row][3],
                            listUser[row][4], listUser[row][5], listUser[row][6], listUser[row][7], listUser[row][8])
                userL.append(user)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": userL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(30)
    else:
        cursor.close()
        return decodeStatus(8)

# get my Concerned list


@app.route('/getMyConc', methods=["POST"])
def GetMyConc():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        pay_id = int(r.get(token))  # myself
        sql_temp = 'select be_paid_id from attention_info where pay_id=%d' % (
            pay_id,)
        try:
            cursor.execute(sql_temp)
            uidL = cursor.fetchall()
            userL = []  # 没有关注任何用户
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    sql = 'select user_id,role,telephone,image_src,name,sign,acc_point,account_name,reg_date from user where user_id=%d' % (
                        uidL[row][0])
                    try:
                        cursor.execute(sql)
                        listUser = cursor.fetchall()
                        user = User(listUser[0][0], listUser[0][1], listUser[0][2], listUser[0][3],
                                    listUser[0][4], listUser[0][5], listUser[0][6], listUser[0][7], listUser[0][8])
                        userL.append(user)
                    except Exception as e:
                        app.logger.debug(str(e))
                        cursor.close()
                        return decodeStatus(32)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": userL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(32)
    else:
        cursor.close()
        return decodeStatus(8)

# approve record 点赞


@app.route('/apprRec', methods=["POST"])
def ApprRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        rec_id = int(req['rec_id'])
        sql = 'update record set appr_num=appr_num+1 where rec_id=%d' % (
            rec_id,)
        try:
            cursor.execute(sql)
            if cursor.rowcount > 0:
                conn.commit()
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    operator,)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                return decodeStatus(0)
            else:
                conn.rollback()
                cursor.close()
                return decodeStatus(33)
        except Exception as e:
            app.logger.debug(str(e))
            cursor.close()
            return decodeStatus(33)
    else:
        cursor.close()
        return decodeStatus(8)

# comment record 评论


@app.route('/commRec', methods=["POST"])
def CommRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    content = req['content']
    if r.exists(token):
        rec_id = int(req['rec_id'])
        commer = int(r.get(token))
        sql = 'insert into comm_rec (rec_id,commer,content,appr_num) values (%d,%d,"%s",%d)' % (
            rec_id, commer, content, 0)
        try:
            cursor.execute(sql)
            conn.commit()
            operator = int(r.get(token))
            sql = 'update user set acc_point=acc_point+20 where user_id=%d' % (
                operator,)
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(34)
        else:
            cursor.close()
            return decodeStatus(0)
    else:
        cursor.close()
        return decodeStatus(8)

# get the comment of record


@app.route('/getCommRec', methods=["POST"])
def GetCommRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        rec_id = int(req['rec_id'])
        sql_temp = 'select commer from comm_rec where rec_id=%d' % (
            rec_id,)
        cursor.execute(sql_temp)
        commer = cursor.fetchall()[0][0]
        sql = 'select comm_rec_id,rec_id,commer,content,appr_num,comm_date ,image_src,account_name from comm_rec,user where comm_rec.rec_id=%d and user.user_id=%d' % (
            rec_id, commer)
        try:
            cursor.execute(sql)
            commList = cursor.fetchall()
            commL = []
            if cursor.rowcount > 0:
                for row in range(len(commList)):
                    commentRec = Comment(commList[row][0], commList[row][1], commList[row][2],
                                         commList[row][3], commList[row][4], commList[row][5], commList[row][6], commList[row][7])
                    commL.append(commentRec)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(37)
        else:
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "date": commL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
    else:
        cursor.close()
        return decodeStatus(8)

# delete the comment of record


@app.route('/delCommRec', methods=["POST"])
def DelCommRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    comm_rec_id = int(req['comm_rec_id'])
    if r.exists(token):
        operator = int(r.get(token))
        sql_temp = 'select commer from comm_rec where comm_rec_id=%d' % (
            comm_rec_id,)
        sql = 'delete from comm_rec where comm_rec_id=%d' % (comm_rec_id,)
        sql1='select * from comm_comm where comm_rec_id=%d'%(comm_rec_id,)
        sql2= 'delete from comm_comm where comm_rec_id=%d' % (comm_rec_id,)
        try:
            cursor.execute(sql_temp)
            commer = cursor.fetchall()
            if cursor.rowcount > 0:
                if operator == commer[0][0]:
                    cursor.execute(sql1)
                    cursor.fetchall()
                    if(cursor.rowcount>0):
                        cursor.execute(sql2)
                        cursor.commit
                    try:
                        cursor.execute(sql)
                        conn.commit()
                    except Exception as e:
                        app.logger.debug(str(e))
                        conn.rollback()
                        cursor.close()
                        return decodeStatus(41)
                    else:
                        cursor.close()
                        return decodeStatus(0)
                else:
                    cursor.close()
                    return decodeStatus(15)
            else:
                cursor.close()
                return decodeStatus(41)
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(41)
    else:
        cursor.close()
        return decodeStatus(8)
# approve comment


@app.route('/apprComm', methods=["POST"])
def ApprComm():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    comm_rec_id = int(req['comm_rec_id'])
    if r.exists(token):
        sql = 'update comm_rec set appr_num=appr_num+1 where comm_rec_id=%d' % (
            comm_rec_id,)
        try:
            cursor.execute(sql)
            if cursor.rowcount > 0:
                conn.commit()
                operator = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    operator,)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                return decodeStatus(0)
            else:
                conn.rollback()
                cursor.close()
                return decodeStatus(35)
        except Exception as e:
            app.logger.debug(str(e))
            cursor.close()
            return decodeStatus(35)
    else:
        cursor.close()
        return decodeStatus(8)

# comment comment


@app.route('/commComm', methods=["POST"])
def CommComm():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    comm_rec_id = int(req['comm_rec_id'])
    content = req['content']
    if r.exists(token):
        commer = int(r.get(token))
        sql = 'insert into comm_comm (comm_rec_id,commer,content,appr_num) values (%d,%d,"%s",%d)' % (
            comm_rec_id, commer, content, 0)
        try:
            cursor.execute(sql)
            conn.commit()
            operator = int(r.get(token))
            sql = 'update user set acc_point=acc_point+20 where user_id=%d' % (
                operator,)
            cursor.execute(sql)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(36)
        else:
            cursor.close()
            return decodeStatus(0)
    else:
        cursor.close()
        return decodeStatus(8)

# delete comment of comment


@app.route('/delCommComm', methods=["POST"])
def DelCommComm():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    comm_comm_id = int(req['comm_comm_id'])
    if r.exists(token):
        operator = int(r.get(token))
        sql_temp = 'select commer from comm_comm where comm_comm_id=%d' % (
            comm_comm_id,)
        sql = 'delete from comm_comm where comm_comm_id=%d' % (comm_comm_id,)
        try:
            cursor.execute(sql_temp)
            commer = cursor.fetchall()
            if cursor.rowcount > 0:
                if operator == commer[0][0]:
                    try:
                        cursor.execute(sql)
                        conn.commit()
                    except Exception as e:
                        app.logger.debug(str(e))
                        conn.rollback()
                        cursor.close()
                        return decodeStatus(40)
                    else:
                        cursor.close()
                        return decodeStatus(0)
                else:
                    cursor.close()
                    return decodeStatus(15)
            else:
                cursor.close()
                return decodeStatus(42)
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(40)
    else:
        cursor.close()
        return decodeStatus(8)

# get comment  of comment


@app.route('/getCommComm', methods=["POST"])
def GetCommComm():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    comm_rec_id = int(req['comm_rec_id'])
    if r.exists(token):
        sql_temp = 'select commer from comm_comm where comm_rec_id=%d' % (
            comm_rec_id,)
        cursor.execute(sql_temp)
        commer = cursor.fetchall()[0][0]
        sql = 'select comm_comm_id,comm_rec_id,commer,content,appr_num,comm_date,image_src,account_name from comm_comm,user where comm_rec_id=%d and user_id=%d' % (
            comm_rec_id, commer)
        try:
            cursor.execute(sql)
            commList = cursor.fetchall()
            commL = []
            if cursor.rowcount > 0:
                for row in range(len(commList)):
                    commentComm = Comment(commList[row][0], commList[row][1], commList[row][2],
                                          commList[row][3], commList[row][4], commList[row][5], commList[row][6], commList[row][7])
                    commL.append(commentComm)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(38)
        else:
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "date": commL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
    else:
        cursor.close()
        return decodeStatus(8)

# recomend rec


@app.route('/recommendRec', methods=["POST"])
def recommendRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    addr = req['addr']
    if r.exists(token):
        operator = int(r.get(token))
        sql = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str from record where recorder != %d order by issue_date desc' % (
            operator,)
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0 and cursor.rowcount <= 2:
                # 返回两条推荐记录
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                    [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                    recL.append(record)
                    app.logger.debug(recL)
            elif cursor.rowcount > 2:
                for row in range(cursor.rowcount):
                    if listRec[row][5] == addr:  # 地点
                        record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                        [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                        recL.append(record)
                if recL.count > 2:
                    recL = recL[:2]
                else:
                    for row in range(2):
                        record = Record(listRec[row][0], listRec[row][1], listRec[row][2], listRec[row][3], listRec[row]
                                        [4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                        recL.append(record)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": recL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(43)
    else:
        cursor.close()
        return decodeStatus(8)

# recommend act


@app.route('/recommendAct', methods=["POST"])
def recommendAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    addr = req['addr']
    if r.exists(token):
        operator = int(r.get(token))
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date from activity where publisher != %d order by issue_date desc' % (
            operator,)
        try:
            cursor.execute(sql)
            listAct = cursor.fetchall()
            actL = []
            if cursor.rowcount > 0 and cursor.rowcount <= 2:
                # 返回两条推荐
                app.logger.debug(cursor.rowcount)
                for row in range(cursor.rowcount):
                    activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                        [4], listAct[row][5], listAct[row][6], listAct[row][7])
                    actL.append(activity)
            elif cursor.rowcount > 2:
                for row in range(cursor.rowcount):
                    if listAct[row][5] == addr:  # 地点
                        activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                            [4], listAct[row][5], listAct[row][6], listAct[row][7])
                app.logger.debug(len(actL))
                if len(actL) > 2:
                    actL = actL[:2]
                else:
                    for row in range(2):
                        activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                            [4], listAct[row][5], listAct[row][6], listAct[row][7])
                        actL.append(activity)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(44)
    else:
        cursor.close()
        return decodeStatus(8)

# modify entry's backgroud


@app.route('/modifyEntryBg', methods=['POST'])
def ModifyEntryBg():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    url = req['url']  # 图片链接
    entry_id = int(req['entry_id'])
    user_id = int(r.get(token))
    if user_id == None:
        cursor.close()
        return decodeStatus(8)
    else:
        sql = 'update entry set url="%s" where entry_id=%d' % (
            url, entry_id)
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


@app.route('/getUserInfo', methods=['POST'])
def GetUserInfo():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    user_id = int(req['user_id'])
    if r.exists(token):
        sql = 'select user_id,role,telephone,image_src,name,sign,acc_point,account_name,reg_date from user where user_id=%d' % (
            user_id,)
        try:
            cursor.execute(sql)
            listUser = cursor.fetchall()
            userL = []
            for row in range(cursor.rowcount):
                user = User(listUser[row][0], listUser[row][1], listUser[row][2], listUser[row][3],
                            listUser[row][4], listUser[row][5], listUser[row][6], listUser[row][7], listUser[row][8])
                userL.append(user)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": userL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(30)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/cancelAccount', methods=['POST'])
def CancelAccount():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        user_id = int(r.get(token))
        sql = 'delete  from user where user_id=%d ' % (user_id,)
        try:
            cursor.execute(sql)
            if cursor.rowcount > 0:
                cursor.close()
                return decodeStatus(0)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(46)
    else:
        cursor.close()
        return decodeStatus(8)

# if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug=True)
