from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Cadastro, Contato, Endereco, Fornecedor, Cliente
from datetime import date, datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        # Verifica se o usuário existe com login e senha corretos
        usuario = Cadastro.query.filter_by(login=login, senha=senha).first()

        if usuario:
            session['usuario'] = usuario.login  # salva login na sessão
            flash(f'Bem-vindo, {usuario.login}!', 'success')

            if usuario.tipo_usuario == 1:
                return redirect(url_for('main.dashboard'))  # redireciona para dashboard
            else:
                return redirect(url_for('main.dashboard_forn'))
        else:
            flash('Login ou senha inválidos.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']
        tipo = int(request.form['tipo_usuario'])  # agora é 1 ou 2

        if Cadastro.query.filter_by(login=login).first():
            flash('Login já existe.', 'danger')
            return redirect(url_for('auth.signup'))

        # Criar contato
        contato = Contato(
            telefone=request.form['telefone'],
            email=request.form['email']
        )
        db.session.add(contato)
        db.session.commit()

        # Criar endereço
        endereco = Endereco(
            cep=request.form['cep'],
            numero=request.form['numero'],
            pontoreferencia=request.form['pontoreferencia']
        )
        db.session.add(endereco)
        db.session.commit()

        # Criar cadastro
        cadastro = Cadastro(
            login=login,
            senha=senha,
            tipo_usuario=tipo
        )
        db.session.add(cadastro)
        db.session.commit()

        if tipo == 1:
            print(">>>>> Criando cliente")
            print("Nome:", request.form['nome_cliente'])
            print("CPF:", request.form['cpf'])
            print("Nascimento:", request.form['data_nascimento'])
            cliente = Cliente(
                nome=request.form['nome_cliente'],
                cpf=request.form['cpf'],
                contato_idcontato=contato.idcontato,
                cadastro_idcadastro=cadastro.idcadastro,
                status=1,
                data_cadastro=date.today(),
                endereco_idendereco=endereco.idendereco,
                data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
            )
            db.session.add(cliente)

        elif tipo == 2:
            fornecedor = Fornecedor(
                nome=request.form['nome_fornecedor'],
                cnpj=request.form['cnpj'],
                contato_idcontato=contato.idcontato,
                cadastro_idcadastro=cadastro.idcadastro,
                endereco_idendereco=endereco.idendereco,
                atualizacao_servico=datetime.strptime(request.form['atualizacao_servico'], '%Y-%m-%d').date()
            )
            db.session.add(fornecedor)

        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/alterar_senha', methods=['GET', 'POST'])
def alterar_senha():
    login = session.get('usuario')
    if not login:
        flash("Você precisa estar logado.", "danger")
        return redirect(url_for('auth.login'))

    cadastro = Cadastro.query.filter_by(login=login).first()

    if request.method == 'POST':
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']
        confirmar = request.form['confirmar']

        if cadastro.senha != senha_atual:
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for('auth.alterar_senha'))

        if nova_senha != confirmar:
            flash("Nova senha e confirmação não coincidem.", "danger")
            return redirect(url_for('auth.alterar_senha'))

        cadastro.senha = nova_senha
        db.session.commit()
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('main.index'))

    return render_template("alterar_senha.html")


@auth.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    login = session.get('usuario')
    if not login:
        flash("Você precisa estar logado.", "danger")
        return redirect(url_for('auth.login'))

    cadastro = Cadastro.query.filter_by(login=login).first()

    # Buscar cliente ou fornecedor ligado ao cadastro
    cliente = Cliente.query.filter_by(cadastro_idcadastro=cadastro.idcadastro).first()
    fornecedor = Fornecedor.query.filter_by(cadastro_idcadastro=cadastro.idcadastro).first()

    if request.method == 'POST':
        # Atualiza contato e endereço
        if cliente:
            cliente.nome = request.form['nome']
            cliente.cpf = request.form['cpf']
            cliente.contato.telefone = request.form['telefone']
            cliente.contato.email = request.form['email']
            cliente.endereco.cep = request.form['cep']
            cliente.endereco.numero = request.form['numero']
            cliente.endereco.pontoreferencia = request.form['pontoreferencia']
        elif fornecedor:
            fornecedor.nome = request.form['nome']
            fornecedor.cnpj = request.form['cnpj']
            fornecedor.contato.telefone = request.form['telefone']
            fornecedor.contato.email = request.form['email']
            fornecedor.endereco.cep = request.form['cep']
            fornecedor.endereco.numero = request.form['numero']
            fornecedor.endereco.pontoreferencia = request.form['pontoreferencia']

        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('main.index'))

    return render_template("editar_perfil.html", cadastro=cadastro, cliente=cliente, fornecedor=fornecedor)
