import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.banco_dados import BancoDados

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
def login():
    # se o usuário já estiver logado, manda direto pro dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = BancoDados.autenticar_usuario(email, password)
        if usuario:
            # grava as informações na sessão
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nome
            return redirect(url_for('dashboard'))
        else:
            # exibe alerta e fica na mesma tela
            flash("Email ou senha incorretos. Tente novamente.", "danger")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # se o usuário já estiver logado, não tem motivo pra ver a tela de registro
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        sucesso = BancoDados.registrar_usuario(name, email, password)
        if sucesso:
            flash("Conta criada com sucesso! Você já pode fazer login.", "success")
            return redirect(url_for('login'))
        else:
            flash("Ocorreu um erro ao criar a conta. Este email pode já estar cadastrado.", "danger")
            
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # se não tiver um ID de usuário na sessão, é expulso para o login
    if 'user_id' not in session:
        flash("Por favor, faça login para acessar o painel.", "warning")
        return redirect(url_for('login'))
        
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
