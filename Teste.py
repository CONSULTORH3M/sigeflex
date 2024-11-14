import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3

# Função para buscar clientes e mostrar na tabela
def buscar_cliente(event=None):  # Modificado para aceitar o evento de tecla
    for item in tree.get_children():
        tree.delete(item)

    conexao = sqlite3.connect('dados.db')
    c = conexao.cursor()

    nome_busca = campo_busca_nome.get()
    id_busca = campo_busca_recibo.get()

    if nome_busca:
        c.execute("SELECT * FROM dados WHERE nome LIKE ?", ('%' + nome_busca + '%',))
    elif id_busca:
        c.execute("SELECT * FROM dados WHERE id_recibo=?", (id_busca,))
    else:
        c.execute("SELECT * FROM dados")

    dados = c.fetchall()
    for dado in dados:
        tree.insert('', 'end', values=dado)

    conexao.close()

# Função para excluir um recibo com senha
def excluir_recibo():
    try:
        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        
        # Pedir a senha para excluir
        senha = simpledialog.askstring("Senha", "Digite uma Senha para Excluir um Recibo:")
        
        if senha != "1":
            messagebox.showerror("Erro", "Senha Incorreta! Exclução não autorizada.")
            return

        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Excluir o recibo selecionado
        c.execute("DELETE FROM dados WHERE id_recibo=?", (id_recibo,))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Recibo Excluído com Sucesso!")

        # Atualiza a tabela
        buscar_cliente()

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Excluir.")

# Função para abrir a janela de inclusão de novos dados
def abrir_janela_inclusao():
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Incluir Novo Recibo")
    janela_inclusao.geometry("430x295")

    tk.Label(janela_inclusao, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_nome_inclusao.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="CPF/CNPJ:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    campo_cnpj_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_cnpj_inclusao.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Valor:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    campo_valor_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_valor_inclusao.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    campo_telefone_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_telefone_inclusao.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Forma de Pagamento:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    campo_forma_pagamento_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_forma_pagamento_inclusao.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Data de Emissão:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    campo_data_emissao_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_data_emissao_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Referente:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    campo_referente_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_referente_inclusao.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Observação:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    campo_observacao_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_observacao_inclusao.grid(row=7, column=1, padx=10, pady=5)

    def salvar_inclusao():
        nome = campo_nome_inclusao.get()
        cnpj = campo_cnpj_inclusao.get()
        valor = campo_valor_inclusao.get()
        telefone = campo_telefone_inclusao.get()
        forma_pagamento = campo_forma_pagamento_inclusao.get()
        data_emissao = campo_data_emissao_inclusao.get()
        referente = campo_referente_inclusao.get()
        observacao = campo_observacao_inclusao.get()

        if not nome or not cnpj or not valor:
            messagebox.showwarning("Atenção", "Nome, CNPJ e Valor são campos obrigatórios.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        try:
            conexao = sqlite3.connect('dados.db')
            c = conexao.cursor()
            c.execute(''' 
                INSERT INTO dados (nome, cnpj, valor, telefone, formaPag, dataEmissao, referente, observacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cnpj, valor, telefone, forma_pagamento, data_emissao, referente, observacao))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Recibo Salvo com Sucesso!")
            janela_inclusao.destroy()  # Fecha a janela de inclusão
            buscar_cliente()  # Atualiza a tabela de dados na janela principal

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar os dados: {e}")

    btn_salvar_inclusao = tk.Button(janela_inclusao, text="Salvar", command=salvar_inclusao, bg="green", fg="white", relief="raised", padx=10, pady=5)
    btn_salvar_inclusao.grid(row=8, column=0, columnspan=2, pady=10)

# Função para editar um recibo
def editar_recibo():
    try:
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado da tabela
        id_recibo = tree.item(item_selecionado)['values'][0]  # Obtém o ID do recibo selecionado

        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Busca os dados do recibo selecionado
        c.execute("SELECT * FROM dados WHERE id_recibo=?", (id_recibo,))
        dados = c.fetchone()

        # Cria a janela de edição
        janela_editar = tk.Toplevel(janela_principal)
        janela_editar.title(f"Editando Recibo {id_recibo}")
        janela_editar.geometry("430x295")  # Aumenta o tamanho da janela

        # Exibe os dados nos campos para edição
        tk.Label(janela_editar, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        campo_nome_editar = tk.Entry(janela_editar, width=40)
        campo_nome_editar.grid(row=0, column=1, padx=10, pady=5)
        campo_nome_editar.insert(0, dados[1])

        tk.Label(janela_editar, text="CPF/CNPJ:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        campo_cnpj_editar = tk.Entry(janela_editar, width=40)
        campo_cnpj_editar.grid(row=1, column=1, padx=10, pady=5)
        campo_cnpj_editar.insert(0, dados[2])

        tk.Label(janela_editar, text="Valor:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        campo_valor_editar = tk.Entry(janela_editar, width=40)
        campo_valor_editar.grid(row=2, column=1, padx=10, pady=5)
        campo_valor_editar.insert(0, dados[3])

        tk.Label(janela_editar, text="Telefone:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        campo_telefone_editar = tk.Entry(janela_editar, width=40)
        campo_telefone_editar.grid(row=3, column=1, padx=10, pady=5)
        campo_telefone_editar.insert(0, dados[4])

        tk.Label(janela_editar, text="Forma de Pagamento:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        campo_forma_pagamento_editar = tk.Entry(janela_editar, width=40)
        campo_forma_pagamento_editar.grid(row=4, column=1, padx=10, pady=5)
        campo_forma_pagamento_editar.insert(0, dados[5])

        tk.Label(janela_editar, text="Data de Emissão:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        campo_data_emissao_editar = tk.Entry(janela_editar, width=40)
        campo_data_emissao_editar.grid(row=5, column=1, padx=10, pady=5)
        campo_data_emissao_editar.insert(0, dados[6])

        tk.Label(janela_editar, text="Referente:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        campo_referente_editar = tk.Entry(janela_editar, width=40)
        campo_referente_editar.grid(row=6, column=1, padx=10, pady=5)
        campo_referente_editar.insert(0, dados[7])

        tk.Label(janela_editar, text="Observação:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
        campo_observacao_editar = tk.Entry(janela_editar, width=40)
        campo_observacao_editar.grid(row=7, column=1, padx=10, pady=5)
        campo_observacao_editar.insert(0, dados[8])

        def salvar_edicao():
            nome = campo_nome_editar.get()
            cnpj = campo_cnpj_editar.get()
            valor = campo_valor_editar.get()
            telefone = campo_telefone_editar.get()
            forma_pagamento = campo_forma_pagamento_editar.get()
            data_emissao = campo_data_emissao_editar.get()
            referente = campo_referente_editar.get()
            observacao = campo_observacao_editar.get()

            if not nome or not cnpj or not valor:
                messagebox.showwarning("Atenção", "Nome, CPF/CNPJ e Valor são campos obrigatórios.")
                return

            try:
                valor = float(valor)
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")
                return

            try:
                conexao = sqlite3.connect('dados.db')
                c = conexao.cursor()

                c.execute(''' 
                    UPDATE dados
                    SET nome=?, cnpj=?, valor=?, telefone=?, formaPag=?, dataEmissao=?, referente=?, observacao=?
                    WHERE id_recibo=?
                ''', (nome, cnpj, valor, telefone, forma_pagamento, data_emissao, referente, observacao, id_recibo))

                conexao.commit()
                conexao.close()

                messagebox.showinfo("Sucesso", "Recibo atualizado com Sucesso!")
                janela_editar.destroy()  # Fecha a janela de edição
                buscar_cliente()  # Atualiza a tabela de dados na janela principal

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar os dados: {e}")

        btn_salvar_edicao = tk.Button(janela_editar, text="Salvar", command=salvar_edicao, bg="green", fg="white", relief="raised", padx=10, pady=5)
        btn_salvar_edicao.grid(row=8, column=0, columnspan=2, pady=10)

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione Antes Um Recibo para EDITAR.")

# Tela principal
janela_principal = tk.Tk()
janela_principal.title("Sistema de Gestao - SigeFLEX")
janela_principal.geometry("1200x600")  # Ajusta o tamanho inicial da janela

# Campo de busca
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

campo_busca_recibo = tk.Entry(janela_principal, width=40)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

######################################################################################################################################
# Botões
btn_buscar = tk.Button(janela_principal, text="Buscar", command=buscar_cliente, bg="blue", fg="white")
btn_buscar.grid(row=0, column=2, padx=10, pady=10)

btn_incluir = tk.Button(janela_principal, text="Incluir Novo", command=abrir_janela_inclusao, bg="green", fg="white")
btn_incluir.grid(row=1, column=2, padx=10, pady=10)  # Coloca o botão na linha 2, coluna 2

# Mudei o botão Editar para a linha 2, na mesma coluna (2)
btn_editar = tk.Button(janela_principal, text="Editar", command=editar_recibo, bg="orange", fg="white")
btn_editar.grid(row=1, column=3, padx=10, pady=10)  # Botão Editar agora está ao lado do Incluir Novo

btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=2, column=2, padx=10, pady=10)

##################################################################################################################
# Botão Fechar
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="purple", fg="white")
btn_fechar.grid(row=4, column=2, padx=10, pady=10)  # Colocando o botão na linha 4, coluna 2

# Criando a árvore para mostrar os dados
cols = ("Numero Recibo", "Nome", "CPF/CNPJ", "Valor", "Telefone", "Forma de Pagamento", "Data de Emissão", "Referente", "Observação")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=120)

tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')  # Grid com expansibilidade

# Ajustando a tela para que a árvore ocupe o restante da janela
janela_principal.grid_rowconfigure(1, weight=1)
janela_principal.grid_columnconfigure(0, weight=1)
janela_principal.grid_columnconfigure(1, weight=1)

janela_principal.mainloop()
