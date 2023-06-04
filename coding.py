from flask import *
from src.dbconnectionnew import *
import socket
import select
import time
import sys
import json
import pymysql
import urllib.parse
import requests
from src.cnn import *
from src.phishing import *
# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
iplist=[]
url= "http://192.168.18.152:5001/"
from flask import *
app=Flask(__name__)
app.secret_key="abc"

conn = pymysql.connect(host='localhost', user='root', passwd='', db='dos detection and loan prediction', port=3306)
cmd=conn.cursor()

app=Flask (__name__)

app.secret_key='123'


import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return redirect('/')
        return func()

    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def log():
    global iplist
    res=selectall("SELECT `ip` FROM `blacklist`")
    for i in res:
        iplist.append(i['ip'])
    return  render_template('login_index.html')

@app.route('/login_code',methods=['post'])
def login_code():
    uname=request.form['textfield']
    password=request.form['textfield2']

    in_values = {'uname': uname, 'password': password}


    global iplist

    ip_address = request.remote_addr
    print (ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()
        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res=selectall2(qry,str(ip_address))
        if len(res)==8:
            row=[]
            row.append(int(res[0]['m'])*60+int(res[0]['s']))
            row.append(int(res[1]['m'])*60+int(res[1]['s']))
            row.append(int(res[2]['m'])*60+int(res[2]['s']))
            row.append(int(res[3]['m'])*60+int(res[3]['s']))
            row.append(int(res[4]['m'])*60+int(res[4]['s']))
            row.append(int(res[5]['m'])*60+int(res[5]['s']))
            row.append(int(res[6]['m'])*60+int(res[6]['s']))
            row.append(int(res[7]['m'])*60+int(res[7]['s']))
            print(row)
            print(row)
            print(row)
            print(row)
            res=predict([row])
            print(res,"result+++++++++++++++++++")
            print(res,"result+++++++++++++++++++")
            print(res,"result+++++++++++++++++++")
            print(res,"result+++++++++++++++++++")
            if res==1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))



        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        print(qry)
        print(res,"++++++++++++++++++++++++++")
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        res = requests.post(url+"login_code", data=in_values)
        res = res.text.split("#")

        if len(res) == 1:
            return '''<script>alert("INVALID USER_NAME OR PASSWORD");window.location="/"</script>'''

        elif res[0] == "admin":
            session['lid'] = res[1]
            # return '''<script>alert("WELCOME ADMIN");window.location="/admin_home"</script>'''
            return redirect('/admin_home')

        elif res[0] == "branch":
            session['lid'] = res[1]
            # return '''<script>alert("WELCOME Branch");window.location="/bank_home"</script>'''
            return redirect('/bank_home')

        elif res[0] == "user":
            session['lid'] = res[1]
            # return '''<script>alert("WELCOME user");window.location="/user_home"</script>'''
            return redirect('/user_home')
        else:
            return '''<script>alert("INVALID USER_NAME OR PASSWORD");window.location="/"</script>'''
    else:
        return ""

@app.route('/admin_home')
@login_required
def admin_home():
    return  render_template('admin_home.html')

@app.route('/add_manage_branch')
@login_required
def add_manage_branch():
    qry = "select * from branch"
    res = selectall(qry)
    return render_template('add_manage_branch.html',val=res)







@app.route('/add_user1')
@login_required
def add_braadd_user1nch1():
    qry="select * from branch"
    res=selectall(qry)
    return render_template('auser_reg_index.html',val=res)

@app.route('/add_user', methods=['post'])
@login_required
def add_user():
    branch_name = request.form['select']
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    user_name = request.form['textfield8']
    password = request.form['textfield92']
    C_password = request.form['textfield9']

    if (password!=C_password):
        return '''<script>alert("Password missmatch");window.location="/"</script>'''
    else:
        qry = "insert into login values(NULL,%s,%s,'user')"
        id = iud(qry, (user_name, password,))
        qry = "insert into user values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        iud(qry,(id, branch_name, f_name,l_name,gender, place, post, pin, phone_no, mail_id))
        return '''<script>alert("ADDED SUCCESSFULLY");window.location="/admin_viewuser#about"</script>'''


@app.route('/add_branch1')
@login_required
def add_branch1():
    return render_template('branch_reg_index.html')

@app.route('/add_branch', methods=['post'])
@login_required
def add_branch():
    branch_name=request.form['textfield']
    place=request.form['textfield3']
    post=request.form['textfield4']
    pin=request.form['textfield5']
    phone_no=request.form['textfield6']
    mail_id=request.form['textfield7']
    user_name=request.form['textfield8']
    password=request.form['textfield9']


    qry = "insert into login values(NULL,%s,%s,'branch')"
    id=iud(qry,(user_name,password))
    qry="insert into branch values(null,%s,%s,%s,%s,%s,%s,%s)"
    iud(qry,(id,branch_name,place,post,pin,phone_no,mail_id))
    return '''<script>alert("ADDED SUCCESSFULLY");window.location="/add_manage_branch#about"</script>'''

@app.route('/admin_edit_branch')
@login_required
def admin_edit_branch():
    id = request.args.get('id')
    session['lid'] = id
    qry = "SELECT * FROM `branch` WHERE `branch_id`=%s"
    res=selectone(qry,id)
    return  render_template('branch_edit_index.html',val=res)



@app.route('/phishing')
@login_required
def phishing():

    return  render_template('phishing.html')

@app.route('/phishing1',methods=['post'])
@login_required
def phishing1():
    url=request.form['textfield3']
    res=getResult(url)
    print(res)
    return "<script>alert('"+res[0]+"');window.location='/phishing'</script>"





@app.route('/update_branch1', methods=['post'])
@login_required
def update_branch1():

    branch_name = request.form['textfield']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    qry = "update branch set branch_name=%s,place=%s,post=%s,pin=%s,phone_no=%s,mail_id=%s where login_id=%s"
    val=(branch_name, place, post, pin_code, phone_no, mail_id,session['lid'])
    iud(qry,val)
    return '''<script>alert("edited");window.location="/add_manage_branch#about"</script>'''



@app.route('/delete_branch')
@login_required
def delete_branch():
    id=request.args.get('id')
    qry1="DELETE FROM login WHERE id=%s"
    iud(qry1, id)
    qry2="DELETE FROM `branch` WHERE login_id=%s"
    iud(qry2,id)
    return '''<script>alert("deleted");window.location="/add_manage_branch#about"</script>'''


@app.route('/branch_changepw')
@login_required
def branch_changepw():

    return render_template("bank_change_password.html")

@app.route('/branch_changepw1',methods=['post'])
@login_required
def branch_changepw1():
    olpass = request.form['textfield']
    nwpassword = request.form['textfield2']
    confirmpass = request.form['textfield3']
    qry="SELECT `password` FROM `login` WHERE `id`=%s "
    res=selectone(qry,session['lid'])
    if(olpass==res['password']):
        if(nwpassword==confirmpass):
            q="UPDATE `login` SET `password`=%s WHERE `id`=%s"
            iud(q,(nwpassword,session['lid']))
            return '''<script>alert("Password  changed");window.location="/bank_home"</script>'''

        else:
            return '''<script>alert("Password doesnt match");window.location="/branch_changepw#about"</script>'''

    else:
        return '''<script>alert("old password is incorrect");window.location="/branch_changepw#about"</script>'''

@app.route('/branch_complaint')
@login_required
def branch_complaint():
    # qry = "SELECT `complaint`.*,`user`.`f_name`,`l_name` FROM `complaint` JOIN `user` ON `user`.`login_id`=`complaint`.`user_id` ORDER BY `date`.`time` DESC"
    # qry="SELECT * FROM `complaint` WHERE `user_id` IN (SELECT  `login_id` FROM `user` WHERE `branch_id`=%s) ORDER BY `date` DESC"
    qry = "SELECT `complaint`.*,`user`.`f_name`,`l_name` FROM `complaint` JOIN `user` ON `user`.`login_id`=`complaint`.`user_id` WHERE `complaint`.`user_id` IN (SELECT  `login_id` FROM `user` WHERE `branch_id`=%s) ORDER BY `complaint`.`date` DESC"
    res = selectall2(qry,session['lid'])
    return render_template('bank_complaint.html', val=res)




@app.route('/branch_reply1')
@login_required
def branch_reply1():
    id=request.args.get('id')
    session['cid']=id
    return  render_template('bank_reply.html')


@app.route('/branch_reply',methods=['post'])
@login_required
def branch_reply():
    reply = request.form['textarea']
    qry ="UPDATE `complaint` SET reply=%s WHERE complaint_id=%s"
    val = (reply,session['cid'])
    iud(qry, val)
    return '''<script>alert("REPLY SENT");window.location="/branch_complaint#about"</script>'''

@app.route('/bank_view_noti')
@login_required
def bank_view_noti():
    qry = "select * from notification order by date desc "
    res = selectall(qry)
    return render_template('bank_notification.html',val=res)


@app.route('/admin_complaint')
@login_required
def admin_complaint():
    qry = "SELECT `complaint`.*,`user`.`f_name`,`l_name` FROM `complaint` JOIN `user` ON `user`.`login_id`=`complaint`.`user_id` WHERE `complaint`.`reply`='pending'"
    res = selectall(qry)
    return render_template('admin_complaint.html', val=res)




@app.route('/admin_reply1')
@login_required
def admin_reply1():
    id=request.args.get('id')
    session['cid']=id
    return  render_template('admin_reply.html')


@app.route('/admin_reply',methods=['post'])
@login_required
def admin_reply():
    reply = request.form['textarea']
    qry ="UPDATE `complaint` SET reply=%s WHERE complaint_id=%s"
    val = (reply,session['cid'])
    iud(qry, val)
    return '''<script>alert("REPLY SENT");window.location="/admin_complaint#about"</script>'''









@app.route('/admin_viewuser')
@login_required
def admin_viewuser():
    qry="SELECT * FROM `user`"
    res=selectall(qry)
    return  render_template('admin_viewuser.html',val=res)



@app.route('/admin_notification1',methods=['post'])
@login_required
def admin_notification1():
    message = request.form['textarea']
    qry="insert into notification values(null,curdate(),curtime(),%s)"
    val=message
    iud(qry,val)
    return '''<script>alert("NOTIFICATION SENT");window.location="/admin_home"</script>'''


@app.route('/admin_notification')
@login_required
def admin_notification():
    return render_template('admin_notification.html')






@app.route('/bank_home')
@login_required
def bank_home():
    return  render_template('bank_home.html')

@app.route('/bank_update_branch',methods=['post'])
@login_required
def bank_update_branch():
    branch_name = request.form['textfield']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    qry = "update branch set branch_name=%s,place=%s,post=%s,pin=%s,phone_no=%s,mail_id=%s where login_id=%s"
    val = (branch_name, place, post, pin_code, phone_no, mail_id, session['lid'])
    iud(qry, val)
    return '''<script>alert("edited");window.location="/bank_home"</script>'''



@app.route('/bank_viewbank')
@login_required
def bank_viewbank():
    qry=" select * from branch where login_id=%s"
    res = selectone(qry, session['lid'])
    return render_template('bbranch_edit_index.html', val=res)




@app.route('/edit_branch')
@login_required
def edit_branch():
    id = request.args.get('id')
    session['lid'] = id
    qry = "SELECT * FROM `branch` WHERE `login_id`=%s"
    res=selectone(qry,id)
    print(res)
    return  render_template('bank_viewbank.html',val=res)


@app.route('/update_branch', methods=['post'])
@login_required
def update_branch():
    branch_name = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    qry = "update branch set branch_name=%s,place=%s,post=%s,pin=%s,phone_no=%s,mail_id=%s where login_id=%s"
    val=(branch_name, place, post, pin_code, phone_no, mail_id,session['lid'])
    iud(qry,val)

    return '''<script>alert("edited");window.location="/bank_viewbank#about"</script>'''




@app.route('/bank_viewuser')
@login_required
def bank_viewuser():
    qry = "SELECT * FROM `user` where branch_id=%s"
    res = selectall2(qry,session['lid'])
    return render_template('bank_viewuser.html', val=res)


@app.route('/bank_edit_user')
@login_required
def bank_edit_user():
    id=request.args.get('id')
    session['uid']=id
    qry="select * from user where use_id=%s"
    res=selectone(qry,id)
    return render_template("user_edit_index.html",val=res)



@app.route('/bank_update_user', methods=['post'])
@login_required
def bank_update_user():
    print(request.form)
    print(session['uid'],"===============================================")
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']

    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    qry = "update user set f_name=%s,l_name=%s,gender=%s,place=%s,post=%s,pin_code=%s,phone_no=%s,email=%s where use_id=%s"
    val=(f_name,l_name,gender, place, post, pin_code, phone_no, mail_id,session['uid'])
    iud(qry,val)

    return '''<script>alert("updated");window.location="/bank_viewuser#about"</script>'''




@app.route('/bank_add_user', methods=['post'])
@login_required
def bank_add_user():
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    user_name = request.form['textfield8']
    password = request.form['textfield92']
    C_password = request.form['textfield9']

    if (password!=C_password):
        return '''<script>alert("Password missmatch");window.location="/bank_home"</script>'''
    else:
        qry = "insert into login values(NULL,%s,%s,'user')"
        id = iud(qry, (user_name, password,))
        qry = "insert into user values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        iud(qry, (id,session['lid'],f_name,l_name,gender, place, post, pin, phone_no, mail_id))
        return '''<script>alert("ADDED SUCCESSFULLY");window.location="/bank_home"</script>'''

@app.route('/bank_add_user1')
@login_required
def bank_add_user1():
    return render_template('bank_adduser.html')






@app.route('/deposit_withdraw',methods=['get','post'])
@login_required
def deposit_withdraw():
    if request.method=="POST":
        sr = request.form['search']
        res = selectall2("SELECT * FROM `user` WHERE `branch_id`=%s AND `use_id`=%s",(session['lid'],sr))
        return render_template('deposit_withdraw.html', val=res)
    else:
        res = selectall2("SELECT * FROM `user` WHERE `branch_id`=%s",session['lid'])
        return  render_template('deposit_withdraw.html',val=res)

@app.route('/deposit_amount',methods=['get','post'])
@login_required
def deposit_amount():
    id = request.args.get('id')
    if request.method == "POST":
        amt = request.form['textfield']
        iud("INSERT INTO `transaction` VALUES(NULL,%s,CURDATE(),CURTIME(),'deposit',%s)", (id, amt))
        return '''<script>alert("Deposited");window.location="/deposit_withdraw#about"</script>'''
    else:
        return render_template('deposit_amount.html')


@app.route('/withdraw_amount',methods=['get','post'])
@login_required
def withdraw_amount():
    id = request.args.get('id')

    if request.method=="POST":
        amt = request.form['textfield']
        iud("INSERT INTO `transaction` VALUES(NULL,%s,CURDATE(),CURTIME(),'withdraw',%s)",(id,amt))
        return '''<script>alert("Withdrawed");window.location="/deposit_withdraw#about"</script>'''

    return  render_template('withdraw_amount.html')




@app.route('/bank_view_balance')
@login_required
def bank_view_balance():
    id = request.args.get('id')
    res = selectall2("SELECT * FROM `transaction` WHERE `user_id`=%s",id)
    res1 = selectone(" SELECT (SELECT SUM(`balance`) FROM `transaction` WHERE `user_id`=%s AND `type`='deposit') - (SELECT SUM(`balance`) FROM `transaction` WHERE `user_id`=%s AND `type`='withdraw')AS total_balance",(id,id))
    return  render_template('bank_view_balance.html',val = res,bal = res1)


@app.route('/select_user')
@login_required
def select_user():
    return  render_template('select_user.html')

@app.route('/signup1')
def signup1():
    q="SELECT * FROM `branch` "
    res=selectall(q)
    return render_template('uuser_reg_index.html',val=res)




@app.route('/signup', methods=['post'])
def signup():
    branch_name = request.form['select']
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    user_name = request.form['textfield8']
    password = request.form['textfield92']
    C_password = request.form['textfield9']

    if (password!=C_password):
        return '''<script>alert("Password missmatch");window.location="/"</script>'''
    else:
        qry = "insert into login values(NULL,%s,%s,'user')"
        id = iud(qry, (user_name, password,))
        qry = "insert into user values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        iud(qry, (id, branch_name, f_name,l_name,gender, place, post, pin, phone_no, mail_id))
        return '''<script>alert("REGISTERED SUCCESSFULLY");window.location="/"</script>'''


@app.route('/user_view_noti')
@login_required
def user_view_noti():
    # in_values = {'lid': session['lid']}

    global iplist

    ip_address = request.remote_addr
    print(ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))


        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        res = requests.post(url + "user_view_noti")
        print(res.text, type(res.text))
        return res.text
    else:
        return ""

        # qry = "select * from notification "
    # res = selectall(qry)
    # return render_template('user_notification.html',val=res)


@app.route('/user_home')
@login_required
def user_home():
    return  render_template('user_home.html')

@app.route('/user_viewuser')
@login_required
def user_viewuser():
    # print(session['lid'])

    # in_values = {'lid': session['lid']}


    global iplist

    ip_address = request.remote_addr
    print (ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        in_values = {'lid': session['lid']}
        res = requests.post(url+"user_viewuser", data=in_values)
        print(res.text,type(res.text))
        # res=dict()
        result = json.loads(res.text)
        print(result)
        print(type(result))
        return render_template('uuser_edit_index.html', val=result)
    else:
        return ""



    qry="SELECT  user.* FROM `user` WHERE `user`.login_id=%s"
    res = selectone(qry, session['lid'])
    return render_template('uuser_edit_index.html', val=res)

@app.route('/user_user_update', methods=['post'])
@login_required
def user_user_update():
    print(request.form)
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']

    qry = "update user set f_name=%s,l_name=%s,gender=%s,place=%s,post=%s,pin_code=%s,phone_no=%s,email=%s where login_id=%s"
    val=(f_name,l_name,gender, place, post, pin_code, phone_no, mail_id,session['lid'])
    iud(qry,val)
    return '''<script>alert("updated");window.location="/user_home"</script>'''




@app.route('/user_update1', methods=['post'])
@login_required
def user_update1():
    print(request.form)
    print(session['uid'])
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']

    # in_values = {'f_name': f_name, 'l_name': l_name, 'gender': gender, "place": place,"post":post,"pin_code":pin_code,"phone_no":phone_no,"mail_id":mail_id}
    #
    # global iplist
    #
    # ip_address = request.remote_addr
    # print(ip_address)
    # if ip_address not in iplist:
    #     cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
    #     conn.commit()
    #
    #     qry = "select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
    #     res = selectall2(qry, ip_address)
    #     if len(res) == 8:
    #         row = []
    #         row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
    #         row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
    #         row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
    #         row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
    #         row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
    #         row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
    #         row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
    #         row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
    #         res = predict([row])
    #         if res == 1:
    #             cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
    #             conn.commit()
    #
    #             iplist.append(str(ip_address))
    #
    #     qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
    #     qry += str(ip_address) + "'"
    #     cmd.execute(qry)
    #     res = cmd.fetchone()
    #     if (res[0] > 10):
    #         cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
    #         conn.commit()
    #
    #         iplist.append(str(ip_address))
    #     res = requests.post(url + "user_update1", in_values)
    #
    #     print(res.text, type(res.text))
    #     if res.text == "ok":
    #             return '''<script>alert("updated");window.location="/bank_viewuser#about"</script>'''
    #
    #
    #
    # else:
    #     return ""

    qry = "update user set f_name=%s,l_name=%s,gender=%s,place=%s,post=%s,pin_code=%s,phone_no=%s,email=%s where use_id=%s"
    val=(f_name,l_name,gender, place, post, pin_code, phone_no, mail_id,session['uid'])
    iud(qry,val)

    return '''<script>alert("updated");window.location="/bank_viewuser#about"</script>'''

    #

@app.route('/user_update', methods=['post'])
@login_required
def user_update():
    print(request.form)
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']

    qry = "update user set f_name=%s,l_name=%s,gender=%s,place=%s,post=%s,pin_code=%s,phone_no=%s,email=%s where login_id=%s"
    val=(f_name,l_name,gender, place, post, pin_code, phone_no, mail_id,session['lid'])
    iud(qry,val)

    return '''<script>alert("updated");window.location="/user_home"</script>'''

@app.route('/user_chngepw')
@login_required
def user_chngepw():
    global iplist

    ip_address = request.remote_addr
    print(ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        in_values = {'lid': session['lid']}
        return render_template("user_change_password.html")

    else:
        return ""

@app.route('/user_chngepw1',methods=['post'])
@login_required
def user_chngepw1():
    olpass = request.form['textfield']
    print(olpass)
    nwpassword = request.form['textfield2']
    confirmpass = request.form['textfield3']

    in_values = {'olpass': olpass, 'nwpassword': nwpassword,'confirmpass':confirmpass,"lid":session['lid']}

    global iplist

    ip_address = request.remote_addr
    print(ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        res = requests.post(url + "user_chngepw1",in_values)

        print(res.text, type(res.text))
        if res.text == "ok":
            return '''<script>alert("Password  changed");window.location="/user_home"</script>'''
        elif res.text == "na":
            return '''<script>alert("Password doesnt match");window.location="/user_chngepw#about"</script>'''

        else:
            return '''<script>alert("old password is incorrect");window.location="/user_chngepw#about"</script>'''


    else:
        return ""


    # qry="SELECT `password` FROM `login` WHERE `id`=%s "
    # res=selectone(qry,session['lid'])
    # if(olpass==res['password']):
    #     if(nwpassword==confirmpass):
    #         q="UPDATE `login` SET `password`=%s WHERE `id`=%s"
    #         iud(q,(nwpassword,session['lid']))
    #         return '''<script>alert("Password  changed");window.location="/user_home"</script>'''
    #
    #     else:
    #         return '''<script>alert("Password doesnt match");window.location="/user_chngepw#about"</script>'''
    #
    # else:
    #     return '''<script>alert("old password is incorrect");window.location="/user_chngepw#about"</script>'''



@app.route('/bank_delete_user')
@login_required
def bank_delete_user():
    id=request.args.get('id')
    qry1="DELETE FROM login WHERE id=%s"
    iud(qry1, id)
    qry2="DELETE FROM `user` WHERE login_id=%s"
    iud(qry2,id)
    return '''<script>alert("deleted");window.location="/bank_viewuser#about"</script>'''



@app.route('/user_view_balance')
@login_required
def user_view_balance():

    in_values = {'lid': session['lid']}


    global iplist

    ip_address = request.remote_addr
    print (ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        res = requests.post(url+"user_view_balance", data=in_values)
        print(res.text,type(res.text))
        return res.text
    else:
        return ""


    # res = selectall2("SELECT * FROM `transaction` WHERE `user_id`=%s",id)
    # res1 = selectone(" SELECT (SELECT SUM(`balance`) FROM `transaction` WHERE `user_id`=%s AND `type`='deposit') - (SELECT SUM(`balance`) FROM `transaction` WHERE `user_id`=%s AND `type`='withdraw')AS total_balance",(id,id))
    # print(res1,res,session['lid'])
    # return  render_template('user_view_balance.html',val = res,bal = res1)




@app.route('/user_complaint',methods=['post'])
@login_required
def user_complaint():
    complaint = request.form['textarea']
    lid = session['lid']


    in_values = {'complaint': complaint,'lid':lid}


    global iplist

    ip_address = request.remote_addr
    print (ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()
                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()
            iplist.append(str(ip_address))
        res = requests.post(url+"user_complaint", data=in_values)
        print(res.text,type(res.text))
        return res.text
    else:
        return ""

    # in_values = {'complaint': complaint}
    #
    # global iplist
    #
    # ip_address = request.remote_addr
    # print(ip_address)
    # if ip_address not in iplist:
    #     cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
    #     conn.commit()
    #     qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
    #     qry += str(ip_address) + "'"
    #     cmd.execute(qry)
    #     res = cmd.fetchone()
    #     if (res[0] > 10):
    #         cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
    #         conn.commit()
    #
    #         iplist.append(str(ip_address))
    #         # in_values = {'lid': session['lid']}
    #         in_values = { id : session['id']}
    #         return '''<script>alert("COMPLAINT SENT");window.location="/user_home"</script>'''
    #
    #         # return render_template("user_complaint.html")
    #
    #     # else:
    #     #     return '''<script>alert("COMPLAINT SENT");window.location="/user_home"</script>'''
    #




            # qry="insert into complaint values(null,%s,%s,curdate(),curtime(),'pending')"
    # val=session['lid'],complaint
    # iud(qry,val)
    return '''<script>alert("COMPLAINT SENT");window.location="/user_home"</script>'''


@app.route('/user_complaint1')
@login_required
def user_complaint1():

    return render_template('user_complaint.html')




@app.route('/user_view_comp')
@login_required
def user_view_comp():


    in_values = {'lid': session['lid']}


    global iplist

    ip_address = request.remote_addr
    print (ip_address)
    if ip_address not in iplist:
        cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
        conn.commit()

        qry="select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
        res = selectall2(qry, ip_address)
        if len(res) == 8:
            row = []
            row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
            row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
            row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
            row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
            row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
            row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
            row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
            row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
            res = predict([row])
            if res == 1:
                cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
                conn.commit()

                iplist.append(str(ip_address))

        qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
        qry += str(ip_address) + "'"
        cmd.execute(qry)
        res = cmd.fetchone()
        if (res[0] > 10):
            cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
            conn.commit()

            iplist.append(str(ip_address))
        res = requests.post(url+"user_view_comp", data=in_values)
        print(res.text,type(res.text))
        return res.text
    else:
        return ""


    # qry = "select * from complaint where user_id=%s"
    # res = selectall2(qry,session['lid'])
    # return render_template('user_view_comp.html', val=res)






@app.route('/delete_user')
@login_required
def delete_usr():
    id=request.args.get('id')
    qry1="DELETE FROM login WHERE id=%s"
    iud(qry1, id)
    qry2="DELETE FROM `user` WHERE login_id=%s"
    iud(qry2,id)
    return '''<script>alert("deleted");window.location="/admin_viewuser#about"</script>'''


@app.route('/edit_user')
@login_required
def edit_user():
    id=request.args.get('id')
    session['id']=id
    qry="select * from user where login_id=%s"
    res=selectone(qry,id)

    return render_template("auser_edit_index.html",val=res)



@app.route('/update', methods=['post'])
@login_required
def update():
    print(request.form)
    f_name = request.form['textfield']
    l_name = request.form['textfield2']
    gender = request.form['gender']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin_code = request.form['textfield5']
    phone_no = request.form['textfield6']
    mail_id = request.form['textfield7']
    qry = "update user set f_name=%s,l_name=%s,gender=%s,place=%s,post=%s,pin_code=%s,phone_no=%s,email=%s where login_id=%s"
    val=(f_name,l_name,gender, place, post, pin_code, phone_no, mail_id,session['id'])
    iud(qry,val)

    return '''<script>alert("updated");window.location="/admin_viewuser#about"</script>'''


# @app.route('/loan_predict')
# @login_required
# def loan_predict():
#     return render_template("loan.html",st="ok")
#
#
#
#
# @app.route('/loan_predict1',methods=['post'])
# @login_required
# def loan_predict1():
#     gender = request.form['radiobutton']
#     merital_status = request.form['select']
#     education = request.form['select3']
#     dependents = request.form['select2']
#     self_emp = request.form['radiobutton1']
#     app_income = request.form['textfield6']
#     coappp_income = request.form['textfield7']
#     loan_amt = request.form['textfield11']
#     term = request.form['textfield8']
#     cred_hist = request.form['radiobutton3']
#     prop_area = request.form['select4']
#
#     in_values = {'gender': gender, 'merital_status': merital_status,'education': education,'dependents': dependents,'app_income': app_income,'coappp_income': coappp_income,'loan_amt': loan_amt,'term': term,'cred_hist': cred_hist,'prop_area': prop_area,'self_emp': self_emp}
#
#     global iplist
#
#     ip_address = request.remote_addr
#     print(ip_address)
#     if ip_address not in iplist:
#         cmd.execute("insert into logs values(null,'" + str(ip_address) + "',curdate(),curtime(),'233')")
#         conn.commit()
#
#         qry = "select id,MINUTE(TIMEDIFF(CURTIME(),`time`)) AS m,SECOND(TIMEDIFF(CURTIME(),`time`)) AS s  FROM `logs`  WHERE `ip`=%s AND DATE=CURDATE()  ORDER BY `id` DESC LIMIT 8"
#         res = selectall2(qry, ip_address)
#         if len(res) == 8:
#             row = []
#             row.append(int(res[0]['m']) * 60 + int(res[0]['s']))
#             row.append(int(res[1]['m']) * 60 + int(res[1]['s']))
#             row.append(int(res[2]['m']) * 60 + int(res[2]['s']))
#             row.append(int(res[3]['m']) * 60 + int(res[3]['s']))
#             row.append(int(res[4]['m']) * 60 + int(res[4]['s']))
#             row.append(int(res[5]['m']) * 60 + int(res[5]['s']))
#             row.append(int(res[6]['m']) * 60 + int(res[6]['s']))
#             row.append(int(res[7]['m']) * 60 + int(res[7]['s']))
#             res = predict([row])
#             if res == 1:
#                 cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
#                 conn.commit()
#
#                 iplist.append(str(ip_address))
#
#         qry = "select  count(id) from logs where date=curdate() and time_to_sec(timediff(curtime(),time))<10 and ip='"
#         qry += str(ip_address) + "'"
#         cmd.execute(qry)
#         res = cmd.fetchone()
#         if (res[0] > 10):
#             cmd.execute("insert into blacklist values(null,'" + str(ip_address) + "',now())")
#             conn.commit()
#
#             iplist.append(str(ip_address))
#         res = requests.post(url + "loan_predict", data=in_values)
#         print(res.text, type(res.text),"eeeeeeeeeeee")
#         if "['0']" ==  res.text:
#             return render_template('loan.html',val ='0',st="no" )
#         else:
#             return render_template('loan.html',val ='1',st="no" )
#
#
#
#     else:
#         return ""

    # return render_template('loan.html')





app.run(debug=True,host="0.0.0.0")
