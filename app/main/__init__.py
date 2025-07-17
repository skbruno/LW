from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import Fornecedor, Servico, Cliente, PropostaCliente, OrcamentoFornecedor, Orcamento, ServicoFornecedor, Cadastro
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
    usuario_id = session.get('idcadastro')
    if not usuario_id:
        return "Fornecedor não encontrado"
    
    todos = Fornecedor.query.all()

    cliente_orcamento = Cliente.query.filter_by(cadastro_idcadastro=usuario_id).first()
    orcamentos_do_cliente = cliente_orcamento.orcamentos

    return render_template('dashboard.html', usuario=session['usuario'], fornecedores=todos, orcamentos=orcamentos_do_cliente)

@main.route('/dashboard_forn')
def dashboard_forn():
    usuario_id = session.get('idcadastro')
    if not usuario_id:
        return "Fornecedor não encontrado"

    fornecedor_logado = Fornecedor.query.filter_by(cadastro_idcadastro=usuario_id).first()
    servicos_do_fornecedor = fornecedor_logado.servicos

    Orcamento_logado = Orcamento.query.filter_by(cadastro_idcadastro=usuario_id).first()
    orcamento_do_fornecedor = Orcamento_logado

    return render_template('dashboard_forn.html', usuario=session.get('usuario'), meus_servicos=servicos_do_fornecedor)

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

    usuario_id = session.get('idcadastro')
    if not usuario_id:
        return "Fornecedor não encontrado"

    fornecedor_logado = Fornecedor.query.filter_by(cadastro_idcadastro=usuario_id).first()

    servicos_do_fornecedor = fornecedor_logado.servicos

    return render_template('servicos_forn.html',servicos=servicos_do_fornecedor )

@main.route('/servico/novo', methods=['GET', 'POST'])
def novo_servico():

    if request.method == 'POST':
        usuario_id = session.get('idcadastro')
        if not usuario_id:
            return "Fornecedor não encontrado"

        fornecedor_logado = Fornecedor.query.filter_by(cadastro_idcadastro=usuario_id).first()

        novo_servico = Servico(
            nome=request.form['nome'],
            descricao=request.form['observacao'],
            preco=request.form['valor']
        )

        # Associar servico fornecedor
        novo_servico.fornecedores.append(fornecedor_logado)

        db.session.add(novo_servico)
        db.session.commit()

        flash('Serviço cadastrado com sucesso', 'success')
        return redirect(url_for('main.dashboard_forn'))

    return render_template('novo_servico.html')

@main.route('/orcamentos/novo', methods=['GET', 'POST'])
def novo_orcamento():
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        area = request.form['area_placas']
        valor = request.form['orcamento_total_final']
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
        return redirect(url_for('main.dashboard'))


    fornecedores = Fornecedor.query.all()
    return render_template('novo_orcamento.html', fornecedores=fornecedores)


