from flask import Flask,render_template,request,jsonify,redirect,url_for,make_response,flash
import json , os  
import razorpay
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['DEBUG'] = True
app.secret_key = "payment_app"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'payment_app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.String(120),nullable=False)

@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        amount = request.form.get('amount')
        user = User(name=name, email=email, amount=amount)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pay' , id = user.id))

    return render_template('index.html')

@app.route('/pay/<id>',methods=["GET","POST"])
def pay(id):
    user = User.query.filter_by(id=id).first()

    client = razorpay.Client(auth=("rzp_test_8KgpMHFByE6Ist","IDLvuwOrpcwQHmeL5gGv3Stq"))
    payment = client.order.create({'amount' :(int(user.amount)*100), 'currency': 'INR' ,  'payment_capture':'1' })

    return render_template('pay.html',payment=payment)

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)