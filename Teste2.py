import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Importação corrigida do simpledialog
import sqlite3

# Função para inicializar o banco de dados e criar a tabela se não existir
def inicializar_tabela():
    conexao = sqlite3.connect('clientes.db')
    c = conexao.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS clientes (
            id_recibo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cnpj TEXT,
            valor REAL,
            telefone TEXT,
            formaPag TEXT,
            dataEmissao TEXT,
            referente TEXT,
            observacao TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para buscar clientes na base de dados
def buscar_cliente():
    nome_cliente = campo_busca_nome.get()  # Obtém o valor digitado no campo de busca de nome
    numero_recibo = campo_busca_recibo.get()  # Obtém o valor digitado no campo de busca de número do recibo
    
    # Conectando ao banco de dados
    conexao = sqlite3.connect('clientes.db')
    c = conexao.cursor()

    # Verifica se foi preenchido algum dos campos
    if nome_cliente or numero_recibo:
        query = "SELECT * FROM clientes WHERE "
        conditions = []
        params = []

        if nome_cliente:
            conditions.append("nome LIKE ?")
            params.append(f'%{nome_cliente}%')

        if numero_recibo:
            conditions.append("id_recibo = ?")
            params.append(numero_recibo)

        query += " AND ".join(conditions)

        # Executa a consulta com base nos parâmetros fornecidos
        c.execute(query, tuple(params))
    else:
        # Se nenhum campo de filtro for preenchido, mostra todos os clientes
        c.execute("SELECT * FROM clientes")

    # Recuperando todos os dados
    clientes = c.fetchall()
    conexao.close()

    # Limpa a tabela antes de mostrar os novos resultados
    for item in tree.get_children():
        tree.delete(item)

    # Adiciona os dados filtrados na tabela
    if clientes:
        for cliente in clientes:
            tree.insert("", "end", values=cliente)
    else:
        messagebox.showinfo("Resultado", "Nenhum cliente encontrado com esses critérios.")

# Função para salvar dados (placeholder)
def salvar_dados():
    # Lógica de salvar dados (você já tem essa parte no seu código)
    pass

# Função para editar recibo (placeholder)
def editar_recibo():
    # Lógica de editar recibo (você já tem essa parte no seu código)
    pass

# Função para excluir recibo (agora com a importação correta)
def excluir_recibo():
    senha = simpledialog.askstring("Confirmação", "Digite a senha para excluir o recibo:", show="*")
    if senha == "1":
        selecionado = tree.focus()
        if selecionado:
            dados_cliente = tree.item(selecionado, 'values')
            recibo_id = dados_cliente[0]  # Supondo que o ID seja a primeira coluna
            conexao = sqlite3.connect('clientes.db')
            c = conexao.cursor()
            c.execute("DELETE FROM clientes WHERE id_recibo = ?", (recibo_id,))
            conexao.commit()
            conexao.close()
            tree.delete(selecionado)
            messagebox.showinfo("Sucesso", "Recibo excluído com sucesso!")
        else:
            messagebox.showwarning("Erro", "Nenhum recibo selecionado para exclusão.")
    else:
        messagebox.showerror("Erro", "Senha incorreta! Exclusão cancelada.")

# Função para gerar recibo em PDF (já descrita anteriormente)
def gerar_recibo(cliente):
    # Aqui você já tem a lógica para gerar o recibo em PDF
    pass

# Janela Principal
janela_principal = tk.Tk()
janela_principal.title("Sistema de Recibos")
janela_principal.geometry("800x600")

# Janela de consulta e cadastro (dividida em 2 áreas)
frame_cadastro = tk.Frame(janela_principal)
frame_cadastro.pack(side=tk.TOP, fill=tk.X, pady=10)

# Campos de cadastro no topo
campo_nome = tk.Entry(frame_cadastro, width=40)
campo_nome.pack(padx=10, pady=2, side=tk.TOP)

campo_cnpj = tk.Entry(frame_cadastro, width=40)
campo_cnpj.pack(padx=10, pady=2, side=tk.TOP)

campo_valor = tk.Entry(frame_cadastro, width=40)
campo_valor.pack(padx=10, pady=2, side=tk.TOP)

campo_telefone = tk.Entry(frame_cadastro, width=40)
campo_telefone.pack(padx=10, pady=2, side=tk.TOP)

campo_forma_pagamento = tk.Entry(frame_cadastro, width=40)
campo_forma_pagamento.pack(padx=10, pady=2, side=tk.TOP)

campo_data_emissao = tk.Entry(frame_cadastro, width=40)
campo_data_emissao.pack(padx=10, pady=2, side=tk.TOP)

campo_referente = tk.Entry(frame_cadastro, width=40)
campo_referente.pack(padx=10, pady=2, side=tk.TOP)

campo_observacao = tk.Entry(frame_cadastro, width=40)
campo_observacao.pack(padx=10, pady=2, side=tk.TOP)

# Campos de busca e consulta (rodapé)
frame_botoes = tk.Frame(janela_principal)
frame_botoes.pack(side=tk.BOTTOM, fill=tk.X)

campo_busca_nome = tk.Entry(frame_botoes, width=30)
campo_busca_nome.pack(side=tk.LEFT, padx=5, pady=5)

campo_busca_recibo = tk.Entry(frame_botoes, width=30)
campo_busca_recibo.pack(side=tk.LEFT, padx=5, pady=5)

botao_buscar = tk.Button(frame_botoes, text="Buscar", command=buscar_cliente)
botao_buscar.pack(side=tk.LEFT, padx=5, pady=5)

# Botões de cadastro
botao_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar_dados)
botao_salvar.pack(side=tk.RIGHT, padx=5, pady=5)

botao_editar = tk.Button(frame_botoes, text="Editar", command=editar_recibo)
botao_editar.pack(side=tk.RIGHT, padx=5, pady=5)

botao_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir_recibo)
botao_excluir.pack(side=tk.RIGHT, padx=5, pady=5)

# Tabela de resultados (Treeview)
tree = ttk.Treeview(janela_principal, columns=("ID", "Nome", "CNPJ", "Valor", "Telefone", "Forma Pagamento", "Data Emissão", "Referente", "Observação"), show="headings")
tree.pack(fill="both", expand=True)

# Definir cabeçalhos e colunas
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Inicializa a tabela e a interface
inicializar_tabela()

# Rodando a interface gráfica
janela_principal.mainloop()
