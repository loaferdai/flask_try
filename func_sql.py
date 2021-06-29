import pymysql

db = pymysql.connect(host="localhost",
                     port=3306,
                     user="root",
                     password="root",
                     db="vltt",
                     charset="utf8"
                     )
cursor = db.cursor(pymysql.cursors.DictCursor)
#管理员登录
def keeper_login(user,pwd):
    sql = 'select * from keeper where Phone=%s and password=%s'
    row = cursor.execute(sql,(user,pwd))
    res = cursor.fetchone()
    return(row,res)
#用户登录
def login(user,pwd):
    sql = 'select * from user where Phone=%s and password=%s'
    row = cursor.execute(sql,(user,pwd))    #返回记录数
    res = cursor.fetchone()                 #返回数据
    if row==0:
        sql = 'select * from keeper where Phone=%s and password=%s'
        row = cursor.execute(sql, (user, pwd))
        res = cursor.fetchone()
    return(row,res)
#用户注册
def user_register(tel, name, address, sex, pwd):
    sql = 'select * from user where Phone=%s'
    res1 = cursor.execute(sql, (tel))
    sql = 'select * from keeper where Phone=%s'
    res2 = cursor.execute(sql, (tel))
    if res1 or res2:
        return 1
    else:
        sql = 'select * from user'
        cursor.execute(sql)
        row = cursor.fetchall()
        res = row[-1]['UID'] + 1
        print(type(res))
        sql='insert into user values(%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (res, pwd, name, address, sex, tel))
        print("register")
        db.commit()
        return 0
#添加活动
def activity_create(pid,name,date,contents):
    sql = 'select * from activity'
    cursor.execute(sql)
    row = cursor.fetchall()
    res = row[-1]['AID'] + 1
    sql = 'insert into activity values(%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (res, pid, name, date, contents, '0'))
    print("created")
    db.commit()
    return 0
#管理员信息修改
def keeper_fix(PID,tel,name,pwd):
    sql='update keeper set password=%s,phone=%s,name=%s where pid=%s'
    cursor.execute(sql, (pwd,tel,name, PID))
    db.commit()
    print('fixed')
def activity_ing(PID):
    sql='select * from activity where PID=%s and status=0'
    row = cursor.execute(sql,(PID))
    res = cursor.fetchall()
    return row,res
def activity_ed(PID):
    sql='select * from activity where PID=%s and status=1'
    row = cursor.execute(sql,(PID))
    res = cursor.fetchall()
    return row,res
def activity_delete(AID):
    sql='delete from activity where AID=%s'
    cursor.execute(sql,(AID))
    db.commit()
def activity_end(AID):
    sql='update activity set status=1 where AID=%s'
    cursor.execute(sql,(AID))
    db.commit()
def activity_info(AID):
    sql = 'select * from activity where AID=%s'
    cursor.execute(sql,(AID))
    res=cursor.fetchone()
    return res
def activity_fix(AID,name, date, content):
    sql = 'update activity set date=%s,content=%s,name=%s where AID=%s'
    cursor.execute(sql, (date, content, name, AID))
    db.commit()
def activity_kcheck(AID):
    sql = 'select * from user where uid in (select uid from joins where AID=%s)'
    cursor.execute(sql,(AID))
    res=cursor.fetchall()
    return res
def joins_info(AID,UID):
    sql = 'select * from joins where AID=%s and UID=%s'
    cursor.execute(sql,(AID,UID))
    res=cursor.fetchone()
    return res
def user_info(UID):
    sql = 'select * from user where UID=%s'
    cursor.execute(sql,(UID))
    res=cursor.fetchone()
    return res
def user_fix(UID,name,sex,phone,address,pwd):
    sql = 'update user set name=%s,sex=%s,phone=%s,address=%s,password=%s where UID=%s'
    cursor.execute(sql, (name,sex,phone,address,pwd,UID))
    db.commit()
def user_will(UID):
    sql = 'select * from activity where aid not in(select aid from joins where uid=%s) and status=0'
    row = cursor.execute(sql,(UID))
    res = cursor.fetchall()
    return row,res
def user_ing(UID):
    sql = 'select * from activity where aid in(select aid from joins where uid=%s) and status=0'
    row = cursor.execute(sql, (UID))
    res = cursor.fetchall()
    return row,res
def user_ed(UID):
    sql = 'select * from activity where aid in(select aid from joins where uid=%s) and status=1'
    row = cursor.execute(sql,(UID))
    res = cursor.fetchall()
    return row,res
#取消加入
def join_cancel(AID,UID):
    sql = 'delete from joins where AID=%s and UID=%s'
    cursor.execute(sql, (AID,UID))
    db.commit()
#加入活动
def join_create(AID,UID,Des):
    sql = 'insert into joins values(%s,%s,%s)'
    cursor.execute(sql, (UID,Des,AID))
    db.commit()
# 关闭数据库连接
#db.close()
