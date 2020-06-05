from webapp import db
import enum
from datetime import datetime

class TipoPessoa(enum.Enum):
    PF = 'PF'
    PJ = 'PJ'

class TipoAjuda(enum.Enum):
    RECEBE = 'RECEBE'
    FORNECE = 'FORNECE'

class FormaAjuda(enum.Enum):
    DINHEIRO = 'DINHEIRO'
    MATERIAL = 'MATERIAL'
    SERVICO = 'SERVICO'
    ONLINE = 'ONLINE'

class TipoBeneficiado(enum.Enum):
    PJ = 'PJ'

class Entidade(db.Model):
    __tablename__ = 'entidades'

    entidade_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    tipo_pessoa = db.Column(db.Enum(TipoPessoa))
    url_entidade = db.Column(db.String())
    descricao = db.Column(db.String())

    def __init__(self, nome, tipo_pessoa, url_entidade, descricao):
        self.nome = nome
        self.tipo_pessoa = tipo_pessoa
        self.url_entidade = url_entidade
        self.descricao = descricao

    def __repr__(self):
        return '<Entidade: %r>' % self.nome

    def serialize(self):
        tipo_p = None
        if self.tipo_pessoa:
            tipo_p = self.tipo_pessoa.value
        return{
            'entidade_id': self.entidade_id,
            'nome': self.nome,
            'tipo_pessoa': tipo_p,
            'url_entidade': self.url_entidade,
            'descricao': self.descricao
        }

class NaMidia(db.Model):
    __tablename__ = 'na_midia'

    na_midia_id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acoes.acao_id'), nullable=False)
    midia_url = db.Column(db.String())
    midia = db.Column(db.String())

    def __init__(self, acao_id, midia_url, midia):
        self.acao_id = acao_id
        self.midia_url = midia_url
        self.midia = midia

    def __repr__(self):
        return '<NaMidia: %r>' % self.midia_url

    def serialize(self):
        return{
            'na_midia_id': self.na_midia_id,
            'acao_id': self.acao_id,
            'midia_url': self.midia_url,
            'midia': self.midia
        }

class Localizacao(db.Model):
    __tablename__ = 'localizacoes'

    localizacao_id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acoes.acao_id'), nullable=False)
    endereco = db.Column(db.String())
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())
    horario = db.Column(db.String())
    obs = db.Column(db.String())

    def __init__(self, acao_id, endereco, latitude, longitude, horario, obs):
        self.acao_id = acao_id
        self.endereco = endereco
        self.latitude = latitude
        self.longitude = longitude
        self.horario = horario
        self.obs = obs

    def __repr__(self):
        return '<Localizacao: %r>' % self.endereco

    def serialize(self):
        return{
            'localizacao_id': self.localizacao_id,
            'acao_id': self.acao_id,
            'endereco': self.endereco,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'horario': self.horario,
            'obs': self.obs
        }

class DadosBancarios(db.Model):
    __tablename__ = 'dados_bancarios'

    dados_bancarios_id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acoes.acao_id'), nullable=False)
    banco = db.Column(db.String())
    agencia = db.Column(db.String())
    operacao = db.Column(db.String())
    conta = db.Column(db.String())
    nome_beneficiado = db.Column(db.String())
    tipo_beneficiado = db.Column(db.Enum(TipoBeneficiado), nullable=False)
    id_beneficiado = db.Column(db.String())

    def __init__(self, acao_id, banco, agencia, operacao, conta, nome_beneficiado, tipo_beneficiado, id_beneficiado):
        self.acao_id = acao_id
        self.banco = banco
        self.agencia = agencia
        self.operacao = operacao
        self.conta = conta
        self.nome_beneficiado = nome_beneficiado
        self.tipo_beneficiado = tipo_beneficiado
        self.id_beneficiado = id_beneficiado

    def __repr__(self):
        return '<Localizacao: %r>' % self.acao_id

    def serialize(self):
        tipo_b = None
        if self.tipo_beneficiado:
            tipo_b = self.tipo_beneficiado.value
        return{
            'dados_bancarios_id': self.dados_bancarios_id,
            'acao_id': self.acao_id,
            'banco': self.banco,
            'agencia': self.agencia,
            'operacao': self.operacao,
            'conta': self.conta,
            'nome_beneficiado': self.nome_beneficiado,
            'tipo_beneficiado': tipo_b,
            'id_beneficiado': self.id_beneficiado
        }

class Acao(db.Model):
    __tablename__ = 'acoes'

    acao_id = db.Column(db.Integer, primary_key=True)
    entidade_id = db.Column(db.Integer, db.ForeignKey('entidades.entidade_id'), nullable=False)
    nome_acao = db.Column(db.String(), nullable=False)
    imagem_acao = db.Column(db.String())
    url_acao = db.Column(db.String())
    descricao = db.Column(db.String())
    contato = db.Column(db.String())
    tipo_ajuda = db.Column(db.Enum(TipoAjuda), nullable=False)
    forma_ajuda = db.Column(db.Enum(FormaAjuda), nullable=False)
    data_insercao = db.Column(db.DateTime())
    data_atualizacao = db.Column(db.DateTime())
    forma_verificacao = db.Column(db.String())
    resp_verificacao = db.Column(db.String())
    ativa = db.Column(db.Boolean)
    permanente = db.Column(db.Boolean)
    validade = db.Column(db.String())
    entidade = db.relationship(Entidade, foreign_keys=entidade_id, backref='entidade_acao')
    localizacoes = db.relationship(Localizacao, primaryjoin="and_(Acao.acao_id==Localizacao.acao_id)")
    midias = db.relationship(NaMidia, primaryjoin="and_(Acao.acao_id==NaMidia.acao_id)")
    dados_bancarios = db.relationship(DadosBancarios, primaryjoin="and_(Acao.acao_id==DadosBancarios.acao_id)")

    def __init__(self, entidade_id, nome_acao, imagem_acao, url_acao, descricao, contato, tipo_ajuda, forma_ajuda, forma_verificacao, resp_verificacao, ativa, permanente, validade):
        self.entidade_id = entidade_id
        self.nome_acao = nome_acao
        self.imagem_acao = imagem_acao
        self.url_acao = url_acao
        self.descricao = descricao
        self.contato = contato
        self.tipo_ajuda = tipo_ajuda
        self.forma_ajuda = forma_ajuda
        self.data_insercao = datetime.now()
        self.data_atualizacao = datetime.now()
        self.forma_verificacao = forma_verificacao
        self.resp_verificacao = resp_verificacao
        self.ativa = ativa
        self.permanente = permanente
        self.validade = validade

    def __repr__(self):
        return '<Acão %r>' % self.nome_acao

    def serialize(self):
        tipo_a = None
        forma_a = None
        if self.tipo_ajuda:
            tipo_a = self.tipo_ajuda.value
        if self.forma_ajuda:
            forma_a = self.forma_ajuda.value
        return{
            'acao_id': self.acao_id,
            'entidade_id': self.entidade_id,
            'nome_acao': self.nome_acao,
            #'imagem_acao': self.imagem_acao,
            'url_acao': self.url_acao,
            'descricao': self.descricao,
            'contato': self.contato,
            'tipo_ajuda': tipo_a,
            'forma_ajuda': forma_a,
            'data_insercao': self.data_insercao,
            'data_atualizacao': self.data_atualizacao,
            'forma_verificacao': self.forma_verificacao,
            'resp_verificacao': self.resp_verificacao,
            'ativa': self.ativa,
            'permanente': self.permanente,
            'validade': self.validade,
            'nome_entidade': self.entidade.nome,
            'localizacoes': [localizacao.serialize() for localizacao in self.localizacoes],
            'midias': [midia.serialize() for midia in self.midias],
            'dados_bancarios': [dado_bancario.serialize() for dado_bancario in self.dados_bancarios]
        }
