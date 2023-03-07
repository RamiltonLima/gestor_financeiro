import os, sys
from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import webbrowser
from filters import format_date, format_currency, print_debug, float_reais, float_porcentagem


caminho_absoluto = os.path.join(os.path.dirname(sys.executable), 'dados_contas_transacoes.db')
app = Flask(__name__,  template_folder='templates', static_folder='static')
app.secret_key = 's6a5s4d6a5s4dqw8e4qss5f4a5f4q962413454d5s4ds65ahj5hj4k4'
app.config['SQLALCHEMY_DATABASE_URI'] =  f'sqlite:///{caminho_absoluto}'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.jinja_env.filters['format_date'] = format_date
app.jinja_env.filters['format_currency'] = format_currency
app.jinja_env.filters['print_debug'] = print_debug
app.jinja_env.filters['float_reais'] = float_reais
app.jinja_env.filters['float_porcentagem'] = float_porcentagem

db = SQLAlchemy(app)

@app.before_first_request
def create_database():
    db.create_all()

from views import *
    
if __name__ == '__main__':
    print(caminho_absoluto)
    porta = 8000
    url = f"http://localhost:{str(porta)}"
    webbrowser.open_new(url)
    app.run(port=porta)