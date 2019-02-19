from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from flask import Flask, render_template, request,jsonify
app = Flask(__name__)

db = SQLAlchemy()

POSTGRES = {
    'user': 'iqldyxtbrctwyb',
    'pw': '4112964cabd8088ffe774fa41dd87f1f3c4060d775edfefa4a61cc7f6b13a3d7',
    'db': 'dbd2sh9omcm15f',
    'host': 'ec2-54-243-128-95.compute-1.amazonaws.com',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


#from flask import Flask, render_template, flash, request,jsonify



class BaseModel(db.Model):
"""Base data model for all objects"""
__abstract__ = True
    # define here __repr__ and json methods or any common method
    # that you need for all your models

css YourModel(BaseModel):
"""modelal for one of your table"""
    __tablename__ = 'holidays'
    # define your model

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



    


class d_holiday(db.Model):
    __tablename__ = 'holidays'

    date = db.Column(db.Integer())
    month = db.Column(db.String())
    holiday = db.Column(db.String())
    
    def __init__(self, date, month, holiday):
        self.date = date
        self.month = month
        self.holiday = holiday

    def __repr__(self):
        return '<month {}>'.format(self.month)
    
    def serialize(self):
        return {
            'date': self.date, 
            'month': self.month,
            'holiday': self.holiday,
      
        }

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enterholiday')
def new_student():
   return render_template('calendar.html')

@app.route('/results', methods = ['POST'])
def results():
    try:
        holidays=d_holiday.query.filter_by(month=month_).first()
        return jsonify(holidays.serialize())
    except Exception as e:
      return(str(e))


@app.route('/search', methods = ['POST', 'GET'])
def search():
   return render_template('search.html')




@app.route('/list')
def list():
    try:
        holidays=d_holiday.query.all()
        return  jsonify([e.serialize() for e in holidays])
    except Exception as e:
      return(str(e))


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   date=request.args.get('date')
    month=request.args.get('month')
    holiday=request.args.get('holiday')
    try:
        holidays=holidays(
            date=date,
            month=month,
            holiday=holiday
        )
        db.session.add(holidays)
        db.session.commit()
        return "Calendar updated"
    except Exception as e:
      return(str(e))

if __name__ == '__main__':
   app.run(debug = True)
   manager.run()
