from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import Fornecedor, Servico, Cliente, PropostaCliente, OrcamentoFornecedor, Orcamento
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/index_forn')
def index_forn():
    return render_template('index_forn.html')

@main.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar o perfil.', 'warning')
        return redirect(url_for('main.index'))

    return render_template('dashboard.html', usuario=session['usuario'])

@main.route('/dashboard_forn')
def dashboard_forn():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar o perfil.', 'warning')
        return redirect(url_for('main.index_forn'))

    return render_template('dashboard_forn.html', usuario=session['usuario'])


@main.route('/fornecedores')
def fornecedores():
    todos = Fornecedor.query.all()
    return render_template('fornecedores.html', fornecedores=todos)

@main.route('/empresas')
def empresas():
    todos = Fornecedor.query.all()
    return render_template('empresas_forn.html', fornecedores=todos)

@main.route('/servicos')
def servicos():
    todos = Servico.query.all()
    return render_template('servicos.html', servicos=todos)

@main.route('/servicos_forn')
def servicos_forn():
    todos = Servico.query.all()
    return render_template('servicos_forn.html', servicos=todos)

@main.route('/servico/novo', methods=['GET', 'POST'])
def novo_servico():
    ...
    return render_template('novo_servico.html')

@main.route('/orcamentos/novo', methods=['GET', 'POST'])
def novo_orcamento():
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        area = request.form['area_placas']
        valor = request.form['valor_orcamento']
        local = request.form['local']
        fornecedor_id = request.form['idfornecedor']

        id_cadastro = session.get('idcadastro')
        cliente = Cliente.query.filter_by(cadastro_idcadastro=id_cadastro).first()
        if not cliente:
            return "Cliente não encontrado", 400

        # Cria o orçamento
        orcamento = Orcamento(
            descricao=descricao,
            area_placas=area,
            valor_orcamento=valor,
            local=local,
            data_proposta=datetime.utcnow().date(),
            status_orcamento=0  # exemplo: 0 = pendente
        )
        db.session.add(orcamento)
        db.session.commit()

        # Associa cliente
        proposta_cliente = PropostaCliente(
            orcamento_idorcamento=orcamento.idproposta,
            cliente_idcliente=cliente.idcliente
        )
        db.session.add(proposta_cliente)

        # Associa fornecedor
        orcamento_forn = OrcamentoFornecedor(
            orcamento_idorcamento=orcamento.idproposta,
            fornecedor_idfornecedor=fornecedor_id
        )
        db.session.add(orcamento_forn)

        db.session.commit()
        return redirect(url_for('main.orcamentos'))

    fornecedores = Fornecedor.query.all()
    return render_template('novo_orcamento.html', fornecedores=fornecedores)


