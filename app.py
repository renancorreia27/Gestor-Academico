import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.banco_dados import BancoDados

# Inicializar o banco de dados (tabelas)
BancoDados.inicializar_banco()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

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
        
    user_id = session['user_id']
    semestres = BancoDados.listar_semestres(user_id)
    
    semestre_atual = None
    materias = []
    
    if semestres:
        sem_id_str = request.args.get('semestre_id')
        if sem_id_str:
            for s in semestres:
                if str(s.id) == sem_id_str:
                    semestre_atual = s
                    break
        if not semestre_atual:
            semestre_atual = semestres[0]
            
        materias = BancoDados.listar_materias(semestre_atual.id)

    ira_geral = BancoDados.calcular_ira_geral(user_id)

    return render_template('index.html', semestres=semestres, materias=materias, semestre_atual=semestre_atual, ira_geral=ira_geral)

@app.route('/semestre/novo', methods=['POST'])
def novo_semestre():
    if 'user_id' not in session: return redirect(url_for('login'))
    nome = request.form.get('nome')
    if nome:
        BancoDados.criar_semestre(session['user_id'], nome)
        flash("Semestre criado com sucesso!", "success")
    return redirect(url_for('dashboard'))

@app.route('/materia/nova', methods=['POST'])
def nova_materia():
    if 'user_id' not in session: return redirect(url_for('login'))
    sem_id = request.form.get('semestre_id')
    nome = request.form.get('nome')
    carga = request.form.get('carga_horaria', type=int, default=60)
    faltas = request.form.get('max_faltas', type=int, default=20)
    media = request.form.get('media_necessaria', type=float, default=7.0)
    
    if sem_id and nome:
        BancoDados.adicionar_materia(sem_id, nome, carga, faltas, media)
        flash("Matéria adicionada com sucesso!", "success")
    return redirect(url_for('dashboard', semestre_id=sem_id))

@app.route('/materia/<int:id>/nota', methods=['POST'])
def adicionar_nota(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    valor = request.form.get('valor', type=float, default=0.0)
    peso = request.form.get('peso', type=float, default=1.0)
    BancoDados.adicionar_nota(id, valor, peso)
    flash("Nota adicionada!", "success")
    sem_id = request.form.get('semestre_id')
    return redirect(url_for('dashboard', semestre_id=sem_id))

@app.route('/materia/<int:id>/falta', methods=['POST'])
def adicionar_falta(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    qtd = request.form.get('qtd', type=int, default=1)
    BancoDados.adicionar_falta(id, qtd)
    flash("Falta registrada!", "warning")
    sem_id = request.form.get('semestre_id')
    return redirect(url_for('dashboard', semestre_id=sem_id))

@app.route('/semestres')
def semestres():
    if 'user_id' not in session: return redirect(url_for('login'))
    user_id = session['user_id']
    semestres_lista = BancoDados.listar_semestres(user_id)
    return render_template('semestres.html', semestres=semestres_lista)

@app.route('/materias')
def materias():
    if 'user_id' not in session: return redirect(url_for('login'))
    user_id = session['user_id']
    semestres_lista = BancoDados.listar_semestres(user_id)
    semestres_com_materias = []
    for s in semestres_lista:
        m = BancoDados.listar_materias(s.id)
        semestres_com_materias.append({'semestre': s, 'materias': m})
    return render_template('materias.html', semestres_com_materias=semestres_com_materias)

@app.route('/semestre/<int:id>/deletar', methods=['POST'])
def deletar_semestre(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    BancoDados.deletar_semestre(id)
    flash("Semestre e suas matérias foram excluídos com sucesso!", "success")
    return redirect(url_for('semestres'))

@app.route('/materia/<int:id>/deletar', methods=['POST'])
def deletar_materia(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    BancoDados.excluir_materia(id)
    flash("Matéria excluída com sucesso!", "success")
    return redirect(url_for('materias'))

@app.route('/semestre/<int:id>/status', methods=['POST'])
def status_semestre(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    situacao = request.form.get('situacao')
    if situacao:
        BancoDados.atualizar_status_semestre(id, situacao)
        flash("Status do semestre atualizado!", "success")
    return redirect(url_for('semestres'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
