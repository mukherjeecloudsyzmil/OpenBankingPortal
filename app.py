from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.00)

class ApplyForAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # Add more fields as necessary

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user = User(username=username, name=name, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template('registration_success.html')
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

# New route for bank employee login
@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic for bank employees here
        if username == 'bank_employee_username' and password == 'bank_employee_password':
            session['username'] = username
            return redirect(url_for('bank_employee_dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('bank_employee_login.html', error=error)
    return render_template('bank_employee_login.html')

# Route for bank employee dashboard
@app.route('/bank_employee_dashboard')
def bank_employee_dashboard():
    # Render the bank employee dashboard template
    return render_template('bank_employee_dashboard.html')

# Route for applying for a savings account
@app.route('/apply_savings_account', methods=['GET', 'POST'])
def apply_savings_account():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        # Add more fields as necessary

        # Save form data to database
        application = ApplyForAccount(name=name, email=email)
        db.session.add(application)
        db.session.commit()

        # Render a new page with the submitted information
        return render_template('application_confirmation.html', name=name, email=email)
    return render_template('apply_savings_account.html')

@app.route('/application_confirmation', methods=['GET', 'POST'])
def application_confirmation():
    if request.method == 'POST':
        # Retrieve form data (if any)
        name = request.form.get('name')
        email = request.form.get('email')
        # Add more fields as necessary

        # Render the application confirmation page with the submitted information
        return render_template('application_confirmation.html', name=name, email=email)
    else:
        # If accessed via GET request, redirect to the apply_savings_account page
        return redirect(url_for('apply_savings_account'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
