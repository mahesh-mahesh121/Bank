from flask import Flask,render_template,request
from mysql.connector import *

mysql = connect(
    host = "localhost",
    user = "root",
    password = "mahesh@121",
    database = "Bank"
)

cursor = mysql.cursor()

app = Flask(__name__)

@app.route("/")
def bank():
    return render_template("bank.html")

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute('SELECT * FROM Bank WHERE Email = %s AND Password = %s',(email,password))
        result = cursor.fetchone()
        if result:
            return render_template("success.html")
        else :
            return "<h1>Invalid!!!</h1>"
        
    return render_template("login.html")

@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get('email')
        password = request.form.get('password')
        insert = """
        INSERT INTO Bank(Name,Email,Password)VALUES(%s,%s,%s);
            """
        values=(name,email,password)
        cursor.execute(insert,values)
        print("Success:Record Inserted")
        mysql.commit()
    return render_template("signup.html")

@app.route("/balance",methods=["POST","GET"])
def balance():
    if request.method == "POST":
        accountno = request.form["accountnumber"]
        pin = request.form["pin"]
        cursor.execute("select * from account where Account_Number = %s and Pin_Number = %s",(accountno,pin))
        result = cursor.fetchone()
        print(result)
        if result:
            return render_template("output.html",result=result)
        else:
            return "Invalid"
    return render_template("balance.html")

@app.route('/withdraw',methods=["POST","GET"])
def withdraw():
    if request.method == "POST":
        accountno = request.form["accountnumber"]
        pin = request.form.get("pin")
        withdraw = request.form.get("withdraw")
        cursor.execute("select * from account where Pin_Number = %s",(pin,))
        res = cursor.fetchone()
        withdraw = float(withdraw)
        if res[2] >= withdraw:
            cursor.execute("insert into ministatement(Account_number,withdraw)values(%s,%s)",(accountno,withdraw))
            mysql.commit()
            cursor.execute('select * from account where pin_number = %s',(pin,))
            result = cursor.fetchone()
            result1 = result[2] - withdraw
            cursor.execute('update account set balance = %s where pin_number = %s',(result1,pin))
            mysql.commit()
            # cursor.execute('select * from account where pin_number = %s',(pin,))
            # bal = cursor.fetchone()
            return render_template("output.html",res=withdraw)
        else:
            return "Invalid"
    return render_template("withdraw.html")

@app.route('/deposit',methods=["POST","GET"])
def deposit_amount():
    if request.method == "POST":
        accountno = request.form["accountnumber"]
        pin = request.form.get("pin")
        amount = request.form.get("deposit")
        cursor.execute('select * from account where pin_number = %s',(pin,))
        result = cursor.fetchone()
        result1 = result[2] + float(amount)
        cursor.execute("update account set balance = %s where pin_number = %s",(result1,pin))
        mysql.commit()
        cursor.execute("insert into ministatement(Account_number,deposit)values(%s,%s)",(accountno,amount))
        mysql.commit()
        if amount:
            return render_template("output.html",amount = amount)
        else :
            return "invalid"
    return render_template("deposit.html")

@app.route("/ministatement",methods=["POST","GET"])
def ministatement():
    if request.method == "POST":
        ac_no = request.form["ac"]
        cursor.execute("select * from ministatement where Account_number = %s",(ac_no,))
        result = cursor.fetchall()
        print(result)
        if result:
            return render_template("output.html",resultmin = result)
        else:
            return "Invalid"
    return render_template("ministatement.html")

@app.route('/accountcreate',methods=["POST","GET"])
def accountcreate():
    if request.method == "POST":
        ac = request.form.get("ac")
        pin = request.form.get("pin")
        balance = request.form.get("balance")
        insert = """insert into account(Account_Number,Pin_Number,Balance)values(%s,%s,%s)"""
        i=(ac,pin,balance)
        cursor.execute(insert,i)
        mysql.commit()
    return render_template("accountcreate.html")

if __name__ == "__main__":
    app.run(debug=True)

