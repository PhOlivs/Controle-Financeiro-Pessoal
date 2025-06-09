class Carteira:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def calcular_saldo(self):
        return sum(t.valor if t.tipo == "receita" else -t.valor for t in self.transacoes)

    def listar_transacoes(self):
        return self.transacoes
    
class CarteiraBancaria:
    def __init__(self):
        self.instituicoes = []

    def adicionar_instituicao(self, instituicao):
        self.instituicoes.append(instituicao)

    def saldo_total(self):
        return sum(inst.saldo_total() for inst in self.instituicoes)