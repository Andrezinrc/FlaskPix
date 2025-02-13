from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)  

    def __repr__(self):
        return f"<User {self.username}>"
    
    def update_balance(self, amount):
        """Atualiza o saldo do usuário"""
        if isinstance(amount, str):
            amount = float(amount)
        self.balance += amount
        db.session.commit()


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    pix_code = db.Column(db.String(100), unique=True, nullable=False)
    recipient_key = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(20), default="pendente")

    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f"<Payment {self.pix_code} - {self.amount} - {self.status}>"
