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
import math
import operator

app = Flask(__name__)
handler = logging.FileHandler('ichp.log')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s :\n %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

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
          46: 'delete user failed',
          47: 'get address failed in mysql',
          48:'concern failed'
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
    psw = str(req['psw'])
    if username == None or psw == None:
        cursor.close()
        return decodeStatus(2)
    else:
        cursor.execute(
            'select psw,user_id from user where account_name="%s"' % (username,))
        psw_id = cursor.fetchall()
        if cursor.rowcount >= 1:
            app.logger.debug(psw_id[0][0]+"*")
            app.logger.debug(psw+"*")
            if psw == psw_id[0][0]:
                app.logger.debug(psw)
                the_uuid = uuid.uuid1()  # the key
                app.logger.debug(the_uuid)
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
            telephone, name, sign, image_src, user_id)
        try:
            cursor.execute(sql)
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                user_id,)
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
            sql = 'insert into entry (name,content,editor,url) values (%s,%s,%s,%s)'
            try:
                cursor.execute(sql, [name, content, editor, url])
                oper = int(r.get(token))
                sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                    oper,)
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
            oper = int(r.get(token))
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                oper,)
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
                oper = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    oper,)
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


@app.route('/getCollEntry', methods=["POST"])
def getCollEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        sql = 'select entry_id from coll_entry '
        try:
            cursor.execute(sql)
            entry_ids = cursor.fetchall()
            entryL = []
            rowCount = cursor.rowcount
            if rowCount >= 0:
                for i in range(rowCount):
                    sql_temp = 'select entry_id,name,content,editor,url from entry where entry_id=%d' % (
                        entry_ids[i][0])
                    cursor.execute(sql_temp)
                    entry = cursor.fetchall()
                    entry_temp = Entry(entry[0][0], entry[0][1],
                                       entry[0][2], entry[0][3], entry[0][4])
                    entryL.append(entry_temp)
                cursor.close()
                return json.dumps({"msg": "successfully", "code": 0, "data": entryL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(16)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/delCollEntry', methods=["POST"])
def delCollEntry():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    entry_id = int(req['entry_id'])
    if r.exists(token):
        sql_isExist = 'select * from coll_entry where entry_id=%d' % (entry_id,)
        cursor.execute(sql_isExist)
        cursor.fetchall()
        if cursor.rowcount > 0:
            oper = int(r.get(token))
            sql_temp = 'select collector from coll_entry where entry_id=%d' % (
                entry_id,)
            cursor.execute(sql_temp)
            recorder = cursor.fetchall()
            if oper == recorder[0][0]:
                sql = 'delete from coll_entry where entry_id=%d' % (entry_id,)
                try:
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    return decodeStatus(0)
                except Exception as de:
                    app.logger.debug(str(de))
                    conn.rollback()
                    cursor.close()
                    return decodeStatus(27)
            else:
                cursor.close()
                return decodeStatus(15)  # 不是发布者删除record
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
    app.logger.debug(token)
    if r.exists(token):
        recorder = int(r.get(token))
        title = req['title']
        discribe = req['discribe']
        url = req['url']
        addr = req['addr']  # 地址]
        labels_id_str = req['labels_id_str']
        sql = 'insert into record (recorder,title,discribe,url,type,addr,appr_num,comm_num,labels_id_str) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        app.logger.debug(sql)
        try:
            cursor.execute(sql, [recorder, title, discribe,
                                 url, 0, addr, 0, 0, labels_id_str])
            app.logger.debug(sql)
            sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                recorder,)
            cursor.execute(sql)
            app.logger.debug(cursor.rowcount)
            conn.commit()
        except Exception as de:
            app.logger.debug(str(de))
            conn.rollback()
            cursor.close()
            return decodeStatus(12)
        else:
            cursor.close()
            app.logger.debug(labels_id_str)
            return json.dumps({"msg": "successfully", "code": 0, "data": labels_id_str})
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
            oper = int(r.get(token))
            sql_temp = 'select recorder from record where rec_id=%d' % (
                rec_id,)
            cursor.execute(sql_temp)
            recorder = cursor.fetchall()
            if oper == recorder[0][0]:
                sql1 = 'select comm_rec_id from comm_rec where rec_id=%d' % (
                    rec_id,)
                try:
                    cursor.execute(sql1)
                    temp = cursor.fetchall()
                    if cursor.rowcount > 0:
                        comm_rec_id = temp[0][0]
                        sql2 = 'select comm_comm_id from comm_comm where comm_rec_id=%d' % (
                            comm_rec_id,)
                        cursor.execute(sql2)
                        temp = cursor.fetchall()
                        if cursor.rowcount > 0:
                            sql3 = 'delete from comm_comm where comm_rec_id=%d' % (
                                comm_rec_id)
                            cursor.execute(sql3)
                            sql4 = 'delete from comm_rec where rec_id=%d' % (
                                rec_id)
                            cursor.execute(sql4)
                    sql = 'delete from record where rec_id=%d' % (rec_id,)
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
        oper = int(r.get(token))
        sql_temp = 'select recorder from record where rec_id=%d' % (rec_id,)
        cursor.execute(sql_temp)
        recorder = cursor.fetchall()
        if oper == recorder[0][0]:
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
        oper=str(r.get(token))
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
                    if r.sismember("rec"+str(record.rec_id),oper):
                        record.isApprove=True
                    else:
                        record.isApprove=False
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
        oper=str(r.get(token))
        sql = 'select rec_id, recorder,title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str  from record where rec_id=%d' % rec_id
        try:
            cursor.execute(sql)
            listRec = cursor.fetchall()
            recL = []
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    record = Record(listRec[row][0],  listRec[row][1], listRec[row][2], listRec[row]
                                    [3], listRec[row][4], listRec[row][5], listRec[row][6], listRec[row][7], listRec[row][8], listRec[row][9], listRec[row][10])
                    if r.sismember("rec"+str(rec_id),oper):
                        record.isApprove=True
                    else:
                        record.isApprove=False
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

@app.route('/getCollRec',methods=["POST"])
def getCollRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        sql = 'select rec_id  from coll_record'
        try:
            cursor.execute(sql)
            rec_ids = cursor.fetchall()
            recL = []
            rowCount=cursor.rowcount
            if rowCount > 0:
                for row in range(rowCount):
                    sql_temp='select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str from record where rec_id=%d'%(rec_ids[row][0],)
                    cursor.execute(sql_temp)
                    listRec=cursor.fetchall()
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


@app.route('/delCollRec', methods=["POST"])
def DelCollRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    rec_id = int(req['rec_id'])
    if r.exists(token):
        sql_isExist = 'select * from coll_record where rec_id=%d' % (rec_id,)
        cursor.execute(sql_isExist)
        cursor.fetchall()
        if cursor.rowcount > 0:
            oper = int(r.get(token))
            sql_temp = 'select collector from coll_record where rec_id=%d' % (
                rec_id,)
            cursor.execute(sql_temp)
            recorder = cursor.fetchall()
            if oper == recorder[0][0]:
                sql = 'delete from coll_record where rec_id=%d' % (rec_id,)
                try:
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    return decodeStatus(0)
                except Exception as de:
                    app.logger.debug(str(de))
                    conn.rollback()
                    cursor.close()
                    return decodeStatus(27)
            else:
                cursor.close()
                return decodeStatus(15)  # 不是发布者删除record
        else:
            cursor.close()
            return decodeStatus(24)
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
                oper = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    oper,)
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
            image_src = req['image_src']
            labels_id_str = req['labels_id_str']
            sql = 'insert into activity (publisher,title,content,hold_date,hold_addr,act_src,image_src,labels_id_str) values (%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor.execute(sql, [publisher, title, content, hold_date,
                                     hold_addr, act_src, image_src, labels_id_str])
                oper = int(r.get(token))
                sql = 'update user set acc_point=acc_point+100 where user_id=%d' % (
                    oper,)
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
            oper = int(r.get(token))
            sql_temp = 'select publisher from activity where act_id=%d' % (
                act_id,)
            cursor.execute(sql_temp)
            publisher = cursor.fetchall()
            if oper == publisher[0][0]:
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
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src, labels_id_str from activity  where title like "%s" ' % (
            '%'+searchAct+'%',)
        try:
            cursor.execute(sql)
            listAct = cursor.fetchall()
            actL = []
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    activity = Activity(listAct[row][0], listAct[row][1], listAct[row][2], listAct[row][3], listAct[row]
                                        [4], listAct[row][5], listAct[row][6], listAct[row][7], listAct[row][8], listAct[row][9])
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
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date ,image_src,labels_id_str from activity'
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            for row in range(cursor.rowcount):
                activity = Activity(act[row][0], act[row][1],
                                    act[row][2], act[row][3], act[row][4], act[row][5], act[row][6], act[row][7], act[row][8], act[row][9])
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
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date ,image_src,labels_id_str from activity where publisher=%d' % (
            publisher,)
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            activity = Activity(act[0][0], act[0][1], act[0][2], act[0][3],
                                act[0][4], act[0][5], act[0][6], act[0][7], act[0][8], act[0][9])
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
        sql = 'select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src,labels_id_str from activity where act_id=%d' % (
            act_id,)
        try:
            cursor.execute(sql)
            act = cursor.fetchall()
            actL = []
            activity = Activity(act[0][0],
                                act[0][1], act[0][2], act[0][3], act[0][4], act[0][5], act[0][6], act[0][7], act[0][8], act[0][9])
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

@app.route('/getCollAct',methods=["POST"])
def getCollAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        sql = 'select act_id from coll_activity '
        try:
            cursor.execute(sql)
            act_ids = cursor.fetchall()
            actL = []
            rowCount=cursor.rowcount
            if rowCount>0:
                for i in range(rowCount):
                    sql_temp='select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src,labels_id_str from activity where act_id=%d' % (
                    act_ids[i][0],)
                    cursor.execute(sql_temp)
                    act=cursor.fechall()
                    activity = Activity(act[0][0],
                                act[0][1], act[0][2], act[0][3], act[0][4], act[0][5], act[0][6], act[0][7], act[0][8], act[0][9])
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
                oper = int(r.get(token))
                sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    oper,)
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

@app.route('/delCollAct',methods=["POST"])
def delCollAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    act_id = int(req['act_id'])
    if r.exists(token):
        sql_isExist = 'select * from coll_activity where act_id=%d' % (act_id,)
        cursor.execute(sql_isExist)
        cursor.fetchall()
        if cursor.rowcount > 0:
            oper = int(r.get(token))
            sql_temp = 'select collector from coll_activity where act_id=%d' % (
                act_id,)
            cursor.execute(sql_temp)
            publisher = cursor.fetchall()
            if oper == publisher[0][0]:
                sql = 'delete from coll_activity where act_id=%d' % (act_id,)
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

@app.route('/getConcMe',methods=["POST"])
def getConcMe():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        be_paid_id = int(r.get(token))  # myself
        sql_temp = 'select pay_id from attention_info where be_paid_id=%d' % (
            be_paid_id,)
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

@app.route('/concerUser',methods=["POST"])
def concerUser():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    user_id=int(req['user_id'])
    if r.exists(token):
        pay_id = int(r.get(token))
        sql='insert into attention_info(pay_id,be_paid_id) values(%d,%d)'%(pay_id,user_id)
        try:
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return decodeStatus(0)
        except:
            conn.rollback()
            cursor.close()
            return decodeStatus(48)
# approve record 点赞


@app.route('/apprRec', methods=["POST"])
def ApprRec():
    cursor=conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        rec_id_str=str(req['rec_id'])
        rec_id = int(rec_id_str)
        oper_str=str(r.get(token))
        oper=int(oper_str)  
        r.sadd("rec"+rec_id_str,oper_str)
        try:
            sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    oper,)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return json.dumps({"msg":"successfully","code":0,"data":r.scard("rec"+rec_id_str)},default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as e:
            app.logger.debug(str(e))
            conn.rollback()
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
            oper = int(r.get(token))
            sql = 'update user set acc_point=acc_point+20 where user_id=%d' % (
                oper,)
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
        oper=str(r.get(token))
        rec_id = int(req['rec_id'])
        commL = []
        cursor.execute('select commer from comm_rec where rec_id= %s', ( rec_id,))
        commer=cursor.fetchall()
        if cursor.rowcount > 0:
            sql = 'select comm_rec_id,rec_id,commer,content,appr_num,comm_date ,image_src,account_name from comm_rec,user where comm_rec.rec_id=%d and user.user_id=%d' % (
                rec_id, commer[0][0])
            try:
                cursor.execute(sql)
                commList = cursor.fetchall()
                if cursor.rowcount > 0:
                    for row in range(cursor.rowcount):
                        commentRec = Comment(commList[row][0], commList[row][1], commList[row][2],
                                             commList[row][3], commList[row][4], commList[row][5], commList[row][6], commList[row][7])
                        if r.sismember("comm_rec"+str(commentRec.comm_rec_id),oper):
                            commentRec.isApprove=True
                        else:
                            commentRec.isApprove=False
                        commL.append(commentRec)
                cursor.close()
                return json.dumps({"msg": "successfully", "code": 0, "data": commL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
            except Exception as de:
                cursor.close()
                return decodeStatus(37)
        cursor.close()
        return json.dumps({"msg": "successfully", "code": 0, "data": commL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
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
        oper = int(r.get(token))
        sql_temp = 'select commer from comm_rec where comm_rec_id=%d' % (
            comm_rec_id,)
        sql = 'delete from comm_rec where comm_rec_id=%d' % (comm_rec_id,)
        sql1 = 'select * from comm_comm where comm_rec_id=%d' % (comm_rec_id,)
        sql2 = 'delete from comm_comm where comm_rec_id=%d' % (comm_rec_id,)
        try:
            cursor.execute(sql_temp)
            commer = cursor.fetchall()
            if cursor.rowcount > 0:
                if oper == commer[0][0]:
                    cursor.execute(sql1)
                    cursor.fetchall()
                    if cursor.rowcount > 0:
                        cursor.execute(sql2)
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
    comm_rec_id_str=str(req['comm_rec_id'])
    if r.exists(token):
        try:
            oper_str=str(r.get(token))
            oper = int(oper_str)
            r.sadd("comm_rec"+comm_rec_id_str,oper_str)
            sql = 'update user set acc_point=acc_point+10 where user_id=%d' % (
                    oper,)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return json.dumps({"msg":"successfully","code":0,"data":r.scard("comm_rec"+comm_rec_id_str)},default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as e:
            app.logger.debug(str(e))
            conn.rollback()
            cursor.close()
            return decodeStatus(35)
    else:
        cursor.close()
        return decodeStatus(8)

@app.route('/removeApprRec',methods=["POST"])
def removeApprRec():
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        rec_id_str=str(req['rec_id'])
        oper_str=str(r.get(token))
        r.srem("rec"+rec_id_str,oper_str)
        return decodeStatus(0)
    else:
        return decodeStatus(8)

@app.route('/removeApprCommRec',methods=["POST"])
def removeApprCommRec():
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        comm_rec_id_str=str(req['comm_rec_id'])
        oper_str=str(r.get(token))
        r.srem("comm_rec"+comm_rec_id_str,oper_str)
        return decodeStatus(0)
    else:
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
            oper = int(r.get(token))
            sql = 'update user set acc_point=acc_point+20 where user_id=%d' % (
                oper,)
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
        oper = int(r.get(token))
        sql_temp = 'select commer from comm_comm where comm_comm_id=%d' % (
            comm_comm_id,)
        sql = 'delete from comm_comm where comm_comm_id=%d' % (comm_comm_id,)
        try:
            cursor.execute(sql_temp)
            commer = cursor.fetchall()
            if cursor.rowcount > 0:
                if oper == commer[0][0]:
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
# apply tf-idf algriothm


@app.route('/recommendRec', methods=["POST"])
def recommendRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    if r.exists(token):
        oper = int(r.get(token))
        # sql_user_lab = 'select labels_id_str from record where recorder=%d' % (
        #     oper,)
        # sql_allUser_lab = 'select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str from record '
        try:
            cursor.execute('select labels_id_str from record where recorder=%s',(oper,))
            # cursor.execute(sql_user_lab)
            user_labs =cursor.fetchall()
            totalRow = cursor.rowcount
            labs_list = []
            small_list=[]
            # get the tj
            for i in range(totalRow):
                small_list = user_labs[i][0].split(',')
                app.logger.debug(totalRow)
                colunmNum = len(small_list)
                app.logger.debug(colunmNum)
                for j in range(colunmNum):
                    labs_list.append(small_list[j])
             # dictionary [item:weight]
            totalNum = len(labs_list)
            app.logger.debug(totalNum)
            cursor.execute('select rec_id, recorder, title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str from record ')
            allUser_record = cursor.fetchall()
            allRow = cursor.rowcount
            all_list = []
            for i in range(allRow):
                little_list = allUser_record[i][10].split(',')
                colunmNum = len(small_list)
                for j in range(colunmNum):
                    all_list.append(little_list)
                    app.logger.debug(little_list)
            # tf-idf
            allNum = len(all_list)
            Dn = 0
            eachWeightDic={}
            for item in labs_list:
                if item not in eachWeightDic:
                    Dn = all_list.count(item)
                    if Dn>0:
                        eachWeightDic[item] = (labs_list.count(
                        item)/totalNum)*math.log(allNum/Dn+1)
                    else:
                         eachWeightDic[item]=0
            index=0
            w ={}
            for rec_id_array in allUser_record:
                rec_id=rec_id_array[0]
                # w = {rec_id: 0}
                w[rec_id] =0 
                little_list = allUser_record[index][10].split(',')
                index=index+1
                l_len = len(little_list)
                for item in little_list:
                    if item in labs_list:
                        w[rec_id] = w[rec_id]+eachWeightDic[item]/l_len
            sorted(w.items(), key=operator.itemgetter(1))
            recordL = []
            keys =list(w.keys())   
            for cnt in range(len(keys)):        
                for k in range(allRow):
                    if len(recordL) < 3:
                        app.logger.debug(keys)
                        if allUser_record[k][0] == keys[cnt]:
                            rec = Record(allUser_record[k][0], allUser_record[k][1], allUser_record[k][2], allUser_record[k][3], allUser_record[k][4],
                                         allUser_record[k][5], allUser_record[k][6], allUser_record[k][7], allUser_record[k][8], allUser_record[k][9], allUser_record[k][10])
                            recordL.append(rec)
                    else:
                        cursor.close()
                        return json.dumps({"code": 0, "msg": "successfully", "data": recordL},default=lambda obj: obj.__dict__, ensure_ascii=False)
            cursor.close()
            return json.dumps({"code": 0,"msg":"sucessfully" ,"data": recordL},default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(de)
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
    if r.exists(token):
        oper = int(r.get(token))
        try:
            cursor.execute('select labels_id_str from activity where publisher=%s',(oper,))
            user_labs =cursor.fetchall()
            totalRow = cursor.rowcount
            labs_list = []
            small_list=[]
            # get the tj
            for i in range(totalRow):
                small_list = user_labs[i][0].split(',')
                app.logger.debug(totalRow)
                colunmNum = len(small_list)
                app.logger.debug(colunmNum)
                for j in range(colunmNum):
                    labs_list.append(small_list[j])
             # dictionary [item:weight]
            totalNum = len(labs_list)
            app.logger.debug(totalNum)
            cursor.execute('select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src,labels_id_str from activity ')
            allUser_act = cursor.fetchall()
            allRow = cursor.rowcount
            all_list = []
            for i in range(allRow):
                little_list = allUser_act[i][9].split(',')
                colunmNum = len(small_list)
                for j in range(colunmNum):
                    all_list.append(little_list)
                    app.logger.debug(little_list)
            # tf-idf
            allNum = len(all_list)
            Dn = 0
            eachWeightDic={}
            for item in labs_list:
                if item not in eachWeightDic:
                    Dn = all_list.count(item)
                    if Dn>0:
                        eachWeightDic[item] = (labs_list.count(
                        item)/totalNum)*math.log(allNum/Dn+1)
                    else:
                         eachWeightDic[item]=0
            index=0
            w ={}
            for rec_id_array in allUser_act:
                rec_id=rec_id_array[0]
                # w = {rec_id: 0}
                w[rec_id] =0 
                little_list = allUser_act[index][9].split(',')
                index=index+1
                l_len = len(little_list)
                for item in little_list:
                    if item in labs_list:
                        w[rec_id] = w[rec_id]+eachWeightDic[item]/l_len
            sorted(w.items(), key=operator.itemgetter(1))
            recordL = []
            keys =list(w.keys())   
            for cnt in range(len(keys)):        
                for k in range(allRow):
                    if len(recordL) < 3:
                        app.logger.debug(keys)
                        if allUser_act[k][0] == keys[cnt]:
                            act = Activity(allUser_act[k][0], allUser_act[k][1], allUser_act[k][2], allUser_act[k][3], allUser_act[k][4],
                                         allUser_act[k][5], allUser_act[k][6], allUser_act[k][7], allUser_act[k][8], allUser_act[k][9])
                            recordL.append(act)
                    else:
                        cursor.close()
                        return json.dumps({"code": 0, "msg": "successfully", "data": recordL},default=lambda obj: obj.__dict__, ensure_ascii=False)
            cursor.close()
            return json.dumps({"code": 0,"msg":"sucessfully" ,"data": recordL},default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(de)
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
        sql1 = 'delete from record where recorder=%d' % (user_id,)
        sql2 = 'delete from activity where publisher=%d' % (user_id,)
        sql3 = 'delete from entry where editor=%d' % (user_id,)
        sql4 = 'delete from comm_rec where commer=%d' % (user_id,)
        sql5 = 'delete from comm_comm where commer=%d' % (user_id,)
        sql = 'delete  from user where user_id=%d ' % (user_id,)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql3)
            cursor.execute(sql4)
            cursor.execute(sql5)
            cursor.execute(sql)
            conn.commit()
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


@app.route('/bigMap', methods=["POST"])
def BigMap():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req["token"]
    if r.exists(token):
        sql = 'select addr,rec_id from record'
        try:
            cursor.execute(sql)
            addr_rec = cursor.fetchall()
            cursor.close()
            return json.dumps({"code": 0, "msg": "sucessfully", "data": addr_rec})
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(47)
    else:
        cursor.close()
        return decodeStatus(8)


@app.route('/smallMap', methods=["POST"])
def SmallMap():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req["token"]
    if r.exists(token):
        user_id = int(r.get(token))
        sql = 'select addr,rec_id from record where recorder=%d' % (user_id,)
        try:
            cursor.execute(sql)
            addr_rec = cursor.fetchall()
            cursor.close()
            return json.dumps({"code": 0, "msg": "sucessfully", "data": addr_rec})
        except Exception as e:
            app.logger.debug(str(e))
            cursor.close()
            return decodeStatus(47)
    else:
        cursor.close()
        return decodeStatus(8)

@app.route('/getEntryRec',methods=["POST"])
def getEntryRec():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    entry_id = str(req['entry_id'])
    if r.exists(token):
        try:
            cursor.execute('select rec_id, recorder,title, url, type, addr, appr_num, comm_num, issue_date, discribe,labels_id_str  from record where labels_id_str like %s' ,('%'+str(entry_id)+'%',))
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

@app.route('/getEntryAct',methods=["POST"])
def getEntryAct():
    cursor = conn.cursor()
    req = request.get_json(force=True)
    token = req['token']
    entry_id = str(req['entry_id'])
    if r.exists(token):
        try:
            cursor.execute('select act_id,publisher,title,content,hold_date,hold_addr,act_src,issue_date,image_src,labels_id_str from activity where labels_id_str like %s' ,('%'+str(entry_id)+'%',))
            act = cursor.fetchall()
            actL = []
            if cursor.rowcount > 0:
                for row in range(cursor.rowcount):
                    activity = Activity(act[0][0],
                                act[0][1], act[0][2], act[0][3], act[0][4], act[0][5], act[0][6], act[0][7], act[0][8], act[0][9])
                    actL.append(activity)
                    app.logger.debug(actL)
            cursor.close()
            return json.dumps({"msg": "successfully", "code": 0, "data": actL}, default=lambda obj: obj.__dict__, ensure_ascii=False)
        except Exception as de:
            app.logger.debug(str(de))
            cursor.close()
            return decodeStatus(28)
    else:
        cursor.close()
        return decodeStatus(8)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
