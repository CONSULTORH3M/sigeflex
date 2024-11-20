# Gerador de recibo com gravaçao dos dado usando Sqlite
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
####################################################################### Função para BUSCAR CLIENTES e mostrar na tabela
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

################################################################## Função para EXCLUIR UM RECIBO com senha
def excluir_recibo():
    try:
        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        
        # Pedir a senha para excluir
        senha = simpledialog.askstring("Senha", "Digite a Senha para Excluir o Recibo:")
        
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

###############################################################Função para abrir a janela INCLUIR NOVO RECIBO de dados
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

def abrir_janela_inclusao():
    # Criando a janela de inclusão
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Incluir Novo Recibo")
    janela_inclusao.geometry("430x350")  # Aumentando o tamanho da janela, como no código de edição

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    janela_inclusao.grid_rowconfigure(8, weight=1, minsize=50)  # Garantir que a última linha tenha espaço para os botões

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_nome_inclusao.grid(row=0, column=1, padx=10, pady=5)
    campo_nome_inclusao.focus_set()

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
    data_atual = datetime.now().strftime("%d/%m/%Y")  # Agora você usa diretamente datetime.now()
    tk.Label(janela_inclusao, text="Data de Emissão:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    campo_data_emissao_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_emissao_inclusao.grid(row=7, column=1, padx=10, pady=5)
    campo_data_emissao_inclusao.insert(0, data_atual)

    # Função para salvar dados
    def salvar_inclusao():
        nome = campo_nome_inclusao.get()
        cnpj = campo_cnpj_inclusao.get()
        valor = campo_valor_inclusao.get()
        telefone = campo_telefone_inclusao.get()
        forma_pagamento = campo_forma_pagamento_inclusao.get()
        dataEmissao = campo_data_emissao_inclusao.get()
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
            ''', (nome, cnpj, valor, telefone, forma_pagamento, dataEmissao, referente, observacao))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Recibo Salvo com Sucesso!")
            janela_inclusao.destroy()
            buscar_cliente()  # Atualiza a tabela de dados na janela principal

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao Salvar os Dados: {e}")

    # Criando os botões na janela
    btn_salvar_inclusao = tk.Button(janela_inclusao, text="Salvar", command=salvar_inclusao, bg="green", fg="white", relief="raised", padx=10, pady=5)
    btn_salvar_inclusao.grid(row=8, column=0, padx=10, pady=10, sticky='ew')

    btn_pdf = tk.Button(janela_inclusao, text="Imprimir_PDF", command=gerar_recibo_na_tela, bg="blue", fg="white", relief="raised", padx=10, pady=5)
    btn_pdf.grid(row=8, column=1, padx=10, pady=10, sticky='ew')

#############################################################################Função para EDITAR\CORRIGIR\ALTERAR um recibo
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
        janela_editar.geometry("430x350")  # Aumenta o tamanho da janela

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
        campo_data_emissao_editar = tk.Entry(janela_editar, width=12)
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
        
########################################################################## SALVAR EDICAO
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
                conexao.commit()
                print("Alterações no banco de dados salvas com sucesso.")
                conexao.close()

                messagebox.showinfo("Sucesso", "Recibo Atualizado com Sucesso!")
                janela_editar.destroy()  # Fecha a janela de edição
                buscar_cliente()  # Atualiza a tabela de dados na janela principal

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao Atualizar os Dados: {e}")

        btn_salvar_edicao = tk.Button(janela_editar, text="Salvar", command=salvar_edicao, bg="green", fg="white", relief="raised", padx=10, pady=5)
        btn_salvar_edicao.grid(row=12, column=0, columnspan=2, pady=10)

        btn_pdf = tk.Button(janela_editar, text="Imprimir_PDF", command=gerar_recibo_na_tela, bg="blue", fg="white", relief="raised", padx=10, pady=5)
        btn_pdf.grid(row=12, column=1, columnspan=2, pady=10)

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione Antes Um Recibo para EDITAR.")

###########################################################################################  RELATORIO COM FILTROS
### PARA FAZER O FITLRO POR DATAS USAR ESSAS BIBLIOTECAS
import sqlite3
import tkinter
from datetime import datetime
from tkinter import simpledialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

######################################################################################### FUNCAO RELATORIO COM FILTRO DATA - falta ajustar
# Função para gerar o relatorio filtrado
def gerar_relatorio_filtrado():
    try:
        # Criar a janela para solicitar as datas
        janela_filtro = tk.Tk()
        janela_filtro.withdraw()  # Ocultar a janela principal

        # Solicitar as datas ao usuário
        data_inicio = simpledialog.askstring("Data Inicial", "Digite a data inicial (YYYY-MM-DD):", parent=janela_filtro)
        if not data_inicio:  # Verificar se o usuário cancelou ou não preencheu
            messagebox.showwarning("Atenção", "Data inicial não informada!")
            janela_filtro.quit()  # Fechar a aplicação se a data inicial não for informada
            return

        data_fim = simpledialog.askstring("Data Final", "Digite a data final (YYYY-MM-DD):", parent=janela_filtro)
        if not data_fim:  # Verificar se o usuário cancelou ou não preencheu
            messagebox.showwarning("Atenção", "Data final não informada!")
            janela_filtro.quit()  # Fechar a aplicação se a data final não for informada
            return

        # Reexibir a janela principal, caso necessário
        #janela_filtro.deiconify()  # Reexibe a janela principal (caso precise dela mais tarde)

        # Aqui você pode buscar os dados no banco de dados com base nas datas informadas
        # Exemplo de query para buscar os dados filtrados
        dados_recibos = buscar_dados_filtrados(data_inicio, data_fim)
        
        # Gerar o arquivo PDF
        nome_arquivo = "Relatorio_Recibos.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        largura, altura = letter

        # Adicionar um título ao PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, altura - 40, f"Relatório de Recibos - {data_inicio} a {data_fim}")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 10)
        y_position = altura - 60

        # Cabeçalho da tabela
        c.drawString(25, y_position, "N Recibo")
        c.drawString(120, y_position, "Nome")
        c.drawString(200, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor")
        c.drawString(400, y_position, "Data Emissão")
        c.drawString(500, y_position, "Referente")
        y_position -= 20

        # Preencher com os dados dos recibos
        for dado in dados_recibos:
            c.drawString(30, y_position, str(dado[0]))  # Número do recibo (id_recibo)
            c.drawString(120, y_position, dado[1])  # Nome
            c.drawString(200, y_position, dado[2])  # CPF/CNPJ
            c.drawString(300, y_position, f"R$ {dado[3]:.2f}")  # Valor
            c.drawString(400, y_position, dado[7])  # Data de Emissão
            c.drawString(500, y_position, dado[8])  # Referente
            y_position -= 20

            # Se a página estiver cheia, crie uma nova página
            if y_position < 50:
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

        # Informar o sucesso da geração do PDF
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abrir o arquivo PDF gerado

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o PDF: {str(e)}")
################################################################################################################################################
############################################################# GERANDO O RELATORIO TOTAL REGISTRADO NO BANCO DE DADOS
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
            messagebox.showwarning("Atenção", "Nenhum Recibo encontrado para gerar o Relatorio.")
            return

        # Criar o arquivo PDF
        nome_arquivo = "Relatorio_Recibos"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        
        largura, altura = letter
        
        # Adicionar um título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, altura - 40, "Relatorio GERAL de Todos Recibos")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 10)
        y_position = altura - 60  # Posição inicial para o texto
        
        # Cabeçalho da tabela
        c.drawString(25, y_position, "Nº Recibo")
        c.drawString(80, y_position, "Nome")
        c.drawString(165, y_position, "CPF/CNPJ")
        c.drawString(245, y_position, "Valor Pago")
        c.drawString(310, y_position, "Telefone") 
        c.drawString(380, y_position, "Data Emissão")
        c.drawString(450, y_position, "Forma")
        c.drawString(515, y_position, "Referente")

        y_position -= 20  # Espaço após o cabeçalho

        # Preencher com os dados
        for dado in dados_recibos:
            c.drawString(30, y_position, str(dado[0]))  # Número do recibo (id_recibo)
            c.drawString(50, y_position, dado[1])  # Nome
            c.drawString(165, y_position, dado[2])  # CNPJ
            c.drawString(245, y_position, f"R$ {dado[3]:.2f}")  # Valor
            c.drawString(310, y_position, dado[4])  # Telefone
            c.drawString(380, y_position, dado[6])  # Data de Emissão
            c.drawString(450, y_position, dado[5])  # Forma
            c.drawString(515, y_position, dado[7])  # Referente
        
            y_position -= 20
            
            if y_position < 50:  # Se a página estiver cheia, crie uma nova página
                c.showPage()
                y_position = altura - 40  # Reinicia a posição na nova página
                c.setFont("Helvetica", 10)
                c.drawString(30, y_position, "Nº Recibo")
                c.drawString(50, y_position, "Nome")
                c.drawString(165, y_position, "CNPJ")
                c.drawString(245, y_position, "Valor Pago")
                c.drawString(310, y_position, "Telefone")
                c.drawString(380, y_position, "Data Emissão")
                c.drawString(450, y_position, "Forma")
                c.drawString(515, y_position, "Referente")
                y_position -= 20

        # Salvar o arquivo PDF
        c.save()
        
        messagebox.showinfo("Sucesso", f"Relatorio gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abre o PDF gerado (Windows)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o Relatorio: {str(e)}")
        ############################################################################################################################
import platform
import subprocess

######################################################################################
######################################################################################LAYOUT NOVO
########################################################################################
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from num2words import num2words

#############################################################################################################################
#############################################################################################################################
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
from tkinter import simpledialog, messagebox
from num2words import num2words
import os

def gerar_recibo_padrao():
    try:
        # Solicitar o ID do recibo ao usuário
        id_recibo = simpledialog.askinteger("Informar ID", "Digite o ID do recibo que deseja imprimir:", minvalue=1)
        
        # Verificar se o usuário cancelou ou não forneceu um ID válido
        if id_recibo is None:
            messagebox.showwarning("Atenção", "ID do recibo não informado. A operação foi cancelada.")
            return
        
        # Conectar ao banco de dados
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Buscar os dados do recibo com o ID fornecido
        c.execute("SELECT * FROM dados WHERE id_recibo = ?", (id_recibo,))
        dado_recibo = c.fetchone()
        conexao.close()

        # Verificar se o recibo foi encontrado
        if not dado_recibo:
            messagebox.showwarning("Atenção", f"Nenhum recibo encontrado com o ID {id_recibo}.")
            return

        # Criar o arquivo PDF
        nome_arquivo = f"Recibo_{id_recibo}_Padrao.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        
        largura, altura = letter

        # Função para desenhar o recibo (para evitar repetição de código)
        def desenhar_recibo(y_position):
            # Adicionar o logotipo no cabeçalho (diminuir a posição y para não ter tanto espaço)
            logotipo = "logo.png"  # Substitua pelo caminho correto do seu logotipo
            c.drawImage(logotipo, 40, y_position, width=80, height=70)  # Ajuste o tamanho e posição conforme necessário

            c.setFont("Helvetica-Bold", 10)
            c.drawString(150, y_position + 40, "IMOBILIARIA LIDER 10.605.092/0001-97")

            c.setFont("Helvetica", 8)
# Ajuste para não sobrepor, agora cada linha tem seu próprio espaçamento
            c.drawString(150, y_position + 25, "www.imobiliariaportoxavier.com.br")
            y_position -= 15  # Ajuste o espaçamento para a próxima linha

            c.drawString(150, y_position + 25, "marcelobeutler@gmail.com Tel(55) 9 8116 -9772")
            y_position -= 15  # Ajuste o espaçamento para a próxima linha

            c.drawString(150, y_position + 10, "Rua Tiradentes, 606 Centro, Porto Xavier - RS")
            y_position -= 15  # Ajuste o espaçamento para logo abaixo dos dados da empresa
            

            # Adicionar um título
            c.setFont("Helvetica-Bold", 12)
            c.drawString(200, y_position, f"Recibo_{id_recibo}")
            y_position -= 15  # Espaço após o título

            # Adicionar as informações do recibo de forma vertical
            c.setFont("Helvetica", 8)
            y_position -= 10  # Ajuste de posição para o início do recibo

            # AQUI A CONVERSÃO: garantir que o valor de "R$ {dado_recibo[3]}" seja tratado como string corretamente
            valor_pago = dado_recibo[3]  # Certifique-se que dado_recibo[3] é float, que representa o valor pago
            valor_formatado = f"R$ {valor_pago:.2f}"  # Converte para string com a formatação de moeda

            # Converter o valor numérico para por extenso
            valor_por_extenso = num2words(valor_pago, lang='pt_BR')

            # Adicionar a frase fixa com variáveis
            frase_fixa1 = f"RECEBEMOS DE: {dado_recibo[1]}, CPF/CNPJ: {dado_recibo[2]}, ENDEREÇO:__________________________________________, o valor de: {valor_formatado} ({valor_por_extenso}), referente a: {dado_recibo[7]}."
            
            # Função para quebrar o texto se for longo
            def quebrar_texto(texto, largura_maxima, y_position):
                palavras = texto.split(" ")  # Dividir o texto em palavras
                linha = ""
                for palavra in palavras:
                    # Verificar se a largura da linha com a nova palavra ultrapassa a largura máxima
                    if c.stringWidth(linha + palavra, "Helvetica", 10) < largura_maxima:
                        linha += palavra + " "
                    else:
                        # Se ultrapassar, desenha a linha e começa uma nova
                        c.drawString(25, y_position, linha)
                        y_position -= 12  # Desce para a próxima linha
                        linha = palavra + " "  # Começa uma nova linha com a palavra atual
                # Desenha o restante da linha
                c.drawString(25, y_position, linha)
                return y_position

            # Chama a função para quebrar a linha da frase fixa
            y_position = quebrar_texto(frase_fixa1, largura - 50, y_position)

            # Descer para a próxima linha após a frase fixa
            y_position -= 20  # Ajuste do espaçamento

            # Adicionar as informações do recibo
            c.drawString(25, y_position, "COMPOSICAO DO RECIBO:")
            c.drawString(100, y_position, dado_recibo[5])  # COMPOSIÇÃO DO RECIBO

            y_position -= 10  # Espaçamento entre as linhas

            c.drawString(25, y_position, "ALUGUEL:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # ALUGUEL

            y_position -= 10
            c.drawString(25, y_position, "ÁGUA:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # AGUA

            y_position -= 10
            c.drawString(25, y_position, "LUZ:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # LUZ
            
            y_position -= 10
            c.drawString(25, y_position, "CONDOMINIO:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # CONDOMINIO
            
            y_position -= 10
            c.drawString(25, y_position, "IPTU:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # IPTU
            
            y_position -= 10
            c.drawString(25, y_position, "Internet:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # Internet

            y_position -= 10
            c.drawString(25, y_position, "Limpeza:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # Limpeza

            y_position -= 10
            c.drawString(25, y_position, "Outros:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # Outros
            
            y_position -= 10
            c.drawString(25, y_position, "-DESCONTOS:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # Forma

            y_position -= 10
            c.drawString(25, y_position, "TOTAL LIQUIDO:")
            c.drawString(100, y_position, f"R$ {dado_recibo[3]:.2f}")  # Referente

            y_position -= 40
            frase_fixa2 = f"                                                                         ASS:--------------------------------                  "
            y_position = quebrar_texto(frase_fixa2, largura - 50, y_position)

            y_position -= 10
            frase_fixa3 = f"              PORTO XAVIER - RS                               IMOBILIARIA LIDER                   {dado_recibo[6]}"
            y_position = quebrar_texto(frase_fixa3, largura - 50, y_position)

            return y_position

        # Desenha o primeiro recibo (posição inicial é y=altura-100)
        desenhar_recibo(altura - 80)

        # Ajuste da posição para o segundo recibo (para garantir que as informações não se sobreponham)
        y_position_segunda_via = altura / 3 + 30  # Espaço de 20 unidades abaixo da metade da página
        desenhar_recibo(y_position_segunda_via)

        # Salvar o arquivo PDF
        c.save()
        
        messagebox.showinfo("Sucesso", f"Recibo gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abre o PDF gerado (Windows)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o Recibo: {str(e)}")







####################################################################################################################
########################################################################### Função para gerar IMPRIMIR PDF do recibo selecionado = MODELO NORMAL
def gerar_pdf():
    try:
        # Verificando se o usuário selecionou uma linha na Grid que mostra os recibos
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
            c.drawString(100, 630, f"Observação: {dados[8]}")
            c.drawString(100, 610, f"Referente: {dados[7]}")
            c.drawString(100, 590, f"Data de Emissão: {dados[6]}")
            c.drawString(100, 550, "PORTO XAVIER - RS IMOBILIARIA LIDER    ____________________________ DATA ______/_____/______")


            # Adicionando uma linha de separação
            c.setLineWidth(1)
            c.line(100, 580, 500, 50)  # Linha horizontal de separação

            # Mensagem de agradecimento (opcional)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(100, 530, "Imobiliaria Lider ____________________________________ ")

            
            c.drawString(100, 570, "-------------------------------------------------------------------------------------")

            # Salvar o PDF
            c.save()
         
           
            # Exibir uma mensagem de sucesso
            messagebox.showinfo("Sucesso", f"PDF Gerado com Sucesso! Arquivo salvo como: {caminho_pdf}")
        else:
            messagebox.showerror("Erro", "Recibo não encontrado.")

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Gerar o PDF.")

############################################################################################################################################
# INTERFACE GRAFICA DA JANELA PRINCIPAL DO SISTEMA, PRIMEIRA JANELA QUE ABRE
# Tela principal
janela_principal = tk.Tk()
janela_principal.title("Sistema de Gestao - SigeFLEX")
janela_principal.geometry("1200x650")  # Ajusta o tamanho inicial da janela

# Campo de busca CLIENTE
tk.Label(janela_principal, text="Nome do Cliente:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

# Campo de busca RECIBO
tk.Label(janela_principal, text="Numero Recibo:").grid(row=0, column=1, padx=10, pady=10, sticky='w')
campo_busca_recibo = tk.Entry(janela_principal, width=15)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

# Colocar o foco no campo de busca "Nome" ao iniciar
campo_busca_nome.focus_set()

######################################################################################################################################
# TODOS OS BOTOES DA INTERFACE GRAFICA DA JANELA PRINCIPAL ##########################################################
# Botao BUSCAR
btn_buscar = tk.Button(janela_principal, text="BUSCAR", command=buscar_cliente, bg="blue", fg="white")
btn_buscar.grid(row=4, column=1, padx=10, pady=10)

# Botão INCLUIR NOVO
btn_incluir = tk.Button(janela_principal, text="Incluir NOVO", command=abrir_janela_inclusao, bg="green", fg="white", width=10)
btn_incluir.grid(row=3, column=0, padx=10, pady=10)  # Coloca o botão na linha 1, coluna 2

# Botão EDITAR
btn_editar = tk.Button(janela_principal, text="EDITAR", command=editar_recibo, bg="brown", fg="white", width=10)
btn_editar.grid(row=4, column=0, padx=10, pady=10)  # Botão Editar agora está ao lado do Incluir Novo

# Botao EXCLUIR
btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=3, column=1, padx=10, pady=10)

# Botão FECHAR
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="purple", fg="white")
btn_fechar.grid(row=4, column=3, padx=10, pady=10)  # Colocando o botão na linha 4, coluna 2

# Botão Gerar RELATORIO = FUNCAO GERAR_REL  LINHA 389
btn_rel = tk.Button(janela_principal, text="Relatorio GERAL-Todos", command=gerar_Rel, bg="cyan", fg="black")
btn_rel.grid(row=4, column=2, padx=10, pady=10)

# Botão IMPRIMIR PDF salva na pasta nao traz na tela
btn_pdf = tk.Button(janela_principal, text="SELECIONE IMPRIMIR", command=gerar_pdf, bg="cyan", fg="red")
btn_pdf.grid(row=0, column=3, padx=10, pady=10)

# Botao Imprimir na tela.. LAOYT NOVO.. A TRABALHAR
btn_recibo = tk.Button(janela_principal, text="NUMERO RECIBO", command=gerar_recibo_padrao, bg="cyan", fg="red")
btn_recibo.grid(row=1, column=3, padx=10, pady=10)

# Botao relatorio FILTRAR POR DATA - quase funcionando
btn_filtro = tk.Button(janela_principal, text="FILTRAR POR DATA", command=gerar_relatorio_filtrado, bg="cyan", fg="red")
btn_filtro.grid(row=0, column=2, padx=10, pady=10)
 
# Criando a árvore para mostrar os dados DOS RECIBOS A GRID MAIOR
cols = ("Numero Recibo", "Nome", "CPF/CNPJ", "Valor", "Telefone", "Forma de Pagamento", "Data de Emissão", "Referente", "Observação")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=120)

tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')  # Grid com expansibilidade PARA MOSTRAR DADOS RECIBOS

# Ajustando a tela para que a árvore ocupe o restante da janela
janela_principal.grid_rowconfigure(1, weight=1)
janela_principal.grid_columnconfigure(0, weight=1)
janela_principal.grid_columnconfigure(1, weight=1)

janela_principal.mainloop()
