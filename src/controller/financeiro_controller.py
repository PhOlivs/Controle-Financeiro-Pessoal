from model.carteira import Carteira, CarteiraBancaria
from model.transacao import Transacao
from model.banco import Instituicao

class FinanceiroController:
    def __init__(self):
        self.carteira = Carteira()
        self.carteira_bancaria = CarteiraBancaria()

    def adicionar_transacao(self, valor, tipo, categoria, descricao="", datahora=None):
        transacao = Transacao(valor, tipo, categoria, descricao, datahora)
        self.carteira.adicionar_transacao(transacao)

    def obter_saldo(self):
        # Soma saldo das transações + saldo total das instituições bancárias
        return self.carteira.calcular_saldo() + self.carteira_bancaria.saldo_total()

    def obter_transacoes(self):
        return self.carteira.listar_transacoes()

    def adicionar_instituicao(self, nome, saldo_corrente=0.0, saldo_poupanca=0.0, saldo_investimentos=0.0):
        instituicao = Instituicao(nome, saldo_corrente, saldo_poupanca, saldo_investimentos)
        self.carteira_bancaria.adicionar_instituicao(instituicao)

    def listar_instituicoes(self):
        return self.carteira_bancaria.instituicoes