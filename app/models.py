from app import db

class Cadastro(db.Model):
    idcadastro = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)

class Contato(db.Model):
    idcontato = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(150))


class Endereco(db.Model):
    idendereco = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(45))
    numero = db.Column(db.Integer)
    pontoreferencia = db.Column(db.String(150))
    fornecedores = db.relationship('Fornecedor', back_populates='endereco')


class Cliente(db.Model):
    idcliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(14))
    contato_idcontato = db.Column(db.Integer, db.ForeignKey('contato.idcontato'))
    cadastro_idcadastro = db.Column(db.Integer, db.ForeignKey('cadastro.idcadastro'))
    status = db.Column(db.Integer)
    data_cadastro = db.Column(db.Date)
    endereco_idendereco = db.Column(db.Integer, db.ForeignKey('endereco.idendereco'))
    endereco = db.relationship('Endereco') 
    data_nascimento = db.Column(db.Date)
    contato = db.relationship('Contato')
    orcamentos = db.relationship(
        'Orcamento',
        secondary='proposta_has_cliente',
        back_populates='clientes'
    )


class Fornecedor(db.Model):
    idfornecedor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cnpj = db.Column(db.String(18))
    contato_idcontato = db.Column(db.Integer, db.ForeignKey('contato.idcontato'))
    cadastro_idcadastro = db.Column(db.Integer, db.ForeignKey('cadastro.idcadastro'))
    endereco_idendereco = db.Column(db.Integer, db.ForeignKey('endereco.idendereco'))
    endereco = db.relationship('Endereco', back_populates='fornecedores')
    atualizacao_servico = db.Column(db.Date)
    contato = db.relationship('Contato')
    servicos = db.relationship(
        'Servico',
        secondary='servico_has_fornecedor',
        back_populates='fornecedores'
    )
    orcamentos = db.relationship(
        'Orcamento',
        secondary='orcamento_has_fornecedor',
        back_populates='fornecedores'
    )


class Servico(db.Model):
    idservico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Integer)
    fornecedores = db.relationship(
        'Fornecedor',
        secondary='servico_has_fornecedor',
        back_populates='servicos'
    )


class ServicoFornecedor(db.Model):
    __tablename__ = 'servico_has_fornecedor'
    servico_idservico = db.Column(db.Integer, db.ForeignKey('servico.idservico'), primary_key=True)
    fornecedor_idfornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.idfornecedor'), primary_key=True)


class Orcamento(db.Model):
    idproposta = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text)
    area_placas = db.Column(db.Integer)
    valor_orcamento = db.Column(db.Integer)
    status_orcamento = db.Column(db.Integer)
    vencedor = db.Column(db.String(45))
    data_proposta = db.Column(db.Date)
    data_reposta = db.Column(db.Date)
    local = db.Column(db.String(100))
    clientes = db.relationship(
        'Cliente',
        secondary='proposta_has_cliente',
        back_populates='orcamentos'
    )
    fornecedores = db.relationship(
        'Fornecedor',
        secondary='orcamento_has_fornecedor',
        back_populates='orcamentos'
    )


class OrcamentoFornecedor(db.Model):
    __tablename__ = 'orcamento_has_fornecedor'
    orcamento_idorcamento = db.Column(db.Integer, db.ForeignKey('orcamento.idproposta'), primary_key=True)
    fornecedor_idfornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.idfornecedor'), primary_key=True)


class PropostaCliente(db.Model):
    __tablename__ = 'proposta_has_cliente'
    orcamento_idorcamento = db.Column(db.Integer, db.ForeignKey('orcamento.idproposta'), primary_key=True)
    cliente_idcliente = db.Column(db.Integer, db.ForeignKey('cliente.idcliente'), primary_key=True)
