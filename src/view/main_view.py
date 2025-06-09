import tkinter as tk
from tkinter import ttk, messagebox
from controller.financeiro_controller import FinanceiroController
from util.formatador import formatar_moeda
from datetime import datetime

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle Financeiro Pessoal")
        self.root.configure(bg="#f5f6fa")
        self.controller = FinanceiroController()

        self.setup_ui()
        self.atualizar_interface()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10), background="#f5f6fa")
        style.configure("TEntry", font=("Segoe UI", 10))

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Valor
        ttk.Label(main_frame, text="Valor:").grid(row=0, column=0, sticky="w")
        self.valor_entry = ttk.Entry(main_frame)
        self.valor_entry.grid(row=0, column=1, sticky="ew")

        # Tipo
        ttk.Label(main_frame, text="Tipo:").grid(row=1, column=0, sticky="w")
        self.tipo_var = tk.StringVar(value="receita")
        self.tipo_combo = ttk.Combobox(main_frame, textvariable=self.tipo_var, values=["receita", "despesa"], state="readonly")
        self.tipo_combo.grid(row=1, column=1, sticky="ew")

        # Categoria
        ttk.Label(main_frame, text="Categoria:").grid(row=2, column=0, sticky="w")
        self.cat_entry = ttk.Entry(main_frame)
        self.cat_entry.grid(row=2, column=1, sticky="ew")

        # Descrição
        ttk.Label(main_frame, text="Descrição:").grid(row=3, column=0, sticky="w")
        self.desc_entry = ttk.Entry(main_frame)
        self.desc_entry.grid(row=3, column=1, sticky="ew")

        # Botão Adicionar
        self.add_btn = ttk.Button(main_frame, text="Adicionar", command=self.adicionar_transacao)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=(10, 10), sticky="ew")

        # Saldo
        self.saldo_label = ttk.Label(main_frame, text="Saldo: R$0,00", font=("Segoe UI", 14, "bold"), foreground="#2980b9")
        self.saldo_label.grid(row=5, column=0, columnspan=2, pady=(10, 10))

        # --- Instituições Bancárias ---
        ttk.Label(main_frame, text="Instituição:").grid(row=6, column=0, sticky="w")
        self.inst_nome_entry = ttk.Entry(main_frame)
        self.inst_nome_entry.grid(row=6, column=1, sticky="ew")

        ttk.Label(main_frame, text="Corrente:").grid(row=7, column=0, sticky="w")
        self.inst_corrente_entry = ttk.Entry(main_frame)
        self.inst_corrente_entry.grid(row=7, column=1, sticky="ew")

        ttk.Label(main_frame, text="Poupança:").grid(row=8, column=0, sticky="w")
        self.inst_poupanca_entry = ttk.Entry(main_frame)
        self.inst_poupanca_entry.grid(row=8, column=1, sticky="ew")

        ttk.Label(main_frame, text="Investimentos:").grid(row=9, column=0, sticky="w")
        self.inst_invest_entry = ttk.Entry(main_frame)
        self.inst_invest_entry.grid(row=9, column=1, sticky="ew")

        self.add_inst_btn = ttk.Button(main_frame, text="Adicionar Instituição", command=self.adicionar_instituicao)
        self.add_inst_btn.grid(row=10, column=0, columnspan=2, pady=(10, 10), sticky="ew")

        # Filtros
        filtro_frame = ttk.Frame(self.root, padding=(20, 5))
        filtro_frame.grid(row=1, column=0, sticky="ew")

        ttk.Label(filtro_frame, text="Tipo:").grid(row=0, column=0)
        self.filtro_tipo = ttk.Combobox(filtro_frame, values=["Todos", "Receita", "Despesa"], state="readonly", width=10)
        self.filtro_tipo.set("Todos")
        self.filtro_tipo.grid(row=0, column=1, padx=5)

        ttk.Label(filtro_frame, text="Mês:").grid(row=0, column=2)
        self.filtro_mes = ttk.Combobox(filtro_frame, values=["Todos"] + [f"{i:02d}" for i in range(1, 13)], state="readonly", width=5)
        self.filtro_mes.set("Todos")
        self.filtro_mes.grid(row=0, column=3, padx=5)

        ttk.Label(filtro_frame, text="Ano:").grid(row=0, column=4)
        ano_atual = datetime.now().year
        self.filtro_ano = ttk.Combobox(filtro_frame, values=["Todos"] + [str(ano_atual + i) for i in range(-5, 6)], state="readonly", width=7)
        self.filtro_ano.set("Todos")
        self.filtro_ano.grid(row=0, column=5, padx=5)

        self.filtro_tipo.bind("<<ComboboxSelected>>", lambda e: self.atualizar_interface())
        self.filtro_mes.bind("<<ComboboxSelected>>", lambda e: self.atualizar_interface())
        self.filtro_ano.bind("<<ComboboxSelected>>", lambda e: self.atualizar_interface())

        # Lista de transações (Treeview) com Data/Hora
        columns = ("datahora", "tipo", "categoria", "descricao", "valor")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
        self.tree.heading("datahora", text="Data/Hora")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("valor", text="Valor")
        self.tree.column("datahora", width=120, anchor="center")
        self.tree.column("tipo", width=80, anchor="center")
        self.tree.column("categoria", width=120, anchor="center")
        self.tree.column("descricao", width=180, anchor="w")
        self.tree.column("valor", width=100, anchor="e")
        self.tree.grid(row=11, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

        # Lista de instituições bancárias
        self.inst_tree = ttk.Treeview(main_frame, columns=("nome", "corrente", "poupanca", "investimentos", "total"), show="headings", height=5)
        self.inst_tree.heading("nome", text="Instituição")
        self.inst_tree.heading("corrente", text="Corrente")
        self.inst_tree.heading("poupanca", text="Poupança")
        self.inst_tree.heading("investimentos", text="Investimentos")
        self.inst_tree.heading("total", text="Total")
        self.inst_tree.column("nome", width=120, anchor="center")
        self.inst_tree.column("corrente", width=100, anchor="e")
        self.inst_tree.column("poupanca", width=100, anchor="e")
        self.inst_tree.column("investimentos", width=120, anchor="e")
        self.inst_tree.column("total", width=120, anchor="e")
        self.inst_tree.grid(row=12, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(12, weight=1)

    def adicionar_transacao(self):
        try:
            valor = float(self.valor_entry.get())
            tipo = self.tipo_var.get()
            cat = self.cat_entry.get()
            desc = self.desc_entry.get()

            self.controller.adicionar_transacao(valor, tipo, cat, desc)
            self.atualizar_interface()

            self.valor_entry.delete(0, tk.END)
            self.cat_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")

    def adicionar_instituicao(self):
        try:
            nome = self.inst_nome_entry.get()
            corrente = float(self.inst_corrente_entry.get() or 0)
            poupanca = float(self.inst_poupanca_entry.get() or 0)
            investimentos = float(self.inst_invest_entry.get() or 0)

            if not nome:
                messagebox.showerror("Erro", "Informe o nome da instituição.")
                return

            self.controller.adicionar_instituicao(nome, corrente, poupanca, investimentos)
            self.atualizar_interface()

            self.inst_nome_entry.delete(0, tk.END)
            self.inst_corrente_entry.delete(0, tk.END)
            self.inst_poupanca_entry.delete(0, tk.END)
            self.inst_invest_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos para saldos.")

    def atualizar_interface(self):
        saldo = self.controller.obter_saldo()
        cor = "#27ae60" if saldo >= 0 else "#c0392b"
        self.saldo_label.config(text=f"Saldo: {formatar_moeda(saldo)}", foreground=cor)

        # Limpa a Treeview de transações
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtros
        tipo_filtro = self.filtro_tipo.get().lower()
        mes_filtro = self.filtro_mes.get()
        ano_filtro = self.filtro_ano.get()

        transacoes = self.controller.obter_transacoes()
        filtradas = []
        for t in transacoes:
            if tipo_filtro != "todos" and t.tipo != tipo_filtro:
                continue
            if mes_filtro != "Todos" and t.datahora.strftime("%m") != mes_filtro:
                continue
            if ano_filtro != "Todos" and t.datahora.strftime("%Y") != ano_filtro:
                continue
            filtradas.append(t)

        for t in filtradas:
            valor_formatado = formatar_moeda(t.valor)
            datahora_formatada = t.datahora.strftime("%d/%m/%Y %H:%M")
            self.tree.insert(
                "", "end",
                values=(datahora_formatada, t.tipo.title(), t.categoria, t.descricao, valor_formatado),
                tags=(t.tipo,)
            )
            self.tree.tag_configure("receita", foreground="#27ae60")
            self.tree.tag_configure("despesa", foreground="#c0392b")

        # Limpa a Treeview de instituições
        for item in self.inst_tree.get_children():
            self.inst_tree.delete(item)

        for inst in self.controller.listar_instituicoes():
            total = inst.saldo_total()
            self.inst_tree.insert(
                "", "end",
                values=(
                    inst.nome,
                    formatar_moeda(inst.saldo_corrente),
                    formatar_moeda(inst.saldo_poupanca),
                    formatar_moeda(inst.saldo_investimentos),
                    formatar_moeda(total)
                )
            )