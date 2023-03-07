from app import app, db, request, redirect, render_template, flash
from models import Transacao, Conta, TipoTransacao
from datetime import datetime
from dateutil.relativedelta import relativedelta
from data_processing import Transacoes, Resumo



@app.route('/')
def index():

    resumo = Resumo()
    resumo = resumo.view_resumo()

    return render_template('index.html', titulo_pagina='Resumo', resumo=resumo)


@app.route('/contas')
def contas():

    contas = Conta.query.all()
    return render_template('contas.html', contas=contas, titulo_pagina='Contas')


@app.route('/transacoes')
def transacoes():
    transacoes = Transacoes()
    transacoes = transacoes.view_transacoes()
    
    tipos_transacao = [ valor for nome, valor in dict(TipoTransacao._member_map_).items()]
    
    contas = Conta.query.all()

    return render_template(
        'transacoes.html',
        contas=contas,
        transacoes=transacoes,
        titulo_pagina='Transações',
        tipos_transacao = tipos_transacao
    )
  


@app.route('/transacoes/nova', methods=['GET', 'POST'])
def adicionar_transacao():
    if request.method == 'POST':
        tipo = request.form['transacao_tipo']
        descricao = request.form['transacao_descricao']
        valor = request.form['transacao_valor']
        data_evento = datetime.strptime(request.form['transacao_data_evento'], '%Y-%m-%dT%H:%M')
        data_execucao =  datetime.strptime(request.form['transacao_data_execucao'], '%Y-%m-%dT%H:%M')
        conta_id = request.form['transacao_conta']
        quantidade_meses = int(request.form['transacao_quantidade_meses'])

        for i in range(quantidade_meses):
            conta = Conta.query.filter_by(id=conta_id).first()
            nova_data_execucao = data_execucao + relativedelta(months=i)
            transacao = Transacao(
                tipo=tipo
                ,descricao=descricao
                ,valor=valor
                ,data_evento=data_evento
                ,data_execucao=nova_data_execucao
                ,conta=conta
            )
            
            db.session.add(transacao)
            db.session.commit()

        return redirect('/transacoes')
    else:
        contas = Conta.query.all()
        return render_template('transacao.html', contas=contas, titulo_pagina='Transações')
    
    
    
@app.route('/transacoes/editar', methods=['GET', 'POST'])
def editar_transacao():
    if request.method == 'POST':
        
        transacao_id = request.form['editar_transacao_id']
        
        transacao_checar = Transacao.query.get(transacao_id)
        if not transacao_checar:
            flash('Transacao inexistente')
            return redirect('/transacoes')
    
        transacao_checar.tipo = request.form['editar_transacao_tipo']
        transacao_checar.descricao = request.form['editar_transacao_descricao']
        transacao_checar.valor = request.form['editar_transacao_valor']
        transacao_checar.data_evento = datetime.strptime(request.form['editar_transacao_data_evento'], '%Y-%m-%dT%H:%M')
        transacao_checar.data_execucao = datetime.strptime(request.form['editar_transacao_data_execucao'], '%Y-%m-%dT%H:%M')
        transacao_checar.conta_id = request.form['editar_transacao_conta']
        
        db.session.commit()

        tipo = request.form['editar_transacao_tipo']
        descricao = request.form['editar_transacao_descricao']
        valor = request.form['editar_transacao_valor']
        data_evento = datetime.strptime(request.form['editar_transacao_data_evento'], '%Y-%m-%dT%H:%M')
        data_execucao =  datetime.strptime(request.form['editar_transacao_data_execucao'], '%Y-%m-%dT%H:%M')
        conta_id = request.form['editar_transacao_conta']
        quantidade_meses = int(request.form['editar_transacao_quantidade_meses'])
        

        for i in range(quantidade_meses - 1):
            print(i)
            print(data_execucao)
            conta = Conta.query.filter_by(id=conta_id).first()
            nova_data_execucao = data_execucao + relativedelta(months=i+1)
            transacao = Transacao(
                tipo=tipo
                ,descricao=descricao
                ,valor=valor
                ,data_evento=data_evento
                ,data_execucao=nova_data_execucao
                ,conta=conta
            )
            
            db.session.add(transacao)
            db.session.commit()

        return redirect('/transacoes')
    
    
    
    
    


@app.route('/contas/adicionar', methods=['GET', 'POST'])
def adicionar_conta():
    if request.method == 'POST':
        nome = request.form['conta_nome']

        conta = Conta.query.filter_by(nome=nome).first()
        if conta:
            flash('Já existe uma conta com esse nome', category='error')
            return redirect('/contas/adicionar')
        else:
            conta = Conta(nome=nome)
            db.session.add(conta)
            db.session.commit()

        return redirect('/contas')
    else:
        contas = Conta.query.all()
        return render_template('contas.html', contas=contas, titulo_pagina='Contas')


@app.route('/contas/excluir/<int:conta_id>', methods=['POST'])
def excluir_conta(conta_id):


    conta_deletar = Conta.query.get(conta_id)
    db.session.delete(conta_deletar)
    db.session.commit()
    flash('Conta excluida.')

    return redirect('/contas')


@app.route('/transacoes/excluir/<int:transacao_id>', methods=['POST'])
def excluir_transacao(transacao_id):

    transacao_deletar = Transacao.query.get(transacao_id)
    db.session.delete(transacao_deletar)
    db.session.commit()
    flash('Conta excluida.')

    return redirect('/transacoes')
