# 导入Flask类,pymsql操作方法
from flask import Flask,render_template,request
import func_sql

# Flask函数接收一个参数__name__，它会指向程序所在的包
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
activity_ed={}
activity_ing={}
len_activity_ing=0
len_activity_ed=0
#网页文件keeper_login所用的信息包
keeper_login_msg = {
    'login_msg': ""
}
#网页文件keeper_manage所用的信息包
keeper_manage_msg = {
    'PID': 0,
    'Password': '',
    'Phone': '',
    'Name': ''
}
#网页文件register所用的信息包
register_msg = {
    'msg_tel': "",
    'msg_pwd': ""
}
#网页user_manage
user_manage_msg={

}
user_will = {}
user_ing = {}
user_ed = {}
len_user_will=0
len_user_ing=0
len_user_ed=0
def user_fresh():
    global user_will
    global user_ing
    global user_ed
    global len_user_will
    global len_user_ing
    global len_user_ed
    len_user_will, user_will = func_sql.user_will(user_manage_msg['UID'])
    len_user_ing, user_ing = func_sql.user_ing(user_manage_msg['UID'])
    len_user_ed, user_ed = func_sql.user_ed(user_manage_msg['UID'])
def keeper_fresh():
    global activity_ing
    global activity_ed
    global len_activity_ing
    global len_activity_ed
    global keeper_manage_msg
    len_activity_ing, activity_ing = func_sql.activity_ing(keeper_manage_msg['PID'])
    len_activity_ed, activity_ed = func_sql.activity_ed(keeper_manage_msg['PID'])
# 装饰器的作用是将路由映射到视图函数 index
@app.route('/',methods=['GET','POST'])
def all_login():
    if request.method == 'GET':
        return render_template('login.html', login_msg = keeper_login_msg['login_msg'])
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    row, res = func_sql.login(user, pwd)
    if row:
        keeper_login_msg['login_msg'] = ""
        if len(res)>5:
            global user_manage_msg
            user_manage_msg = res
            user_fresh()
            return render_template('user_manage.html',
                                   user_manage_msg=user_manage_msg,
                                   user_will=user_will,
                                   user_ing=user_ing,
                                   user_ed=user_ed,
                                   len_user_will=len_user_will,
                                   len_user_ing=len_user_ing,
                                   len_user_ed=len_user_ed)
        else:
            global keeper_manage_msg
            keeper_manage_msg= res
            keeper_fresh()
            return render_template('keeper_manage.html',
                                   len_activity_ing=len_activity_ing,
                                   len_activity_ed = len_activity_ed,
                                   activity_ed=activity_ed,
                                   activity_ing=activity_ing,
                                   keeper_manage_msg = keeper_manage_msg)
    else:
        keeper_login_msg['login_msg'] = "账号或密码错误"
        return render_template('login.html', login_msg=keeper_login_msg['login_msg'])
@app.route('/aftlog')
def logined():
    return render_template('keeper_manage.html', keeper_manage_msg=keeper_manage_msg)
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', msg_tel=register_msg['msg_tel'], msg_pwd=register_msg['msg_pwd'])
    tel = request.form.get('tel')
    name = request.form.get('name')
    address = request.form.get('address')
    sex = request.form.get('sex')
    pwd = request.form.get('pwd')
    pwd_con = request.form.get('pwd_con')
    if len(tel) != 11:
        register_msg['msg_tel'] = "手机号长度应为11位"
    else:
        register_msg['msg_tel'] = ""
    if pwd != pwd_con:
        register_msg['msg_pwd'] = "密码不一致"
    else:
        register_msg['msg_pwd'] = ""
    if register_msg['msg_pwd'] != "" or register_msg['msg_tel'] != "":
        return render_template('register.html', msg_tel=register_msg['msg_tel'], msg_pwd=register_msg['msg_pwd'])
    res = func_sql.user_register(tel, name, address, sex, pwd)
    if res:
        register_msg['msg_tel'] = "手机号已注册"
        return render_template('register.html', msg_tel=register_msg['msg_tel'], msg_pwd=register_msg['msg_pwd'])
    else:
        return '注册成功了！<a href="/">登录</a>'
@app.route('/keeper_fix/<int:PID>',methods=['GET','POST'])
def keeper_fix(PID):
    global keeper_manage_msg
    if request.method == 'GET':
        return render_template('keeper_fix.html',keeper_manage_msg = keeper_manage_msg)
    tel = request.form.get('tel')
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    func_sql.keeper_fix(PID,tel,name,pwd)
    keeper_manage_msg = {
        'PID': PID,
        'Password': pwd,
        'Phone': tel,
        'Name': name
    }
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/activity_create',methods=['GET','POST'])
def activity_create():
    global keeper_manage_msg
    if request.method == 'GET':
        return render_template('activity_create.html',keeper_manage_msg = keeper_manage_msg)
    pid = request.form.get('pid')
    name = request.form.get('name')
    date = request.form.get('date')
    contents = request.form.get('contents')
    func_sql.activity_create(pid, name, date, contents)
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/activity_delete/<int:AID>')
def activity_delete(AID):
    func_sql.activity_delete(AID)
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/activity_end/<int:AID>')
def activity_end(AID):
    func_sql.activity_end(AID)
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/activity_fix/<int:AID>',methods=['GET','POST'])
def activity_fix(AID):
    activity_info = func_sql.activity_info(AID)
    if request.method == 'GET':
        return render_template('activity_fix.html', activity_info=activity_info)
    name = request.form.get('name')
    date = request.form.get('date')
    contents = request.form.get('contents')
    func_sql.activity_fix(AID, name, date, contents)
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/activity_chcek/<int:AID>')
def activity_kcheck(AID):
    userpack = func_sql.activity_kcheck(AID)
    len_userpack = len(userpack)
    activitypack=func_sql.activity_info(AID)
    return render_template('keeper_check.html',
                           AID=AID,
                           len_userpack=len_userpack,
                           userpack=userpack,
                           activitypack=activitypack,
                           keeper_manage_msg=keeper_manage_msg
                           )
@app.route('/check_detail',methods=['GET'])
def check_detail():
    AID=request.args.get('AID')
    UID=request.args.get('UID')
    userpack = func_sql.activity_kcheck(AID)
    activitypack = func_sql.activity_info(AID)
    len_userpack = len(userpack)
    user_info=func_sql.user_info(UID)
    joins_info=func_sql.joins_info(AID,UID)
    return render_template('check_detail.html',
                           activitypack=activitypack,
                           user_info=user_info,
                           joins_info=joins_info,
                           len_userpack=len_userpack,
                           userpack=userpack,
                           keeper_manage_msg=keeper_manage_msg
                           )
@app.route('/join_create',methods=['GET','POST'])
def join_create():
    AID = request.args.get('AID')
    UID = request.args.get('UID')
    if request.method == 'GET':
        return render_template('join_create.html',
                               user_manage_msg=user_manage_msg,
                               user_will=user_will,
                               user_ing=user_ing,
                               user_ed=user_ed,
                               len_user_will=len_user_will,
                               len_user_ing=len_user_ing,
                               len_user_ed=len_user_ed)
    Des = request.form.get('Des')
    func_sql.join_create(AID,UID,Des)
    user_fresh()
    return render_template('user_manage.html',
                           user_manage_msg=user_manage_msg,
                           user_will=user_will,
                           user_ing=user_ing,
                           user_ed=user_ed,
                           len_user_will=len_user_will,
                           len_user_ing=len_user_ing,
                           len_user_ed=len_user_ed)
@app.route('/join_cancel',methods=['GET'])
def join_cancel():
    AID=request.args.get('AID')
    UID=request.args.get('UID')
    func_sql.join_cancel(AID,UID)
    userpack = func_sql.activity_kcheck(AID)
    len_userpack = len(userpack)
    activitypack = func_sql.activity_info(AID)
    return render_template('keeper_check.html',
                           activitypack=activitypack,
                           len_userpack=len_userpack,
                           userpack=userpack,
                           keeper_manage_msg=keeper_manage_msg
                           )
@app.route('/cancel_join',methods=['GET'])
def cancel_join():
    AID=request.args.get('AID')
    UID=request.args.get('UID')
    func_sql.join_cancel(AID,UID)
    user_fresh()
    return render_template('user_manage.html',
                           user_manage_msg=user_manage_msg,
                           user_will=user_will,
                           user_ing=user_ing,
                           user_ed=user_ed,
                           len_user_will=len_user_will,
                           len_user_ing=len_user_ing,
                           len_user_ed=len_user_ed)
@app.route('/index')
def index():
    keeper_fresh()
    return render_template('keeper_manage.html',
                           len_activity_ing=len_activity_ing,
                           len_activity_ed=len_activity_ed,
                           activity_ed=activity_ed,
                           activity_ing=activity_ing,
                           keeper_manage_msg=keeper_manage_msg)
@app.route('/user_fix/<int:UID>',methods=['GET','POST'])
def user_fix(UID):
    global user_manage_msg
    if request.method == 'GET':
        return render_template('user_fix.html',
                               user_manage_msg = user_manage_msg)
    tel = request.form.get('tel')
    name = request.form.get('name')
    sex = request.form.get('sex')
    address = request.form.get('address')
    pwd = request.form.get('pwd')
    func_sql.user_fix(UID,name,sex,tel,address,pwd)
    user_manage_msg = {
        'UID': UID,
        'Sex': sex,
        'Address':address,
        'Password': pwd,
        'Phone': tel,
        'Name': name
    }
    keeper_fresh()
    return render_template('user_manage.html',
                           user_manage_msg=user_manage_msg,
                           user_will=user_will,
                           user_ing=user_ing,
                           user_ed=user_ed,
                           len_user_will=len_user_will,
                           len_user_ing=len_user_ing,
                           len_user_ed=len_user_ed)
def motai():
    return render_template('/temp/login.html')
if __name__ == '__main__':
    app.run()     
    # 可以指定运行的主机IP地址，端口，是否开启调试模式
    #app.run(host="0.0.0.0", port=5000)

