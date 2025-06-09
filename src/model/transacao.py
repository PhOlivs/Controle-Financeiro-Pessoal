from datetime import datetime

class Transacao:
    def __init__(self, valor: float, tipo: str, categoria: str, descricao: str = "", datahora: datetime = None):
        self.valor = valor
        self.tipo = tipo  # "receita" ou "despesa"
        self.categoria = categoria
        self.descricao = descricao
        self.datahora = datahora or datetime.now()

    def __str__(self):
        sinal = "+" if self.tipo == "receita" else "-"
        return (f"[{self.datahora.strftime('%d/%m/%Y %H:%M')}] {sinal} R${self.valor:,.2f} "
                f"{self.categoria} - {self.descricao}")