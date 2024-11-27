# SISTEMA GDI DE RECIBO com GRAVACAO BANCO DE DADOS SQLYTE
import customtkinter as ctk
from tkinter import messagebox
import sys
import datetime  # Para pegar a data atual

# Função para determinar a senha válida com base na data
def obter_senha():
    # Data de referência: vamos definir a data inicial como sendo o primeiro dia do programa
    data_inicio = datetime.date(2024, 11, 25)  # Defina a data inicial aqui
    
    # Pegando a data de hoje
    data_atual = datetime.date.today()
    
    # Calculando a diferença em dias entre a data de início e a data atual
    dias_passados = (data_atual - data_inicio).days
    
    # Definindo a lógica para as senhas
    if dias_passados <= 10:
        return "1"  # Para os primeiros 7 dias
    elif dias_passados <= 10 + 365:  # Se passou mais de 10 dias, mas menos que 1 ano
        return "55"  # Para o próximo ano
    else:
        return "2"  # Depois de 1 ano, senha muda para "2"

# Função para a janela de boas-vindas
def janela_boas_vindas():
    janela_boas = ctk.CTk()
    janela_boas.title("Bem Vindo A GDI!")
    janela_boas.geometry("690x200")  # Tamanho da janela de boas-vindas
    janela_boas.resizable(False, False)

    # Adicionar mensagem de boas-vindas
    ctk.CTkLabel(janela_boas, text="Seja Bem-Vindo ao Sistema GDI! - INDIQUE PARA SEUS AMIGOS e CONHECIDOS!!!", font=("Arial", 16)).pack(pady=10)
    ctk.CTkLabel(janela_boas, text="***Realizado Correçoes e Melhorias como a Descriminaçao de Valores por Extenso. (VERSAO 2024.1)***", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(janela_boas, text="DÚVIDAS - (54)9 9104 - 1029 com Gláucio ou Envie E-mail = glauciogrando@gmail.com", font=("Arial", 16)).pack(pady=10)
    
    # Botão para continuar para a janela principal
    btn_continuar = ctk.CTkButton(janela_boas, text="Continuar -Enter", command=lambda: [janela_boas.destroy()])
    btn_continuar.pack(pady=20)

    # Associar o evento de pressionar a tecla Enter ao botão "Continuar"
    janela_boas.bind("<Return>", lambda event: btn_continuar.invoke())  # Chama a função associada ao botão

    janela_boas.mainloop()

# Função para verificar o login
def verificar_login():
    usuario = entry_usuario.get()
    senha_digitada = entry_senha.get()

    # Ler a senha válida com base na data
    senha_armazenada = obter_senha()

    # Verificar as credenciais (usuário fixo e senha dinâmica)
    if usuario == "PADRAO" and senha_digitada == senha_armazenada:
        janela_login.destroy()  # Fechar a janela de login
        janela_boas_vindas()  # Abrir a janela de boas-vindas
    else:
        messagebox.showerror("Erro", "SENHA ERRADA, Digite Novamente")

# Função para encerrar completamente o programa ao fechar a janela de login
def on_close():
    sys.exit()  # Encerra o programa completamente

# Janela de login
janela_login = ctk.CTk()
janela_login.title("Login")
janela_login.geometry("300x180")  # Tamanho da janela de login
janela_login.resizable(False, False)  # Impede redimensionamento

# Definindo o comportamento de fechamento da janela de login
janela_login.protocol("WM_DELETE_WINDOW", on_close)  # Fecha o programa ao clicar no X

# Widgets de login
ctk.CTkLabel(janela_login, text="Usuário:").grid(row=0, column=0, pady=10, padx=20)  # Label do usuário
entry_usuario = ctk.CTkEntry(janela_login)
entry_usuario.grid(row=0, column=1, pady=5, padx=20)  # Entrada do usuário
entry_usuario.insert(0, "PADRAO")  # Definir o nome de usuário padrão
entry_usuario.configure(state="disabled")  # Desabilitar o campo de usuário

ctk.CTkLabel(janela_login, text="Senha:").grid(row=1, column=0, pady=10, padx=20)  # Label da senha
entry_senha = ctk.CTkEntry(janela_login, show="*")  # A senha será escondida
entry_senha.grid(row=1, column=1, pady=5, padx=20)  # Entrada da senha

# Colocar o foco no campo de senha após 100ms
janela_login.after(100, lambda: entry_senha.focus())

# Botões "Login" e "Fechar"
btn_login = ctk.CTkButton(janela_login, text="Entrar", command=verificar_login)
btn_login.grid(row=2, column=0, pady=20, padx=20, sticky="w", columnspan=2)  # Fica abaixo da senha e ocupa as duas colunas

# Botão "Fechar" - Fica ao lado direito do botão "Login"
btn_fechar = ctk.CTkButton(janela_login, text="Fechar", command=on_close, fg_color="gray", width=10)  # Cor cinza e largura ajustada
btn_fechar.grid(row=2, column=1, pady=20, padx=10, sticky="e")  # Alinha o botão "Fechar" à direita

# Configurando o evento de pressionamento da tecla ENTER
janela_login.bind("<Return>", lambda event: verificar_login())  # Associa o Enter à função de login

# Inicia a interface gráfica da janela de login
janela_login.mainloop()

##############################################################################################################################
##############################################################################################################################
# Gerador de recibo com gravaçao as informaçoes no Banco de Dados usando Sqlite e demais função de um sistema BASE
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
#################################################### Função para BUSCAR CLIENTES e E MOSTRAR NA TELA ###################################
def buscar_cliente(event=None):  # Modificado para aceitar o evento de tecla
    for item in tree.get_children():
        tree.delete(item)

    conexao = sqlite3.connect('dados.db')
    c = conexao.cursor()

    nome_busca = campo_busca_nome.get()
    id_busca = campo_busca_recibo.get()

    # Verifica se há algum critério de busca
    if nome_busca:
        c.execute("SELECT * FROM dados WHERE nome LIKE ?", ('%' + nome_busca + '%',)) # Buscar por Nome do Cliente
    elif id_busca:
        c.execute("SELECT * FROM dados WHERE id_recibo=?", (id_busca,)) # Buscar pelo Numero do Recibo
    else:
        c.execute("SELECT * FROM dados ORDER BY ID_RECIBO DESC")

    dados = c.fetchall()
    conexao.close()
      
    if not dados:  # Se a consulta não retornar resultados
        messagebox.showinfo("Resultado", "Nenhuma Dado Encontrado.")
        return  # Interrompe a função, não inserindo dados na árvore

    # Preenche a árvore com os dados retornados
    for dado in dados:
        tree.insert('', 'end', values=dado)
#####################################################################################################################################################
################################################################## Função para EXCLUIR UM RECIBO com senha= 55 #####################################
def excluir_recibo():
    try:
        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        
        # Pedir a senha para excluir
        senha = simpledialog.askstring("Senha", "Digite a Senha para Excluir o Recibo:", show="*")
        # SENHA PADRAO PARA EXCLUIR RECIBO
        if senha != "55":
            messagebox.showerror("Erro", "Senha Incorreta! Exclusão Não Autorizada.")
            return

        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Excluir o recibo selecionado
        c.execute("DELETE FROM dados WHERE id_recibo=?", (id_recibo,))
        conexao.commit()
        conexao.close()
       
        messagebox.showinfo("Sucesso", "Recibo EXCLUIDO com Sucesso!")
        # Atualiza a tabela
        buscar_cliente()
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Excluir.")
############################################################################################################################################
##################################################### FUNCAO para abrir a janela INCLUIR NOVO RECIBO e SALVAR BANCO DE DADOS #################
def abrir_janela_inclusao():
    # Criando a janela de inclusão
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Incluindo Novo Recibo")
    janela_inclusao.geometry("500x520")
    janela_inclusao.resizable(False, False)

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    janela_inclusao.grid_rowconfigure(15, weight=1, minsize=50)  # Garantir que a última linha tenha espaço para os botões

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_nome_inclusao.grid(row=0, column=1, padx=10, pady=5)
    campo_nome_inclusao.focus_set()

    tk.Label(janela_inclusao, text="CPF/CNPJ:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    campo_cnpj_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_cnpj_inclusao.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Endereco:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    campo_endereco_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_endereco_inclusao.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Referente:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    campo_referente_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_referente_inclusao.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="ALUGUEL:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    campo_aluguel_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_aluguel_inclusao.grid(row=4, column=1, padx=10, pady=5)
  
    tk.Label(janela_inclusao, text="Água:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    campo_agua_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_agua_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Luz:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    campo_luz_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_luz_inclusao.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Condomínio:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    campo_condominio_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_condominio_inclusao.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="IPTU:").grid(row=8, column=0, padx=10, pady=5, sticky='w')
    campo_iptu_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_iptu_inclusao.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Internet:").grid(row=9, column=0, padx=10, pady=5, sticky='w')
    campo_internet_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_internet_inclusao.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Limpeza:").grid(row=10, column=0, padx=10, pady=5, sticky='w')
    campo_limpeza_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_limpeza_inclusao.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Outros:").grid(row=11, column=0, padx=10, pady=5, sticky='w')
    campo_outros_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_outros_inclusao.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="DESCONTOS:").grid(row=12, column=0, padx=10, pady=5, sticky='w')
    campo_descontos_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_descontos_inclusao.grid(row=12, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Observação:").grid(row=13, column=0, padx=10, pady=5, sticky='w')
    campo_observacao_inclusao = tk.Entry(janela_inclusao, width=40)
    campo_observacao_inclusao.grid(row=13, column=1, padx=10, pady=5)

    ##################### SALVANDO DATA ATUAL NO FORMULARIO ########################################################## 
    # Obtendo a data atual no formato DD/MM/AAAA
    data_atual = datetime.now().strftime("%d/%m/%Y")  # Agora você usa diretamente datetime.now()
    tk.Label(janela_inclusao, text="Data de Emissão:").grid(row=14, column=0, padx=10, pady=5, sticky='w')
    campo_data_emissao_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_emissao_inclusao.grid(row=14, column=1, padx=10, pady=5)
    campo_data_emissao_inclusao.insert(0, data_atual)

    ########################################################################################################################
    ##################### FUNÇÃO CALCULAR VALOR LIQUIDO = SOMA tudo - DESCONTO = VALOR LIQUIDO ##############################
    def calcular_valor_liquido():
        try:
            aluguel = float(campo_aluguel_inclusao.get())
            agua = float(campo_agua_inclusao.get() or 0)
            luz = float(campo_luz_inclusao.get() or 0)
            condominio = float(campo_condominio_inclusao.get() or 0)
            iptu = float(campo_iptu_inclusao.get() or 0)
            internet = float(campo_internet_inclusao.get() or 0)
            limpeza = float(campo_limpeza_inclusao.get() or 0)
            outros = float(campo_outros_inclusao.get() or 0)
            descontos = float(campo_descontos_inclusao.get() or 0)

            # Somando os valores e subtraindo os descontos
            valor_liquido = (aluguel + agua + luz + condominio + iptu + internet + limpeza + outros) - descontos

            return valor_liquido
        except ValueError:
            messagebox.showerror("Erro", "Por Favor, Insira Valores Numéricos válidos os Campos de Valor.")
            janela_inclusao.attributes('-topmost', True) 
            return 0
        
    def salvar_inclusao():
        nome = campo_nome_inclusao.get()
        cnpj = campo_cnpj_inclusao.get()
        endereco = campo_endereco_inclusao.get()
        aluguel = campo_aluguel_inclusao.get()

        valor_liquido = calcular_valor_liquido()  # Chama a função para calcular o valor líquido

        agua = campo_agua_inclusao.get()
        luz = campo_luz_inclusao.get()
        condominio = campo_condominio_inclusao.get()
        iptu = campo_iptu_inclusao.get()
        internet = campo_internet_inclusao.get()
        limpeza = campo_limpeza_inclusao.get()
        outros = campo_outros_inclusao.get()
        descontos = campo_descontos_inclusao.get()
        referente = campo_referente_inclusao.get()
        dataEmissao = campo_data_emissao_inclusao.get()
        observacao = campo_observacao_inclusao.get()

        if not nome or not aluguel:
            messagebox.showwarning("Atenção", "NOME e ALUGUEL são Campos Obrigatórios.")
            janela_inclusao.attributes('-topmost', True)
            return

        else:
            conexao = sqlite3.connect('dados.db')
            c = conexao.cursor()

        try:
        # Aqui fazemos o ajuste de validar os campos vazios para float, como isso pode ficar sem preencher os dados nos campos
            aluguel = float(aluguel) if aluguel else 0.0
            agua = float(agua) if agua else 0.0
            luz = float(luz) if luz else 0.0
            condominio = float(condominio) if condominio else 0.0
            iptu = float(iptu) if iptu else 0.0
            internet = float(internet) if internet else 0.0
            limpeza = float(limpeza) if limpeza else 0.0
            outros = float(outros) if outros else 0.0
            descontos = float(descontos) if descontos else 0.0
            valor_liquido = float(valor_liquido) if valor_liquido else 0.0

            c.execute(''' 
        INSERT INTO dados (nome, cnpj, endereco, aluguel, dataEmissao, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, referente, observacao, valor_liquido)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cnpj, endereco, f"{aluguel:.2f}", dataEmissao, f"{agua:.2f}", f"{luz:.2f}", f"{condominio:.2f}", f"{iptu:.2f}", f"{internet:.2f}", f"{limpeza:.2f}", f"{outros:.2f}", f"{descontos:.2f}", referente, observacao, f"{valor_liquido:.2f}"))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Recibo SALVO com Sucesso!")
            janela_inclusao.destroy()
            buscar_cliente()  # Atualiza a tabela de dados na janela principal

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao Salvar, Banco de dados Inexistente: {e}")

##########################################################################################################################################
################################ BOTOES QUE FICA DENTRO DA JANELA INCLUIR - SALVAR RECIBO BANCO DADOS ###################################
    # Botao  na Janela para SALVAR   
    btn_salvar_inclusao = tk.Button(janela_inclusao, text="SALVAR NOVO", command=salvar_inclusao, bg="green", fg="white", relief="raised", padx=10, pady=5)
    btn_salvar_inclusao.grid(row=15, column=1, padx=10, pady=10, sticky='ew')
   
    # BOTAO FECHAR JANELA
    btn_fechar = tk.Button(janela_inclusao, text="Fechar", command=janela_inclusao.destroy, bg="gray", fg="white")
    btn_fechar.grid(row=15, column=0, padx=10, pady=10, sticky="ew")  # Coloca o botão na próxima coluna, lado a lado

###################################################################################################################################################
################################################################ EDITAR RECIBOS ###################################################################
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

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
        janela_editar.title(f"EDITAR RECIBO {id_recibo}")
        janela_editar.geometry("400x520")
        janela_editar.resizable(False, False)

        # Define os campos e os respectivos índices
        campos = [
            ("Nome", 1), ("CPF/CNPJ", 2), ("Endereco", 3), ("Referente", 6), ("ALUGUEL", 4),
            ("Água", 8), ("Luz", 9), ("Condomínio", 10), ("IPTU", 11),
            ("Internet", 12), ("Limpeza", 13), ("Outros", 14), ("DESCONTOS", 15), ("Observação", 16), ("Data de Emissão", 7),
        ]

        entradas = {}  # Para armazenar os widgets Entry

        # Criar os rótulos e campos dinamicamente
        for i, (rotulo, indice) in enumerate(campos):
            tk.Label(janela_editar, text=f"{rotulo}:").grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entrada = tk.Entry(janela_editar, width=40)
            entrada.grid(row=i, column=1, padx=10, pady=5)
            entrada.insert(0, dados[indice])
            entradas[rotulo] = entrada

        # Função para calcular o VALOR_LIQUIDO
        def calcular_valor_liquido(valores):
            try:
                aluguel = float(valores.get("ALUGUEL", 0) or 0)
                agua = float(valores.get("Água", 0) or 0)
                luz = float(valores.get("Luz", 0) or 0)
                condominio = float(valores.get("Condomínio", 0) or 0)
                iptu = float(valores.get("IPTU", 0) or 0)
                internet = float(valores.get("Internet", 0) or 0)
                limpeza = float(valores.get("Limpeza", 0) or 0)
                outros = float(valores.get("Outros", 0) or 0)
                descontos = float(valores.get("DESCONTOS", 0) or 0)

                # Somando os valores e subtraindo os descontos
                valor_liquido = (aluguel + agua + luz + condominio + iptu + internet + limpeza + outros) - descontos

                return valor_liquido
            except ValueError:
                messagebox.showerror("Erro", "Por Favor, Insira Valores Numéricos Válidos nos Campos de Valor.")
                janela_editar.attributes('-topmost', True)
                return 0

        # Função para atualizar a árvore (Treeview)
        def atualizar_árvore():
            for item in tree.get_children():
                tree.delete(item)
            conexao = sqlite3.connect('dados.db')
            c = conexao.cursor()
            c.execute("SELECT * FROM dados ORDER BY ID_RECIBO DESC")
            todos_os_dados = c.fetchall()
            conexao.close()
            for dado in todos_os_dados:
                tree.insert("", "end", values=dado)

        # Função para salvar a edição
        def salvar_edicao():
            valores = {rotulo: entrada.get() for rotulo, entrada in entradas.items()}

            # Validações básicas
            if not valores.get("Nome", "").strip() or not valores.get("ALUGUEL", "").strip():
                messagebox.showwarning("Atenção", "Os campos NOME e ALUGUEL são Obrigatórios.")
                janela_editar.attributes('-topmost', True)
               
                return

            try:
                # Calcular o VALOR_LIQUIDO antes de salvar
                valor_liquido = calcular_valor_liquido(valores)

                # Conectar ao banco de dados e salvar a edição
                conexao = sqlite3.connect('dados.db')
                c = conexao.cursor()

                # Atualizar os dados no banco de dados
                c.execute("""
                    UPDATE dados
                    SET Nome = ?, CNPJ = ?, Endereco = ?, ALUGUEL = ?, Referente = ?, 
                        DataEmissao = ?, Agua = ?, Luz = ?, Condominio = ?, IPTU = ?, 
                        Internet = ?, Limpeza = ?, Outros = ?, DESCONTOS = ?, Observacao = ?, valor_liquido = ?
                    WHERE id_recibo = ?;
                """, (valores["Nome"], valores.get("CPF/CNPJ", ""), valores.get("Endereco", ""),
                      float(valores.get("ALUGUEL", 0) or 0), valores.get("Referente", ""),
                      valores.get("Data de Emissão", ""), float(valores.get("Água", 0) or 0),
                      float(valores.get("Luz", 0) or 0), float(valores.get("Condomínio", 0) or 0),
                      float(valores.get("IPTU", 0) or 0), float(valores.get("Internet", 0) or 0),
                      float(valores.get("Limpeza", 0) or 0), float(valores.get("Outros", 0) or 0),
                      float(valores.get("DESCONTOS", 0) or 0), valores.get("Observação", ""), valor_liquido, id_recibo))

                conexao.commit()
                conexao.close()

                # Atualizar a árvore e fechar a janela
                atualizar_árvore()
                messagebox.showinfo("Sucesso", "EDIÇÃO Salva com Sucesso!")
                janela_editar.destroy()

            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao Salvar, Banco de Dados Inexistente: {e}")
########################################################################################################################
######################################BOTOES DENTRO DA JANELA EDITAR RECIBOS############################################
        # Botão de salvar
        btn_salvar_edicao = tk.Button(janela_editar, text="SALVAR EDICÃO", command=salvar_edicao, bg="green", fg="white", relief="raised", padx=10, pady=5)
        btn_salvar_edicao.grid(row=len(campos), column=1, columnspan=2, padx=10, pady=10)
        btn_salvar_edicao.bind("<Return>", lambda event: salvar_edicao())

        # Botao fechar Janela EDICAO
        btn_fechar = tk.Button(janela_editar, text="Fechar", command=janela_editar.destroy, bg="gray", fg="white")
        btn_fechar.grid(row=len(campos), column=0, columnspan=1, pady=10, sticky="ew")  # Coloca o botão na próxima coluna, lado a lado

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Editar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao Editar o Recibo: {e}")
        
######################################################################################################################################################
############################################ FUNCAO PARA ATUALIZAR SEMPRE A GRID QUE MOSTRA OS RECIBOS, TELA PRINCIPAL ###############################
# Função para atualizar a árvore de dados
def atualizar_árvore():
    # Limpa a árvore
    for item in tree.get_children():
        tree.delete(item)

    # Conectar ao banco de dados e carregar os dados atualizados
    conexao = sqlite3.connect('dados.db')
    c = conexao.cursor()

    # Carregar os dados da tabela 'dados'
    c.execute("SELECT * FROM dados ORDER BY ID_RECIBO DESC")
    registros = c.fetchall()

    # Inserir os dados na árvore
    for registro in registros:
        tree.insert("", "end", values=registro)

    conexao.close()
###########################################################################################  RELATORIO COM FILTROS POR PERIODO DE DATAS
### PARA FAZER O FITLRO POR DATAS USAR ESSAS BIBLIOTECAS
import sqlite3
import tkinter
from datetime import datetime
from tkinter import simpledialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
############################################################################################################################################
########################################################### FUNCAO RELATORIO COM FILTRO DATA ###############################################
def buscar_recibos_por_data(data_inicio, data_fim):
    try:
        # Conectar ao banco de dados
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Executar a consulta SQL para buscar os recibos dentro do intervalo de datas
        query = """
            SELECT * FROM dados 
            WHERE dataEmissao BETWEEN ? AND ?
        """
        c.execute(query, (data_inicio, data_fim))
        dados_recibos = c.fetchall()

        conexao.close()

        return dados_recibos

    except sqlite3.Error as e:
        print(f"Erro ao consultar o Banco de Dados: {e}")
        return []
############################################################################################################################
########################################### FUNCAO DO FILTRO POR DATA FEITO ACIMA ##########################################

def gerar_relatorio_filtrado():
    try:
        # Criar a janela de filtro para solicitação da data inicial
        data_inicio = simpledialog.askstring("Data Inicio", "(ANO-MES-DIA):", parent=janela_principal)
        
        if not data_inicio:  # Verificar se o usuário cancelou ou não preencheu
            messagebox.showwarning("Atenção", "Data inicial não informada!")
            janela_principal.deiconify()  # Mostrar novamente a janela principal
            return

        janela_principal.update()

        # Criar a janela para a data final
        data_fim = simpledialog.askstring("Data Final", "(ANO-MES-DIA):", parent=janela_principal)
        
        if not data_fim:  # Verificar se o usuário cancelou ou não preencheu
            messagebox.showwarning("Atenção", "Data final não informada!")
            janela_principal.deiconify()  # Mostrar novamente a janela principal
            return

        # Converter as datas de formato 'YYYY-MM-DD' para 'DD/MM/YYYY'
        try:
            data_inicio_convertida = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%d/%m/%Y")
            data_fim_convertida = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use o formato 'YYYY-MM-DD'.")
            return

        # Buscar os dados filtrados usando o formato correto
        dados_recibos = buscar_recibos_por_data(data_inicio_convertida, data_fim_convertida)

        ########## SE QUISER MOSTRAR A IMPRESSÃO NA DEPURAÇAO DO CODIGO##########
        #print("Dados filtrados:", dados_recibos)  # Para depuração

        if not dados_recibos:
            messagebox.showwarning("Atenção", f"Não há Recibos para o Período de {data_inicio} a {data_fim}. Consulte (54) 9 9104 1029.")
            janela_principal.deiconify()  # Mostrar novamente a janela principal
            return
        
        # Gerar o arquivo PDF
        nome_arquivo = "Relatorio_Periodo.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        largura, altura = letter

        # Adicionar um título ao PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, altura - 40, f"Relatório de Recibos do Periodo - {data_inicio} a {data_fim}")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 10)
        y_position = altura - 60

        # Cabeçalho da tabela
        c.drawString(25, y_position, "Numero")
        c.drawString(65, y_position, "Nome")
        c.drawString(210, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor")
        c.drawString(370, y_position, "DESCONTOS")
        c.drawString(440, y_position, "Data Emissão")
        c.drawString(510, y_position, "Referente")
        y_position -= 20

        # Preencher com os dados dos recibos
        for dado in dados_recibos:
            c.drawString(30, y_position, str(dado[0]))  # Número do recibo (id_recibo)
            c.drawString(65, y_position, dado[1])  # Nome
            c.drawString(210, y_position, dado[2])  # CPF/CNPJ
            c.drawString(300, y_position, f"R$ {dado[4]:.2f}")  # Valor
            c.drawString(370, y_position, f"R$ {dado[5]:.2f}")  # Desconto
            c.drawString(440, y_position, dado[7])  # Data de Emissão
            c.drawString(510, y_position, dado[6])  # Referente
            y_position -= 20

            # Se a página estiver cheia, crie uma nova página
            if y_position < 50:
                c.showPage()
                y_position = altura - 40  # Reinicia a posição na nova página
                c.setFont("Helvetica", 10)
                c.drawString(30, y_position, "Número Recibo")
                c.drawString(65, y_position, "Nome")
                c.drawString(210, y_position, "CNPJ")
                c.drawString(300, y_position, "Valor")
                c.drawString(370, y_position, "Desconto")
                c.drawString(440, y_position, "Data Emissão")
                c.drawString(510, y_position, "Referente")
                y_position -= 20

        # Salvar o arquivo PDF
        c.save()

        # Informar o sucesso da geração do PDF
        messagebox.showinfo("Sucesso", f"RELATORIO POR PERIODO Gerado Com Sucesso! Arquivo Salvo como {nome_arquivo}")
        os.startfile(nome_arquivo)  # Abrir o arquivo PDF gerado

        janela_principal.deiconify()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao Gerar o Relatório: {str(e)}")
        janela_principal.deiconify()

################################################################################################################################################
################################################################################################################################################
################################################## GERANDO O RELATORIO TOTAL REGISTRADO NO BANCO DE DADOS + TOTALIZADOR NO FINAL
def gerar_Rel_Total():
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
        nome_arquivo = os.path.join(os.getcwd(), "Relatorio_TODOS_Recibos.pdf")  # Caminho absoluto

        # Verifique se o diretório de trabalho tem permissão para salvar o arquivo
        if not os.access(os.getcwd(), os.W_OK):
            messagebox.showerror("Erro", "Permissão de escrita no diretório não encontrada.")
            return
        
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        
        largura, altura = letter
        
        # Adicionar um título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(150, altura - 40, "Relatorio GERAL de Todos os Recibos")

        # Adicionar os dados dos recibos no PDF
        c.setFont("Helvetica", 8)
        y_position = altura - 60  # Posição inicial para o texto
        
        # Cabeçalho da tabela
        c.drawString(25, y_position, "NUMERO")
        c.drawString(80, y_position, "Nome")
        c.drawString(230, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor Pago")
        c.drawString(360, y_position, "Desconto")
        c.drawString(420, y_position, "Data Emissão")
        c.drawString(510, y_position, "Referente")

        y_position -= 20  # Espaço após o cabeçalho
        
        # Variável para acumular o total de "Valor Pago"
        total_pago = 0.0

        # Iterar sobre os dados e adicionar no PDF
        for dado in dados_recibos:
            print(dado)  # Depuração para ver os dados

            # Verifique quantos valores há na tupla
            if len(dado) < 7:
                print(f"Erro: Esperado 7 campos, mas encontrado {len(dado)}. Recebido: {dado}")
                continue  # Pule este recibo se o número de campos for menor que o esperado
            
            # Pegue os campos do recibo, usando os índices corretos da tupla
            numero = dado[0]
            nome = dado[1]
            cpf_cnpj = dado[2]
            valor_pago = dado[4]  # Campo Valor Pago
            desconto = dado[5]    # Campo Desconto
            data_emissao = dado[7]
            referente = dado[6]

            # Verifique se o valor_pago e desconto são válidos e convertê-los para float
            try:
                valor_pago = float(valor_pago) if valor_pago is not None and valor_pago != '' else 0.0
                desconto = float(desconto) if desconto is not None and desconto != '' else 0.0
            except ValueError:
                print(f"Valor inválido para 'Valor Pago' ou 'Desconto': {valor_pago}, {desconto}")
                valor_pago = desconto = 0.0  # Se não for um número válido, atribui 0.0

            # Formatar os valores para a apresentação
            valor_pago_formatado = f"R$ {valor_pago:,.2f}"
            desconto_formatado = f"R$ {desconto:,.2f}"

            # Escrever os dados no PDF
            c.drawString(25, y_position, str(numero))  # Número do recibo
            c.drawString(80, y_position, nome)  # Nome
            c.drawString(230, y_position, cpf_cnpj)  # CPF/CNPJ
            c.drawString(300, y_position, valor_pago_formatado)  # Valor Pago
            c.drawString(370, y_position, desconto_formatado)  # Desconto
            c.drawString(440, y_position, data_emissao)  # Data de Emissão
            c.drawString(510, y_position, referente)  # Referente
            y_position -= 20  # Desce para a próxima linha
            
            # Acumula o valor pago
            total_pago += valor_pago
            
            # Se estiver chegando no final da página, cria uma nova
            if y_position < 50:
                c.showPage()  # Cria uma nova página
                c.setFont("Helvetica", 8)
                y_position = altura - 40  # Reseta a posição Y para o topo
                # Recria o cabeçalho da tabela na nova página
                c.drawString(25, y_position, "NUMERO")
                c.drawString(80, y_position, "Nome")
                c.drawString(230, y_position, "CPF/CNPJ")
                c.drawString(300, y_position, "Valor Pago")
                c.drawString(360, y_position, "Desconto")
                c.drawString(420, y_position, "Data Emissão")
                c.drawString(510, y_position, "Referente")
                y_position -= 20  # Espaço após o cabeçalho

        # Desenha o totalizador de "Valor Pago"
        y_position -= 20  # Ajusta a posição para o totalizador
        total_pago_formatado = f"Total Recebido: R$ {total_pago:,.2f}"
        c.drawString(300, y_position, total_pago_formatado)  # Desenha o total pago

        # Tenta salvar o PDF e verifica se ocorreu algum erro
        try:
            c.save()
            print(f"Relatório gerado com sucesso: {nome_arquivo}")  # Adiciona confirmação no terminal
            messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso: {nome_arquivo}")
            
            # Abrir o PDF gerado automaticamente após o salvamento
            if sys.platform == "win32":  # Para Windows
                os.startfile(nome_arquivo)
            
        except Exception as e:
            print(f"Erro ao salvar o arquivo: {e}")  # Exibe erro no terminal
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o relatório: {e}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

###################################################################################################################
###################################################################################################################
############################################# MODELO NORMAL RESUMIDO - AVULSO - SIMPLES
 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3
from tkinter import messagebox
import os

def gerar_pdf(): # SELECIONA O ID_RECIBO E GERA UMA IMPRESSAO SIMPLES, 1 VIA APENAS
    try:  
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

            # Inserindo o logo no topo (ajuste o caminho do arquivo de imagem)
            logo_path = "logo.png"  # Caminho para o arquivo de imagem do logo
            c.drawImage(logo_path, 100, 740, width=100, height=50)  # Ajuste o tamanho e posição conforme necessário

            # Título do Recibo
            c.setFont("Helvetica-Bold", 16)
            c.drawString(210, 760, f"Recibo Avulso N°: {dados[0]}")
            
            # Adicionando informações do recibo
            c.setFont("Helvetica", 12)
            c.drawString(100, 725, f"Nome: {dados[1]}")
            c.drawString(100, 705, f"CPF/CNPJ: {dados[2]}")
            c.drawString(100, 685, f"Endereco: {dados[3]}")
            c.drawString(100, 665, f"Valor Pago: R$ {dados[5]:.2f}")
            c.drawString(100, 645, f"Aluguel: R$ {dados[4]:.2f}")
            c.drawString(100, 625, f"Descontos: {dados[15]}")
            c.drawString(100, 605, f"Referente: {dados[6]}")
            c.drawString(100, 585, f"Observacao: {dados[16]}")
            c.drawString(100, 555, f"Tipo: RECEBEMOS( )     PAGAMOS( )")
            c.drawString(100, 525, "PORTO XAVIER - RS IMOBILAIRA LIDER")
            c.drawString(100, 495, "ASS ---------------------------------------")
            c.drawString(100, 475, f"Data Emissao: {dados[7]}")
            # Mensagem de agradecimento (opcional)
            c.setFont("Helvetica-Bold", 10)
                       

            # Salvar o PDF
            c.save()

            os.startfile(caminho_pdf)  # CHAMA ao arquivo para o código e abre ele na tela
            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Recibo_Avulso_{id_recibo} Gerado com Sucesso!")
        
        else:
            messagebox.showerror("Erro", "Recibo Não Encontrado.")

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo na GRID para Gerar o PDF.")

###########################################################################################################################################
###########################################################################################################################################        
########################################### IMPRIMIR RECIBO SELECIONADO ##########################################################

def formatar_valor(valor):
    try:
        # Tenta converter o valor para Decimal
        valor_decimal = Decimal(valor)
        return f"R$ {valor_decimal:,.2f}"  # Formatação monetária com duas casas decimais
    except (ValueError, InvalidOperation, TypeError):
        # Caso não seja um número válido, retorna "R$ 0.00"
        return "R$ 0.00"

# Função para obter o número do recibo via caixa de diálogo
def obter_numero_recibo():
    # Criando a janela principal do Tkinter
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    
    # Abre uma janela de entrada solicitando o número do recibo
    numero_recibo = simpledialog.askstring("Número do Recibo", "Por favor, insira o Número do Recibo:")
    
    # Quando o usuário fornece o número, o Tdef gerar_pdf():
    
    # Quando o usuário fornece o número, o Tkinter é fechado e o número é retornado
    root.quit()
    
    if numero_recibo:  # Se o usuário não cancelar ou deixar em branco
        print(f"Número do recibo: {numero_recibo}")
        return numero_recibo
    else:
        print("Nenhum número de recibo informado.")
        return None

def selecionar_operacao():
    root = tk.Tk()
    root.title("Seleção da Operação")
    root.geometry("300x150")  # Tamanho da janela
    root.resizable(False, False)
    
    
    # Variável para armazenar a operação selecionada
    operacao_selecionada = None

    def confirmar():
        nonlocal operacao_selecionada
        operacao_selecionada = combobox.get()
        if operacao_selecionada:
            root.quit()  # Fecha a janela
            root.destroy()  # Destroi a janela após confirmação
        else:
            messagebox.showwarning("Atenção", "Selecione uma Operação antes de Continuar.")
    
    # Título da janela
    tk.Label(root, text="Selecione a Operação:", font=("Helvetica", 12)).pack(pady=10)

   
    # Combobox para selecionar entre RECEBEMOS ou PAGAMOS
    combobox = ttk.Combobox(root, values=["RECEBEMOS DE:", "PAGAMOS A:"], state="readonly", width=20)
    combobox.set("RECEBEMOS DE:")  # Definindo o valor padrão
    combobox.pack(pady=10)
    
    # Botão para confirmar a escolha, com cor de fundo e cor do texto
    tk.Button(root, text="Confirmar", command=confirmar, bg="blue", fg="white", font=("Helvetica", 10, "bold")).pack(pady=20)
    
    root.mainloop()

    return operacao_selecionada

#################################### A FUNCAO QUE CHAMA O IMPRIMIR RECIBO SELECIONADO ################################################################
import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from decimal import Decimal, InvalidOperation
import os

def imprimir_recibo_selecionado():
    try:
        ########## Solicitar o ID do recibo via a nova função ########################################################
        def obter_numero_recibo():
            # Criando a janela principal do Tkinter
            root = tk.Tk()
            root.withdraw()  # Esconde a janela principal
    
            # Abre uma janela de entrada solicitando o número do recibo
            numero_recibo = simpledialog.askstring("Número do Recibo", "Insira o Número do Recibo:")
    
            # Quando o usuário fornece o número, o Tkinter é fechado e o número é retornado
            root.destroy()  # Fechar a janela de entrada sem fechar a janela principal
    
            if numero_recibo:  # Se o usuário não cancelar ou deixar em branco
                return numero_recibo
            else:
                return None  # Retorna None se o usuário cancelar ou não informar nada

        id_recibo = obter_numero_recibo()
        
        # Verifica se o id_recibo foi fornecido
        if not id_recibo:
            messagebox.showwarning("Aviso", "Nenhum número de recibo foi informado. O processo foi cancelado.")
            return  # Interrompe o processo, pois o recibo não foi fornecido
        
        # Conectar ao banco de dados para verificar se o recibo existe
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM dados WHERE id_recibo = ?", (id_recibo,))
        dado_recibo = c.fetchone()
        conexao.close()

        # Se não encontrar o recibo no banco de dados
        if not dado_recibo:
            messagebox.showwarning("Atenção", f"Nenhum recibo encontrado com o ID {id_recibo}.")
            return

        # Solicitar a operação (RECEBEMOS ou PAGAMOS)
        operacao = selecionar_operacao()  # Agora você tem o valor selecionado do ComboBox
        if not operacao:
            messagebox.showwarning("Atenção", "Operação inválida. O recibo não será gerado.")
            return
        
        # Criar o arquivo PDF
        nome_arquivo = f"Recibo_Selecao_{id_recibo}.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)

        # Função para desenhar as informações do recibo (para duas vias)
        def desenhar_recibo(y_position, primeira_via=True):
            # Desenhar o logo no topo da via
            desenhar_logo(c, y_position)

            # Desenhar os dados da empresa ao lado do logo
            y_position = desenhar_dados_empresa(c, y_position, id_recibo)

            c.setFont("Helvetica", 10)
            y_position -= 5
        
            # Mensagem dinâmica com as variáveis # TA FORMATANDO OS VALROES AQUI NOVAMENTE PODE SER QUE AI SEJA NA IMPRESSAO DO PDF?
            try:
                valor_extenso = formatar_valor_por_extenso(Decimal(dado_recibo[5]))  # Valor por extenso
            except InvalidOperation:
                valor_extenso = "Valor inválido"

            mensagem = f"{operacao} {dado_recibo[1]}, CPF/CNPJ: {dado_recibo[2]}, {dado_recibo[3]}. O VALOR de: {formatar_valor(dado_recibo[5])}({formatar_valor_por_extenso(dado_recibo[5])}), " \
                       f"REFERENTE a: {dado_recibo[6]}."
            y_position = draw_text(c, mensagem, y_position, align='right')
            y_position -= 5

            # Campos financeiros com alinhamento à direita
            campos_financeiros = [
                ("ALUGUEL", dado_recibo[4]),
                ("Água", dado_recibo[8]),
                ("Luz", dado_recibo[9]),
                ("Condomínio", dado_recibo[10]),
                ("IPTU", dado_recibo[11]),
                ("Internet", dado_recibo[12]),
                ("Limpeza", dado_recibo[13]),
                ("Outros", dado_recibo[14]),
                ("DESCONTOS", dado_recibo[15]),
                ("Total Líquido", dado_recibo[5])
            ]
            
            # Desenhando os campos financeiros na página com alinhamento à direita
            for descricao, valor in campos_financeiros:
                # Verificar se o valor é numérico antes de formatar
                valor_formatado = formatar_valor(valor)
                
                # Desenhar a descrição à esquerda (coluna 100)
                c.drawString(100, y_position, f"{descricao}:")
                
                # Desenhar o valor à direita (coluna 500) e alinhado à direita
                c.drawRightString(500, y_position, valor_formatado)
                
                # Descer para o próximo item
                y_position -= 15

                # Verificar se atingiu o final da página e mover para a próxima linha
                if y_position < 100:  # Verifique se ainda há espaço suficiente na página
                    c.showPage()  # Cria uma nova página
                    y_position = 718  # Começar na posição inicial da nova página

            # Mensagem adicional
            y_position -= 15
            draw_text(c, f"ASS ---------------------------------------"f"     Data: {dado_recibo[7]}", y_position)

            y_position -= 30
            draw_text(c, f"            IMOBILIÁRIA LIDER                              "                         "PORTO XAVIER-RS", y_position)
            
            if primeira_via:
                return 360  # Início da segunda via na metade da página
            else:
                return y_position + 120  # Ajuste da posição para a segunda via

        # Desenhar a primeira via
        y_position = 725
        y_position = desenhar_recibo(y_position, primeira_via=True)

        # Desenhar a segunda via
        y_position = desenhar_recibo(y_position, primeira_via=False)

        # Salvar o PDF
        c.save()

        # Mensagem de sucesso = SE QUISER VIR A MENSAGEM, TEM QUE DESCOMENTAR A LINHA
        messagebox.showinfo("Sucesso", f"Recibo Gerado com Sucesso! Arquivo Salvo como {nome_arquivo}")

        # Abrir o PDF após gerar
        os.startfile(nome_arquivo)  # Para Windows
        # Para macOS, use: os.system(f"open {nome_arquivo}")
        # Para Linux, use: os.system(f"xdg-open {nome_arquivo}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao Gerar o Recibo: {str(e)}")
######################################################################################################################################################
######################################################################################################################################################
######################################################## GERAR_RECIBO_PADRAO - É A PARTE PRINCIPAL DO PROJETO

from decimal import Decimal, InvalidOperation
from num2words import num2words
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import textwrap
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Importando o Combobox

###################################################################################
# Função para garantir que os valores sejam formatados corretamente como Decimal
def formatar_valor(valor):
    try:
        # Tenta converter o valor para Decimal
        valor_decimal = Decimal(valor)
        return f"R$ {valor_decimal:,.2f}"  # Formatação monetária com duas casas decimais
    except (ValueError, InvalidOperation, TypeError):
        # Caso não seja um número válido, retorna "R$ 0.00"
        return "R$ 0.00"

# Função para desenhar o logo no topo esquerdo de cada via
def desenhar_logo(c, y_position):
    c.drawImage("logo.png", 35, y_position, width=65, height=65)  # Ajuste a posição e tamanho do logo conforme necessário

# Função para desenhar os dados da empresa ao lado do logo
def desenhar_dados_empresa(c, y_position, id_recibo):
    x_position_empresa = 160  # Definido para começar um pouco à direita do logo (ajustável conforme necessário)
    c.setFont("Helvetica", 12)
    c.drawString(x_position_empresa, y_position, f"IMOBILIÁRIA LIDER   10.605.092/0001-97                         RECIBO N°{id_recibo}")
    y_position -= 12
    c.drawString(x_position_empresa, y_position, "marcelobeutler@gmail.com | (55) 9 8116 - 9772")
    y_position -= 12
    c.drawString(x_position_empresa, y_position, "Rua Tiradentes, 606 Centro  98995-000 PORTO XAVIER - RS")
    y_position -= 12
    c.drawString(x_position_empresa, y_position, "'IMÓVEL SÓ  COM O CORRETOR'")
    y_position -= 14
    return y_position

# Função para desenhar o texto com quebra de linha e alinhamento para iniciar a 2 via 580
def draw_text(c, text, y, align='left', max_width=200):
    wrapped_text = textwrap.fill(text, width=75)  # Ajuste conforme necessário 75
    lines = wrapped_text.splitlines()
    line_height = 12  # Altura da linha
    for line in lines:
        if align == 'center':
            text_width = c.stringWidth(line, "Helvetica", 12)
            x_position = (595 - text_width) / 2  # 595 é a largura total da página
            c.drawString(x_position, y, line)
        elif align == 'right':
            text_width = c.stringWidth(line, "Helvetica", 12)
            x_position = 595 - text_width - 50  # 50 é a margem à direita
            c.drawString(x_position, y, line)
        else:
            c.drawString(50, y, line)  # Ajuste a margem esquerda conforme necessário
        y -= line_height  # Abaixar para a próxima linha
    return y

############################################################### SELECIONANDO RECEBEMOS OU PAGAMOS
def selecionar_operacao():
    root = tk.Tk()
    root.title("Seleção da Operação")
    root.geometry("300x150")  # Tamanho da janela
    root.resizable(False, False)
    operacao_selecionada = None

    def confirmar():
        nonlocal operacao_selecionada
        operacao_selecionada = combobox.get()
        if operacao_selecionada:
            root.quit()  # Fecha a janela
            root.destroy()  # Destroi a janela após confirmação
        else:
            messagebox.showwarning("Atenção", "Selecione uma Operação antes de continuar.")
    
    tk.Label(root, text="Selecione a Operação:", font=("Helvetica", 12)).pack(pady=10)
    combobox = ttk.Combobox(root, values=["RECEBEMOS DE:", "PAGAMOS A:"], state="readonly", width=20)
    combobox.set("RECEBEMOS DE:")  # Definindo o valor padrão
    combobox.pack(pady=10)
    tk.Button(root, text="Confirmar", command=confirmar, bg="blue", fg="white", font=("Helvetica", 10, "bold")).pack(pady=20)
    root.mainloop()

    return operacao_selecionada
################################# FUNÇAO QUE CONVERTE OS VALORES NAO TAO BEM GRAVADOS NO BANCO DE DADOS ###########
###################################################################################################################
def formatar_valor_por_extenso(valor):
    """
    Converte um valor numérico em reais para a forma por extenso em português.
    Exemplo: 1505.62 -> "um mil, quinhentos e cinco reais e sessenta e dois centavos"
    """
    valor_int = int(valor)  # Parte inteira
    valor_dec = round(valor - valor_int, 2)  # Parte decimal (centavos)

    # Converte a parte inteira
    valor_extenso_int = num2words(valor_int, lang='pt_BR')

    # Converte a parte decimal (centavos)
    if valor_dec > 0:
        valor_extenso_dec = num2words(int(valor_dec * 100), lang='pt_BR')

        # Corrigir a forma para "centavos" no final
        valor_extenso_dec = f"{valor_extenso_dec} centavos"
        return f"{valor_extenso_int} reais e {valor_extenso_dec}"
    else:
        return f"{valor_extenso_int} reais"

##################################################################################################################
###################################################################################################################

def gerar_recibo_padrao():  # SELECIONA O ID_RECIBO E PREVISUALIZA O RECIBO PADRAO
    try:
        if not tree.selection():
            messagebox.showwarning("Selecione Um Recibo", "Por Favor, Selecione um Recibo para Prosseguir!")
            return  # Impede a execução do resto do código

        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        operacao = selecionar_operacao()  # Agora você tem o valor selecionado do ComboBox

        if not operacao:
            messagebox.showwarning("Atenção", "Operação inválida. O recibo não será gerado.")
            return

        # Conectar ao banco de dados
        conexao = sqlite3.connect('dados.db')
        c = conexao.cursor()

        # Buscar os dados do recibo com o ID fornecido
        c.execute("SELECT * FROM dados WHERE id_recibo = ?", (id_recibo,))
        dado_recibo = c.fetchone()
        conexao.close()

        if not dado_recibo:
            messagebox.showwarning("Atenção", f"Nenhum Recibo encontrado com o ID {id_recibo}.")
            return

        # Criar o arquivo PDF
        nome_arquivo = f"Recibo_{id_recibo}_Padrao.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)

        # Função para desenhar o recibo na mesma página
        def desenhar_recibo(y_position, primeira_via=True):
            desenhar_logo(c, y_position)  # Desenhar o logo no topo da via
            y_position = desenhar_dados_empresa(c, y_position, id_recibo)

            c.setFont("Helvetica", 10)
            y_position -= 5

            # Mensagem dinâmica com as variáveis
            try:
                valor_extenso = formatar_valor_por_extenso(Decimal(dado_recibo[5]))  # Valor por extenso
            except InvalidOperation:
                valor_extenso = "Valor inválido"

            mensagem = f"{operacao} {dado_recibo[1]}, CPF/CNPJ: {dado_recibo[2]}, {dado_recibo[3]}. O VALOR de: {formatar_valor(dado_recibo[5])}({formatar_valor_por_extenso(dado_recibo[5])}), " \
                       f"REFERENTE a: {dado_recibo[6]}."
            y_position = draw_text(c, mensagem, y_position, align='right')
            y_position -= 3

            # Campos financeiros com alinhamento à direita
            campos_financeiros = [
                ("ALUGUEL", dado_recibo[4]),
                ("Água", dado_recibo[8]),
                ("Luz", dado_recibo[9]),
                ("Condomínio", dado_recibo[10]),
                ("IPTU", dado_recibo[11]),
                ("Internet", dado_recibo[12]),
                ("Limpeza", dado_recibo[13]),
                ("Outros", dado_recibo[14]),
                ("- DESCONTOS", dado_recibo[15]),
                ("Total Líquido", dado_recibo[5])
            ]

            # Desenhando os campos financeiros na página com alinhamento à direita
            for descricao, valor in campos_financeiros:
                valor_formatado = formatar_valor(valor)
                y_position -= 12
                c.drawString(50, y_position, descricao)
                c.drawString(450, y_position, valor_formatado)

            y_position -= 20

            # Nome do Recebedor
            c.drawString(50, y_position, f"Recebido Em: {dado_recibo[7]}                          IMOBILIARIA LIDER")
            y_position -= 30

            c.drawString(80, y_position,   f"                       Ass:_____________________________________")
            y_position -= 5

            #if primeira_via:
                
                #c.drawString(80, y_position,        "ASS:_________________________________________")

            return y_position  # Retorna a posição Y atualizada

        # Ajustar a posição inicial de Y para a primeira via
        y_position_inicial = 710

        # Desenhar as duas vias na mesma página, ajustando a posição Y
        y_position = desenhar_recibo(y_position_inicial)  # Primeira via
        y_position -= 90  # Ajuste o valor para mover a segunda via para baixo

        y_position -= 10  # Ajuste maior se necessário

        desenhar_recibo(y_position, primeira_via=False)  # Segunda via

        # Salvar a página do PDF
        c.showPage()  # Chama o showPage após desenhar as duas vias
        c.save()

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Recibo Gerado", f"Recibo {id_recibo} Gerado com Sucesso!")
        os.startfile(nome_arquivo)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um Erro: {str(e)}")
        
############################################### GERAR O RECIBO AVULSO #######################################################################
#############################################################################################################################################
#############################################################################################################################################
import tkinter as tk # NAO MEXER AQUI VAI SABER O PORQUE
import customtkinter as ctk
from tkinter import messagebox
from fpdf import FPDF
import os
import win32print
import win32api
from num2words import num2words
from datetime import datetime
import time

# Função para validar os valores (substituindo vírgula por ponto)
def validar_valor(valor):
    if valor:
        valor = valor.replace(',', '.')  # Substitui a vírgula por ponto
    try:
        return float(valor) if valor else 0.0  # Retorna 0.0 se o valor estiver vazio
    except ValueError:
        return None  # Retorna None caso não seja possível converter para float

# Função para obter o número do próximo recibo
def obter_numero_recibo():
    arquivo_contador = "contador_recibo.txt"
    try:
        with open(arquivo_contador, "r") as file:
            numero = int(file.read().strip())
        return numero
    except (FileNotFoundError, ValueError):
        return 0

# Função para salvar o número do próximo recibo
def salvar_numero_recibo(numero):
    arquivo_contador = "contador_recibo.txt"
    with open(arquivo_contador, "w") as file:
        file.write(str(numero))

# Função para gerar o recibo com SITE
def gerar_recibo(nome_pagador, cpf_pagador, endereco, motivo, aluguel, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, data):
    try:
        if not nome_pagador or not aluguel or not data:
            messagebox.showwarning("Atenção", "Por Regra, Preencha os seguintes Campos (Nome e Vlr_Aluguel), antes de Gerar o Recibo!")
            return

        aluguel = validar_valor(aluguel)
        if aluguel is None:
            messagebox.showwarning("Atenção", "O Valor do Aluguel Precisa ser um Número Válido.")
            return

        valor_extras = 0
        agua = validar_valor(agua) if agua else 0.0
        luz = validar_valor(luz) if luz else 0.0
        condominio = validar_valor(condominio) if condominio else 0.0
        iptu = validar_valor(iptu) if iptu else 0.0
        internet = validar_valor(internet) if internet else 0.0
        limpeza = validar_valor(limpeza) if limpeza else 0.0
        outros = validar_valor(outros) if outros else 0.0

        valor_extras = agua + luz + condominio + iptu + internet + limpeza + outros

        if descontos != "":
            descontos = validar_valor(descontos)
            if descontos is None:
                messagebox.showwarning("Atenção", "O Valor dos Descontos Precisa ser um Número Válido.")
                return
            elif descontos < 0:
                messagebox.showwarning("Atenção", "O Valor dos Descontos não pode ser Negativo.")
                return
        else:
            descontos = 0

        valor_total = aluguel + valor_extras - descontos
        valor_por_extenso = num2words(valor_total, lang='pt_BR', to='currency')

        cpf_pagador_formatado = f"{cpf_pagador[:3]}.{cpf_pagador[3:6]}.{cpf_pagador[6:9]}-{cpf_pagador[9:]}" 

        empresa = "IMOBILIARIA LIDER"
        cnpj = "10.605.092/0001-97"
        local = "PORTO XAVIER - RS"

        numero_recibo = obter_numero_recibo() + 1
        salvar_numero_recibo(numero_recibo)

        from fpdf import FPDF

        pdf = FPDF()

# Primeira página com logo
        pdf.add_page()
        pdf.image('logo.png', 10, 3, w=40)  # Logo na parte superior
        pdf.set_font("Arial", size=10)

# Função para gerar o conteúdo do recibo
        def gerar_recibo_na_posicao(y_offset, logo_pos=True):
            texto_incial = 'IMOBILIARIA LIDER  10.605.092/0001-97  www.imobiliariaportoxavier.com.br'
            contato = 'marcelobeutler@gmail.com | Tel (55) 9 8116-9772'
            endereco_imob = 'Rua Tiradentes, 606 Centro 98995-000 PORTO XAVIER - RS'
            obs = '"IMÓVEL SÓ COM O CORRETOR"'

            texto = (f"                                                RECEBEMOS DE: {nome_pagador}, CPF/CNPJ sob nº: {cpf_pagador_formatado}, Endereço: {endereco}, O valor de R$ {valor_total:.2f}({valor_por_extenso}), referente a: {motivo}.")
            extras_texto = ""
            if aluguel:
                extras_texto += f"ALUGUEL:     R$ {aluguel:.2f}\n"
            if agua > 0:
                extras_texto += f"Água:              R$  {agua:.2f}\n"
            if luz > 0:
                extras_texto += f"Luz:                 R$  {luz:.2f}\n"
            if condominio > 0:
                extras_texto += f"Condomínio:    R$  {condominio:.2f}\n"
            if iptu > 0:
                extras_texto += f"IPTU:               R$  {iptu:.2f}\n"
            if internet > 0:
                extras_texto += f"Internet:           R$  {internet:.2f}\n"
            if limpeza > 0:
                extras_texto += f"Limpeza:          R$  {limpeza:.2f}\n"
            if outros > 0:
                extras_texto += f"Outros:              R$  {outros:.2f}\n"
            if descontos > 0:
                extras_texto += f"- DESCONTOS: R$ {descontos:.2f}\n"
            if valor_total > 0:
                extras_texto += f"Total Liquido:  R$  {valor_total:.2f}\n"

            texto_extras = f"Composição do Recibo: \n{extras_texto}" if extras_texto else ""

    # Definindo a posição Y para o conteúdo
            pdf.set_y(y_offset)
            pdf.multi_cell(0, 5, txt=texto_incial, align='R')
            pdf.multi_cell(0, 5, txt=contato, align='R')
            pdf.multi_cell(0, 5, txt=endereco_imob, align='R')
            pdf.multi_cell(0, 5, txt=obs, align='R')

            pdf.ln(3)
            pdf.cell(0, 5, txt=f'      RECIBO Nº {numero_recibo}', ln=True, align='C')
            pdf.multi_cell(0, 5, txt=texto, align='C')
            pdf.multi_cell(0, 5, txt=texto_extras, align='C')

            pdf.ln(10)
            pdf.multi_cell(0, 5, txt='-------------------------------------------------------', align='C')
            pdf.ln(3)
            pdf.multi_cell(0, 5, txt=f"{local}                  {empresa}                                  {data}", align='C')
            pdf.ln(1)

# Gerando o conteúdo nas posições desejadas na primeira via (topo da página)
        gerar_recibo_na_posicao(10)  # Primeira via (ou primeira parte)

# Agora vamos para a segunda via, com espaço para ela abaixo da primeira via
# Ajuste da posição Y para a segunda via
        pdf.ln(8)  # Aumente o valor se precisar de mais espaço entre as vias

# Agora adicionamos o logo corretamente no topo da segunda via
        pdf.image('logo.png', 10, pdf.get_y(), w=40)  # Logo na segunda via, com a posição Y ajustada

# Gerando o conteúdo na segunda via
        gerar_recibo_na_posicao(pdf.get_y() + 8)  # Ajuste para a segunda via iniciar abaixo do logo

# Gerando o arquivo PDF
        caminho_arquivo = f'recibo_AVULSO_{numero_recibo}.pdf'
        pdf.output(caminho_arquivo)

####################################################################################################################################

        
        # Função para abrir e imprimir o PDF
        def gerar_e_imprimir_recibo(caminho_arquivo, numero_recibo):
            try:
                os.startfile(caminho_arquivo)  # Abre o arquivo no visualizador de PDF padrão
                time.sleep(2)  # Ajuste conforme necessário
                resposta = messagebox.askyesno("Impressão", f"Recibo nº {numero_recibo} Gerado Com Sucesso. Deseja Imprimir?")
                
                if resposta:
                    printer_name = win32print.GetDefaultPrinter()
                    win32api.ShellExecute(0, "print", caminho_arquivo, f'/d:"{printer_name}"', ".", 0)
                    messagebox.showinfo("Impressão", "Recibo enviado a Impressora! Aguarde IMPRESSÃO")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao tentar gerar ou imprimir o recibo: {str(e)}")



        gerar_e_imprimir_recibo(caminho_arquivo, numero_recibo)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao Gerar o Recibo: {str(e)}")
      
############################################################################################################
        # # Imprimir o arquivo PDF DIRETO NA IMPRESSORA sem chamar PREVIZUALIAÇÃO
        # printer_name = win32print.GetDefaultPrinter()
        # win32api.ShellExecute(0, "print", caminho_arquivo, f'/d:"{printer_name}"', ".", 0)

        # messagebox.showinfo("Recibo Gerado", f"Recibo {numero_recibo} gerado com sucesso!")

###############################################################################################################
###################################################TELA DE INSERCAO DE DADOS NO RECIBO AVULSO - FEITO COM CUSTOMTKINTER #########################     
##############################################################################################################################################
import customtkinter as ctk
from datetime import datetime

def chamar_tela_insercao():
    # Criar a janela de inserção
    root = ctk.CTkToplevel()
    root.title("Inserir Dados Recibo Avulso")
    root.geometry("480x600")
    root.resizable(False, False)  # Impede o redimensionamento da janela

    # Coloca a janela root na frente da janela principal
    root.lift()
    root.attributes("-topmost", True)  # Garante que a janela fique no topo
    root.after(100, lambda: root.lift())  # Tenta novamente após 100ms

    labels = [
        "NOME:", "CPF/CNPJ:", "Endereço:", "Referente:", "ALUGUEL:", "Água:", "Luz:", "Condomínio:", "IPTU:", "Internet:", "Limpeza:", "Outros:", "DESCONTOS:", "Data:"
    ]
    entries = []

    # Adiciona os campos de entrada
    for i, label_text in enumerate(labels):
        label = ctk.CTkLabel(root, text=label_text)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

        entry = ctk.CTkEntry(root, width=350)
        entry.grid(row=i, column=1, padx=10, pady=5)

        # Preenche o campo "Data" com a data atual
        if label_text == "Data:":
            data_atual = datetime.now().strftime("%d/%m/%Y")
            #print(f"Preenchendo o campo 'Data' com: {data_atual}")
            entry.insert(0, data_atual)

        entries.append(entry)

    # Função para garantir que o foco seja definido corretamente no primeiro campo
    def set_focus():
        entries[0].focus_set()  # Define o foco no primeiro campo

    # Chama a função para definir o foco após 200ms (para garantir que a janela esteja completamente carregada)
    root.after(200, set_focus)

    # Função de callback para o botão "GERAR RECIBO"
    def on_gerar_recibo():
        # Oculta a janela de inserção enquanto o PDF está sendo gerado
        root.withdraw()

        # Obter os dados dos campos de entrada
        dados = [entry.get() for entry in entries]
        
        # Chama a função de geração do recibo
        gerar_recibo(*dados)
        
        # Limpa os campos após gerar o recibo
        for entry in entries:
            entry.delete(0, ctk.END)  # Limpa cada campo de entrada

        # Exibe novamente a janela de inserção depois de gerar o PDF
        root.deiconify()

        # Preenche novamente o campo "Data" com a data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        for i, entry in enumerate(entries):
            if labels[i] == "Data:":
                #print(f"Preenchendo o campo 'Data' novamente com: {data_atual}")
                entry.insert(0, data_atual)

        # Define o foco novamente no campo "Nome" após a janela ser restaurada
        entries[0].focus_set()  # O campo "Nome" é o primeiro campo da lista `entries`

#############################################################################################################
# BOTOES QUE FICAM DENTRO DA JANELA DE INCLUSAO RECIBO RAPIDO
   
    # Adiciona um botão para gerar o recibo (exemplo)
    btn_gerar = ctk.CTkButton(root, text="GERAR RECIBO - (Enter)", command=on_gerar_recibo)
    btn_gerar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    # Usando o bind para associar a tecla "Enter" com a função
    root.bind("<Return>", lambda event: on_gerar_recibo())  # Quando "Enter" for pressionado, chama on_gerar_recibo

    # Botão para fechar
    btn_fechar = tk.Button(root, text="Fechar", command=root.destroy, bg="gray", fg="white")
    btn_fechar.grid(row=len(labels), column=0, padx=10, pady=10, sticky="ew")  # Coloca o botão na próxima coluna, lado a lado

    root.mainloop()
###########################################################################################################################################
############################################################################################################################################
# INTERFACE GRAFICA DA JANELA PRINCIPAL DO SISTEMA, PRIMEIRA JANELA QUE ABRE - AONDE ESTA TODOS OS BOTOES E FUNÇOES PRINCIPAIS
# Tela principal
import tkinter as tk

janela_principal = tk.Tk()
janela_principal.title("Gerenciador de Recibos - GDI")
janela_principal.geometry("1200x650+0+0")  # Ajusta o tamanho inicial da janela
#janela_principal.resizable(False, False) # SE PRECISAR BLOQUEAR A JANELA

tk.Label(janela_principal, text="Nome do Cliente:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca
campo_busca_nome.focus_set()

# Campo de busca RECIBO
tk.Label(janela_principal, text="Número Recibo:").grid(row=0, column=1, padx=10, pady=10, sticky='w')
campo_busca_recibo = tk.Entry(janela_principal, width=15)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_cliente)  # Pressionar ENTER ativa a busca

# Colocar o foco no campo "Nome do Cliente" ao iniciar
campo_busca_nome.focus_set()  

######################################################################################################################################
# TODOS OS BOTOES DA INTERFACE GRAFICA DA JANELA PRINCIPAL ##########################################################
# Botão INCLUIR NOVO
btn_incluir = tk.Button(janela_principal, text="Incluir NOVO", command=abrir_janela_inclusao, bg="green", fg="white", width=10)
btn_incluir.grid(row=2, column=0, padx=10, pady=10)  # Coloca o botão na linha 1, coluna 2

# Botão EDITAR
btn_editar = tk.Button(janela_principal, text="EDITAR", command=editar_recibo, bg="orange", fg="red", width=10)
btn_editar.grid(row=3, column=0, padx=10, pady=10)  # Botão Editar agora está ao lado do Incluir Novo

# Botao EXCLUIR
btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=3, column=1, padx=10, pady=10)

# Botao BUSCAR
btn_buscar = tk.Button(janela_principal, text="PROCURAR - 'Enter'", command=buscar_cliente, bg="orange", fg="black")
btn_buscar.grid(row=2, column=1, padx=10, pady=10)

# Botão IMPRIMIR PDF salva na pasta nao traz na tela
btn_pdf = tk.Button(janela_principal, text="RECIBO PEQUENO", command=gerar_pdf, bg="yellow", fg="black") # Um recibo simples e rapido - Resumido( 1 VIA)
btn_pdf.grid(row=3, column=3, padx=10, pady=10)

# Botao relatorio FILTRAR POR DATA - quase funcionando
btn_filtro = tk.Button(janela_principal, text="Relatório POR DATA", command=gerar_relatorio_filtrado, bg="purple", fg="white") # FILTRO POR DATA
btn_filtro.grid(row=3, column=2, padx=10, pady=10) # Filtrar por Data

# Botão Gerar RELATORIO = FUNCAO GERAR_REL  LINHA 389
btn_rel = tk.Button(janela_principal, text="Pré-Visualizar-Todos Recibos", command=gerar_Rel_Total, bg="purple", fg="white") # traz todos os recibos da base
btn_rel.grid(row=4, column=2, padx=10, pady=10) # Relatorio GERAL-Todos

# Botao Imprimir na tela.. LAOYT NOVO.. A TRABALHAR
btn_recibo = tk.Button(janela_principal, text="PRÉ-VISUALIZAR RECIBO", command=gerar_recibo_padrao, bg="blue", fg="white") # PADRAO 2 VIAS
btn_recibo.grid(row=4, column=0, padx=10, pady=10)

# Botão FECHAR
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="gray", fg="white")  # FECHAR JANELA PRINCIPAL
btn_fechar.grid(row=4, column=3, padx=10, pady=10)  # Colocando o botão na linha 4, coluna 2

btn_pdf = tk.Button(janela_principal, text="INFORME o N° RECIBO IMPRESSÃO", command=imprimir_recibo_selecionado, bg="brown", fg="white") #
btn_pdf.grid(row=2, column=2, padx=10, pady=10)

# BOTAO PARA INCLUIR RECIBO AVULSO SEM GRAVAR NO BANCO DE DADOS
btn_avulso = tk.Button(janela_principal, text="RECIBO AVULSO", command=chamar_tela_insercao, bg="blue", fg="white") # RECIBO AVULSO, SEM INSERIR NADA NO BANCO DE DADOS
btn_avulso.grid(row=4, column=1, padx=10, pady=10)

####################################################################################################################### 
# Criando a árvore para mostrar os dados DOS RECIBOS A GRID MAIOR
cols = ("ID_RECIBO", "Nome", "CPF/CNPJ","Endereco", "ALUGUEL", "VALOR PAGO", "Referente", "Data de Emissão", "Agua", "Luz", "Condominio", "IPTU", "Internet", "Limpeza", "Outros", "Descontos","OBS")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

# Definindo larguras personalizadas para cada coluna
larguras = [30, 150, 100, 150, 70, 80, 150, 80, 50, 50, 50, 50, 50, 50, 50, 50, 100]

# Itera pelas colunas e aplica as larguras correspondentes
for col, largura in zip(cols, larguras):
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=largura)

# DELIMITANDO AS COLUNAS FIXAS EM 80
#for col in cols:
    #tree.heading(col, text=col)
    #tree.column(col, anchor="w", width=80)

tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')  # Grid com expansibilidade PARA MOSTRAR DADOS RECIBOS

# Ajustando a tela para que a árvore ocupe o restante da janela
janela_principal.grid_rowconfigure(1, weight=1)
janela_principal.grid_columnconfigure(0, weight=1)
janela_principal.grid_columnconfigure(1, weight=1)

janela_principal.mainloop()