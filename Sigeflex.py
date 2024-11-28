import customtkinter as ctk
from tkinter import messagebox
import sys
import datetime  # Para pegar a data atual
import mysql.connector
from mysql.connector import Error

# Função para obter a senha válida com base na data
def obter_senha():
    data_inicio = datetime.date(2024, 11, 25)  # Defina a data inicial aqui
    data_atual = datetime.date.today()  # Pegando a data de hoje
    dias_passados = (data_atual - data_inicio).days  # Calculando a diferença em dias

    if dias_passados <= 10:
        return "1"
    elif dias_passados <= 10 + 365:
        return "55"
    else:
        return "2"

# Função para criar a conexão com o MySQL
def conectar_mysql():
    try:
        conexao = mysql.connector.connect(
            host='localhost',    # Nome do host (normalmente 'localhost')
            user='root',         # Nome de usuário
            password='mysql147', # Sua senha do MySQL
            database='dados'     # Nome do banco de dados (ajuste conforme seu banco)
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para criar a tabela "usuarios" no MySQL (caso ainda não exista)
def criar_tabela_usuarios():
    conexao = conectar_mysql()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    login VARCHAR(50) NOT NULL,
                    senha VARCHAR(50) NOT NULL,
                    data DATE NOT NULL
                );
            ''')
            conexao.commit()
            print("Tabela 'usuarios' criada ou já existe.")
        except Error as e:
            print(f"Erro ao criar a tabela: {e}")
        finally:
            cursor.close()
            conexao.close()

# Função para obter os usuários cadastrados no banco de dados
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

# Função para verificar o login no banco de dados
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
                    janela_boas_vindas()  # Abrir a janela de boas-vindas
                else:
                    messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
        except Error as e:
            print(f"Erro ao consultar o banco de dados: {e}")
        finally:
            cursor.close()
            conexao.close()

# Função para salvar o último usuário selecionado em um arquivo
def salvar_ultimo_usuario(usuario):
    try:
        with open("config.txt", "w") as f:
            f.write(usuario)
    except Exception as e:
        print(f"Erro ao salvar o último usuário: {e}")

# Função para carregar o último usuário do arquivo
def carregar_ultimo_usuario():
    try:
        with open("config.txt", "r") as f:
            ultimo_usuario = f.read().strip()  # Lê e remove espaços em branco extras
            return ultimo_usuario
    except FileNotFoundError:
        return None  # Se o arquivo não existir, retorna None

# Função para janela de boas-vindas
def janela_boas_vindas():
    janela_boas = ctk.CTk()
    janela_boas.title("Bem Vindo A GDI!")
    janela_boas.geometry("690x200")
    janela_boas.resizable(False, False)

    ctk.CTkLabel(janela_boas, text="Seja Bem-Vindo ao Sistema GDI!", font=("Arial", 16)).pack(pady=10)
    ctk.CTkLabel(janela_boas, text="***Versão 2024.1***", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(janela_boas, text="DÚVIDAS: (54) 9 9104-1029", font=("Arial", 16)).pack(pady=10)
    
    btn_continuar = ctk.CTkButton(janela_boas, text="Continuar -Enter", command=lambda: [janela_boas.destroy()])
    btn_continuar.pack(pady=20)
    janela_boas.bind("<Return>", lambda event: btn_continuar.invoke())  # Chama a função associada ao botão

    janela_boas.mainloop()

# Função para encerrar o programa
def on_close():
    sys.exit()

# Janela de login
janela_login = ctk.CTk()
janela_login.title("Login")
janela_login.geometry("300x250")  # Aumentei a altura para caber a lista de usuários
janela_login.resizable(False, False)

# Definindo o comportamento de fechamento
janela_login.protocol("WM_DELETE_WINDOW", on_close)

# Widgets de login
ctk.CTkLabel(janela_login, text="Usuário:").grid(row=0, column=0, pady=10, padx=20)

# Obtendo a lista de usuários do banco de dados
usuarios = obter_usuarios()

# Criando o ComboBox para selecionar o usuário
entry_usuario = ctk.CTkOptionMenu(janela_login, values=[usuario[0] for usuario in usuarios])  # Só mostra os logins
entry_usuario.grid(row=0, column=1, pady=5, padx=20)

# Carregar o último usuário selecionado e definir como padrão
ultimo_usuario = carregar_ultimo_usuario()
if ultimo_usuario in [usuario[0] for usuario in usuarios]:  # Se o último usuário existir na lista
    entry_usuario.set(ultimo_usuario)
else:
    entry_usuario.set("Escolha o usuário")  # Mensagem inicial para indicar a seleção

ctk.CTkLabel(janela_login, text="Senha:").grid(row=1, column=0, pady=10, padx=20)
entry_senha = ctk.CTkEntry(janela_login, show="*")
entry_senha.grid(row=1, column=1, pady=5, padx=20)

# Colocar o foco no campo de senha após 100ms
janela_login.after(100, lambda: entry_senha.focus())

# Botões "Login" e "Fechar"
btn_login = ctk.CTkButton(janela_login, text="Entrar", command=verificar_login)
btn_login.grid(row=2, column=0, pady=20, padx=20, sticky="w", columnspan=2)

btn_fechar = ctk.CTkButton(janela_login, text="Fechar", command=on_close, fg_color="gray", width=10)
btn_fechar.grid(row=2, column=1, pady=20, padx=10, sticky="e")

# Configurando o evento de pressionamento da tecla ENTER
janela_login.bind("<Return>", lambda event: verificar_login())

# Inicializa a tabela "usuarios" no MySQL (caso ainda não exista)
criar_tabela_usuarios()

# Inicia a interface gráfica da janela de login
janela_login.mainloop()

####################################################################################################################################################
# CRIANDO A INTERFACE PRINCIPAL#########
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

# Função de Conexão com MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",  # Endereço do servidor MySQL
        user="root",       # Usuário MySQL
        password="mysql147",  # Senha MySQL
        database="dados"  # Nome do banco de dados
    )

# Funções para exclusão, busca, inclusão e geração de relatórios

# Continuando a interface da janela principal com a utilização de widgets e ações

####################################################################################################################################################
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime

# Função de Conexão com MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql147",
        database="dados"
    )

def buscar_cliente(event=None):
    # Limpar a árvore de resultados anteriores
    for item in tree.get_children():
        tree.delete(item)

    # Conectar ao MySQL
    conexao = conectar_mysql()
    c = conexao.cursor()

    # Obter os valores de busca
    nome_busca = campo_busca_nome.get()
    #id_busca = campo_busca_recibo.get()

    # Verifica se há algum critério de busca
    if nome_busca:
        c.execute("SELECT * FROM pessoas WHERE nome LIKE %s", ('%' + nome_busca + '%',))  # Buscar por Nome do Cliente
    elif nome_busca:
        c.execute("SELECT * FROM pessoas WHERE id LIKE = %s", ('%' + nome_busca + '%',))  # Buscar pelo Número CLIENTE
      
        c.execute("SELECT * FROM pessoas DESC")  # Caso não tenha critério, retorna todos os dados

    dados = c.fetchall()  # Recupera todos os dados da consulta
    conexao.close()  # Fecha a conexão com o banco

    if not dados:  # Se a consulta não retornar resultados
        messagebox.showinfo("Resultado", "Nenhum Dado Encontrado.")
        return  # Interrompe a função, não inserindo dados na árvore

    # Preenche a árvore com os dados retornados
    for dado in dados:
        tree.insert('', 'end', values=dado)  # Adiciona cada linha de dados na árvore


# Função de exclusão
def excluir_recibo():
    pass  # Aqui vai a lógica da sua função excluir_recibo

# Função de inclusão
import mysql.connector
from tkinter import messagebox
import tkinter as tk
from datetime import datetime

def abrir_janela_inclusao():
    # Criando a janela de inclusão
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Incluindo Novo Recibo")
    janela_inclusao.geometry("500x550")  # Ajuste no tamanho da janela para permitir mais espaço
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
    campo_cpfcnpj_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_cpfcnpj_inclusao.grid(row=1, column=1, padx=10, pady=5)

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
            messagebox.showerror("Erro", "Por Favor, Insira Valores Numéricos válidos nos Campos de Valor.")
            janela_inclusao.attributes('-topmost', True) 
            return 0

    def salvar_inclusao():
        nome = campo_nome_inclusao.get()
        cpfcnpj = campo_cpfcnpj_inclusao.get()
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

        try:
            # Conexão com MySQL
            conexao = mysql.connector.connect(
                host="localhost",  # Substitua pelo seu host MySQL
                user="root",     # Substitua pelo seu usuário MySQL
                password="mysql147",   # Substitua pela sua senha MySQL
                database="dados"    # Substitua pelo seu banco de dados
            )

            cursor = conexao.cursor()

            # Ajuste dos campos vazios para valores numéricos
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

            # Comando SQL para inserir os dados no banco MySQL
            query = '''
                INSERT INTO recibos (nome, cnpj, endereco, aluguel, dataEmissao, agua, luz, condominio, iptu, internet, limpeza, outros, descontos, referente, observacao, valor_liquido)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (nome, cpfcnpj, endereco, f"{aluguel:.2f}", dataEmissao, f"{agua:.2f}", f"{luz:.2f}", f"{condominio:.2f}", f"{iptu:.2f}", f"{internet:.2f}", f"{limpeza:.2f}", f"{outros:.2f}", f"{descontos:.2f}", referente, observacao, f"{valor_liquido:.2f}"))

            # Commit e fechamento da conexão
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Recibo SALVO com Sucesso!")
            janela_inclusao.destroy()
            buscar_cliente()  # Atualiza a tabela de dados na janela principal

        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao Salvar no Banco de Dados: {e}")

    # Botão para salvar
    botao_salvar = tk.Button(janela_inclusao, text="Salvar", command=salvar_inclusao, width=15, height=2)
    botao_salvar.grid(row=15, column=0, padx=10, pady=10, sticky='w')

    # Botão para fechar
    botao_fechar = tk.Button(janela_inclusao, text="Fechar", command=janela_inclusao.destroy, width=15, height=2)
    botao_fechar.grid(row=15, column=1, padx=10, pady=10, sticky='e')


#################################### EDITAR RECIBO ###############################################################################################
import mysql.connector
from tkinter import messagebox

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",  # Endereço do servidor MySQL
        user="root",       # Usuário MySQL
        password="mysql147",  # Senha MySQL
        database="dados"  # Nome do banco de dados
    )

import mysql.connector
from tkinter import messagebox

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",  # Endereço do servidor MySQL
        user="root",       # Usuário MySQL
        password="mysql147",  # Senha MySQL
        database="dados"  # Nome do banco de dados
    )

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
        janela_editar.title(f"EDITAR RECIBO {id_recibo}")
        janela_editar.geometry("400x520")
        janela_editar.resizable(False, False)

        # Define os campos e os respectivos índices
        campos = [
            ("Nome", 1), ("CPF/CNPJ", 2), ("Endereco", 3), ("Referente", 5), ("ALUGUEL", 4),
            ("Água", 7), ("Luz", 8), ("Condomínio", 10), ("IPTU", 11),
            ("Internet", 12), ("Limpeza", 13), ("Outros", 14), ("DESCONTOS", 15), ("Observação", 16), ("Data de Emissão", 6),
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
            conexao = conectar_mysql()
            c = conexao.cursor()
            c.execute("SELECT * FROM recibos ORDER BY id_recibo DESC")
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

                # Conectar ao banco de dados MySQL e salvar a edição
                conexao = conectar_mysql()
                c = conexao.cursor()

                # Atualizar os dados no banco de dados
                c.execute("""
                    UPDATE recibos
                    SET Nome = %s, CNPJ = %s, Endereco = %s, ALUGUEL = %s, Referente = %s,
                        DataEmissao = %s, Agua = %s, Luz = %s, Condominio = %s, IPTU = %s,
                        Internet = %s, Limpeza = %s, Outros = %s, DESCONTOS = %s, Observacao = %s, valor_liquido = %s
                    WHERE id_recibo = %s;
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

            except mysql.connector.Error as e:
                messagebox.showerror("Erro", f"Erro ao Salvar no Banco de Dados: {e}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")

def relatorio_por_data():
    pass
def relatorio_geral():
    pass
def imprimir_recibo_selecionado():
    pass
def fechar_janela():
    janela_principal.quit()  # Corrigido de "qui" para "quit"
####################################################################### EDITAR ACIMA #################################################################
########################################################################################################################################################
###################################### CADASTRO DE CLIENTE ABAIXO
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Função para salvar o cliente no banco de dados MySQL
def salvar_cliente():
    try:
        # Conectar ao banco de dados MySQL
        conn = mysql.connector.connect(
            host='localhost',         # Endereço do servidor (pode ser 'localhost' ou IP do servidor)
            user='root',       # Seu usuário MySQL
            password='mysql147',     # Sua senha MySQL
            database='dados' # O nome do seu banco de dados
        )
        
        # Criando um cursor para executar as queries
        cursor = conn.cursor()

        # Pegando os dados inseridos no formulário
        nome = campo_nome_inclusao.get()
        fantasia = campo_fantasia_inclusao.get() or None
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
        aluguel = campo_aluguel_inclusao.get() or None
        agua = campo_agua_inclusao.get() or None
        luz = campo_luz_inclusao.get() or None
        condominio = campo_condominio_inclusao.get() or None
        iptu = campo_iptu_inclusao.get() or None
        internet = campo_internet_inclusao.get() or None
        limpeza = campo_limpeza_inclusao.get() or None
        outros = campo_outros_inclusao.get() or None
       
       
               # Insirindo DATA automaticamente

        data = datetime.now().strftime('%Y-%m-%d')  # Formato 'AAAA-MM-DD'

        # Verificar se algum campo obrigatório está vazio (por exemplo, nome)
        if not nome:
            messagebox.showwarning("Campos obrigatórios", "O nome é obrigatório!")
            return

        # Comando SQL para inserir os dados na tabela 'pessoas' (sem o campo id e data_emissao)
        sql = """
        INSERT INTO pessoas (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, 
            internet, limpeza, outros
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Dados a serem inseridos (em ordem), incluindo o campo 'rua'
        valores = (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, 
            internet, limpeza, outros
        )

        # Verificar se o número de valores corresponde ao número de placeholders (%s)
        if len(valores) != 21:
            raise ValueError(f"O número de parâmetros não corresponde ao número de campos na consulta. Parâmetros: {len(valores)}, Query espera 21 parâmetros.")

        # Executando a inserção dos dados no banco
        cursor.execute(sql, valores)

        # Commitando a transação (salvando no banco de dados)
        conn.commit()

        # Fechar a conexão
        conn.close()

        # Informar ao usuário que o cliente foi salvo com sucesso
        messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")

        # Limpar os campos após salvar
        limpar_campos()

    except mysql.connector.Error as err:
        # Caso ocorra algum erro com o MySQL, exibe a mensagem de erro
        messagebox.showerror("Erro", f"Erro ao salvar o cliente: {err}")
    except Exception as e:
        # Caso ocorra outro erro, exibe a mensagem de erro genérica
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
   
# Função para fechar a janela
def fechar_janela(janela):
    janela.destroy()  # Fecha a janela



# Função para abrir a janela de cadastro de cliente
def abrir_janela_inclusao_cliente():
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Cadastro de Cliente")
    janela_inclusao.geometry("600x750")  # Aumentar a altura para caber mais campos
    janela_inclusao.resizable(False, False)

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    janela_inclusao.grid_rowconfigure(22, weight=1, minsize=50)  # Ajuste para o botão final

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    global campo_nome_inclusao
    campo_nome_inclusao = tk.Entry(janela_inclusao, width=60)
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
    campo_contato_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_contato_inclusao.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Email:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    global campo_email_inclusao
    campo_email_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_email_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 1:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone1_inclusao
    campo_telefone1_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_telefone1_inclusao.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 2:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone2_inclusao
    campo_telefone2_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_telefone2_inclusao.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Endereço:").grid(row=8, column=0, padx=10, pady=5, sticky='w')
    global campo_endereco_inclusao
    campo_endereco_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_endereco_inclusao.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="numero:").grid(row=9, column=0, padx=10, pady=5, sticky='w')
    global campo_numero_inclusao
    campo_numero_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_numero_inclusao.grid(row=9, column=1, padx=10, pady=5)
    
    tk.Label(janela_inclusao, text="Complemento:").grid(row=10, column=0, padx=10, pady=5, sticky='w')
    global campo_complemento_inclusao
    campo_complemento_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_complemento_inclusao.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Bairro:").grid(row=11, column=0, padx=10, pady=5, sticky='w')
    global campo_bairro_inclusao
    campo_bairro_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_bairro_inclusao.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Cidade:").grid(row=12, column=0, padx=10, pady=5, sticky='w')
    global campo_cidade_inclusao
    campo_cidade_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_cidade_inclusao.grid(row=12, column=1, padx=10, pady=5)
    
    tk.Label(janela_inclusao, text="Aluguel:").grid(row=13, column=0, padx=10, pady=5, sticky='w')
    global campo_aluguel_inclusao
    campo_aluguel_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_aluguel_inclusao.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Água:").grid(row=14, column=0, padx=10, pady=5, sticky='w')
    global campo_agua_inclusao
    campo_agua_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_agua_inclusao.grid(row=14, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Luz:").grid(row=15, column=0, padx=10, pady=5, sticky='w')
    global campo_luz_inclusao
    campo_luz_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_luz_inclusao.grid(row=15, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Condomínio:").grid(row=16, column=0, padx=10, pady=5, sticky='w')
    global campo_condominio_inclusao
    campo_condominio_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_condominio_inclusao.grid(row=16, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="IPTU:").grid(row=17, column=0, padx=10, pady=5, sticky='w')
    global campo_iptu_inclusao
    campo_iptu_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_iptu_inclusao.grid(row=17, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Internet:").grid(row=18, column=0, padx=10, pady=5, sticky='w')
    global campo_internet_inclusao
    campo_internet_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_internet_inclusao.grid(row=18, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Limpeza:").grid(row=19, column=0, padx=10, pady=5, sticky='w')
    global campo_limpeza_inclusao
    campo_limpeza_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_limpeza_inclusao.grid(row=19, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Outros:").grid(row=20, column=0, padx=10, pady=5, sticky='w')
    global campo_outros_inclusao
    campo_outros_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_outros_inclusao.grid(row=20, column=1, padx=10, pady=5)

    data = datetime.now().strftime("%d/%m/%Y")  # Agora você usa diretamente datetime.now()
    global campo_data_inclusao
    campo_data_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_inclusao.grid(row=14, column=1, padx=10, pady=5)
    campo_data_inclusao.insert(0, data)



    # Botão para salvar as informações
    botao_salvar = tk.Button(janela_inclusao, text="Salvar", command=salvar_cliente)
    botao_salvar.grid(row=21, column=1, columnspan=2, pady=20)

    # Botão para fechar a janela
    botao_fechar = tk.Button(janela_inclusao, text="Fechar", command=lambda: fechar_janela(janela_inclusao))
    botao_fechar.grid(row=21, column=0, columnspan=2)


######################################################################## CADASTRO DE CLIENTE ACIMA #######################






########################################### CRIANDO A JANELA PRINCIPAL ABAIXO
# Criando a janela principal
janela_principal = tk.Tk()
janela_principal.title("Gerenciador de Recibos - GDI")
janela_principal.geometry("1200x650+0+0")

# Criando o menu
menu_bar = tk.Menu(janela_principal)

# Menu Cadastros
menu_Clientes = tk.Menu(menu_bar, tearoff=0)
menu_Clientes.add_command(label="Cadastrar Cliente", command=abrir_janela_inclusao_cliente)
menu_Clientes.add_separator()
menu_Clientes.add_command(label="CONSULTAR Cliente", command=abrir_janela_inclusao_cliente)
menu_Clientes.add_separator()
menu_Clientes.add_command(label="Incluir Recibo Manual", command=abrir_janela_inclusao)

# Menu Relatórios
menu_relatorios = tk.Menu(menu_bar, tearoff=0)
menu_relatorios.add_command(label="Relatório por Data", command=relatorio_por_data)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório Por Cliente", command=relatorio_geral)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório Geral", command=relatorio_geral)
  # Se quiser uma linha separadora

# Menu Imprimir
menu_imprimir = tk.Menu(menu_bar, tearoff=0)
menu_imprimir.add_command(label="Imprimir Recibo Selecionado", command=imprimir_recibo_selecionado)

# Menu Sair
menu_sair = tk.Menu(menu_bar, tearoff=0)
menu_sair.add_command(label="Sair", command=fechar_janela)

# Adicionando os submenus ao menu principal
menu_bar.add_cascade(label="CLIENTES", menu=menu_Clientes)
menu_bar.add_cascade(label="Relatórios", menu=menu_relatorios)
menu_bar.add_cascade(label="Imprimir", menu=menu_imprimir)
menu_bar.add_cascade(label="FECHAR", menu=menu_sair)  # Aqui adiciona o menu "Sair"

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

# Botões e campos de entrada para busca
tk.Label(janela_principal, text="Nome do Cliente:").grid(row=0, column=0, padx=15, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_cliente) # Pressionar ENTER ativa a busca
campo_busca_nome.focus_set()

# # CODIGO PARA INSERIR DESCRIÇAO E CAMPO PARA inserir id_recibo para PROCURAR
tk.Label(janela_principal, text="Número Cliente:").grid(row=0, column=1, padx=10, pady=10, sticky='w')
campo_busca_recibo = tk.Entry(janela_principal, width=15)
campo_busca_recibo.grid(row=0, column=1, padx=10, pady=10)
campo_busca_recibo.bind("<Return>", buscar_cliente)  

# Botões de funções
btn_incluir = tk.Button(janela_principal, text="Incluir NOVO", command=abrir_janela_inclusao, bg="green", fg="white", width=10)
btn_incluir.grid(row=2, column=0, padx=10, pady=10)

btn_editar = tk.Button(janela_principal, text="EDITAR", command=editar_recibo, bg="orange", fg="red", width=10)
btn_editar.grid(row=2, column=1, padx=10, pady=10)

btn_excluir = tk.Button(janela_principal, text="Excluir", command=excluir_recibo, bg="red", fg="white")
btn_excluir.grid(row=2, column=2, padx=10, pady=10)

btn_buscar = tk.Button(janela_principal, text="PROCURAR - 'Enter'", command=buscar_cliente, bg="orange", fg="black")
btn_buscar.grid(row=2, column=3, padx=10, pady=10)

# Botão FECHAR
btn_fechar = tk.Button(janela_principal, text="Fechar", command=janela_principal.destroy, bg="gray", fg="white")  # FECHAR JANELA PRINCIPAL
btn_fechar.grid(row=3, column=3, padx=10, pady=10)

# Criando a árvore (grid de dados)
cols = ("Codigo", "Tipo", "Nome", "FANTASIA", "CPFCNPJ", "IE", "Telefone", "Celular", "CONTATO", "E-mail", "Endereco", "Nº", "COMPL.", "Bairro", "Cidade", "Data", "Aluguel")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

# Definindo larguras
larguras = [20, 10, 60, 50, 50, 50, 80, 80, 30, 100, 100, 15, 30, 50, 60, 10, 30]
for col, largura in zip(cols, larguras):
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=largura)

tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Main loop
janela_principal.mainloop()