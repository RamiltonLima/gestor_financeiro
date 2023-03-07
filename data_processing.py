from models import Transacao, TipoTransacao, joinedload
import pandas as pd


class Transacoes:
    def __init__(self) -> None:
        pass

    def view_transacoes(self):

        transacoes = Transacao.query.options(joinedload(Transacao.conta))
        transacoes = transacoes.order_by(Transacao.data_execucao.asc()).all()

        if transacoes:

            df = pd.DataFrame([transacao.to_dict() for transacao in transacoes])
            df = df.sort_values(by="data_execucao")

            df["valor_temp"] = df.apply(
                lambda x: -1 * x["valor"]
                if x["tipo"] in [TipoTransacao.SAIDA]
                else x["valor"],
                axis=1,
            )

            df["acumulado"] = df["valor_temp"].cumsum()

            transacoes_com_acumulado = df.to_dict("records")

            return transacoes_com_acumulado
        else:
            return []


class Chave:
    def __init__(self, nome,  ordenador, quantidade_filhos=0, quantidade_descendentes=0, hash_key=None):
        self.nome = nome
        self.ordenador = ordenador
        self.quantidade_filhos = quantidade_filhos
        self.quantidade_descendentes = quantidade_descendentes
        self.hash_key = hash_key if hash_key is not None else self.nome
        
    def __lt__(self, other):
        if isinstance(other, Chave):
            return self.ordenador < other.ordenador
        else:
            raise NotImplementedError
    
    def __hash__(self):
        return hash(self.hash_key if self.hash_key is not None else self.nome)

    def __eq__(self, other):
        if isinstance(other, Chave):
            return self.hash_key == other.hash_key if self.hash_key is not None else self.nome == other.nome
        else:
            raise NotImplementedError
        
    def __repr__(self) -> str:
        variaveis = ''
        for chave, valor in self.__dict__.items():
            if valor is None:
                variaveis += f'{chave}=None, '
            elif hasattr(valor, '__repr__'):
                variaveis += f'{chave}={valor.__repr__()}, '
            else:
                variaveis += f'{chave}=<{type(valor).__name__} object>, '
        return f'{self.__class__.__name__}({variaveis[:-2]})'
    
    
class ContaInfo(Chave):
    def __init__(self, nome, ordenador, quantidade_filhos=0, id=0 , soma_entrada=0.0, soma_saida=0.0, soma_saldo=0.0, acumulado=0.0, hash_key=None):
        super().__init__(nome, ordenador, quantidade_filhos, hash_key)
        self.id = id
        self.soma_entrada = soma_entrada
        self.soma_saida = soma_saida
        self.soma_saldo = soma_saldo
        self.acumulado = acumulado
        
        
class MesAno(Chave):
    def __init__(self, nome, ordenador, quantidade_filhos=0, quantidade_descendentes=0, hash_key=None):
        super().__init__(nome, ordenador, quantidade_filhos, quantidade_descendentes, hash_key)
        
        
class ParteMes(Chave):
    def __init__(self, nome, ordenador, quantidade_filhos=0,quantidade_descendentes=0, hash_key=None):
        super().__init__(nome, ordenador, quantidade_filhos,quantidade_descendentes, hash_key)
        

class Agrupador:

    from itertools import groupby

    def __init__(self, niveis, dados) -> None:
        self.niveis = niveis
        self.dados = dados
        self.valor_acumulado = 0
        self.grupamento = self.__agrupador(self.dados, self.niveis)
        self.grupamento_limpo = self.__operacoes_recursivas(self.grupamento, self.niveis)
        

    def __ordernador(self, transacoes, nivel_atual):
        return sorted(transacoes, key=lambda x: x[nivel_atual])

    def __remove_chaves(self, transacao, campos_chave_remover):
        transaca_limpa = {}

        for campo in transacao.keys():

            if campo not in campos_chave_remover:
                transaca_limpa[campo] = transacao[campo]

        return transaca_limpa

    def __agrupador(self, pacote, niveis):

        if not niveis:
            return pacote

        nivel_atual = niveis[0]

        if isinstance(pacote, list):

            pacote = self.__ordernador(pacote, nivel_atual)

            pacote_agrupado = self.groupby(pacote, lambda x: x[nivel_atual])

            pacote_final = {}


            for chave_grupo, grupos in pacote_agrupado:

                grupo_convertido = list(grupos)

                if chave_grupo is not None:
                    pacote_final[chave_grupo] = self.__agrupador(grupo_convertido, niveis[1:])

            return pacote_final

        else:

            return pacote
        
        
        
    def __operacoes_recursivas(self, grupos, niveis_navegacao):

        if isinstance(grupos, dict):

            for chave_agrupamento, grupo in grupos.items():
                
                grupos[chave_agrupamento] = self.__operacoes_recursivas(grupo, niveis_navegacao[1:])
                
                if isinstance(grupo, list):
                    if isinstance(chave_agrupamento, Chave):
                                
                        chave_agrupamento.quantidade_filhos = len(grupo)

                        
                        if isinstance(chave_agrupamento, ContaInfo):
                            acumulado_transacoes = 0
                            
                            for transacao in grupo:
                                
                                if transacao['tipo'].name == 'ENTRADA':
                                    transacao['valor_acumulado'] = acumulado_transacoes + transacao['valor']
                                    
                                elif  transacao['tipo'].name == 'SAIDA':
                                    transacao['valor_acumulado'] = acumulado_transacoes - transacao['valor']
                                
                                acumulado_transacoes =  transacao['valor_acumulado']
                                
                            
                            chave_agrupamento.soma_entrada = sum(item['valor'] for item in grupo if item['tipo'].name == 'ENTRADA')
                            chave_agrupamento.soma_saida = sum(item['valor'] for item in grupo if item['tipo'].name == 'SAIDA')
                            chave_agrupamento.soma_saldo = chave_agrupamento.soma_entrada - chave_agrupamento.soma_saida
                            chave_agrupamento.acumulado = self.valor_acumulado + chave_agrupamento.soma_saldo
                            
                            chave_agrupamento.quantidade_descendentes = 2
                            
                            self.valor_acumulado = chave_agrupamento.acumulado
                    
                elif  isinstance(grupos, dict):
                    chave_agrupamento.quantidade_filhos = len(grupo.keys())
                    chave_agrupamento.quantidade_descendentes = sum(chave.quantidade_descendentes for chave in grupo.keys())
                    
                    
            
            return grupos
                    
                
                
        
        elif  isinstance(grupos, list):
            nova_lista = []

            for dicionario in grupos:                
                nova_lista.append(self.__remove_chaves(dicionario, self.niveis))
            return nova_lista
                

class Resumo():
    
    def __init__(self) -> None:
        pass
    
    def view_resumo(self):
        transacoes = Transacao.query.options(joinedload(Transacao.conta)).all()
        
        if transacoes:
        
            transacoes_raw = pd.DataFrame([transacao.to_dict() for transacao in transacoes])
            
            
            
            transacoes_raw["mes_ano"] = transacoes_raw["data_execucao"].apply(
                lambda linha: MesAno(
                nome=linha.date().replace(day=1),
                ordenador=linha.date().replace(day=1),
            )
            )

            transacoes_raw["parte_mes"] = transacoes_raw["data_execucao"].apply(
                lambda linha: ParteMes(
                    nome="Primeira", ordenador=0
                )
                if linha.day < 20
                else ParteMes(nome="Segunda", ordenador=1)
            )

            transacoes_raw["conta"] = transacoes_raw["conta"].apply(
                lambda linha: ContaInfo(
                    nome=linha["nome"],
                    ordenador=int(linha["id"]),
                    id=int(linha["id"])
                )
            )
            transacoes_raw = transacoes_raw.rename( mapper={'id':'transacao_id'}, axis='columns')
            transacoes_raw = transacoes_raw[['mes_ano', 'parte_mes', 'conta', 'transacao_id', 'descricao', 'data_evento','data_execucao','tipo','valor']]
            
            transacoes_raw = transacoes_raw.sort_values('data_execucao')

            
            dados = transacoes_raw.to_dict('records')
            
            niveis = ['mes_ano','parte_mes','conta']
            self.dados_resumo = Agrupador(niveis=niveis, dados=dados)
            return self.dados_resumo.grupamento_limpo
        else:
            return {}