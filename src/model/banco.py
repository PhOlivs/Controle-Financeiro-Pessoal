class Banco:
    def __init__(self, saldo_inicial=0.0):
        self.saldo = saldo_inicial

    def atualizar_saldo(self, valor):
        self.saldo += valor

    def obter_saldo(self):
        return self.saldo

class Instituicao:
    def __init__(self, nome, saldo_corrente=0.0, saldo_poupanca=0.0, saldo_investimentos=0.0):
        self.nome = nome
        self.saldo_corrente = saldo_corrente
        self.saldo_poupanca = saldo_poupanca
        self.saldo_investimentos = saldo_investimentos

    def saldo_total(self):
        return self.saldo_corrente + self.saldo_poupanca + self.saldo_investimentos