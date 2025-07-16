CREATE TABLE cadastro (
    idcadastro INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT,
    senha TEXT,
    tipo_usuario INTEGER
);

CREATE TABLE contato (
    idcontato INTEGER PRIMARY KEY AUTOINCREMENT,
    telefone TEXT,
    email TEXT
);

CREATE TABLE endereco (
    idendereco INTEGER PRIMARY KEY AUTOINCREMENT,
    cep TEXT,
    numero INTEGER,
    pontoreferencia TEXT
);

CREATE TABLE cliente (
    idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cpf TEXT,
    contato_idcontato INTEGER,
    cadastro_idcadastro INTEGER,
    status INTEGER,
    data_cadastro DATE,
    endereco_idendereco INTEGER,
    data_nascimento DATE,
    FOREIGN KEY (contato_idcontato) REFERENCES contato(idcontato),
    FOREIGN KEY (cadastro_idcadastro) REFERENCES cadastro(idcadastro),
    FOREIGN KEY (endereco_idendereco) REFERENCES endereco(idendereco)
);

CREATE TABLE fornecedor (
    idfornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cnpj TEXT,
    contato_idcontato INTEGER,
    cadastro_idcadastro INTEGER,
    endereco_idendereco INTEGER,
    atualizacao_servico DATE,
    FOREIGN KEY (contato_idcontato) REFERENCES contato(idcontato),
    FOREIGN KEY (cadastro_idcadastro) REFERENCES cadastro(idcadastro),
    FOREIGN KEY (endereco_idendereco) REFERENCES endereco(idendereco)
);

CREATE TABLE servico (
    idservico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    descricao TEXT,
    preco INTEGER
);

CREATE TABLE servico_has_fornecedor (
    servico_idservico INTEGER,
    fornecedor_idfornecedor INTEGER,
    PRIMARY KEY (servico_idservico, fornecedor_idfornecedor),
    FOREIGN KEY (servico_idservico) REFERENCES servico(idservico),
    FOREIGN KEY (fornecedor_idfornecedor) REFERENCES fornecedor(idfornecedor)
);

CREATE TABLE orcamento (
    idproposta INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    area_placas INTEGER,
    valor_orcamento INTEGER,
    status_orcamento INTEGER,
    vencedor TEXT,
    data_proposta DATE,
    data_reposta DATE,
    local TEXT
);

CREATE TABLE orcamento_has_fornecedor (
    orcamento_idorcamento INTEGER,
    fornecedor_idfornecedor INTEGER,
    PRIMARY KEY (orcamento_idorcamento, fornecedor_idfornecedor),
    FOREIGN KEY (orcamento_idorcamento) REFERENCES orcamento(idproposta),
    FOREIGN KEY (fornecedor_idfornecedor) REFERENCES fornecedor(idfornecedor)
);

CREATE TABLE proposta_has_cliente (
    orcamento_idorcamento INTEGER,
    cliente_idcliente INTEGER,
    PRIMARY KEY (orcamento_idorcamento, cliente_idcliente),
    FOREIGN KEY (orcamento_idorcamento) REFERENCES orcamento(idproposta),
    FOREIGN KEY (cliente_idcliente) REFERENCES cliente(idcliente)
);
