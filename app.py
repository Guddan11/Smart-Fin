from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    income = db.Column(db.Float)
    expense = db.Column(db.Float)
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    target = db.Column(db.Float)
    saved = db.Column(db.Float)

# Home
@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔐 HASH PASSWORD
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        data = Finance.query.filter_by(user=session['user']).all()
        goal = Goal.query.filter_by(user=session['user']).first()

        income_list = [d.income for d in data]
        expense_list = [d.expense for d in data]

        return render_template(
            'dashboard.html',
            user=session['user'],
            data=data,
            income_list=income_list,
            expense_list=expense_list,
            goal=goal
        )

    return redirect('/login')         
    
@app.route('/set_goal', methods=['POST'])
def set_goal():
    if 'user' in session:
        target = float(request.form['target'])

        goal = Goal(user=session['user'], target=target, saved=0)
        db.session.add(goal)
        db.session.commit()

    return redirect('/dashboard')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
    @app.route('/add', methods=['POST'])
    def add():
     if 'user' in session:
        income = float(request.form['income'])
        expense = float(request.form['expense'])

        record = Finance(user=session['user'], income=income, expense=expense)
        db.session.add(record)

        # Calculate savings
        saving = income - expense

        goal = Goal.query.filter_by(user=session['user']).first()
        if goal:
            goal.saved += saving

        db.session.commit()

     return redirect('/dashboard')
      