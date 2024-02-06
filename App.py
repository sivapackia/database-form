from flask import Flask,render_template,redirect,request,session,url_for
from flask_mysqldb import MySQL

App=Flask(__name__)
App.secret_key="sivapackia"
App.config['MYSQL_HOST']='localhost'
App.config['MYSQL_USER']='root'
App.config['MYSQL_PASSWORD']='Rspk2822@'
App.config['MYSQL_DB']='form_database'
mysql=MySQL(App)

@App.route("/")
def Home():
    return render_template("Home.html")

@App.route("/SIGN",methods=["GET","POST"])
def Signup():
    if request.method == "POST":
        Name=request.form.get('name')
        Password=request.form.get('password')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO signup (Name,Password) VALUES(%s,%s)",(Name,Password))
        cur.connection.commit()
        cur.close()
        return redirect(url_for('Home'))
    return render_template("Signup.html")

@App.route("/",methods=["GET","POST"])
def Login():
    if request.method == "POST":
        Name=request.form.get('name')
        Password=request.form.get('password')
        cur=mysql.connection.cursor()
        cur.execute("select * from signup where Name=%s and Password=%s",(Name,Password))
        data=cur.fetchall()
        cur.connection.commit()
        cur.close()
        if data:
            session["Name"]=Name
            return redirect(url_for('Table'))
        else:
            return "INVAILED NAME AND PASSWORD"
    return render_template("Home.html")

@App.route("/")
def Logout():
    session.pop("Name",None)
    return redirect(url_for('Home'))

@App.route("/TABLE")
def Table():
    cur=mysql.connection.cursor()
    cur.execute("select *from employee")
    data=cur.fetchall()
    cur.close()
    return render_template("Table.html",value=data)

@App.route("/ADD",methods=["GET","POST"])
def Add():
    if request.method =="POST":
       Name=request.form.get('name')
       Id=request.form.get('id')
       Dept=request.form.get('dept')
       Salary=request.form.get('salary')
       cur=mysql.connection.cursor()
       cur.execute("insert into employee(Name,Id,Dept,Salary) values(%s,%s,%s,%s)",(Name,Id,Dept,Salary))
       cur.connection.commit()
       cur.close()
       return redirect(url_for('Table'))
    return render_template("Add.html")

@App.route("/EDIT/<string:SL_NO>",methods=["GET","POST"])
def Edit(SL_NO):
    if request.method =="POST":
       Name=request.form.get('name')
       Id=request.form.get('id')
       Dept=request.form.get('dept')
       Salary=request.form.get('salary')
       cur=mysql.connection.cursor()
       cur.execute("update employee set Name=%s,Id=%s,Dept=%s,Salary=%s where SL_NO=%s",(Name,Id,Dept,Salary,SL_NO))
       cur.connection.commit()
       cur.close()
       return redirect(url_for('Table'))
    cur=mysql.connection.cursor()
    cur.execute("select *from employee where SL_NO=%s",(SL_NO,))
    data=cur.fetchone()
    cur.close()
    return render_template("Edit.html",data=data)

@App.route("/DELETE/<string:SL_NO>")

def Delete(SL_NO):
    cur=mysql.connection.cursor()
    cur.execute("delete from employee where SL_NO=%s",(SL_NO,))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('Table'))

if __name__ =="__main__":
    App.run(debug=True)
 