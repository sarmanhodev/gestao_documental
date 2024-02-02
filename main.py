from flask import *
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy import asc, func
from sqlalchemy.orm import joinedload
from tables import *
import pandas as pd
from datetime import datetime, date, timedelta


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()
app = Flask(__name__, template_folder='./templates')

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}  

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:ROOT@localhost/controle_processos"

app.config["SECRET_KEY"] = 'secret'
db.init_app(app)


#ROTAS REFERENTES AOS RELATÓRIOS DE PRODUTIVIDADE
@app.route("/relatorio_produtividade", methods = ['GET', 'POST'])
def relatorio_produtividade():
    ano_corrente = date.today() 
    ano_atual = db.session.query(Anos).filter(Anos.ano== ano_corrente.year).first()
    mes_atual = db.session.query(Meses).filter(Meses.id==ano_corrente.month).first()
    clientes = db.session.query(Clientes_Documentos).options(joinedload(Clientes_Documentos.clientes_cdoc)).all()
    documentos = db.session.query(Documentos).options(joinedload(Documentos.documentos_cdoc)).filter(Documentos.ano_id==ano_atual.id).all()

    documentos_enviados = db.session.query(Documentos).options(joinedload(Documentos.documentos_cdoc)).filter(Documentos.data_envio_!= 'Aguardando envio').filter(Documentos.ano_id==ano_atual.id).filter(Documentos.mes_id==mes_atual.id).all()
    documentos_aguardando_envio = db.session.query(Documentos).options(joinedload(Documentos.documentos_cdoc)).filter(Documentos.data_envio_== 'Aguardando envio').filter(Documentos.ano_id==ano_atual.id).filter(Documentos.mes_id==mes_atual.id).all()
    
    #VARIÁVEL PEGARÁ SOMENTE OS DADOS DO MÊS CORRENTE
    clientes_documentos_mes = db.session.query(Cliente_Documento).options(joinedload(Cliente_Documento.c_clientes), joinedload(Cliente_Documento.c_documentos),\
    joinedload(Cliente_Documento.cd_anos), joinedload(Cliente_Documento.cd_meses)).filter(Cliente_Documento.ano_id==ano_atual.id).filter(Cliente_Documento.mes_id==mes_atual.id).all()

    #VARIÁVEL PEGARÁ SOMENTE TODOS OS DADOS DO ANO CORRENTE
    clientes_documentos = db.session.query(Cliente_Documento).options(joinedload(Cliente_Documento.c_clientes), joinedload(Cliente_Documento.c_documentos),\
    joinedload(Cliente_Documento.cd_anos), joinedload(Cliente_Documento.cd_meses)).filter(Cliente_Documento.ano_id==ano_atual.id).all()

    anos = db.session.query(Anos).order_by(asc(Anos.id)).options(joinedload(Anos.ano_documento)).order_by(asc(Anos.id)).all()
    mes_ano = db.session.query(Mes_Ano).options(joinedload(Mes_Ano.mes_ano_documentos)).filter(Mes_Ano.ano_id==ano_atual.id).filter(Mes_Ano.mes_id==mes_atual.id).first()

    return render_template ("relatorio_produtividade.html", clientes = clientes, documentos = documentos, clientes_documentos=clientes_documentos,
            clientes_documentos_mes = clientes_documentos_mes, documentos_enviados=documentos_enviados, documentos_aguardando_envio=documentos_aguardando_envio,
            anos = anos, mes_ano = mes_ano, ano_atual=ano_atual)


#ROTA PARA RELATÓRIO DE PRODUTIVIDADE ANUAL
@app.route("/produtividade_anual/<ano>", methods=['GET','POST'])
def produtividade_anual(ano):
    ano_atual = db.session.query(Anos).options(joinedload(Anos.ano_mes)).filter(Anos.ano==ano).first()
    anos = db.session.query(Anos).options(joinedload(Anos.ano_documento)).order_by(asc(Anos.id)).all()
    meses = db.session.query(Meses).options(joinedload(Meses.mes_documento)).all()
    mes_clientes = db.session.query(Mes_Clientes_Documentos).options(joinedload(Mes_Clientes_Documentos.m_cliente)).all()
    documentos_enviados = db.session.query(Documentos).filter(Documentos.data_envio_!= 'Aguardando envio').filter(Documentos.ano_id == ano_atual.id).all()
    documentos_aguardando_envio = db.session.query(Documentos).filter(Documentos.data_envio_ == 'Aguardando envio').filter(Documentos.ano_id == ano_atual.id).all()
    mes_ano = db.session.query(Mes_Ano).order_by(asc(Mes_Ano.id)).options(joinedload(Mes_Ano.mes_ano_documentos), joinedload(Mes_Ano.mes_mes_ano), joinedload(Mes_Ano.mes_ano_ano)).filter(Mes_Ano.ano_id==ano_atual.id).all()
    
    #VARIÁVEL PEGARÁ SOMENTE TODOS OS DADOS DO ANO CORRENTE
    clientes_documentos = db.session.query(Cliente_Documento).options(joinedload(Cliente_Documento.c_clientes), joinedload(Cliente_Documento.c_documentos),\
    joinedload(Cliente_Documento.cd_anos), joinedload(Cliente_Documento.cd_meses)).filter(Cliente_Documento.ano_id==ano_atual.id).all()

    return render_template("relatorio_produtividade_anual.html", ano_atual=ano_atual, anos = anos, meses = meses, mes_ano = mes_ano, mes_clientes=mes_clientes, 
                    clientes_documentos=clientes_documentos, documentos_aguardando_envio= documentos_aguardando_envio, documentos_enviados=documentos_enviados)


#ROTA PARA CADASTRAR NOVO DOCUMENTO
@app.route("/cadastra_documento", methods=['GET', 'POST'])
def cadastra_documento():   

    if request.method=='POST':
        nome_cliente = request.form['nome_cliente']
        cliente = db.session.query(Clientes_Documentos).filter(Clientes_Documentos.nome==nome_cliente).first()

        tipo_documento = request.form['tipo_documento']
        data_solicitacao = request.form['data_solicitacao']
        dt_solicita  = datetime.strptime(data_solicitacao,'%Y-%m-%d').date()
        data_solicitacao_formatada = datetime.strftime(dt_solicita,'%d/%m/%Y')

        data_envio = request.form['data_envio']
        mes_value = request.form['mes_value']
        mes_id = db.session.query(Meses).filter(Meses.mes==mes_value).first()
        ano_value = request.form['ano_value']
        ano_id = db.session.query(Anos).filter(Anos.ano==ano_value).first()
        mes_ano = db.session.query(Mes_Ano).filter(Mes_Ano.ano_id==ano_id.id).filter(Mes_Ano.mes_id==mes_id.id).first()

        if not cliente:
            novo_cliente = Clientes_Documentos(nome = nome_cliente)
            db.session.add(novo_cliente)
            db.session.commit()

            if data_envio == 'Invalid Date':
                novo_documento = Documentos(tipo_doc = tipo_documento, data_solicita = data_solicitacao_formatada, data_envio_ = 'Aguardando envio',
                                            mes_id = mes_id.id, ano_id = ano_id.id, mes_ano_id = mes_ano.id)
                db.session.add(novo_documento)
                db.session.commit()
            else:
                novo_documento = Documentos(tipo_doc = tipo_documento, data_solicita = data_solicitacao_formatada, data_envio_ = data_envio,
                                            mes_id = mes_id.id, ano_id = ano_id.id, mes_ano_id = mes_ano.id)
                db.session.add(novo_documento)
                db.session.commit()

            cliente_mes = Mes_Clientes_Documentos(cliente_id = novo_cliente.id, mes_id = mes_id.id)
            db.session.add(cliente_mes)
            db.session.commit()

            cliente_ano = Ano_Clientes_Documentos(cliente_id = novo_cliente.id, ano_id = ano_id.id)
            db.session.add(cliente_ano)
            db.session.commit()

            #tabela many to many
            cliente_documento = Cliente_Documento(cliente_id = novo_cliente.id, documento_id = novo_documento.id, ano_id = ano_id.id, mes_id = mes_id.id)
            db.session.add(cliente_documento)
            db.session.commit()

            return redirect(url_for('relatorio_produtividade'))
        
        else:
            if data_envio == '':
                novo_documento = Documentos(tipo_doc = tipo_documento, data_solicita = data_solicitacao_formatada, data_envio_ = 'Aguardando envio',
                                            mes_id = mes_id.id, ano_id = ano_id.id, mes_ano_id = mes_ano.id)
                db.session.add(novo_documento)
                db.session.commit()
            else:
                novo_documento = Documentos(tipo_doc = tipo_documento, data_solicita = data_solicitacao_formatada, data_envio_ = data_envio,
                                            mes_id = mes_id.id, ano_id = ano_id.id, mes_ano_id = mes_ano.id)
                db.session.add(novo_documento)
                db.session.commit()

            cliente_mes = Mes_Clientes_Documentos(cliente_id = cliente.id, mes_id = mes_id.id)
            db.session.add(cliente_mes)
            db.session.commit()

            cliente_ano = Ano_Clientes_Documentos(cliente_id = cliente.id, ano_id = ano_id.id)
            db.session.add(cliente_ano)
            db.session.commit()

            #tabela many to many
            cliente_documento = Cliente_Documento(cliente_id = cliente.id, documento_id = novo_documento.id, ano_id = ano_id.id, mes_id = mes_id.id)
            db.session.add(cliente_documento)
            db.session.commit()

            return redirect(url_for('relatorio_produtividade'))

#ROTA PARA EDITAR REGISTRO RELATÓRIO DE PRODUTIVIDADE
@app.route("/update_relatorio_produtividade/<cliente_id>_<documento_id>", methods =['GET','POST'])
def update_relatorio_produtividade(cliente_id,documento_id):
    clientes = db.session.query(Clientes_Documentos).filter(Clientes_Documentos.id==cliente_id).first()
    documento = db.session.query(Documentos).filter(Documentos.id==documento_id).first()

    data_solicitacao = request.form['data_solicitacao']

    data_envio = request.form['data_envio']
    dt_envio  = datetime.strptime(data_envio,'%Y-%m-%d').date()
    data_envio_formatada = datetime.strftime(dt_envio,'%d/%m/%Y')


    if request.method == 'POST':
        clientes.nome = request.form['nome_cliente_editado']
        documento.tipo_doc = request.form['tipo_documento']
        documento.data_solicita = data_solicitacao
        documento.data_envio_ = data_envio_formatada

        flash('Registro atualizado com sucesso')

        db.session.commit()

        return redirect (url_for('relatorio_produtividade'))


#ROTA PARA APAGAR REGISTRO
@app.route("/deletar_relatorio_produtividade/<cliente_id>_<documento_id>", methods =['GET','POST'])
def deletar_relatorio_produtividade(cliente_id,documento_id):
    cliente_documento = db.session.query(Cliente_Documento).filter(Cliente_Documento.cliente_id==cliente_id).filter(Cliente_Documento.documento_id==documento_id).first()
    db.session.delete(cliente_documento)
    db.session.commit()

    documento = db.session.query(Documentos).filter(Documentos.id==documento_id).first()
    db.session.delete(documento)
    db.session.commit()

    flash('Registro excluído com sucesso')

    return redirect (url_for('relatorio_produtividade'))




if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
