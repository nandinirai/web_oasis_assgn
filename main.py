from flask import Flask, render_template, request, redirect, url_for, session
import re
import sqlite3 as sql


app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        
        con = sql.connect("pythonlogin.sqlite")
       

        cur = con.cursor()
        cur.execute("select * FROM accounts WHERE username = ? AND password = ?;",[username,password])
       
        account = cur.fetchall()
        
        
        if account:
            
            session['loggedin'] = True
            session['id'] = account[0][0]
            session['username'] = account[0][1]

            return redirect(url_for('home'))

        else:
           
            return render_template('error.html')
  
        
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
  
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
  
   return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
 
    msg = ''
   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        con = sql.connect("pythonlogin.sqlite")
        cur = con.cursor()
        
        cur.execute("select * FROM accounts WHERE username =?;",[username])
        account = cur.fetchall()
       
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
           
            cur.execute("insert INTO accounts VALUES (NULL,?, ?, ?);",[username,password,email])
            con.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
       
        msg = 'Please fill out the form!'

   
    
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home')
def home():
    
    if 'loggedin' in session:
        cur_session = session['id']
        con = sql.connect("pythonlogin.sqlite")
        con.row_factory =sql.Row
        cur = con.cursor()
        cur.execute("select * FROM recipe_book;")
        rows = cur.fetchall()
        print(rows)
        
        return render_template('home.html', username=session['username'],rows=rows)
    
    return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    
    if 'loggedin' in session:
       
        
        cur_session = str(session['id'])
        
        con = sql.connect("pythonlogin.sqlite")
        cur = con.cursor()
        cur.execute("select * FROM accounts WHERE username =?;",[cur_session])
        data = cur.fetchall()
        
        #print(session['id'])
       
        return render_template('profile.html', username=session['username'] )
   
    return redirect(url_for('login'))

@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    if request.method == 'GET':
        lname = request.args.get('lname')
        fname = request.args.get('fname')
        print (fname)
        
        con = sql.connect("pythonlogin.sqlite")
        cur = con.cursor()

        cur.execute("delete from `recipe_book` where `id`=?;",fname)
        con.commit()
        con.close()
################################################
    
    con = sql.connect("pythonlogin.sqlite")
    con.row_factory = sql.Row
    
    cur =  con.cursor()
    cur.execute("select * from recipe_book;")
    
    rows = cur.fetchall()
    return render_template('home.html',rows=rows) 

@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    if request.method == 'GET':
        lid =request.args.get('fid')
        lname = request.args.get('fname')
        fingd = request.args.get('elname')
        vg_nvg = request.args.get('eport')
        print(lid)
    
    
    return render_template('edit.html',lname=lname,fingd=fingd,vg_nvg=vg_nvg,lid=lid)

@app.route("/create", methods=['GET', 'POST'])
def list():
     
    msg = ''

    if request.method == 'POST'and 'Recipe' in request.form and 'Ingredients' in request.form and 'Veg_nonveg' in request.form :
        
        Recipe = request.form['Recipe']
        Ingredients = request.form['Ingredients']
        Veg_nonveg = request.form['Veg_nonveg']


        con = sql.connect("pythonlogin.sqlite")
        cur = con.cursor()

        if not Recipe or not  Ingredients or not Veg_nonveg :
            msg= "Please complete the form"
        else:
            cur.execute("insert INTO recipe_book VALUES (NULL,?,?,?);",[Recipe,Ingredients,Veg_nonveg])
            con.commit()

    elif request.method == 'POST':
           
        msg = 'Please fill out the form!'
    
    return render_template('form.html',msg=msg)

@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    #from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        
        idn = request.form['id']
        Recipe = request.form['Recipe']
        Ingredients = request.form['Ingredients']
        Veg_nonveg = request.form['Veg_nonveg']

        
        con = sql.connect("pythonlogin.sqlite")
        cur = con.cursor()
        
        if not Recipe or not  Ingredients or not Veg_nonveg :
            msg= "Please complete the form"
        else:
            cur.execute("update recipe_book set `recipe_name`=? ,`ingredients`= ? , `veg_nonveg`= ? where `id`= ? ;",[Recipe,Ingredients,Veg_nonveg,idn])
            con.commit()
    return render_template('form.html')

if __name__ == '__main__':
       app.run(debug = True,host="127.0.0.1", port = 5000)