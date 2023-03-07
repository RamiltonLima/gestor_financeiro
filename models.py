from app import db

from enum import Enum
from sqlalchemy.orm import joinedload


class TipoTransacao(Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saida"
    

class Conta(db.Model):
    __tablename__ = "conta"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    transacoes = db.relationship("Transacao", cascade="all, delete-orphan", backref="conta")
    
    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Transacao(db.Model):
    __tablename__ = "transacao"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(TipoTransacao), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_evento = db.Column(db.DateTime, nullable=False)
    data_execucao = db.Column(db.DateTime, nullable=False)
    conta_id = db.Column(db.Integer, db.ForeignKey("conta.id"), nullable=False)

    def to_dict(self):
        dicionario = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        dicionario["conta"] = self.conta.to_dict()
        return dicionario
    
