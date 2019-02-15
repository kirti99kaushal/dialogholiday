import sqlite3

conn = sqlite3.connect('holidays.db')
print ("Opened database successfully")

#conn.execute('CREATE TABLE holidays (month TEXT, date TEXT, holiday TEXT)')
#print ("Table created successfully")
conn.close()

from flask import Flask, render_template, request,jsonify
#from flask import Flask, render_template, flash, request,jsonify
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enterholiday')
def new_student():
   return render_template('calendar.html')

@app.route('/results', methods = ['POST'])
def results():
    con=sql.connect("holidays.db")
    month = request.form['month']
    cur = con.cursor()
    cur.execute("SELECT * FROM holidays WHERE month=?",(month,))    
    #cur.execute("SELECT * FROM students ")
    rows = cur.fetchall()
    print("print rows", rows)
    return render_template("search.html",data=rows)

@app.route('/jresults', methods = ['POST'])
def jresults():
    con=sql.connect("holidays.db")
    #month = request.form['month']
    req = request.get_json(silent=True, force=True)
    action = req['queryResult']['parameters']['Holiday']
    month = req['queryResult']['parameters']['Months']
    cur = con.cursor()
    cur.execute("SELECT * FROM holidays WHERE month=?",(month,))    
    #cur.execute("SELECT * FROM students ")
    rows = cur.fetchall()
    print("print rows", rows)
    i = 0
    for row in rows:
       i = i +1 
       print('-- ',i,'-', row[0],'-',row[1],'-',row[2])
    response =  """
                Response : {0}
                """.format(rows)
    reply = {"fulfillmentText": response,}
    return jsonify(reply)

@app.route('/search', methods = ['POST', 'GET'])
def search():
   return render_template('search.html')




@app.route('/list')
def list():
   con = sql.connect("holidays.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from holidays")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       
      
      month = request.form['month']
      date = request.form['date']
      holiday = request.form['holiday']
        
         
      with sql.connect("holidays.db") as con:
         cur = con.cursor()
            
         cur.execute("INSERT INTO holidays (month,date,holiday) VALUES (?,?,?)",(month,date,holiday) )
            
         con.commit()
         msg = "Record successfully added"
      #except:
      con.rollback()
      msg = "error in insert operation"
      
      
      return render_template("result.html",msg = msg)
      con.close()

if __name__ == '__main__':
   app.run(debug = True)
