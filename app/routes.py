from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import User, Payment
import random


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", 
                           username=current_user.username,
                           balance=current_user.balance,
                           payments=payments)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas", "danger")
    
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/gerar_pix", methods=["POST"])
@login_required
def gerar_pix():
    """Gera um pix e armazena no banco"""
    data = request.json
    amount = data.get("amount")
    recipient_key = data.get("recipient_key")

    if not amount or not recipient_key:
        return jsonify({"error": "Valor ou chave Pix inválidos"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Valor de pagamento inválido"}), 400

    pix_code = f"000201{random.randint(100000, 999999)}"


    new_payment = Payment(
        user_id=current_user.id,
        amount=amount,
        pix_code=pix_code,
        recipient_key=recipient_key,
        status="pendente"
    )
    
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"pix_code": pix_code, "message": "Pix gerado com sucesso!"})


@app.route("/extrato")
@login_required
def extrato():
    """Retorna o extrato dos pagamento do usuario"""
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    extrato_data = [
        {
            "amount": p.amount,
            "pix_code": p.pix_code,
            "recipient_key": p.recipient_key,
            "status": p.status,
            "timestamp": p.timestamp.strftime("%d/%m/%Y %H:%M:%S")
        } 
        for p in payments
    ]
    return jsonify(extrato_data)


@app.route("/confirmar_pix", methods=["POST"])
@login_required
def confirmar_pix():
    """Simula a confirmacao de um pix"""
    data = request.json
    pix_code = data.get("pix_code")

    payment = Payment.query.filter_by(pix_code=pix_code, user_id=current_user.id).first()
    
    if not payment:
        return jsonify({"error": "Pagamento não encontrado"}), 404
 
    if payment.status != "confirmado":
        payment.status = "confirmado"
        current_user.balance += payment.amount  

        db.session.commit()

        multiplicador = 1.05

        current_user.balance *= multiplicador
        db.session.commit()

        return jsonify({"message": "Pix confirmado com sucesso!", "new_balance": current_user.balance})

    return jsonify({"error": "Pix já foi confirmado."}), 400
