import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#################################################################################### Função para buscar clientes e mostrar na tabela
def buscar_cliente(event=None):  # Modificado para aceitar o evento de tecla
    for item in tree.get_children():
        tree.delete(item)

    conexao = sqlite3.connect('dados.db')
    c = conexao.cursor()

    nome_busca = campo_busca_nome.get()
    id_busca = campo_busca_recibo.get()

    # Verifica se há algum critério de busca
    if nome_busca:
        c.execute("SELECT * FROM dados WHERE nome LIKE ?", ('%' + nome_busca + '%',))
    elif id_busca:
        c.execute("SELECT * FROM dados WHERE id_recibo=?", (id_busca,))
    else:
        c.execute("SELECT * FROM dados")

    dados = c.fetchall()
    conexao.close()

    if not dados:  # Se a consulta não retornar resultados
        messagebox.showinfo("Resultado", "Nenhuma Dado Encontrado.")
        return  # Interrompe a função, não inserindo dados na árvore

    # Preenche a árvore com os dados retornados
    for dado in dados:
        tree.insert('', 'end', values=dado)


############################################################################################################### Função para excluir um recibo com senha
def excluir_recibo():
    try:
        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        
        # Pedir a senha para excluir
        senha = simpledialog.askstring("Senha", "Digite uma Senha para Excluir o Recibo:")
        
        if senha != "1":
            messagebox.showerror("Erro", "Senha Incorreta! Exclusão Não Autorizada.")
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


##################################################################################################### Função para gerar PDF do recibo selecionado
def gerar_pdf_recibo():
    try:
        # Verificando se o usuário selecionou uma linha na árvore
        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]

        # Conectando ao banco de dados para pegar os dados do recibo
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM dados WHERE id_recibo=?", (id_recibo,))
        dados = c.fetchone()
        conexao.close()

        if dados:
            # Criando o arquivo PDF com o nome do recibo
            caminho_pdf = f"recibo_{id_recibo}.pdf"
            c = canvas.Canvas(caminho_pdf, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Título do Recibo
            c.setFont("Helvetica-Bold", 16)
            c.drawString(220, 770, f"Recibo N°: {dados[0]}")
            
            # Adicionando informações do recibo
            c.setFont("Helvetica", 12)
            c.drawString(100, 730, f"Nome: {dados[1]}")
            c.drawString(100, 710, f"CPF/CNPJ: {dados[2]}")
            c.drawString(100, 690, f"Valor: R$ {dados[3]:.2f}")
            c.drawString(100, 670, f"Telefone: {dados[4]}")
            c.drawString(100, 650, f"Forma de Pagamento: {dados[5]}")
            c.drawString(100, 630, f"Data de Emissão: {dados[8]}")
            c.drawString(100, 610, f"Referente: {dados[6]}")
            c.drawString(100, 590, f"Observação: {dados[7]}")

            # Adicionando uma linha de separação
            c.setLineWidth(1)
            c.line(100, 580, 500, 580)  # Linha horizontal de separação

            # Mensagem de agradecimento (opcional)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(100, 570, "Agradecemos pela confiança! Este é um recibo oficial.")

            # Salvar o PDF
            c.save()

           
           
            # Exibir uma mensagem de sucesso
            messagebox.showinfo("Sucesso", f"PDF Gerado com Sucesso! Arquivo salvo como: {caminho_pdf}")
        else:
            messagebox.showerror("Erro", "Recibo não encontrado.")

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Gerar o PDF.")


############################################################################ Função para abrir a janela de inclusão de novos dados
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


    tk.Label(janela_inclusao, text="Referente:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    campo_referente_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_referente_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Observação:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    campo_observacao_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_observacao_inclusao.grid(row=6, column=1, padx=10, pady=5)

    # Obtendo a data atual no formato DD/MM/AAAA
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y")  # Formato desejado: dia/mês/ano
    tk.Label(janela_inclusao, text="Data de Emissão:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    campo_data_emissao_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_emissao_inclusao.grid(row=7, column=1, padx=10, pady=5)
    campo_data_emissao_inclusao.insert(0, data_atual)  # Inserindo a data no campo de "Data de Emissão"

#################################################################################################################################
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
            messagebox.showwarning("Atenção", "Nome, CNPJ e Valor são Campos Obrigatórios.")
            return

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor Inválido.")
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
            messagebox.showerror("Erro", f"Erro ao Salvar os Dados: {e}")

    btn_salvar_inclusao = tk.Button(janela_inclusao, text="Salvar", command=salvar_inclusao, bg="green", fg="white", relief="raised", padx=10, pady=5)
    btn_salvar_inclusao.grid(row=8, column=0, columnspan=2, pady=10)

###################################################################################################### Função para editar um recibo
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
        janela_editar.geometry("430x395")  # Aumenta o tamanho da janela

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

        tk.Label(janela_editar, text="Referente:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        campo_referente_editar = tk.Entry(janela_editar, width=40)
        campo_referente_editar.grid(row=5, column=1, padx=10, pady=5)
        campo_referente_editar.insert(0, dados[6])

        tk.Label(janela_editar, text="Observação:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        campo_observacao_editar = tk.Entry(janela_editar, width=40)
        campo_observacao_editar.grid(row=6, column=1, padx=10, pady=5)
        campo_observacao_editar.insert(0, dados[7])

        tk.Label(janela_editar, text="Data de Emissão:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
        campo_data_emissao_editar = tk.Entry(janela_editar, width=12)
        campo_data_emissao_editar.grid(row=7, column=1, padx=10, pady=5)
        campo_data_emissao_editar.insert(0, dados[8])
        

########################################################################## SALVAR EDICAO
        def salvar_edicao():
            nome = campo_nome_editar.get()
            cnpj = campo_cnpj_editar.get()
            valor = campo_valor_editar.get()
            telefone = campo_telefone_editar.get()
            forma_pagamento = campo_forma_pagamento_editar.get()
            referente = campo_referente_editar.get()
            observacao = campo_observacao_editar.get()
            data_emissao = campo_data_emissao_editar.get()

            if not nome or not cnpj or not valor:
                messagebox.showwarning("Atenção", "Nome, CPF/CNPJ e Valor são Campos Obrigatórios.")
                return

            try:
                valor = float(valor)
            except ValueError:
                messagebox.showerror("Erro", "Valor Inválido.")
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

                messagebox.showinfo("Sucesso", "Recibo Atualizado com Sucesso!")
                janela_editar.destroy()  # Fecha a janela de edição
                buscar_cliente()  # Atualiza a tabela de dados na janela principal

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao Atualizar os Dados: {e}")

        btn_salvar_edicao = tk.Button(janela_editar, text="Salvar", command=salvar_edicao, bg="green", fg="white", relief="raised", padx=10, pady=5)
        btn_salvar_edicao.grid(row=12, column=0, columnspan=2, pady=10)


    except IndexError:
        messagebox.showwarning("Atenção", "Selecione Antes Um Recibo para EDITAR.")
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
import os
############################################################# GERANDO O RELATORIO
def gerar_Rel():
    try:
        # Obter dados dos recibos no banco de dados
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()
        
        # Buscar todos os dados
        c.execute("SELECT * FROM dados")
        dados_recibos = c.fetchall()
        conexao.close()

        if not dados_recibos:
            messagebox.showwarning("Atenção", "Nenhum recibo encontrado para gerar o PDF.")
            return

        # Criar o arquivo PDF
        nome_arquivo = "relatorio_recibos.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        
        largura, altura = letter
        
        # Adicionar um título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, altura - 40, "Relatório de Recibos")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 10)
        y_position = altura - 60  # Posição inicial para o texto
        
        # Cabeçalho da tabela
        c.drawString(25, y_position, "N Recibo")
        c.drawString(120, y_position, "Nome")
        c.drawString(200, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor")
        c.drawString(400, y_position, "Data Emissão")
        c.drawString(500, y_position, "Referente")
        y_position -= 20  # Espaço após o cabeçalho

        # Preencher com os dados
        for dado in dados_recibos:
            c.drawString(30, y_position, str(dado[0]))  # Número do recibo (id_recibo)
            c.drawString(120, y_position, dado[1])  # Nome
            c.drawString(200, y_position, dado[2])  # CNPJ
            c.drawString(300, y_position, f"R$ {dado[3]:.2f}")  # Valor
            c.drawString(400, y_position, dado[7])  # Data de Emissão
            c.drawString(500, y_position, dado[8])  # OBS
            y_position -= 20
            
            if y_position < 50:  # Se a página estiver cheia, crie uma nova página
                c.showPage()
                y_position = altura - 40  # Reinicia a posição na nova página
                c.setFont("Helvetica", 10)
                c.drawString(30, y_position, "Número Recibo")
                c.drawString(120, y_position, "Nome")
                c.drawString(200, y_position, "CNPJ")
                c.drawString(300, y_position, "Valor")
                c.drawString(400, y_position, "Data Emissão")
                c.drawString(500, y_position, "Referente")
                y_position -= 20

        # Salvar o arquivo PDF
        c.save()
        
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abre o PDF gerado (Windows)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o PDF: {str(e)}")

# GERAR O PDF AQUI CONSTRUIR A EXTRUTURA AQUI DENTRO
def gerar_pdf():
    try:
        # Obter dados dos recibos no banco de dados
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()
        
        # Buscar todos os dados
        c.execute("SELECT * FROM dados")
        dados_recibos = c.fetchall()
        conexao.close()

        if not dados_recibos:
            messagebox.showwarning("Atenção", "Nenhum recibo encontrado para gerar o PDF.")
            return

        # Criar o arquivo PDF
        nome_arquivo = "relatorio_recibos.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        
        largura, altura = letter
        
        # Adicionar um título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, altura - 40, "Relatório de Recibos")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 10)
        y_position = altura - 60  # Posição inicial para o texto
        
        # Cabeçalho da tabela
        c.drawString(25, y_position, "N Recibo")
        c.drawString(120, y_position, "Nome")
        c.drawString(200, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor")
        c.drawString(400, y_position, "Data Emissão")
        c.drawString(500, y_position, "Referente")
        y_position -= 20  # Espaço após o cabeçalho

        # Preencher com os dados
        for dado in dados_recibos:
            c.drawString(30, y_position, str(dado[0]))  # Número do recibo (id_recibo)
            c.drawString(120, y_position, dado[1])  # Nome
            c.drawString(200, y_position, dado[2])  # CNPJ
            c.drawString(300, y_position, f"R$ {dado[3]:.2f}")  # Valor
            c.drawString(400, y_position, dado[7])  # Data de Emissão
            c.drawString(500, y_position, dado[8])  # OBS
            y_position -= 20
            
            if y_position < 50:  # Se a página estiver cheia, crie uma nova página
                c.showPage()
                y_position = altura - 40  # Reinicia a posição na nova página
                c.setFont("Helvetica", 10)
                c.drawString(30, y_position, "Número Recibo")
                c.drawString(120, y_position, "Nome")
                c.drawString(200, y_position, "CNPJ")
                c.drawString(300, y_position, "Valor")
                c.drawString(400, y_position, "Data Emissão")
                c.drawString(500, y_position, "Referente")
                y_position -= 20

        # Salvar o arquivo PDF
        c.save()
        
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abre o PDF gerado (Windows)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o PDF: {str(e)}")






############################################################################################################################################

# Tela principal
janela_principal = tk.Tk()
janela_principal.title("Sistema de Gestao - SigeFLEX")
janela_principal.geometry("1200x750")  # Ajusta o tamanho inicial da janela

# Campo de busca
tk.Label(janela_principal, text="Nome do Cliente:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca


tk.Label(janela_principal, text="Numero Recibo:").grid(row=0, column=1, padx=10, pady=10, sticky='w')
campo_busca_recibo = tk.Entry(janela_principal, width=15)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

# Colocar o foco no campo de busca "Nome" ao iniciar
campo_busca_nome.focus_set()

######################################################################################################################################


# Botões
btn_buscar = tk.Button(janela_principal, text="Buscar", command=buscar_cliente, bg="blue", fg="white")
btn_buscar.grid(row=0, column=2, padx=10, pady=10)

# Botão Incluir Novo
btn_incluir = tk.Button(janela_principal, text="Incluir Novo", command=abrir_janela_inclusao, bg="green", fg="white", width=10)
btn_incluir.grid(row=3, column=0, padx=10, pady=10)  # Coloca o botão na linha 1, coluna 2

# Botão Editar
btn_editar = tk.Button(janela_principal, text="Editar", command=editar_recibo, bg="brown", fg="white", width=10)
btn_editar.grid(row=4, column=0, padx=10, pady=10)  # Botão Editar agora está ao lado do Incluir Novo

# Botao EXCLUIR
btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=4, column=2, padx=10, pady=10)

# Botão Fechar
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="purple", fg="white")
btn_fechar.grid(row=4, column=3, padx=10, pady=10)  # Colocando o botão na linha 4, coluna 2

# Botão Gerar RELATORIO
btn_rel = tk.Button(janela_principal, text="Relatorio", command=gerar_Rel, bg="cyan", fg="black")
btn_rel.grid(row=1, column=2, padx=10, pady=10)

# Botao GERAR PDF - RECIBO
btn_pdf = tk.Button(janela_principal, text="Recibo", command=gerar_pdf_recibo, bg="cyan", fg="red")
btn_pdf.grid(row=1, column=3, padx=10, pady=10)


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
