from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import config

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/entidade', methods = ['POST', 'GET'])
def entidade():
    if request.method == 'POST':
        nome=request.form.get('nome')
        tipo_pessoa=request.form.get('tipo_pessoa')
        url_entidade=request.form.get('url_entidade')
        descricao=request.form.get('descricao')
        try:
            entidade=models.Entidade(
                nome=nome,
                tipo_pessoa=tipo_pessoa,
                url_entidade=url_entidade,
                descricao=descricao,
            )
            db.session.add(entidade)
            db.session.commit()
            return "Entidade Adicionada. instituicao id={}".format(entidade.entidade_id)
        except Exception as e:
	        return(str(e))
    if request.method == 'GET':
        tipo_request = request.args.get('tipo_request')
        if tipo_request == 'id':
            entidade_id=request.args.get('entidade_id')
            try:
                entidade=models.Entidade.query.filter_by(entidade_id=entidade_id).first()
                return jsonify({'success': True, 'data': entidade.serialize()})
            except Exception as e:
                return jsonify({'success': False, 'data': str(e)})
        elif tipo_request == 'all':
            try:
                entidades=models.Entidade.query.all()
                return jsonify({'success': True, 'data': [e.serialize() for e in entidades]})
            except Exception as e:
                return jsonify({'success': False, 'data': str(e)})
        else:
            return jsonify({'success': False, 'data': 'Tipo não informado'})


@app.route("/acao", methods=['POST', 'GET'])
def acao():
    if request.method == 'POST':
        entidade_id=request.form.get('entidade_id')
        nome_acao=request.form.get('nome_acao')
        url_acao=request.form.get('url_acao')
        descricao=request.form.get('descricao')
        contato=request.form.get('contato')
        tipo_ajuda=request.form.get('tipo_ajuda')
        forma_ajuda=request.form.get('forma_ajuda')
        forma_verificacao=request.form.get('forma_verificacao')
        resp_verificacao=request.form.get('resp_verificacao')
        ativa=request.form.get('ativa') == 'true'
        permanente=request.form.get('permanente') == 'true'
        validade=request.form.get('validade')
        if 'imagem_acao' in request.files:
            imagem_acao = request.files['imagem_acao']
        else:
            imagem_acao = None
        try:
            acao=models.Acao(
                entidade_id=entidade_id,
                nome_acao=nome_acao,
                imagem_acao=imagem_acao,
                url_acao=url_acao,
                descricao=descricao,
                contato=contato,
                tipo_ajuda=tipo_ajuda,
                forma_ajuda=forma_ajuda,
                forma_verificacao=forma_verificacao,
                resp_verificacao=resp_verificacao,
                ativa=ativa,
                permanente=permanente,
                validade=validade
            )
            db.session.add(acao)
            db.session.commit()
            return "Acao adicionada. acao id={}".format(acao.acao_id)
        except Exception as e:
            return(str(e))
    if request.method == 'GET':
        tipo_request = request.args.get('tipo_request')
        if(tipo_request == 'id'):
            acao_id=request.args.get('acao_id')
            try:
                acao=models.Acao.query.filter_by(acao_id=acao_id).first()
                return jsonify({'success': True, 'data': acao.serialize()})
            except Exception as e:
                return jsonify({'success': False, 'data': str(e)})
        if tipo_request == 'entidade':
            entidade_id=request.args.get('entidade_id')
            try:
                acoes=models.Acao.query.filter_by(entidade_id=entidade_id).all()
                return jsonify({'success': True, 'data': [a.serialize() for a in acoes]})
            except Exception as e:
                return jsonify({'success': False, 'data': str(e)})
        elif tipo_request == 'all':
            try:
                acoes=models.Acao.query.all()
                return jsonify({'success': True, 'data': [a.serialize() for a in acoes]})
            except Exception as e:
                return jsonify({'success': False, 'data': str(e)})
        else:
            return jsonify({'success': False, 'data': 'Tipo não informado'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
