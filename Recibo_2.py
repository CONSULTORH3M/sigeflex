import customtkinter as ctk
from tkinter import messagebox
import sys
import mysql.connector
from mysql.connector import Error

import configparser

# Função para obter o IP do servidor a partir do arquivo config.ini
def obter_host_config():
    config = configparser.ConfigParser()
    config.read('config.ini')  # Lê o arquivo de configuração

    # Pega o valor do host da seção [mysql]
    host = config.get('mysql', 'host', fallback='localhost')  # Default é 'localhost' se não encontrado
    return host

# Usando o valor do host no código
def conectar_mysql():
    try:
        host = obter_host_config()  # Obtém o host do arquivo de configuração
        user = 'root'               # Nome do usuário do MySQL
        password = 'mysql147'       # Senha do MySQL
        database = 'dados'          # Nome do banco de dados

        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Exemplo de uso
host = obter_host_config()
print(f"O IP do servidor MySQL é: {host}")

# FUNCAO PARA NO LOGIN APARECER OS USUARIOS CADASTRADOS NO BANCO DE DADOS
def obter_usuarios():
    conexao = conectar_mysql()
    usuarios = []
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT login FROM usuarios")  # Seleciona todos os logins
            usuarios = cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar os usuários: {e}")
        finally:
            cursor.close()
            conexao.close()
    return usuarios

# FUNCAO QUE VERIFICA A SENHA CORRETA
def verificar_login():
    usuario_selecionado = entry_usuario.get()  # Obtemos o login selecionado do menu
    senha_digitada = entry_senha.get()

    # Conectar ao banco de dados
    conexao = conectar_mysql()
    if conexao:
        try:
            cursor = conexao.cursor()
            # Consulta para pegar os dados do usuário no banco
            cursor.execute("SELECT * FROM usuarios WHERE login = %s", (usuario_selecionado,))
            usuario_encontrado = cursor.fetchone()

            # Verificar se o usuário existe
            if usuario_encontrado:
                # Se o usuário for encontrado, verifica a senha
                id_usuario, nome, login, senha, data = usuario_encontrado
                if senha_digitada == senha:
                    # Salva o login do último usuário no arquivo
                    salvar_ultimo_usuario(usuario_selecionado)
                    janela_login.destroy()  # Fechar a janela de login
                    # Abrir a janela de boas-vindas
                    print(f"Bem-vindo, {nome}!")
                else:
                    messagebox.showerror("Erro", "Senha Incorreta. Tente Novamente.")
            else:
                messagebox.showerror("Erro", "Usuário Não Encontrado.")
        except Error as e:
            print(f"Erro ao consultar o banco de dados: {e}")
        finally:
            cursor.close()
            conexao.close()

# FUNCAO QUE SALVA O ULTIMO USUÁRIO LOGADO
def salvar_ultimo_usuario(usuario):
    try:
        with open("parametros.txt", "w") as f:
            f.write(usuario)
    except Exception as e:
        print(f"Erro ao salvar o último usuário: {e}")

# Função para carregar o último usuário do arquivo
def carregar_ultimo_usuario():
    try:
        with open("parametros.txt", "r") as f:
            ultimo_usuario = f.read().strip()  # Lê e remove espaços em branco extras
            return ultimo_usuario
    except FileNotFoundError:
        return None  # Se o arquivo não existir, retorna None

# Função para encerrar o programa
def on_close():
    sys.exit()

# CRIANDO A JANELA DE LOGIN
import customtkinter as ctk

# Aqui você obteria o host do MySQL (ajuste conforme sua função)
host = obter_host_config()

# Criando a janela de login
janela_login = ctk.CTk()
janela_login.title("Login")
janela_login.geometry("300x190")  # Aumentei a altura para caber a lista de usuários
janela_login.resizable(False, False)

# Definindo o comportamento de fechamento
janela_login.protocol("WM_DELETE_WINDOW", on_close)

# Exibindo o IP do servidor MySQL no topo da janela de login
label_host = ctk.CTkLabel(janela_login, text=f" Conectando no Servidor MySQL: {host}")
label_host.grid(row=0, column=0, columnspan=2, pady=5, padx=20)  # Colocando no topo, com espaçamento

# Widgets de login
ctk.CTkLabel(janela_login, text="Usuário:").grid(row=1, column=0, pady=10, padx=20)

# Obtendo a lista de usuários do banco de dados
usuarios = obter_usuarios()

# Criando o ComboBox para selecionar o usuário
entry_usuario = ctk.CTkOptionMenu(janela_login, values=[usuario[0] for usuario in usuarios])  # Só mostra os logins
entry_usuario.grid(row=1, column=1, pady=5, padx=20)

# Carregar o último usuário selecionado e definir como padrão
ultimo_usuario = carregar_ultimo_usuario()
if ultimo_usuario in [usuario[0] for usuario in usuarios]:  # Se o último usuário existir na lista
    entry_usuario.set(ultimo_usuario)
else:
    entry_usuario.set("Escolha o usuário")  # Mensagem inicial para indicar a seleção

ctk.CTkLabel(janela_login, text="Senha:").grid(row=2, column=0, pady=10, padx=20)
entry_senha = ctk.CTkEntry(janela_login, show="*")
entry_senha.grid(row=2, column=1, pady=5, padx=20)

# Colocar o foco no campo de senha após 100ms
janela_login.after(100, lambda: entry_senha.focus())

# Botões "Login" e "Fechar"
btn_login = ctk.CTkButton(janela_login, text="Entrar", command=verificar_login)
btn_login.grid(row=3, column=0, pady=20, padx=20, sticky="w", columnspan=2)

btn_fechar = ctk.CTkButton(janela_login, text="Fechar", command=on_close, fg_color="gray", width=10)
btn_fechar.grid(row=3, column=1, pady=20, padx=10, sticky="e")

# Configurando o evento de pressionamento da tecla ENTER
janela_login.bind("<Return>", lambda event: verificar_login())

# Executando a interface
janela_login.mainloop()



######################################### LOGIN ACIMA
####################################################################################################################################################
#  TELA DE PROCURAR DOS RECIBOS NA TELA PRINCIPAL E MOSTRAR NA TELA
####################################################################################################################################################
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime

# Função de Conexão com MySQL
def buscar_recibos(event=None): # FUNCAO PARA BUSCAR RECIBOS NA  JANELA PRINCIPAL
    # Limpar a árvore de resultados anteriores
    for item in tree.get_children():
        tree.delete(item)

    # Conectar ao MySQL
    conexao = conectar_mysql()
    c = conexao.cursor()

    # Obter os valores de busca
    nome_busca = campo_busca_nome.get()
    id_busca = campo_busca_recibo.get() 
    
    # Verifica se há algum critério de busca SETANDO O ID RECIBO EM DORDEM CRESCENTE
    if nome_busca and id_busca:
        # Buscar por nome e id
        c.execute("SELECT * FROM recibos WHERE nome LIKE %s AND id_recibo LIKE %s", 
                  ('%' + nome_busca + '%', '%' + id_busca + '%'))
    elif nome_busca:
        # Buscar apenas por nome
        c.execute("SELECT * FROM recibos WHERE nome LIKE %s", ('%' + nome_busca + '%',))
    elif id_busca:
        # Buscar apenas por id
        c.execute("SELECT * FROM recibos WHERE id_recibo LIKE %s", ('%' + id_busca + '%',))
    else:
        # Se não houver nenhum critério de busca, retornar todos os dados
        c.execute("SELECT * FROM recibos ORDER BY id_recibo DESC")

    dados = c.fetchall()  # Recupera todos os dados da consulta
    conexao.close()  # Fecha a conexão com o banco

    if not dados:  # Se a consulta não retornar resultados
        messagebox.showinfo("Resultado", "Nenhum Recibo Encontrado.")
        return  # Interrompe a função, não inserindo dados na árvore

    # Preenche a árvore com os dados retornados
    for dado in dados:
        tree.insert('', 'end', values=dado)  # Adiciona cada linha de dados na árvore
##########################################################################FUNCAO BUSCAR RECIBOS ACIMA

###################################################################################################################
##############################################FUNCAO DE EXCLUIR RECIBO ABAIXO
#######################################################################################################################
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
# Função para excluir um recibo com senha de confirmação
def excluir_recibo():
    # Obter o item selecionado (linha do Treeview)
    selected_item = tree.selection()  # Retorna a linha selecionada
    
    if not selected_item:
        messagebox.showwarning("Atenção", "Selecione um Recibo para Excluir!")
        return
    
    # Obter o ID_RECIBO da linha selecionada
    id_recibo = tree.item(selected_item, 'values')[0]  # O ID_RECIBO está na primeira coluna
    
    # Criar uma nova janela para a senha
    senha_janela = tk.Toplevel()  # Cria uma janela secundária
    senha_janela.title("Confirmar Exclusão")
    
    #senha_janela.configure(bg="red")
    
    # Adicionando um rótulo (Label) e campo de entrada (Entry) para a senha
    tk.Label(senha_janela, text="Digite a Senha para Excluir o Recibo:", fg="red").pack(padx=10, pady=10)
       
    senha_entry = tk.Entry(senha_janela, show="*")  # O parâmetro 'show' oculta a senha
    senha_entry.pack(padx=10, pady=5)
    
    def verificar_senha():
        senha = senha_entry.get()  # Pega a senha digitada
        
        if senha != "55":
            messagebox.showerror("Erro", "Senha Incorreta! Exclusão Cancelada.")
            senha_janela.destroy()  # Fecha a janela da senha
            return
        
        # Confirmar com o usuário antes de excluir
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Você Tem Certeza que Deseja Excluir o Recibo Numero: {id_recibo}?")
        
        if confirm:
            try:
                # Conectando ao banco de dados MySQL
                conn = conexao = conectar_mysql()
                        
                c = conexao.cursor()
                cursor = conn.cursor()
                
                # Query para deletar o recibo com base no ID
                query = "DELETE FROM recibos WHERE ID_RECIBO = %s"
                cursor.execute(query, (id_recibo,))
                conn.commit()  # Salvar a exclusão no banco
                
                # Fechar conexão
                cursor.close()
                conn.close()
                
                # Remover o item da interface (Treeview)
                tree.delete(selected_item)
                
                # Exibir mensagem de sucesso
                messagebox.showinfo("Sucesso", f"Recibo {id_recibo}, Excluído com Sucesso!")
            
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao Excluir Recibo: {err}")
        
        senha_janela.destroy()  # Fecha a janela de senha após o processo de exclusão

    # Adicionando o botão para verificar a senha
    tk.Button(senha_janela, text="Confirmar", command=verificar_senha).pack(padx=10, pady=10)
    
    # Exibir a janela de senha
    senha_janela.mainloop()

#################################################################### ACIMA FUNÇAO EXCLUIR RECIBO ###########
##########################################################################################################

######################################################################INCLUIR NOVO RECIBO ABAIXO##################
# Função de inclusão - INCLUIR NOVO RECIBO
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
def abrir_janela_inclusao():  # INCLUSAO DE RECIBO MANUAL
    # Criando a janela de inclusão
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("INCLUIR Recibo MANUAL")
    janela_inclusao.geometry("600x620+5+5")  # Ajuste no tamanho da janela para permitir mais espaço
    janela_inclusao.resizable(False, False)

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    
    # Configurando o peso das linhas para garantir que a última linha (onde os botões estão) tenha mais espaço
    for i in range(16):  # Configurando peso para as linhas, até a linha 15
        janela_inclusao.grid_rowconfigure(i, weight=1)

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="NOME:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=60, bg="lightblue", fg="black")  # Cor de fundo azul claro
    campo_nome_inclusao.grid(row=0, column=1, padx=10, pady=5)
    campo_nome_inclusao.focus_set()

    tk.Label(janela_inclusao, text="CPF/CNPJ:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    campo_cpfcnpj_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_cpfcnpj_inclusao.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Endereco Completo:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    campo_endereco_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_endereco_inclusao.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Referente:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    campo_referente_inclusao = tk.Entry(janela_inclusao, width=60, bg="lightblue", fg="black")  # Cor de fundo azul claro
    campo_referente_inclusao.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="ALUGUEL:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    campo_aluguel_inclusao = tk.Entry(janela_inclusao, width=15, bg="lightblue", fg="black")  # Cor de fundo azul claro
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
    data_atual = datetime.now().strftime("%d/%m/%Y")  # Data atual no formato DD/MM/YYYY
    tk.Label(janela_inclusao, text="Data de Emissão:").grid(row=14, column=0, padx=10, pady=5, sticky='w')

    campo_data_emissao_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_emissao_inclusao.grid(row=14, column=1, padx=10, pady=5)
    campo_data_emissao_inclusao.insert(0, data_atual)  # Preenchendo o campo com a data atual

# Capturando o valor da data inserido pelo usuário
    dataEmissao = campo_data_emissao_inclusao.get()
    print(f"Data inserida pelo usuário: {dataEmissao}")  # Verificação para garantir que o valor foi capturado corretamente

# Tentando converter a data de DD/MM/YYYY para YYYY-MM-DD
    try:
        dataEmissao = datetime.strptime(dataEmissao, "%d/%m/%Y").strftime("%Y-%m-%d")
        print(f"Data convertida para o formato adequado: {dataEmissao}")  # Verifique se a conversão está correta
    except ValueError as e:
        print(f"Erro ao converter a data: {e}")
    # Caso haja erro de formatação, a data não foi convertida corretamente.
        messagebox.showerror("Erro", "A data inserida não está no formato correto (DD/MM/YYYY).")
        return  # Encerra a função, pois a data não é válida

# Agora, a data está convertida e pronta para ser inserida no banco
    print(f"Data pronta para inserção no banco: {dataEmissao}")

######################################################################### INCLUINDO RECIBO MANUAL ACIMA #################
###################################################################################################################################
################################ FUNÇÃO CALCULAR VALOR LIQUIDO = SOMA tudo - DESCONTO = VALOR LIQUIDO ##############################
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
            messagebox.showerror("Erro", "Por Favor, Insira Valores Numéricos Válidos nos Campos de Valor.")
            janela_inclusao.attributes('-topmost', True) 
            return 0

    def salvar_inclusao():
        nome = campo_nome_inclusao.get()
        cpfcnpj = campo_cpfcnpj_inclusao.get()
        endereco = campo_endereco_inclusao.get()
        aluguel = campo_aluguel_inclusao.get()
    
        valor_liquido = calcular_valor_liquido()  # Chama a função para calcular o valor líquido
        data_emissao = campo_data_emissao_inclusao.get()
    
        if not nome or not aluguel:
            messagebox.showwarning("Atenção", "NOME e ALUGUEL são Campos Obrigatórios.")
            janela_inclusao.attributes('-topmost', True)
            return

        try:
        # Conectando ao banco de dados MySQL
            conn = conexao = conectar_mysql()

            c = conexao.cursor()
            cursor = conn.cursor()

        # Garantir que os valores sejam convertidos para float
            aluguel = float(aluguel or 0.0)
            agua = float(campo_agua_inclusao.get() or 0.0)
            luz = float(campo_luz_inclusao.get() or 0.0)
            condominio = float(campo_condominio_inclusao.get() or 0.0)
            iptu = float(campo_iptu_inclusao.get() or 0.0)
            internet = float(campo_internet_inclusao.get() or 0.0)
            limpeza = float(campo_limpeza_inclusao.get() or 0.0)
            outros = float(campo_outros_inclusao.get() or 0.0)
            descontos = float(campo_descontos_inclusao.get() or 0.0)

        # Formatação dos valores para 2 casas decimais
            aluguel_formatado = f"{aluguel:.2f}"
            agua_formatado = f"{agua:.2f}"
            luz_formatado = f"{luz:.2f}"
            condominio_formatado = f"{condominio:.2f}"
            iptu_formatado = f"{iptu:.2f}"
            internet_formatado = f"{internet:.2f}"
            limpeza_formatado = f"{limpeza:.2f}"
            outros_formatado = f"{outros:.2f}"
            descontos_formatado = f"{descontos:.2f}"
            valor_liquido_formatado = f"{valor_liquido:.2f}"

        # Garantindo que campos opcionais como 'referente', 'observacao', etc., sejam preenchidos corretamente
            referente = campo_referente_inclusao.get() or None
            observacao = campo_observacao_inclusao.get() or None
           
        # Query de inserção
            query = '''
        INSERT INTO recibos (nome, cpfcnpj, endereco, aluguel, valor_liquido, referente, dataEmissao, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, observacao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # Executando a query com os parâmetros
            cursor.execute(query, (
                nome, cpfcnpj, endereco, aluguel_formatado, valor_liquido_formatado, referente, dataEmissao, agua_formatado,
                luz_formatado, condominio_formatado, iptu_formatado, internet_formatado, limpeza_formatado,
                outros_formatado, descontos_formatado, observacao
        ))

        # Commit na transação e fechamento da conexão
            conn.commit()
            cursor.close()
            conn.close()

        # Mensagem de sucesso
            messagebox.showinfo("Sucesso", "NOVO Recibo, Salvo com Sucesso!")
            janela_inclusao.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
           

    ##################### CRIANDO OS BOTÕES NA PARTE INFERIOR NA INCLUSAO DOS RECIBOS MANUAL ##################################################
    # Criando o frame para os botões (para garantir que fiquem na parte inferior)
    frame_botoes = tk.Frame(janela_inclusao)
    frame_botoes.grid(row=15, column=0, columnspan=2, pady=10)  # Colocando o frame na última linha

       # Botão "Fechar"
    botao_fechar = tk.Button(frame_botoes, text="Fechar", bg="gray", fg="white", command=janela_inclusao.destroy, width=15, height=2)
    botao_fechar.pack(side=tk.LEFT, padx=10)

    def pressionar_enter(event):
        salvar_inclusao()

     # Botão "Salvar"
    botao_salvar = tk.Button(frame_botoes, text="Salvar (Enter)", bg="green", fg="white",command=salvar_inclusao, width=15, height=2)
    botao_salvar.pack(side=tk.RIGHT, padx=10)

    # Associa a tecla Enter ao botão
    janela_inclusao.bind('<Return>', pressionar_enter)
    # Atualizar a janela (isso pode ajudar a forçar a renderização da interface corretamente)
    janela_inclusao.update()

###################################### FUNCAO PARA INCLUIR RECIBOS  MANUAL ACIMA #######


#################################### EDITAR RECIBO ###############################################################################################
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

def editar_recibo():
    try:
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado da tabela
        id_recibo = tree.item(item_selecionado)['values'][0]  # Obtém o ID do recibo selecionado

        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        # Busca os dados do recibo selecionado
        c.execute("SELECT * FROM recibos WHERE id_recibo = %s", (id_recibo,))
        dados = c.fetchone()

        # Cria a janela de edição
        janela_editar = tk.Toplevel(janela_principal)
        janela_editar.title(f"EDITANDO RECIBO N° {id_recibo}")
        janela_editar.geometry("500x680+5+5")  # Aumentando a altura da janela
        janela_editar.resizable(False, False)

        # Define os campos e os respectivos índices
        campos = [
            ("NOME", 1), ("CPF/CNPJ", 2), ("Endereco", 3), ("Referente", 6), ("ALUGUEL", 4),
            ("Água", 8), ("Luz", 9), ("Condomínio", 10), ("IPTU", 11),
            ("Internet", 12), ("Limpeza", 13), ("Outros", 14), ("DESCONTOS", 15), ("Observação", 16), ("Data de Emissão", 7),
        ]

        entradas = {}  # Para armazenar os widgets Entry
        campo_nome_inclusao = None  # Variável para armazenar o campo NOME *

        # Adicionando a data atual ao campo de Data de Emissão
        data_atual = datetime.now().strftime("%d/%m/%Y")  # Data atual no formato DD/MM/YYYY

        # Criar os rótulos e campos dinamicamente
        for i, (rotulo, indice) in enumerate(campos):
            tk.Label(janela_editar, text=f"{rotulo}:").grid(row=i, column=0, padx=10, pady=10, sticky='w')
            entrada = tk.Entry(janela_editar, width=50)
            entrada.grid(row=i, column=1, padx=10, pady=5)

            # Aplica a cor de fundo azul claro para os campos específicos
            if rotulo in ["NOME", "ALUGUEL", "Referente"]:
                entrada.config(bg="#ADD8E6")  # Azul claro (Light Blue)

            if dados[indice]:  # Se houver dados, insira no campo, senão deixe vazio
                if rotulo == "Data de Emissão":
                    # Verificar se dados[indice] é do tipo datetime
                    if isinstance(dados[indice], datetime):
                        entrada.insert(0, dados[indice].strftime("%d/%m/%Y"))
                    elif isinstance(dados[indice], str):
                        try:
                            entrada.insert(0, datetime.strptime(dados[indice], "%Y-%m-%d").strftime("%d/%m/%Y"))
                        except ValueError:
                            entrada.insert(0, data_atual)
                    else:
                        entrada.insert(0, data_atual)
                else:
                    entrada.insert(0, dados[indice])
            elif rotulo == "Data de Emissão":
                entrada.insert(0, data_atual)

            entradas[rotulo] = entrada

        # Coloca o foco no campo "NOME *"
        if "NOME" in entradas:
            entradas["NOME"].focus_set()

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

                valor_liquido = (aluguel + agua + luz + condominio + iptu + internet + limpeza + outros) - descontos
                return valor_liquido
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
                return 0

        # Função para atualizar a árvore (Treeview)
        def atualizar_árvore():
            for item in tree.get_children():
                tree.delete(item)
            conexao = conectar_mysql()
            c = conexao.cursor()
            c.execute("SELECT * FROM recibos ORDER BY id_recibo DESC")
            todos_os_dados = c.fetchall()
            conexao.close()
            for dado in todos_os_dados:
                tree.insert("", "end", values=dado)

        # Função para salvar a edição
        def salvar_edicao(event=None):
            valores = {rotulo: entrada.get() for rotulo, entrada in entradas.items()}

            if not valores.get("NOME", "").strip() or not valores.get("ALUGUEL", "").strip():
                messagebox.showwarning("Atenção", "Os campos NOME e ALUGUEL são obrigatórios.")
                return

            try:
                data_emissao = valores.get("Data de Emissão", "")
                if data_emissao:
                    try:
                        data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/YYYY.")
                        return
                else:
                    data_emissao = datetime.now().strftime("%Y-%m-%d")

                valor_liquido = calcular_valor_liquido(valores)

                conexao = conectar_mysql()
                c = conexao.cursor()
                c.execute("""UPDATE recibos SET 
                    Nome = %s, CpfCnpj = %s, Endereco = %s, ALUGUEL = %s, Referente = %s,
                    DataEmissao = %s, Agua = %s, Luz = %s, Condominio = %s, IPTU = %s,
                    Internet = %s, Limpeza = %s, Outros = %s, DESCONTOS = %s, Observacao = %s, valor_liquido = %s
                    WHERE id_recibo = %s""",
                    (valores["NOME"], valores.get("CPF/CNPJ", ""), valores.get("Endereco", ""),
                     float(valores.get("ALUGUEL", 0) or 0), valores.get("Referente", ""),
                     data_emissao, float(valores.get("Água", 0) or 0),
                     float(valores.get("Luz", 0) or 0), float(valores.get("Condomínio", 0) or 0),
                     float(valores.get("IPTU", 0) or 0), float(valores.get("Internet", 0) or 0),
                     float(valores.get("Limpeza", 0) or 0), float(valores.get("Outros", 0) or 0),
                     float(valores.get("DESCONTOS", 0) or 0), valores.get("Observação", ""), valor_liquido, id_recibo))

                conexao.commit()
                conexao.close()

                atualizar_árvore()
                messagebox.showinfo("Sucesso", f"EDIÇÃO RECIBO {id_recibo} salva com sucesso!")
                janela_editar.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")
             
        # Botão FECHAR
        btn_fechar = tk.Button(janela_editar, text="Fechar", command=janela_editar.destroy, bg="gray", fg="white", width=10)
        btn_fechar.grid(row=len(campos), column=0, padx=10, pady=10)
         
        # Botão SALVAR
        btn_incluir = tk.Button(janela_editar, text="SALVAR (Enter)", command=salvar_edicao, bg="green", fg="white", width=15)
        btn_incluir.grid(row=len(campos), column=1, padx=20, pady=10)
        
        # Associar a tecla "Enter" ao botão SALVAR
        janela_editar.bind('<Return>', lambda event: salvar_edicao())

    except IndexError:
        messagebox.showwarning("Atenção", "Nenhum recibo selecionado.")
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco: {e}")

# Garanta que a janela seja redimensionada para acomodar os botões
        janela_editar.grid_rowconfigure(len(campos), weight=1)
        janela_editar.grid_columnconfigure(0, weight=1)
        janela_editar.grid_columnconfigure(1, weight=1)

# Configuração de redimensionamento
        janela_editar.resizable(True, True)  # Permitir redimensionamento
######################################################################################
#####################################################################################
#####################################################################################
# Função chamada para fechar o menu QUAL MENU?
def fechar_menu():
    menu_post_click.unpost()  # Fecha o menu de contexto

# Função chamada quando o botão direito do mouse é pressionado
def on_right_click(event):
    try:
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado na árvore
        
        # Exibir o menu de contexto
        menu_post_click.post(event.x_root, event.y_root)
    
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo na GRID para gerar o PDF.")

####################################################################### EDITAR ACIMA #################################################################


######################### RELATORIO DE RECIBOS POR DATA

# REALTORIO POR DATA ACIMA        
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector
from mysql.connector import Error
import os
import sys

# Função para buscar recibos por data
def buscar_recibos_por_data(data_inicio, data_fim):
    try:
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()

        cursor = conexao.cursor()
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            query = """
                SELECT * FROM recibos
                WHERE dataEmissao BETWEEN %s AND %s
                ORDER BY dataEmissao
            """
            cursor.execute(query, (data_inicio, data_fim))
            dados_recibos = cursor.fetchall()
            cursor.close()
            conexao.close()
            return dados_recibos
    except Error as e:
        print(f"Erro ao consultar o Banco de Dados: {e}")
        return []

# Função para converter data de 'YYYY-MM-DD' para 'DD/MM/YYYY'
def formatar_data_para_pdf(data):
    try:
        if isinstance(data, date):
            data = data.strftime("%Y-%m-%d")
        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        return data_formatada
    except ValueError:
        return data

# Função para gerar o relatório filtrado
def gerar_relatorio_filtrado():
    try:
        # Criando a janela principal
        janela_principal = tk.Tk()
        janela_principal.withdraw()  # Ocultando a janela principal

        # Solicitar a data de início
        data_inicio = simpledialog.askstring("Data Inicio", "(ANO-MES-DIA):", parent=janela_principal)
        if not data_inicio:
            messagebox.showwarning("Atenção", "Data Inicial não Informada!")
            return

        # Criação do campo de entrada para a data final
        data_fim = simpledialog.askstring("Data Final", "(ANO-MES-DIA):", parent=janela_principal)
        if not data_fim:
            messagebox.showwarning("Atenção", "Data Final não Informada!")
            return

        # Converter as datas para o formato esperado pelo banco de dados
        try:
            data_inicio_convertida = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m-%d")
            data_fim_convertida = datetime.strptime(data_fim, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de Data Inválido. Use o formato 'YYYY-MM-DD'.")
            return

        # Buscar os dados do banco
        dados_recibos = buscar_recibos_por_data(data_inicio_convertida, data_fim_convertida)
        if not dados_recibos:
            messagebox.showwarning("Atenção", f"Não há Recibos para o Período de {data_inicio} a {data_fim}.")
            return

        # Gerar o arquivo PDF
        nome_arquivo = "Relatorio_Periodo.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        largura, altura = letter

        # Título do relatório
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, altura - 40, f"Relatório de Recibos do Período - {data_inicio} a {data_fim}")

        # Cabeçalho da tabela
        c.setFont("Helvetica", 10)
        y_position = altura - 60
        c.drawString(25, y_position, "Numero")
        c.drawString(65, y_position, "Nome")
        c.drawString(210, y_position, "CPF/CNPJ")
        c.drawString(300, y_position, "Valor")
        c.drawString(370, y_position, "DESCONTOS")
        c.drawString(440, y_position, "Data Emissão")
        c.drawString(510, y_position, "Referente")
        y_position -= 20

        # Preencher dados dos recibos
        for dado in dados_recibos:
            # Verifica se o dado não é None antes de tentar usá-lo
            numero = str(dado[0]) if dado[0] is not None else "Desconhecido"
            nome = dado[1] if dado[1] is not None else "Desconhecido"
            cpf_cnpj = dado[2] if dado[2] is not None else "Desconhecido"
            valor = f"R$ {dado[4]:.2f}" if dado[4] is not None else "R$ 0,00"
            descontos = f"R$ {dado[5]:.2f}" if dado[5] is not None else "R$ 0,00"
            referente = dado[6] if dado[6] is not None else "Desconhecido"
            
            # Verifica se a data de emissão é None
            if dado[7] is not None:
                data_emissao_formatada = formatar_data_para_pdf(dado[7])
            else:
                data_emissao_formatada = "Data Inválida"
            
            # Preenche os dados no PDF
            c.drawString(30, y_position, numero)  # Número do recibo
            c.drawString(65, y_position, nome)  # Nome
            c.drawString(210, y_position, cpf_cnpj)  # CPF/CNPJ
            c.drawString(300, y_position, valor)  # Valor
            c.drawString(370, y_position, descontos)  # Desconto
            c.drawString(440, y_position, data_emissao_formatada)  # Data de Emissão
            c.drawString(510, y_position, referente)  # Referente
            y_position -= 20

            # Criar nova página se necessário
            if y_position < 50:
                c.showPage()
                y_position = altura - 40
                c.setFont("Helvetica", 10)
                c.drawString(30, y_position, "Número Recibo")
                c.drawString(65, y_position, "Nome")
                c.drawString(210, y_position, "CNPJ")
                c.drawString(300, y_position, "Valor")
                c.drawString(370, y_position, "Desconto")
                c.drawString(440, y_position, "Data Emissão")
                c.drawString(510, y_position, "Referente")
                y_position -= 20

        # Salvar o PDF
        c.save()

        # Abrir o arquivo PDF
        if sys.platform == "win32":
            os.startfile(nome_arquivo)
        elif sys.platform == "darwin":
            os.system(f"open {nome_arquivo}")
        else:
            os.system(f"xdg-open {nome_arquivo}")

        messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso! Arquivo salvo como {nome_arquivo}")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o relatório: {str(e)}")


# RELATORIO DE TODOS OS CLIENTES NO SISTEMA
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import messagebox
import os
import sys
import mysql.connector

def rel_Clientes():
    try:
        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()

        cursor = conexao.cursor()

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar todos os dados da tabela 'pessoas' (ajustado para a tabela de clientes)
            cursor.execute("SELECT id, nome, endereco, telefone1, email, aluguel, valor_liquido, referente FROM pessoas")
            dados_clientes = cursor.fetchall()

            # Fechar a conexão
            cursor.close()
            conexao.close()

            if not dados_clientes:
                messagebox.showwarning("Atenção", "Nenhum Cliente encontrado para gerar o Relatório.")
                return

            # Criar o arquivo PDF
            nome_arquivo = os.path.join(os.getcwd(), "Relatorio_Clientes.pdf")  # Caminho absoluto

            # Verifique se o diretório de trabalho tem permissão para salvar o arquivo
            if not os.access(os.getcwd(), os.W_OK):
                messagebox.showerror("Erro", "Permissão de escrita no diretório não encontrada.")
                return
            
            c = canvas.Canvas(nome_arquivo, pagesize=letter)
            largura, altura = letter
            
            # Adicionar um título
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, altura - 40, "Relatório de Dados Cadastrais dos Clientes")

            # Adicionar os dados dos clientes no PDF
            c.setFont("Helvetica", 8)
            y_position = altura - 60  # Posição inicial para o texto
            
            # Cabeçalho da tabela
            c.drawString(15, y_position, "ID")
            c.drawString(30, y_position, "Nome")
            c.drawString(160, y_position, "Endereço")
            c.drawString(320, y_position, "Telefone")
            c.drawString(390, y_position, "Email")
            c.drawString(440, y_position, "Aluguel")
            c.drawString(490, y_position, "VALOR PAGO")
            c.drawString(550, y_position, "Referente")

            y_position -= 20  # Espaço após o cabeçalho

            # Iterar sobre os dados e adicionar no PDF
            for dado in dados_clientes:
                id_cliente, nome, endereco, telefone1, email, aluguel, valor_liquido, referente = dado

                # Tratamento para valores None (nulos)
                nome = nome if nome is not None else ""
                endereco = endereco if endereco is not None else ""
                telefone1 = telefone1 if telefone1 is not None else ""
                email = email if email is not None else ""
                aluguel = aluguel if aluguel is not None else ""
                valor_liquido = valor_liquido if valor_liquido is not None else ""
                referente = referente if referente is not None else ""

                # Escrever os dados no PDF
                c.drawString(15, y_position, str(id_cliente))  # ID
                c.drawString(30, y_position, nome)  # Nome
                c.drawString(160, y_position, endereco)  # Endereço
                c.drawString(320, y_position, telefone1)  # Telefone
                c.drawString(390, y_position, email)  # Email
                c.drawString(440, y_position, str(aluguel))  # Aluguel
                c.drawString(490, y_position, str(valor_liquido))  # VALOR PAGO
                             
                c.drawString(550, y_position, referente)  # Referente
                y_position -= 20  # Desce para a próxima linha

                # Se estiver chegando no final da página, cria uma nova
                if y_position < 50:
                    c.showPage()  # Cria uma nova página
                    c.setFont("Helvetica", 8)
                    y_position = altura - 40  # Reseta a posição Y para o topo
                    # Recria o cabeçalho da tabela na nova página
                    c.drawString(15, y_position, "ID")
                    c.drawString(30, y_position, "Nome")
                    c.drawString(160, y_position, "Endereço")
                    c.drawString(320, y_position, "Telefone")
                    c.drawString(390, y_position, "Email")
                    c.drawString(450, y_position, "Aluguel")
                    c.drawString(490, y_position, "VALOR_PAGO")
                    c.drawString(550, y_position, "Referente")
                    y_position -= 20  # Espaço após o cabeçalho

            # Tenta salvar o PDF e verifica se ocorreu algum erro
            try:
                c.save()
                
                messagebox.showinfo("Sucesso", "Relatório Dados de Clientes, Gerado com Sucesso")
                
                # Abrir o PDF gerado automaticamente após o salvamento
                if sys.platform == "win32":  # Para Windows
                    os.startfile(nome_arquivo)
                
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")  # Exibe erro no terminal
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o relatório: {e}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
 
# RELATORIOS DADOS CLIENTES ACIMA

# FUNCAO NOVA GERAR RECIBOS DO X CLIENTE APENAS OU QUBERAR POR CLIENTE
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import messagebox, simpledialog
import os
import sys

def gerar_Rel_Cliente():
    try:
        # Criar a janela de input para o nome do cliente
        nome_cliente = simpledialog.askstring("Nome do Cliente", "Informe o nome do Cliente:", parent=None)
        
        if not nome_cliente:
            messagebox.showwarning("Atenção", "Nenhum nome de Cliente Informado.")
            return
        
        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar dados filtrados pela consulta com o nome do cliente
            cursor.execute("SELECT * FROM recibos WHERE nome LIKE %s", ('%' + nome_cliente + '%',))
            dados_recibos = cursor.fetchall()

            # Fechar a conexão
            cursor.close()
            conexao.close()

            if not dados_recibos:
                messagebox.showwarning("Atenção", f"Nenhum Recibo Encontrado para o Cliente: {nome_cliente}.")
                return

            # Criar o arquivo PDF
            nome_arquivo = os.path.join(os.getcwd(), f"Relatorio_Recibos_{nome_cliente}.pdf")  # Caminho absoluto

            # Verifique se o diretório de trabalho tem permissão para salvar o arquivo
            if not os.access(os.getcwd(), os.W_OK):
                messagebox.showerror("Erro", "Permissão de escrita no diretório não encontrada.")
                return
            
            c = canvas.Canvas(nome_arquivo, pagesize=letter)
            largura, altura = letter
            
            # Adicionar um título
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, altura - 40, f"Relatório de Recibos Cliente: {nome_cliente}")

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

            # Atualize o número de colunas esperadas
            colunas = [
                'id', 'nome', 'cpf_cnpj', 'endereco', 'valor_pago', 'desconto', 'referente', 'data_emissao',
                'campo_9', 'campo_10', 'campo_11', 'campo_12', 'campo_13', 'campo_14', 'campo_15', 'campo_16',
                'observacao', 'campo_18', 'campo_19', 'campo_20'
            ]
            
            # Iterar sobre os dados e adicionar no PDF
            for dado in dados_recibos:
                print(f"Dados recebidos: {dado}")  # Depuração para ver o que está sendo retornado
                
                # Verifique se o número de colunas é o esperado (20 campos)
                if len(dado) != len(colunas):
                    print(f"Erro: Esperado {len(colunas)} campos, mas encontrado {len(dado)} campos. Recebido: {dado}")
                    continue  # Pule este recibo se o número de campos for incorreto

                # Crie um dicionário com os dados
                recibo = dict(zip(colunas, dado))  # Mapeia os dados para as colunas
                print(f"Recibo processado: {recibo}")  # Exemplo de como acessar os dados

                # Acessando os campos do recibo diretamente pelo dicionário
                numero = recibo['id']
                nome = recibo['nome']
                cpf_cnpj = recibo['cpf_cnpj']
                valor_pago = recibo['valor_pago']
                desconto = recibo['desconto']
                data_emissao = recibo['data_emissao']
                referente = recibo['referente']

                # Verifique se o valor_pago e desconto são válidos e converta-os para float
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
                c.drawString(440, y_position, str(data_emissao))  # Data de Emissão
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
                messagebox.showinfo("Sucesso", f"Relatório Gerado com Sucesso: {nome_arquivo}")
                
                # Abrir o PDF gerado automaticamente após o salvamento
                if sys.platform == "win32":  # Para Windows
                    os.startfile(nome_arquivo)
                
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")  # Exibe erro no terminal
                messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o relatório: {e}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# RELATORIO DE TODOS OS CLIENTES ACIMA

# OPÇOES DO SISTEMA
def opcoes_sistema():
    messagebox.showinfo("Em Desenvolvimento!","DÚVIDAS: (54) 9 9104-1029")  


########################################################################################################################################################
###################################### CADASTRO DE CLIENTE 
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Função para salvar o cliente no banco de dados MySQL
def salvar_cliente():
    try:
        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()
        cursor = conn.cursor()

        nome = campo_nome_inclusao.get()
        fantasia = campo_fantasia_inclusao.get() or ''
        cpfcnpj = campo_cpfcnpj_inclusao.get() or None
        ie = campo_ie_inclusao.get() or None
        contato = campo_contato_inclusao.get() or None
        email = campo_email_inclusao.get() or None
        telefone1 = campo_telefone1_inclusao.get() or None
        telefone2 = campo_telefone2_inclusao.get() or None
        endereco = campo_endereco_inclusao.get()
        numero = campo_numero_inclusao.get() or None
        complemento = campo_complemento_inclusao.get() or None
        bairro = campo_bairro_inclusao.get() or None
        cidade = campo_cidade_inclusao.get() or None
        aluguel = campo_aluguel_inclusao.get()
        agua = campo_agua_inclusao.get() or None
        luz = campo_luz_inclusao.get() or None
        condominio = campo_condominio_inclusao.get() or None
        iptu = campo_iptu_inclusao.get() or None
        internet = campo_internet_inclusao.get() or None
        limpeza = campo_limpeza_inclusao.get() or None
        outros = campo_outros_inclusao.get() or None
        descontos = campo_descontos_inclusao.get() or None
        referente = campo_referente_inclusao.get() or None

        # Inserir data automaticamente
        data = datetime.now().strftime('%Y-%m-%d')

        if not nome:
            messagebox.showwarning("Campos obrigatórios", "O Nome e Aluguel é obrigatório!")
            return

        # Comando SQL para inserir os dados na tabela 'pessoas' (sem o campo id e data_emissao)
        sql = """
        INSERT INTO pessoas (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, internet, limpeza, outros, referente, descontos, data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, internet, limpeza, outros, referente, descontos, data
        )

        cursor.execute(sql, valores)

        # Commitando a transação (salvando no banco de dados)
        conn.commit()

        # Fechar a conexão
        conn.close()

        messagebox.showinfo("Sucesso", "Cliente Salvo com Sucesso!")
        limpar_campos()

    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao salvar o cliente: {err}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro desconhecido: {e}")


# Função para limpar os campos após salvar
def limpar_campos():
    campo_nome_inclusao.delete(0, tk.END)
    campo_fantasia_inclusao.delete(0, tk.END)
    campo_cpfcnpj_inclusao.delete(0, tk.END)
    campo_ie_inclusao.delete(0, tk.END)
    campo_contato_inclusao.delete(0, tk.END)
    campo_email_inclusao.delete(0, tk.END)
    campo_telefone1_inclusao.delete(0, tk.END)
    campo_telefone2_inclusao.delete(0, tk.END)
    campo_endereco_inclusao.delete(0, tk.END)
    campo_numero_inclusao.delete(0, tk.END)
    campo_complemento_inclusao.delete(0, tk.END)
    campo_bairro_inclusao.delete(0, tk.END) 
    campo_cidade_inclusao.delete(0, tk.END) 
    campo_aluguel_inclusao.delete(0, tk.END)
    campo_agua_inclusao.delete(0, tk.END)
    campo_luz_inclusao.delete(0, tk.END)
    campo_condominio_inclusao.delete(0, tk.END)
    campo_iptu_inclusao.delete(0, tk.END)
    campo_internet_inclusao.delete(0, tk.END)
    campo_limpeza_inclusao.delete(0, tk.END)
    campo_outros_inclusao.delete(0, tk.END)
    campo_descontos_inclusao.delete(0, tk.END)
    campo_referente_inclusao.delete(0, tk.END)
   
# Função para fechar a janela
def fechar_janela(janela):
    janela.destroy()  # Fecha a janela

#########################################################################
# Função para abrir a janela de CADASTRO DE CLIENTES
def abrir_janela_inclusao_cliente(): # JANELA SECUNDARIA DE CONSULTA DE CLIENTES
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Cadastro de Cliente")
    janela_inclusao.geometry("600x740+5+5")  # Aumentar a altura para caber mais campos
    janela_inclusao.resizable(False, False)

    # Garantir que a janela de inclusão fique na frente da janela principal
    janela_inclusao.lift()  # Coloca a janela em primeiro plano
    janela_inclusao.attributes("-topmost", True)  # Fica sempre na frente até ser minimizada
    
    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    janela_inclusao.grid_rowconfigure(22, weight=1, minsize=20)  # Ajuste para o botão final

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="NOME:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    global campo_nome_inclusao
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=60, bg="lightblue", fg="black")
    campo_nome_inclusao.grid(row=0, column=1, padx=10, pady=5)
    campo_nome_inclusao.focus_set()

    tk.Label(janela_inclusao, text="Fantasia:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    global campo_fantasia_inclusao
    campo_fantasia_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_fantasia_inclusao.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="CPF/CNPJ:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
    global campo_cpfcnpj_inclusao
    campo_cpfcnpj_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_cpfcnpj_inclusao.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="IE:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    global campo_ie_inclusao
    campo_ie_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_ie_inclusao.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Contato:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
    global campo_contato_inclusao
    campo_contato_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_contato_inclusao.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Endereço:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    global campo_endereco_inclusao
    campo_endereco_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_endereco_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Nº:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    global campo_numero_inclusao
    campo_numero_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_numero_inclusao.grid(row=6, column=1, padx=10, pady=5)
    
    tk.Label(janela_inclusao, text=" Compl.:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    global campo_complemento_inclusao
    campo_complemento_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_complemento_inclusao.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Bairro:").grid(row=8, column=0, padx=10, pady=5, sticky='w')
    global campo_bairro_inclusao
    campo_bairro_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_bairro_inclusao.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Cidade:").grid(row=9, column=0, padx=10, pady=5, sticky='w')
    global campo_cidade_inclusao
    campo_cidade_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_cidade_inclusao.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Email:").grid(row=10, column=0, padx=10, pady=5, sticky='w')
    global campo_email_inclusao
    campo_email_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_email_inclusao.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 1:").grid(row=11, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone1_inclusao
    campo_telefone1_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_telefone1_inclusao.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 2:").grid(row=12, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone2_inclusao
    campo_telefone2_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_telefone2_inclusao.grid(row=12, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="ALUGUEL:").grid(row=13, column=0, padx=10, pady=5, sticky='w')
    global campo_aluguel_inclusao
    campo_aluguel_inclusao = tk.Entry(janela_inclusao, width=20, bg="lightblue", fg="black")
    campo_aluguel_inclusao.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Água:").grid(row=14, column=0, padx=10, pady=2, sticky='w')
    global campo_agua_inclusao
    campo_agua_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_agua_inclusao.grid(row=14, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Luz:").grid(row=15, column=0, padx=10, pady=2, sticky='w')
    global campo_luz_inclusao
    campo_luz_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_luz_inclusao.grid(row=15, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Condomínio:").grid(row=16, column=0, padx=10, pady=2, sticky='w')
    global campo_condominio_inclusao
    campo_condominio_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_condominio_inclusao.grid(row=16, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="IPTU:").grid(row=17, column=0, padx=10, pady=2, sticky='w')
    global campo_iptu_inclusao
    campo_iptu_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_iptu_inclusao.grid(row=17, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Internet:").grid(row=18, column=0, padx=10, pady=2, sticky='w')
    global campo_internet_inclusao
    campo_internet_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_internet_inclusao.grid(row=18, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Limpeza:").grid(row=19, column=0, padx=8, pady=2, sticky='w')
    global campo_limpeza_inclusao
    campo_limpeza_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_limpeza_inclusao.grid(row=19, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="OUTROS:").grid(row=20, column=0, padx=10, pady=2, sticky='w')
    global campo_outros_inclusao
    campo_outros_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_outros_inclusao.grid(row=20, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Descontos:").grid(row=21, column=0, padx=10, pady=2, sticky='w')
    global campo_descontos_inclusao
    campo_descontos_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_descontos_inclusao.grid(row=21, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Referente:").grid(row=22, column=0, padx=10, pady=2, sticky='w')
    global campo_referente_inclusao
    campo_referente_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_referente_inclusao.grid(row=22, column=1, padx=10, pady=5)

    data = datetime.now().strftime("%d/%m/%Y")  # Agora você usa diretamente datetime.now()
    global campo_data_inclusao
    campo_data_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_inclusao.grid(row=23, column=1, padx=10, pady=5)
    campo_data_inclusao.insert(0, data)
    campo_data_inclusao.grid_forget()

    campo_nome_inclusao.focus_set()

########### BOTOES INCLUIR CLIENTES
    # Botão para salvar as informações
    btn_incluir = tk.Button(janela_inclusao, text="SALVAR (Enter)", command=salvar_cliente, bg="green", fg="white", width=15)
    btn_incluir.grid(row=24, column=1, padx=5, pady=15)

    def on_enter(event):
        salvar_cliente()
        campo_nome_inclusao.focus_set()

    janela_inclusao.bind('<Return>', on_enter)
    
    btn_fechar = tk.Button(janela_inclusao, text="Fechar", command=janela_inclusao.destroy, bg="gray", fg="white", width=15)
    btn_fechar.grid(row=24, column=0, padx=5, pady=15)

######################################################################## CADASTRO DE CLIENTE ACIMA #######################

################################################################################################################################
################################################################################################################################
####################################################### GERADO RECIBO CONVERTNDO O VALOR PARA A EXTENSAO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from tkinter import messagebox
import os
from num2words import num2words  # Importa a biblioteca para converter números em texto

# Função para converter número para por extenso
def numero_por_extenso(valor):
    return num2words(valor, lang='pt_BR')

# Função para gerar e atualizar o ID do recibo
def obter_id_recibo():
    contador_path = "contador_recibo.txt"
    
    # Verifica se o arquivo existe
    if os.path.exists(contador_path):
        # Lê o contador atual
        with open(contador_path, "r") as f:
            contador = int(f.read().strip())  # Lê e converte para inteiro
    else:
        # Se o arquivo não existir, cria o arquivo e inicia o contador
        contador = 1
        with open(contador_path, "w") as f:
            f.write(str(contador))  # Inicia o contador com 1
    
    # Atualiza o contador (incrementa)
    contador += 1
    with open(contador_path, "w") as f:
        f.write(str(contador))  # Atualiza o arquivo com o novo contador
    
    return contador - 1  # Retorna o ID do recibo antes de incrementar

# FUNCAO PARA GERAR POR EXTENSO O VALOR DO ALUGUEL(VALOR PAGO)
from num2words import num2words
from decimal import Decimal, InvalidOperation

# Função para formatar valor monetário em formato R$
def formatar_valor(valor):
    try:
        # Tenta converter o valor para Decimal
        valor_decimal = Decimal(valor)
        return f"R$ {valor_decimal:,.2f}"  # Formatação monetária com duas casas decimais
    except (ValueError, InvalidOperation, TypeError):
        # Caso não seja um número válido, retorna "R$ 0.00"
        return "R$ 0.00"

# Função para formatar valor por extenso (em reais e centavos)
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


#########################################################################################################################
######################################################################################################################
#####################################################################################################################
########################################################## GERAR RECIBO ENCIMA DO CLIENTE ##########################################
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os
from num2words import num2words
from decimal import Decimal, InvalidOperation

# Definição de outras funções já existentes (como obter_id_recibo, formatar_valor, etc.)

# Função para gerar o PDF
def gerar_pdf(cliente):  # GERAR O RECIBO ENCIMA DO PROPRIO CADASTRO DO CLIENTE, COM O BOTÃO DIREITO DO MOUSE ENCIMA DA LINHA DO X CLIENTE
    try:
        print(f"Cliente selecionado: {cliente}")  # Depuração para ver os dados
        print(f"Tamanho da lista cliente antes de ajustes: {len(cliente)}")  # Depuração do tamanho da lista

        # Substituir valores ausentes por "Não informado"
        cliente = [campo if campo not in [None, 'None', ''] else "Não informado" for campo in cliente]

        # Garantir que a lista tenha pelo menos 23 campos
        if len(cliente) < 23:
            cliente.extend(["Não informado"] * (23 - len(cliente)))  # Preencher até 23 elementos

        print(f"Lista cliente após ajustes: {cliente}")  # Verifique a lista após os ajustes
        print(f"Tamanho da lista cliente após ajustes: {len(cliente)}")  # Verifique o tamanho após os ajustes
        
        # Criando um dicionário para mapear os campos
        campos_cliente = {
            "nome": cliente[1],
            "cpfcnpj": cliente[4],
            "endereco": cliente[9],
            "numero": cliente[10],
            "bairro": cliente[11],
            "cidade": cliente[12],
            "agua": cliente[15],
            "luz": cliente[16],
            "condominio": cliente[17],
            "iptu": cliente[18],
            "internet": cliente[19],
            "limpeza": cliente[19],
            "outros": cliente[20],
            "descontos": cliente[21],
            "referente": cliente[22]
        }

        # A partir daqui, você pode acessar os dados do cliente normalmente
        nome = campos_cliente["nome"]
        cpfcnpj = campos_cliente["cpfcnpj"]
        endereco = campos_cliente["endereco"]
        numero = campos_cliente["numero"]
        bairro = campos_cliente["bairro"]
        cidade = campos_cliente["cidade"]
        agua = campos_cliente["agua"]
        luz = campos_cliente["luz"]
        condominio = campos_cliente["condominio"]
        iptu = campos_cliente["iptu"]
        internet = campos_cliente["internet"]
        limpeza = campos_cliente["limpeza"]
        outros = campos_cliente["outros"]
        descontos = campos_cliente["descontos"]
        referente = campos_cliente["referente"]

        # Verificar se o NOME CLIENTE está no formato correto para o nome do arquivo
        if not nome or nome == "Não informado":
            messagebox.showerror("Erro", "O nome do cliente não está informado.")
            return

        # Obter o ID do recibo usando o contador
        id_recibo = obter_id_recibo()

        # Gerar o nome do arquivo com o ID do recibo
        pdf_filename = f"Recibo_{id_recibo}_{cpfcnpj}_Padrao.pdf" if nome == "Não informado" else f"Recibo_{id_recibo}_{nome}_Padrao.pdf"
        print(f"Gerando PDF: {pdf_filename}")  # Depuração

        # Criação do canvas para o PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Dimensões da página
        page_width, page_height = letter

        # Função para desenhar o logo
        def desenhar_logo(canvas, y_position):
            try:
        # Substitua pelo caminho correto do arquivo de logo
                logo_path = "logo.png"  # Caminho do arquivo logo (ajuste conforme necessário)
                x_position = 45  # Ajuste a posição X conforme necessário
                width = 110  # Largura do logo
                height = 65  # Altura do logo

        # Tente desenhar a imagem
                canvas.drawImage(logo_path, x_position, y_position, width, height, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"Erro ao carregar o logo: {e}")

        # Função para desenhar os dados financeiros no PDF
        def desenhar_pessoa(c, y_position, id, operacao, pessoa_dados):
            c.setFont("Helvetica", 10)

            try:
                aluguel_valor = float(pessoa_dados[12])
            except ValueError:
                aluguel_valor = 0.0

            aluguel_por_extenso = formatar_valor_por_extenso(aluguel_valor)
            texto = f"Recebemos de {operacao} {pessoa_dados[1]}, CPF/CNPJ: {pessoa_dados[3]}, Residente na {pessoa_dados[8]}, {pessoa_dados[9]}, {pessoa_dados[10]}, {pessoa_dados[11]}. O VALOR de: R$ {pessoa_dados[12]}({aluguel_por_extenso}), REFERENTE: {pessoa_dados[22]}."

            largura_maxima = 450
            palavras = texto.split(" ")
            linha_atual = ""
            linhas = []

            for palavra in palavras:
                if c.stringWidth(linha_atual + " " + palavra if linha_atual else palavra) <= largura_maxima:
                    linha_atual += " " + palavra if linha_atual else palavra
                else:
                    linhas.append(linha_atual)
                    linha_atual = palavra

            if linha_atual:
                linhas.append(linha_atual)

            for linha in linhas:
                c.drawString(50, y_position, linha)
                y_position -= 12

            campos_financeiros = [
                ("ALUGUEL", pessoa_dados[13]),
                ("Água", pessoa_dados[14]),
                ("Luz", pessoa_dados[15]),
                ("Condomínio", pessoa_dados[16]),
                ("IPTU", pessoa_dados[17]),
                ("Internet", pessoa_dados[18]),
                ("Limpeza", pessoa_dados[19]),
                ("Outros", pessoa_dados[20]),
                ("- DESCONTOS", pessoa_dados[21]),
                ("Total Líquido", pessoa_dados[12])
            ]

            y_position -= 12
            for descricao, valor in campos_financeiros:
                valor_formatado = formatar_valor(valor)
                c.drawString(50, y_position, descricao)
                c.drawString(450, y_position, valor_formatado)
                y_position -= 12

            y_position -= 10

            data_original = pessoa_dados[6]
            if data_original == "Não informado" or not data_original:
                data_formatada = datetime.now().strftime("%d/%m/%Y")
            else:
                try:
                    if isinstance(data_original, str):
                        data_original = datetime.strptime(data_original, "%Y-%m-%d")
                    data_formatada = data_original.strftime("%d/%m/%Y")
                except ValueError:
                    data_formatada = datetime.now().strftime("%d/%m/%Y")

            c.drawString(50, y_position, f"Recebido Em: {data_formatada}                          IMOBILIARIA LIDER")
            y_position -= 30

            c.drawString(80, y_position, f"                       Ass:_____________________________________")
            y_position -= 5

            return y_position

        # Ajuste da posição inicial de Y para a primeira via
        y_position_inicial = 725
        desenhar_logo(c, y_position_inicial)  # Logo na primeira via
        y_position = desenhar_dados_empresa(c, y_position_inicial, id_recibo)  # Dados da empresa na primeira via
        y_position -= 10
        desenhar_pessoa(c, y_position, id_recibo, "Aluguel", cliente)  # Primeira via

        # Desenhar o retângulo ao redor da primeira via (sem alterar layout)
        c.setStrokeColorRGB(0, 0, 0)  # Cor da borda (preto)
        c.setLineWidth(1)  # Espessura da linha
        
        # Ajuste da posição para a segunda via
        y_position_inicial = 310
        desenhar_logo(c, y_position_inicial)  # Logo na segunda via
        y_position = desenhar_dados_empresa(c, y_position_inicial, id_recibo)  # Dados da empresa na segunda via
        y_position -= 10
        desenhar_pessoa(c, y_position, id_recibo, "Aluguel", cliente)  # Segunda via

        # Desenhar o retângulo
        c.rect(20, 390, 570, 400, stroke=1, fill=0)  # Ajuste o valor de Y (200) para subir

        # Retângulo ao redor da segunda via
        c.rect(20, 5, 570, 380, stroke=1, fill=0)  # Ajuste o valor de Y (50) para a segunda via

        # Salvar o PDF
        c.save()

        messagebox.showinfo("PDF Gerado", f"Recibo Nº {id_recibo} para {nome}, Gerado com Sucesso!")
        os.startfile(pdf_filename)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        print(f"Erro ao gerar o PDF: {e}")


###################################################### PEGAR O X CLIENTE NA GRID DE CONSULTA PARA GERAR O RECIBO DO CLIENTE

# Função para testar com a interface gráfica
def obter_cliente_selecionado():
    selected_item = tree.selection()  # Pega o item selecionado no Treeview
    if selected_item:
        cliente = tree.item(selected_item)["values"]  # Pega os valores da linha
        print(f"Cliente selecionado: {cliente}")  # Depuração para verificar se o cliente foi obtido corretamente
        gerar_pdf(cliente)  # Chama a função gerar_pdf com os dados do cliente selecionado
    else:
        messagebox.showwarning("Seleção Inválida", "Nenhum Cliente Selecionado.")


    # Após fechar a janela de sucesso, traz a janela_consulta para frente
    janela_consulta.after(100, lambda: janela_consulta.lift())  # Traz a janela para frente após a mensagem

def abrir_janela_consulta_clientes():
    global tree, janela_consulta

    # Criando a janela de consulta
    janela_consulta = tk.Toplevel()
    janela_consulta.title("Consulta de Clientes")
    janela_consulta.geometry("1360x640+5+5")
    # Define a janela como fullscreen
    #janela_consulta.attributes('-fullscreen', True)
    
    cols = ("Codigo", "Nome", "Fantasia", "CPFCNPJ", "Telefone", "Celular", "CONTATO", "E-mail", "Endereco", "Nº", "Bairro", "Cidade", "VLR_RECIBO", "ALUGUEL", "AGUA", "LUZ", "CONDOMINIO", "IPTU", "INTERNET", "LIMPEZA", "OUTROS", "Descontos", "REF")
    tree = ttk.Treeview(janela_consulta, columns=cols, show="headings")
    
    larguras = [15, 130, 60, 75, 80, 60, 30, 80, 150, 25, 55, 100, 70, 40, 38, 40, 40, 40, 40, 40, 40, 40, 40]
    for col, largura in zip(cols, larguras):
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=largura)

    tree.tag_configure("blue", background="#D0E0FF")  # Cor azul claro
    tree.tag_configure("gray", background="#F0F0F0")  # Cor cinza claro  
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
   

    # Adicionar um menu de contexto (botão direito do mouse)
    def exibir_menu(event):
        item = tree.identify('item', event.x, event.y)  # Identifica o item sob o cursor
        if item:
            menu = tk.Menu(janela_consulta, tearoff=0)
            menu.add_command(label="Gerar Recibo", command=lambda: gerar_recibo_cliente(item))  # Adiciona opção de gerar recibo
            menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", exibir_menu)  # Bind para o botão direito

    # Função para gerar o recibo do cliente
    def gerar_recibo_cliente(item):
        cliente = tree.item(item, 'values')  # Pega os dados da linha selecionada
        if cliente:
            gerar_pdf(cliente)  # Chama a função de gerar PDF

    # Restante do código para buscar clientes no banco e atualizar a Treeview
    def procurar_cliente():
        nome_cliente = entry_nome_cliente.get().strip()
        for item in tree.get_children():
            tree.delete(item)

        try:
            # Conectar ao banco de dados MySQL
            conexao = conectar_mysql()
            c = conexao.cursor()

            conn = conexao = conectar_mysql()

            c = conexao.cursor()

            cursor = conexao.cursor()

            if nome_cliente:
                cursor.execute("""
                SELECT id, nome, fantasia, cpfcnpj, telefone1, telefone2, contato, email, endereco, numero, bairro, cidade, valor_liquido, aluguel, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, referente
                FROM pessoas
                WHERE nome LIKE %s
                ORDER BY id DESC
                """, ('%' + nome_cliente + '%',))
            else:
                cursor.execute("""
                SELECT id, nome, fantasia, cpfcnpj, telefone1, telefone2, contato, email, endereco, numero, bairro, cidade, valor_liquido, aluguel, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, referente
                FROM pessoas
                ORDER BY id DESC
                """)

            clientes = cursor.fetchall()

            # Preencher a Treeview com os dados
             # Preencher a Treeview com os dados e alternar as cores das linhas
            for i, cliente in enumerate(clientes):
                item_id = tree.insert("", tk.END, values=cliente)
                
                # Alternando entre tags "blue" e "gray"
                if i % 2 == 0:
                    tree.item(item_id, tags=("blue",))  # Linha azul
                else:
                    tree.item(item_id, tags=("gray",))  # Linha cinza

            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao Consultar os Clientes: {err}")

# GERAR RECIBO ENCIMA DO CLIENTE ACIMA

############################################################################
######################################## EDITAR CLIENTE################   
    # Função de editar cliente
    def editar_cliente():
        item = tree.selection()  # Pega o item selecionado na Treeview
        if item:
            cliente = tree.item(item, "values")  # Pega os dados da linha selecionada
            id_cliente = cliente[0]  # O ID do cliente está na primeira coluna
            print(f"Editando o Cliente com ID: {id_cliente}")

        # Criar a janela de edição
            janela_edicao_cliente = tk.Toplevel()
            janela_edicao_cliente.title(f"Edição de Cliente {id_cliente}")
            janela_edicao_cliente.geometry("480x650+5+5")
            janela_edicao_cliente.resizable(False, False)

        # Criando as labels (descrições) e campos de edição
            labels = [
            "Id", "NOME", "Fantasia", "CPF/CNPJ", "Telefone", "Celular", "Contato", "e-mail", "Endereço", 
            "N°", "Bairro", "Cidade", "VALOR_RECIBO", "ALUGUEL", "Agua", "Luz", "Condomínio", "IPTU", 
            "Internet", "limpeza", "OUTROS", "Descontos", "Referente"
            ]

            entradas = []  # Lista para armazenar as entradas criadas

        # Criando os campos de entrada
            for i, label_text in enumerate(labels[1:]):  # Ignora o primeiro campo (Id)
                label = tk.Label(janela_edicao_cliente, text=f"{label_text}:")
                label.grid(row=i, column=0, padx=10, pady=3, sticky="e")

                entry = tk.Entry(janela_edicao_cliente, width=50)
                if label_text == "Valor_Liquido":  # Se for o campo 'VALOR_RECIBO', deixamos ele desabilitado.
                    entry.config(state="readonly")
                entry.grid(row=i, column=1, padx=10, pady=3)
                entradas.append(entry)  # Adiciona a entrada à lista

        # Limpar os campos antes de preencher com dados
            for entry in entradas:
                entry.delete(0, tk.END)  # Limpa os campos de entrada antes de preencher

        # Preenchendo as entradas com os valores do cliente
            idx_cliente = 1  # Índice inicial do cliente após o 'Id' e 'Data' removida
            for i, entry in enumerate(entradas):
                try:
                    valor = cliente[idx_cliente]  # Preenche com os dados correspondentes

                # Se o valor for None, substitua por uma string vazia
                    if valor is None or valor == "None" or valor == "ONE":
                        valor = ""  # Deixa o campo vazio se o valor for None ou "ONE"

                    print(f"Preenchendo campo {labels[i + 1]} com valor: {valor}")  # Debugging
                    entry.insert(0, valor)  # Preenche com os dados correspondentes

                    idx_cliente += 1
                except IndexError:
                    entry.insert(0, "")  # Se não encontrar dados, insira vazio

        # Adicionar o campo VALOR_LIQUIDO, que é calculado a partir dos outros valores
            valor_liquido_label = tk.Label(janela_edicao_cliente, text="VALOR_LIQUIDO/Pago:")
            valor_liquido_label.grid(row=len(labels) - 1, column=0, padx=10, pady=1, sticky="e")

            valor_liquido_value = tk.Label(janela_edicao_cliente, text="0.00")  # Inicializa com 0.00
            valor_liquido_value.grid(row=len(labels) - 1, column=1, padx=10, pady=2)

        # Função para calcular o valor líquido e atualizar o Label de VALOR_LIQUIDO
            def calcular_valor_liquido():
                aluguel = float(entradas[12].get() or 0)
                agua = float(entradas[13].get() or 0)
                luz = float(entradas[14].get() or 0)
                condominio = float(entradas[15].get() or 0)
                iptu = float(entradas[16].get() or 0)
                internet = float(entradas[17].get() or 0)
                limpeza = float(entradas[18].get() or 0)
                outros = float(entradas[19].get() or 0)
                descontos = float(entradas[20].get() or 0)

            # Fórmula para calcular o valor líquido
                valor_liquido = (aluguel + agua + luz + iptu + condominio + internet + limpeza + outros) - descontos
                valor_liquido_value.config(text=f"{valor_liquido:.2f}")  # Atualiza o valor no Label

        # Calcular o valor líquido sempre que qualquer campo relevante for alterado
            for i in range(12, 21):
                entradas[i].bind("<FocusOut>", lambda event: calcular_valor_liquido())

        # Função para salvar a edição
            def salvar_edicao():
                try:
                    conn = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='mysql147',
                        database='dados'
                    )
                    cursor = conn.cursor()

                # Recuperar os valores das entradas
                    valores = [entry.get() for entry in entradas]

                # Ajustar os campos numéricos (como 'descontos', 'aluguel', 'valor_liquido', etc)
                    for i in range(len(valores)):
                        if valores[i] == "" or valores[i] is None:
                            valores[i] = None  # Deixa como NULL se vazio
                        else:
                        # Verificar se o valor é numérico antes de tentar a conversão
                            try:
                                if isinstance(valores[i], str) and valores[i].replace(",", "", 1).replace(".", "").isdigit():
                                    valores[i] = valores[i].replace(",", ".")  # Garante que a vírgula seja tratada como ponto decimal
                                    valores[i] = float(valores[i])  # Converte para float
                            except ValueError:
                                valores[i] = 0.00  # Se falhar, coloca 0.00 no campo numérico

                # Atualiza o valor líquido com o valor calculado
                    valor_liquido = float(valor_liquido_value.cget("text"))
                    valores[11] = valor_liquido  # Atualiza o valor_liquido na lista de valores

                    valores.append(id_cliente)  # Adiciona o id_cliente no final da tupla

                # Verificar se o número de valores corresponde ao número de parâmetros na consulta SQL
                    expected_length = 23  # São 22 campos a serem atualizados
                    if len(valores) != expected_length:
                        messagebox.showerror("Erro", f"Erro: número incorreto de parâmetros. Esperado {expected_length}, mas encontrado {len(valores)}.")
                        return  # Não prosseguir se o número de parâmetros não estiver correto

                # Criando a consulta SQL
                    sql = """
                    UPDATE pessoas SET 
                        nome = %s, fantasia = %s, cpfcnpj = %s, telefone1 = %s, telefone2 = %s, contato = %s, email = %s, endereco = %s, numero = %s,
                        bairro = %s, cidade = %s, aluguel = %s, valor_liquido = %s, agua = %s, luz = %s, condominio = %s, iptu = %s, internet = %s, limpeza = %s, 
                        outros = %s, descontos = %s, referente = %s
                    WHERE id = %s
                    """

                    cursor.execute(sql, tuple(valores))  # Passa os valores para o SQL
                    conn.commit()

                    messagebox.showinfo("Sucesso", f"Cliente {id_cliente} Atualizado com Sucesso!")
                    conn.close()
                    janela_edicao_cliente.destroy()

                except mysql.connector.Error as err:
                    print(f"Erro ao salvar: {err}")  # Exibir o erro específico no console
                    messagebox.showerror("Erro", f"Erro ao salvar a edição: {err}")


   
######### BOTOES JANELA EDITAR CLIENTES
    # Botão Salvar com cor verde e texto branco
        btn_salvar = tk.Button(janela_edicao_cliente, text=" Salvar   (Enter)     ) ...)", command=salvar_edicao, bg="green", fg="white")
        btn_salvar.grid(row=len(labels) - 1, column=1, padx=15, pady=15, sticky="e")  # Alinhado à direita

# Binding para tecla Enter chamar a função salvar_edicao
        janela_edicao_cliente.bind('<Return>', lambda event: salvar_edicao())

    # Botão Fechar
        btn_fechar = tk.Button(janela_edicao_cliente, text="Fechar", command=janela_edicao_cliente.destroy, bg="gray", fg="white")
        btn_fechar.grid(row=len(labels) - 1, column=1, padx=5, pady=10, sticky="e")  # Alinhado à esquerda

         
    # Campo de texto para procurar cliente
    lbl_nome_cliente = tk.Label(janela_consulta, text="Procurar Cliente:")
    lbl_nome_cliente.pack(side=tk.LEFT, padx=15, pady=35)

    entry_nome_cliente = tk.Entry(janela_consulta)
    entry_nome_cliente.pack(side=tk.LEFT, padx=10, pady=10)

    # Botão para procurar cliente
    btn_procurar = tk.Button(janela_consulta, text="PROCURAR (Enter)", command=procurar_cliente, bg="orange", fg="black")
    btn_procurar.pack(side=tk.LEFT, padx=10, pady=10)

# Binding para tecla Enter chamar a função procurar_cliente
    janela_consulta.bind('<Return>', lambda event: procurar_cliente())

# Função para exibir a janela de sucesso
    def exibir_mensagem_sucesso():
        messagebox.showinfo("Cliente Atualizado", "Cliente Atualizado com Sucesso!")
        janela_consulta.after(100, lambda: janela_consulta.lift())

# Botões para a Janela de Consulta de Clientes
    btn_incluir_cliente = tk.Button(janela_consulta, text="INCLUIR", command=abrir_janela_inclusao_cliente, bg="green", fg="white")
    btn_incluir_cliente.pack(padx=10, pady=10)
   
    btn_editar = tk.Button(janela_consulta, text="EDITAR", command=editar_cliente, bg="blue", fg="white")
    btn_editar.pack(padx=10, pady=10)

    btn_fechar = tk.Button(janela_consulta, text="Fechar", command=janela_consulta.destroy, bg="gray", fg="white")
    btn_fechar.pack()

##################################################################################### EDITANDO O CLIENTE ACIMA

###################################### GERANDO O PDF COM BOTAO DIREITO DO MOUSE - RECIBO SIMPLES
from tkinter import ttk, Menu, messagebox
import mysql.connector  # Importação correta para MySQL
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime  # Importando datetime para usar a data atual

# Função para gerar PDF - que É O RECIBO SIMPLES, - AVULSO, MAS SE MEXER NO GERAR MES NAO FUNCIONA.
def gerar_mes():
    try:  
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado na árvore
        id_recibo = tree.item(item_selecionado)['values'][0]  # Pegando o ID do recibo

        # Conectando ao banco de dados para pegar os dados do recibo
        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()

        cursor = conexao.cursor()
        
        # Executando a consulta SQL
        cursor.execute("SELECT * FROM recibos WHERE id_recibo = %s", (id_recibo,))
        
        # Buscando o resultado
        recibos = cursor.fetchone()
        
        # Fechando a conexão
        conexao.close()
        
        if recibos:
            # Criando o arquivo PDF com o nome do recibo
            caminho_pdf = f"recibo_{id_recibo}.pdf"
            c = canvas.Canvas(caminho_pdf, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Inserindo o logo no topo (ajuste o caminho do arquivo de imagem)
            logo_path = "logo.png"  # Caminho para o arquivo de imagem do logo
            c.drawImage(logo_path, 100, 710, width=120, height=80)  # Ajuste o tamanho e posição conforme necessário

            # Título do Recibo
            c.setFont("Helvetica-Bold", 16)
            c.drawString(225, 760, f"Recibo Avulso N°: {recibos[0]}")
            
            # Adicionando informações do recibo
            c.setFont("Helvetica", 12)
            c.drawString(100, 695, f"Nome: {recibos[1]}")
            c.drawString(100, 675, f"CPF/CNPJ: {recibos[2]}")
            c.drawString(100, 655, f"Endereco: {recibos[3]}")
            c.drawString(100, 635, f"Valor Pago: R$ {recibos[5]:.2f}")
            c.drawString(100, 615, f"Aluguel: R$ {recibos[4]:.2f}")
            c.drawString(100, 595, f"Descontos: {recibos[15]}")
            c.drawString(100, 575, f"Referente: {recibos[6]}")
            c.drawString(100, 555, f"Observacao: {recibos[16]}")
            c.drawString(100, 525, f"Tipo: RECEBEMOS ( )     PAGAMOS ( )")
            c.drawString(100, 495, "        IMOBILAIRA LIDER      Porto Xavier - RS ")
            c.drawString(100, 465, "ASS ---------------------------------------")

            # Obtendo a data atual
            data_atual = datetime.now().strftime("%d/%m/%Y")  # Formato: DD/MM/YYYY
            c.drawString(100, 445, f"Data Emissao: {data_atual}")  # Substituindo pela data atual

            # AJUSTE RETANGULO
            c.rect(20, 390, 570, 400, stroke=1, fill=0)  # Ajuste o valor de Y (200) para subir

        
            # Salvar o PDF
            c.save()

            os.startfile(caminho_pdf)  # Abre o arquivo PDF gerado
            # Mensagem de sucesso
            messagebox.showinfo("Sucesso", f"Recibo_Avulso_{id_recibo}, Gerado com Sucesso!")
        
        else:
            messagebox.showerror("Erro", "Recibo Não Encontrado.")

    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um Recibo na GRID para Gerar o PDF.")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ou executar a consulta: {err}")
        messagebox.showerror("Erro de Banco de Dados", "Erro ao acessar o banco de dados.")

############################################################### ACIMA IMPRESSAO DO PDF COM BOTAO DIREITO MOUSE DATA ATUAL AVULSO RESUMIDO



############################################### GERAR RECIBO PADRAO 2 VIAS - LOGO - SELECIONAR - COM DATA DE CRIACAO
   
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
    c.drawImage("logo.png", 55, y_position, width=105, height=75)  # Ajuste a posição e tamanho do logo conforme necessário

# Função para desenhar os dados da empresa ao lado do logo
def desenhar_dados_empresa(c, y_position, id_recibo):
    x_position_empresa = 180  # Definido para começar um pouco à direita do logo (ajustável conforme necessário)
    c.setFont("Helvetica", 14)
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

def gerar_recibo_padrao():  # SELECIONA O ID_RECIBO E PREVISUALIZA O RECIBO PADRAO COM DATA DE CRIACAO
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

        # Conectar ao banco de dados MySQL
        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()

        # Buscar os dados do recibo com o ID fornecido
        c.execute("SELECT * FROM recibos WHERE id_recibo = %s", (id_recibo,))
        dado_recibo = c.fetchone()

# Fechar a conexão
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

            # Supondo que dado_recibo[7] seja a data no formato 'YYYY-MM-DD'
            data_original = dado_recibo[7]  # A data que vem do banco de dados

# Verifica se a data original é uma string (no formato 'YYYY-MM-DD')
            if isinstance(data_original, str):
    # Converte a data no formato 'YYYY-MM-DD' para um objeto datetime
                data_original = datetime.strptime(data_original, "%Y-%m-%d")

# Agora, converte a data para o formato 'DD/MM/YYYY'
            data_formatada = data_original.strftime("%d/%m/%Y")
            
            c.drawString(50, y_position, f"Recebido Em: {data_formatada}                          IMOBILIARIA LIDER")
            y_position -= 30

            c.drawString(80, y_position,   f"                       Ass:_____________________________________")
            y_position -= 5

           
            return y_position  # Retorna a posição Y atualizada

        # Ajustar a posição inicial de Y para a primeira via
        y_position_inicial = 710

        # Desenhar as duas vias na mesma página, ajustando a posição Y
        y_position = desenhar_recibo(y_position_inicial)  # Primeira via
        y_position -= 80  # Ajuste o valor para mover a segunda via para baixo

        y_position -= 50  # Ajuste maior se necessário

        desenhar_recibo(y_position, primeira_via=False)  # Segunda via

        
        # Desenhar o retângulo - LINHA ENVOLTA RECIBO
        c.rect(20, 390, 570, 400, stroke=1, fill=0)  # Ajuste o valor de Y (200) para subir

        # Retângulo ao redor da segunda via
        c.rect(20, 5, 570, 380, stroke=1, fill=0)  # Ajuste o valor de Y (50) para a segunda via

        c.showPage()  # Chama o showPage após desenhar as duas vias
        # Salvar a página do PDF
        c.save()

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Recibo Gerado", f"Recibo Padrao {id_recibo}, Gerado com Sucesso!")
        os.startfile(nome_arquivo)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um Erro: {str(e)}")
############################################################################# GERAR RECIBO PADRAO ACIMA COM DATA DA CRIACAO
#
#
# 
# ######################################################RECIBO PADRAO COM DATA ATUAL E BOTAO DIREITO MOUSE  DATA ATUAL
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
################################### GERAR RECIBO PADRAO DATA HOJE - ATUAL
def gerar_recibo_padrao_data():  # SELECIONA O ID_RECIBO E PREVISUALIZA O RECIBO PADRAO = FUNCAO GERAR_RECIBO_PADRAO_ COMO BOTAO DIREITO MOUSE
        if not tree.selection():
            messagebox.showwarning("Selecione Um Recibo", "Por Favor, Selecione um Recibo para Prosseguir!")
            return  # Impede a execução do resto do código

        item_selecionado = tree.selection()[0]
        id_recibo = tree.item(item_selecionado)['values'][0]
        operacao = selecionar_operacao()  # Agora você tem o valor selecionado do ComboBox

        if not operacao:
            messagebox.showwarning("Atenção", "Operação inválida. O recibo não será gerado.")
            return

        # Conectar ao banco de dados MySQL
        conexao = conectar_mysql()
        c = conexao.cursor()

        conn = conexao = conectar_mysql()

        c = conexao.cursor()
        
        # Buscar os dados do recibo com o ID fornecido
        c.execute("SELECT * FROM recibos WHERE id_recibo = %s", (id_recibo,))
        dado_recibo = c.fetchone()

# Fechar a conexão
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

        ##################  Obtendo a data atual#####################
            data_atual = datetime.now().strftime("%d/%m/%Y")  # Formato: DD/MM/YYYY
            

        ###############################################################################################    

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

            
            #c.drawString(100, 475, f"Data Emissao: {data_atual}")  # Substituindo pela data atual
            c.drawString(50, y_position, f"Recebido Em: {data_atual}                          IMOBILIARIA LIDER")
            y_position -= 30

            c.drawString(80, y_position,   f"                       Ass:_____________________________________")
            y_position -= 5

            
            return y_position  # Retorna a posição Y atualizada

        # Ajustar a posição inicial de Y para a primeira via
        y_position_inicial = 710

        # Desenhar as duas vias na mesma página, ajustando a posição Y
        y_position = desenhar_recibo(y_position_inicial)  # Primeira via
        y_position -= 90  # Ajuste o valor para mover a segunda via para baixo

        y_position -= 45  # Ajuste maior se necessário

        desenhar_recibo(y_position, primeira_via=False)  # Segunda via

        # Salvar a página do PDF
        c.rect(20, 390, 570, 400, stroke=1, fill=0)  # Ajuste o valor de Y (200) para subir

        # Retângulo ao redor da segunda via
        c.rect(20, 5, 570, 380, stroke=1, fill=0)  # Ajuste o valor de Y (50) para a segunda via

        c.showPage()  # Chama o showPage após desenhar as duas vias
        c.save()

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Recibo Gerado", f"Recibo {id_recibo} , com DATA DE HOJE, Gerado com Sucesso!")
        os.startfile(nome_arquivo)


################################### RECIBO PADRAO DATA ATUAL ACIMA ##################################

############################################################## FUNCAO DO BOTAO DIREITO MOUSE
# Função chamada para fechar o menu
def fechar_menu():
    menu_post_click.unpost()  # Fecha o menu de contexto

# Função chamada quando o botão direito do mouse é pressionado
def on_right_click(event):
    try:
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado na árvore
        
        # Exibir o menu de contexto
        menu_post_click.post(event.x_root, event.y_root)
    
    except IndexError:
        messagebox.showwarning("Atenção", "Selecione um RECIBO na GRID para gerar o PDF.")

# Função que gera o PDF e fecha o menu de contexto
def gerar_e_fechar():
    gerar_mes()  # Chama a função para gerar o PDF
    menu_post_click.unpost()  # Fecha o menu de contexto
################################################# USANDO O IMPRESSAO DOS DADOS CLIENTES X RECIBO ACIMA ########################



# BACKUP DO BANCO DE DADOS DO SISTEMA
import os
import subprocess
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import configparser
from datetime import datetime

# Função para obter o IP do servidor a partir do arquivo config.ini
def obter_host_config():
    config = configparser.ConfigParser()
    config.read('config.ini')  # Lê o arquivo de configuração
    # Pega o valor do host da seção [mysql]
    host = config.get('mysql', 'host', fallback='localhost')  # Default é 'localhost' se não encontrado
    return host

# Função para conectar ao MySQL
def conectar_mysql():
    try:
        host = obter_host_config()  # Obtém o host do arquivo de configuração
        user = 'root'               # Nome do usuário do MySQL
        password = 'mysql147'       # Senha do MySQL
        database = 'dados'          # Nome do banco de dados

        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para realizar o backup
def realizar_backup():
    try:
        # Obtendo o IP do servidor a partir do arquivo de configuração
        host = obter_host_config()  
        user = 'root'  # Usuário do MySQL
        senha = 'mysql147'  # Senha do MySQL
        banco = 'dados'  # Nome do banco de dados a ser feito o backup
        
        # Gerando a data atual no formato desejado
        data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato: "2024-12-08_14-30-00"
        
        # Caminho do arquivo de backup com a data no nome
        destino = f'C:\\Sigeflex\\Backup\\Backup_Dados_{data_atual}.sql'  # Caminho de destino

        # Comando mysqldump com o IP de host dinâmico
        comando_backup = f'mysqldump -h {host} -u {user} -p{senha} {banco} > "{destino}"'

        # Executando o comando
        processo = subprocess.run(comando_backup, shell=True, capture_output=True, text=True)

        # Verificando se ocorreu algum erro
        if processo.returncode != 0:
            raise Exception(processo.stderr)

        # Exibe uma mensagem de sucesso
        messagebox.showinfo("Backup Realizado com Sucesso", f"Backup do Banco de Dados do Sistema Salvo em = {destino}")
   
    except Exception as e:
        # Se houver um erro, exibe uma mensagem de erro
        messagebox.showerror("Erro", f"Erro ao realizar o backup: {e}")

# Exemplo de uso
conexao = conectar_mysql()
   
   ################################################
# Função para criar a janela principal
def criar_janela_principal():
    janela_boas = ctk.CTk()
    janela_boas.title("Tela de Boas Vinda - A GDI")
    janela_boas.geometry("730x280")
    janela_boas.resizable(False, False)

    ctk.CTkLabel(janela_boas, text="Seja Bem-Vindo! Aos Sistemas Desenvolvidos pela GDI Informática", font=("Arial", 16)).pack(pady=10)
    ctk.CTkLabel(janela_boas, text="*** Agora em MYSQL, um Banco de Dados, Muito Mais Robusto, e com Possibilidade para Fazer Backup - Versão 2024.2***", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(janela_boas, text="*** Caminho onde será salvo o Backup = C\\SIGEFLEX\\BACKUP ***", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(janela_boas, text="DÚVIDAS: (54) 9 9104-1029 com Glaucio ou E-mail = glauciogrando@gmail.com", font=("Arial", 16)).pack(pady=10)

    # Botão para realizar o backup
    btn_backup = tk.Button(janela_boas, text="Realizar Backup do Banco de Dados", command=realizar_backup, bg="green", fg="white", width=30)
    btn_backup.pack(padx=10, pady=10)

# Botão para fechar a janela
    btn_fechar = tk.Button(janela_boas, text="CONTINUAR - Entrar no Sistema", command=janela_boas.destroy, bg="purple", fg="white", width=25)
    btn_fechar.pack(padx=10, pady=10)
  
    # Executar a janela
    janela_boas.mainloop()

# Chama a função para criar a janela principal
criar_janela_principal()



# BACKUP DENTRO DO SISTEMA para SALVAR TODOS OS ARQUIVOS DENTRO DA PASTA BACKUP
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import zipfile
import shutil

def realizar_backup_2():
    # Função para atualizar a barra de progresso
    def atualizar_progresso(stdout_line):
        if "Copiados" in stdout_line:
            # Extrai o número de arquivos copiados a partir da saída do robocopy
            partes = stdout_line.split()
            if len(partes) > 3 and partes[2].isdigit():
                arquivos_copiados = int(partes[2])
                progresso['value'] = arquivos_copiados
                root.update_idletasks()

    try:
        # Caminho de origem dos arquivos
        origem = "C:\\Sigeflex\\recibo"  # Diretório de origem (os arquivos que você quer salvar)

        # Permitir que o usuário escolha o diretório de destino
        destino = filedialog.askdirectory(title="Escolha o diretório de destino")
        
        # Verifica se o usuário cancelou a escolha do diretório
        if not destino:
            raise Exception("Nenhum diretório de destino foi selecionado.")

        # Verifica se o diretório de destino existe, senão cria
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Nome do arquivo ZIP
        nome_arquivo_zip = "Backup_Sistema.zip"
        caminho_arquivo_zip = os.path.join(destino, nome_arquivo_zip)

        # Inicia a interface gráfica
        root = tk.Tk()
        root.title("Backup em Progresso")
        
        # Label de status
        label_status = tk.Label(root, text="Backup em Progresso...", padx=10, pady=10)
        label_status.pack()

        # Barra de progresso
        progresso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progresso.pack(padx=10, pady=10)

        # Comando robocopy para copiar arquivos, com opções para substituir arquivos existentes
        comando_backup = f'robocopy "{origem}" "{destino}\\temp_backup" /E /Z /R:3 /W:5 /IS /IT'

        # Executando o comando de backup dos arquivos, capturando a saída em tempo real
        processo = subprocess.Popen(comando_backup, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Loop para ler a saída em tempo real e atualizar a barra de progresso
        for stdout_line in processo.stdout:
            atualizar_progresso(stdout_line)

        # Aguarda o término do processo
        processo.communicate()

        # Ignorar códigos de erro que não sejam críticos (3 ou menores)
        if processo.returncode <= 3:
            # Compactar os arquivos copiados para um arquivo ZIP
            with zipfile.ZipFile(caminho_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root_dir, dirs, files in os.walk(os.path.join(destino, "temp_backup")):
                    for file in files:
                        zipf.write(os.path.join(root_dir, file), os.path.relpath(os.path.join(root_dir, file), os.path.join(destino, "temp_backup")))

            # Exclui o diretório temporário após a compactação
            shutil.rmtree(os.path.join(destino, "temp_backup"))

            messagebox.showinfo("Backup Realizado com Sucesso", f"Todos Arquivos da Pasta do Sistema, foi Salvo em {caminho_arquivo_zip}")
        
        else:
            # Se houver um erro fatal (código maior que 3), exibe um erro
            raise Exception(f"Erro no processo de backup. Código de erro: {processo.returncode}")

    except Exception as e:
        # Se houver um erro, exibe uma mensagem de erro
        messagebox.showerror("Erro", f"Erro ao realizar o backup: {e}")

    finally:
        # Garante que a janela será fechada independentemente de sucesso ou falha
        root.destroy()  # Fecha a janela de progresso
   
  
#################################### CRIADO ACIMA BACKUP INTERNO NO SISTEMA PARA SALVAR EM X PASTA QUE ESCOLHER

# chamar anydesk
import subprocess
import os

def acesso_remoto():
    # Caminho do programa AnyDesk
    caminho_anydesk = os.path.join(os.getcwd(), 'AnyDesk.exe')

    # Executando o AnyDesk em segundo plano
    try:
        subprocess.Popen(caminho_anydesk)  # Popen não bloqueia a execução do código
        print("AnyDesk foi executado com sucesso.")
    except FileNotFoundError:
        print("O programa AnyDesk não foi encontrado na pasta.")


########################################## CRIANDO A JANELA PRINCIPAL ABAIXO#####################
# Criando a janela principal
janela_principal = tk.Tk()
janela_principal.title("Gerenciador de Recibos - GDI")
janela_principal.geometry("1260x750+5+5")

# Criando o menu
menu_bar = tk.Menu(janela_principal)

# Menu Cadastros
menu_Cadastro = tk.Menu(menu_bar, tearoff=0)
menu_Cadastro.add_command(label="CONSULTAR/CADASTRAR Clientes", command=abrir_janela_consulta_clientes)
#menu_Cadastro.add_separator()
#menu_Cadastro.add_command(label="INCLUIR Recibo Manual", command=abrir_janela_inclusao)

# Menu Relatórios
menu_relatorios = tk.Menu(menu_bar, tearoff=0)
menu_relatorios.add_command(label="Relatório RECIBOS por Data", command=gerar_relatorio_filtrado)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório RECIBOS Por Cliente", command=gerar_Rel_Cliente)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório DADOS dos Clientes", command=rel_Clientes)
  # Se quiser uma linha separadora

# Menu Opcoes
menu_preferencias = tk.Menu(menu_bar, tearoff=0)
menu_preferencias.add_command(label="Opcoes do Sistema", command=opcoes_sistema)


# Menu Sair
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_ajuda.add_command(label="Acesso Remoto", command=acesso_remoto)
menu_ajuda.add_separator()
menu_ajuda.add_command(label="Backup de Todos os Arquivos do Sistema", command=realizar_backup_2)
menu_ajuda.add_separator()
menu_ajuda.add_command(label="Sair", command=lambda: fechar_janela(janela_principal))


# Adicionando os submenus ao menu principal
menu_bar.add_cascade(label="CADASTRO", menu=menu_Cadastro)
menu_bar.add_cascade(label="RELATORIOS", menu=menu_relatorios)
menu_bar.add_cascade(label="Preferencias", menu=menu_preferencias)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)  # Aqui adiciona o menu "Sair"

# Adicionando o menu à janela principal
janela_principal.config(menu=menu_bar)

# Configuração do grid
janela_principal.grid_rowconfigure(0, weight=1)   # Linha de pesquisa
janela_principal.grid_rowconfigure(1, weight=3)   # Árvore de dados
janela_principal.grid_rowconfigure(2, weight=1)   # Botões de Ação
janela_principal.grid_columnconfigure(0, weight=1)
janela_principal.grid_columnconfigure(1, weight=1)
janela_principal.grid_columnconfigure(2, weight=1)
janela_principal.grid_columnconfigure(3, weight=1)
#############################################################################################################

#####################################################BUSCAR CLIENTE INTERFACE PRINCIPAL
tk.Label(janela_principal, text="NOME CLIENTE:").grid(row=0, column=0, padx=3, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_recibos) # Pressionar ENTER ativa a busca


# # CODIGO PARA INSERIR DESCRIÇAO E CAMPO PARA inserir id_recibo para PROCURAR
tk.Label(janela_principal, text="NÚMERO:").grid(row=0, column=1, padx=3, pady=10, sticky='w')
campo_busca_recibo = tk.Entry(janela_principal, width=15)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_recibos)  

# Botões de funções
btn_buscar = tk.Button(janela_principal, text="PROCURAR - (Enter)", command=buscar_recibos, bg="orange", fg="black")
btn_buscar.grid(row=0, column=2, padx=10, pady=10)

btn_incluir = tk.Button(janela_principal, text="INCLUIR RECIBO MANUAL", command=abrir_janela_inclusao, bg="green", fg="white", width=20)
btn_incluir.grid(row=2, column=0, padx=10, pady=10)

btn_editar = tk.Button(janela_principal, text="EDITAR", command=editar_recibo, bg="blue", fg="white", width=10)
btn_editar.grid(row=2, column=1, padx=10, pady=10)

btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=2, column=2, padx=10, pady=10)

# Botão FECHAR
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="gray", fg="white")  # FECHAR JANELA PRINCIPAL
btn_fechar.grid(row=2, column=3, padx=10, pady=10)

# Criando a árvore (grid de dados) da TELA PRINCIPAL DE CONSULTA DOS RECIBOS
cols = ("N° RECIBO", "NOME", "Cpf/Cnpj", "Endereco", "ALUGUEL", "VLR_PAGO", "REFERENTE", "DATA", "Agua", "Luz", "Condomínio", "IPTU", "Internet", "Limpeza", "OUTROS", "DESCONTO", "OBS")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

# Definindo larguras
larguras = [18, 125, 45, 150, 30, 40, 80, 35, 20, 20, 20, 20, 20, 21, 23, 24, 25]

for col, largura in zip(cols, larguras):
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=largura)


tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')  # Grid com expansibilidade PARA MOSTRAR DADOS RECIBOS

############################################################################ BOTAO DIREITO
# Supondo que tree seja sua árvore já existente
tree.bind("<Button-3>", on_right_click)  # Associando o clique direito

# Ajustando a tela para que a árvore ocupe o restante da janela
janela_principal.grid_rowconfigure(1, weight=1)
janela_principal.grid_columnconfigure(0, weight=1)
janela_principal.grid_columnconfigure(1, weight=1)

# Criando a JANELINHA ao cliclar com o BOTAO DIREITO MOUSE
menu_post_click = Menu(janela_principal, tearoff=0)
menu_post_click.add_command(label="Impressão PADRAO", command=gerar_recibo_padrao)

menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="REIMPRESSAO com DATA de HOJE", command=gerar_recibo_padrao_data)


menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="Impressão Simples", command=gerar_e_fechar)

menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="Fechar", command=fechar_menu)


janela_principal.mainloop()





