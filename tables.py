from main import db
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import DECIMAL

 
    

class Mes_Ano(db.Model,UserMixin):
    __tablename__="mes_ano"
    id = db.Column(db.Integer, primary_key=True)
    mes_id=db.Column(db.Integer,db.ForeignKey("meses.id"), unique=False)
    ano_id=db.Column(db.Integer,db.ForeignKey("anos.id"), unique=False)

    mes_mes_ano = db.relationship('Meses', back_populates = 'mes_mes_mes', lazy = True)
    mes_ano_ano = db.relationship('Anos', back_populates = 'ano_ano_ano', lazy = True)
    mes_ano_documentos = db.relationship('Documentos', back_populates = 'documentos_mes_ano', lazy = True)

class Meses(db.Model,UserMixin):
    __tablename__="meses"
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(256), unique=True, nullable=False)

    mes_mes_mes = db.relationship('Mes_Ano', back_populates = 'mes_mes_ano', lazy = True)
    mes_ano=db.relationship('Anos', secondary="mes_ano", back_populates="ano_mes", lazy=True,overlaps="mes_mes_ano,mes_mes_mes,mes_ano_ano")      
    mes_documento = db.relationship('Documentos', back_populates = 'documento_mes', lazy = True)
    mes_clientes_documentos = db.relationship('Clientes_Documentos', secondary ='mes_clientes_documentos', back_populates = 'clientes_documentos_meses', lazy = True)    
    meses_cd = db.relationship('Cliente_Documento', back_populates = 'cd_meses', lazy = True)


    def __len__(self):
        return len(self.mes_controle_processos)

    

class Anos(db.Model,UserMixin):
    __tablename__="anos"
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, unique=True, nullable=False)

    ano_ano_ano = db.relationship('Mes_Ano', back_populates = 'mes_ano_ano', lazy = True, overlaps="mes_ano")
    ano_mes=db.relationship('Meses', secondary="mes_ano", back_populates="mes_ano", lazy=True, overlaps="ano_ano_ano,mes_ano_ano,mes_mes_ano,mes_mes_mes")    
    ano_documento = db.relationship('Documentos', back_populates = 'documento_ano', lazy = True)
    ano_clientes_documentos = db.relationship('Clientes_Documentos', secondary="ano_clientes_documentos", back_populates = "clientes_documentos_anos", lazy = True)
    anos_cd = db.relationship('Cliente_Documento', back_populates = 'cd_anos', lazy = True)



class Clientes_Documentos(db.Model, UserMixin):
    __tablename__ = 'clientes_documentos'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(256), nullable = False, unique = False)

    clientes_cdoc = db.relationship('Cliente_Documento', back_populates = 'c_clientes', lazy = True)
    clientes_ano = db.relationship('Ano_Clientes_Documentos', back_populates = 'a_cliente', lazy = True, overlaps="clientes_ano,ano_clientes_documentos")
    clientes_mes = db.relationship('Mes_Clientes_Documentos', back_populates = 'm_cliente', lazy = True, overlaps="meses_clientes,mes_clientes_documentos")
    clientes_documentos_anos = db.relationship('Anos', secondary="ano_clientes_documentos", back_populates = "ano_clientes_documentos", lazy = True,overlaps="clientes_ano")
    clientes_documentos = db.relationship('Documentos', secondary ='cliente_documento', back_populates = 'documentos_clientes', lazy = True, overlaps="clientes_cdoc")
    clientes_documentos_meses = db.relationship('Meses', secondary ='mes_clientes_documentos', back_populates = 'mes_clientes_documentos', lazy = True, overlaps="clientes_mes")


class Documentos(db.Model, UserMixin):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key = True)
    tipo_doc = db.Column(db.String(500), nullable = False, unique = False)
    data_solicita = db.Column(db.String(256), nullable = True, unique = False)
    data_envio_ = db.Column(db.String(256), nullable = True, unique = False)
    mes_id = db.Column(db.Integer,db.ForeignKey("meses.id"), unique=False)
    ano_id = db.Column(db.Integer,db.ForeignKey("anos.id"), unique=False)
    mes_ano_id = db.Column(db.Integer, db.ForeignKey("mes_ano.id"))

    documentos_cdoc = db.relationship('Cliente_Documento', back_populates = 'c_documentos', lazy = True, overlaps="clientes_documentos")
    documento_mes = db.relationship('Meses', back_populates = 'mes_documento', lazy = True)
    documento_ano = db.relationship('Anos', back_populates = 'ano_documento', lazy = True)
    documentos_clientes = db.relationship('Clientes_Documentos', secondary ='cliente_documento', back_populates = 'clientes_documentos', lazy = True, overlaps="documentos_cdoc,clientes_cdoc")
    documentos_mes_ano = db.relationship('Mes_Ano', back_populates = 'mes_ano_documentos', lazy = True)

#MANY TO MANY
class Cliente_Documento(db.Model, UserMixin):
    __tablename__ = 'cliente_documento'
    id = db.Column(db.Integer, primary_key = True)
    cliente_id=db.Column(db.Integer,db.ForeignKey("clientes_documentos.id"), unique=False)
    documento_id=db.Column(db.Integer,db.ForeignKey("documentos.id"), unique=False)
    ano_id = db.Column(db.Integer,db.ForeignKey("anos.id"), unique=False)
    mes_id = db.Column(db.Integer,db.ForeignKey("meses.id"), unique=False)

    c_clientes = db.relationship('Clientes_Documentos', back_populates = 'clientes_cdoc', lazy = True, overlaps="clientes_documentos,documentos_clientes")
    c_documentos = db.relationship('Documentos', back_populates = 'documentos_cdoc', lazy = True, overlaps="clientes_documentos,documentos_clientes")
    cd_anos = db.relationship('Anos', back_populates = 'anos_cd', lazy = True)
    cd_meses = db.relationship('Meses', back_populates = 'meses_cd', lazy = True) 

#TABELA PARA CADASTRAR CLIENTES SOMENTE PARA DOCUMENTOS
class Mes_Clientes_Documentos(db.Model, UserMixin):
    __tablename__ = 'mes_clientes_documentos'
    id = db.Column(db.Integer, primary_key = True)
    cliente_id=db.Column(db.Integer,db.ForeignKey("clientes_documentos.id"), unique=False)
    mes_id=db.Column(db.Integer,db.ForeignKey("meses.id"), unique=False)

    m_cliente= db.relationship('Clientes_Documentos', back_populates = 'clientes_mes', lazy = True, overlaps="clientes_meses,meses_clientes,clientes_documentos_meses,mes_clientes_documentos")

#TABELA PARA CADASTRAR CLIENTES SOMENTE PARA DOCUMENTOS
class Ano_Clientes_Documentos(db.Model, UserMixin):
    __tablename__ = 'ano_clientes_documentos'
    id = db.Column(db.Integer, primary_key = True)
    cliente_id=db.Column(db.Integer,db.ForeignKey("clientes_documentos.id"), unique=False)
    ano_id=db.Column(db.Integer,db.ForeignKey("anos.id"), unique=False)

    a_cliente = db.relationship('Clientes_Documentos', back_populates = 'clientes_ano', lazy = True, overlaps="ano_clientes,clientes_anos,ano_clientes_documentos,clientes_documentos_anos")


