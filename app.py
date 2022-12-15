# flask app and routes
from flask import Flask, render_template
from routes.employee import employees
from routes.contract import contracts
from routes.format import format

# Database
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from Models.models import Employee


# create the app
app = Flask(__name__)

# settings
app.secret_key = 'mysecret'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(employees)
app.register_blueprint(contracts)
app.register_blueprint(format)


SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html', employees=Employee.query.all())


@app.route('/about/')
def about():
    return render_template('about.html')


@app.context_processor
def utility_processor():
    from utils.format import format_currency
    return dict(format_currency=format_currency)
