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
                    messagebox.showerror("Erro", "Senha Incorreta. Tente Novamente.")
            else:
                messagebox.showerror("Erro", "Usuário Não Encontrado.")
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


# Função para encerrar o programa
def on_close():
    sys.exit()

# Janela de login
janela_login = ctk.CTk()
janela_login.title("Login")
janela_login.geometry("300x180")  # Aumentei a altura para caber a lista de usuários
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
######################################### LOGIN ACIMA
####################################################################################################################################################
#  TELA DE PROCURAR DOS RECIBOS NA TELA PRINCIPAL E MOSTRAR NA TELA
####################################################################################################################################################
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime

# Função de Conexão com MySQL
def buscar_recibos(event=None):
    # Limpar a árvore de resultados anteriores
    for item in tree.get_children():
        tree.delete(item)

    # Conectar ao MySQL
    conexao = conectar_mysql()
    c = conexao.cursor()

    # Obter os valores de busca
    nome_busca = campo_busca_nome.get()
    id_busca = campo_busca_recibo.get()

    # Verifica se há algum critério de busca
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
        messagebox.showinfo("Resultado", "Nenhum Dado Encontrado.")
        return  # Interrompe a função, não inserindo dados na árvore

    # Preenche a árvore com os dados retornados
    for dado in dados:
        tree.insert('', 'end', values=dado)  # Adiciona cada linha de dados na árvore



###################################################################################################################
##############################################FUNCAO DE EXCLUIR RECIBO ABAIXO
#######################################################################################################################
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
def excluir_cliente(janela_consulta, tree):
    try:
        # Obter o item selecionado (linha do Treeview)
        selected_item = tree.selection()  # Retorna a linha selecionada
        
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir!")
            return
        
        # Obter o ID_CLIENTE da linha selecionada
        id_cliente = tree.item(selected_item, 'values')[0]  # O ID_CLIENTE está na primeira coluna
        
        # Criar uma nova janela para a senha
        senha_janela = tk.Toplevel(janela_consulta)  # Cria uma janela secundária dentro de janela_consulta
        senha_janela.title("Confirmar Exclusão")
        
        # Impede que a janela principal fique à frente
        janela_principal.attributes("-topmost", False)  # Desabilita o comportamento de "sempre à frente" para a janela principal
        
        # Garantir que a janela de senha fique em primeiro plano
        senha_janela.lift()  # Coloca a janela de senha acima da janela de consulta
        senha_janela.focus_force()  # Garante que a janela de senha receba o foco
        senha_janela.grab_set()  # Captura o foco e bloqueia as outras janelas até a interação terminar
        
        # Adicionando um rótulo (Label) e campo de entrada (Entry) para a senha
        tk.Label(senha_janela, text="Digite a senha para excluir o cliente:").pack(padx=10, pady=10)
        
        senha_entry = tk.Entry(senha_janela, show="*")  # O parâmetro 'show' oculta a senha
        senha_entry.pack(padx=10, pady=5)
        
        def verificar_senha():
            senha = senha_entry.get()  # Pega a senha digitada
            
            if senha != "55":  # Definindo a senha de confirmação como '55' (modifique conforme necessário)
                messagebox.showerror("Erro", "Senha incorreta! Exclusão cancelada.")
                senha_janela.destroy()  # Fecha a janela da senha
                return
            
            # Confirmar com o usuário antes de excluir
            confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja excluir o cliente com ID {id_cliente}?")
            
            if confirm:
                try:
                    # Conectando ao banco de dados MySQL
                    conn = mysql.connector.connect(
                        host="localhost", user="root", password="mysql147", database="Dados"
                    )
                    cursor = conn.cursor()
                    
                    # Query para deletar o cliente com base no ID
                    query = "DELETE FROM pessoas WHERE ID_CLIENTE = %s"
                    cursor.execute(query, (id_cliente,))
                    conn.commit()  # Salvar a exclusão no banco
                    
                    # Fechar conexão
                    cursor.close()
                    conn.close()
                    
                    # Remover o item da interface (Treeview)
                    tree.delete(selected_item)
                    
                    # Exibir mensagem de sucesso
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    
                    # Aqui, trazemos a janela_consulta de volta para frente após a exclusão
                    janela_consulta.lift()  # Traz a janela de consulta para frente
                    janela_consulta.focus_force()  # Coloca o foco na janela de consulta

                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao excluir cliente: {err}")
            
            senha_janela.destroy()  # Fecha a janela de senha após o processo de exclusão

        # Adicionando o botão para verificar a senha
        tk.Button(senha_janela, text="Confirmar", command=verificar_senha).pack(padx=10, pady=10)
        
        # Exibir a janela de senha
        senha_janela.mainloop()

        # Garantir que a janela de consulta fique na frente após o fechamento da janela de confirmação de exclusão
        janela_consulta.lift()  # Traz a janela de consulta para frente
        janela_consulta.focus_force()  # Coloca o foco na janela de consulta

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    
    finally:
        # Certificar que a janela principal não ficará à frente das outras
        janela_principal.attributes("-topmost", True)  # Restabelece o comportamento de "sempre à frente" para a janela principal



#################################################################### ACIMA FUNÇAO EXCLUIR RECIBO###########
##########################################################################################################

######################################################################INCLUIR NOVO RECIBO ABAIXO##################
# Função de inclusão - INCLUIR NOVO RECIBO
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

def abrir_janela_inclusao():
    # Criando a janela de inclusão
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Incluindo Novo Recibo MANUAL")
    janela_inclusao.geometry("650x750")  # Ajuste no tamanho da janela para permitir mais espaço
    janela_inclusao.resizable(False, False)

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    
    # Configurando o peso das linhas para garantir que a última linha (onde os botões estão) tenha mais espaço
    for i in range(16):  # Configurando peso para as linhas, até a linha 15
        janela_inclusao.grid_rowconfigure(i, weight=1)

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
    from datetime import datetime

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
        data_emissao = campo_data_emissao_inclusao.get()
    
        if not nome or not aluguel:
            messagebox.showwarning("Atenção", "NOME e ALUGUEL são Campos Obrigatórios.")
            janela_inclusao.attributes('-topmost', True)
            return

        try:
        # Conectando ao banco de dados MySQL
            conn = mysql.connector.connect(
                host="localhost", user="root", password="mysql147", database="Dados"
        )
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
            messagebox.showinfo("Sucesso", "Recibo SALVO com Sucesso!")
            janela_inclusao.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")


            
    ##################### CRIANDO OS BOTÕES NA PARTE INFERIOR NA INCLUSAO DOS RECIBOS MANAUSI ##################################################
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

###################################### FUNCAO PARA INCLUIR RECIBOS  MANUAL ACIMA#######


#################################### EDITAR RECIBO ###############################################################################################
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
        janela_editar.geometry("400x550")  # Aumentando a altura da janela
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
            if dados[indice]:  # Se houver dados, insira no campo, senão deixe vazio
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
        def salvar_edicao(event=None):  # Aceita o parâmetro 'event' para o bind do Enter
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
                c.execute("""UPDATE recibos SET 
                    Nome = %s, CpfCnpj = %s, Endereco = %s, ALUGUEL = %s, Referente = %s,
                    DataEmissao = %s, Agua = %s, Luz = %s, Condominio = %s, IPTU = %s,
                    Internet = %s, Limpeza = %s, Outros = %s, DESCONTOS = %s, Observacao = %s, valor_liquido = %s
                    WHERE id_recibo = %s""",
                    (valores["Nome"], valores.get("CPF/CNPJ", ""), valores.get("Endereco", ""),
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

        # Adicionar os botões "Incluir" e "Fechar"
        btn_incluir = tk.Button(janela_editar, text="SALVAR (Enter)", command=salvar_edicao, bg="green", fg="white", width=15)
        btn_incluir.grid(row=len(campos), column=1, padx=10, pady=10)

        btn_fechar = tk.Button(janela_editar, text="Fechar", command=janela_editar.destroy, bg="gray", fg="white", width=10)
        btn_fechar.grid(row=len(campos), column=0, padx=10, pady=10)

        # Associar a tecla 'Enter' para chamar a função de salvar
        janela_editar.bind("<Return>", salvar_edicao)  # Quando pressionar Enter, chama salvar_edicao

    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")
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
        messagebox.showwarning("Atenção", "Selecione um item na GRID para gerar o PDF.")

####################################################################### EDITAR ACIMA #################################################################

######################### VAMOS COLOCAR AQUI OS RELATORIOS AS FUNÇOES DE CADA UM

def relatorio_por_data():
    pass
def relatorio_geral():
    pass
def imprimir_recibo_selecionado():
    pass



def fechar_janela():
    janela_principal.quit() 

######################### VAMOS COLOCAR AQUI OS RELATORIOS AS FUNÇOES DE CADA UM ACIMA

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
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mysql147',
            database='dados'
        )

        cursor = conn.cursor()

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

        # Inserir data automaticamente
        data = datetime.now().strftime('%Y-%m-%d')

        if not nome:
            messagebox.showwarning("Campos obrigatórios", "O nome é obrigatório!")
            return

        # Comando SQL para inserir os dados na tabela 'pessoas' (sem o campo id e data_emissao)
        sql = """
        INSERT INTO pessoas (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, internet, limpeza, outros
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome, fantasia, cpfcnpj, ie, contato, email, telefone1, telefone2, endereco, numero, complemento, bairro, cidade,
            aluguel, agua, luz, condominio, iptu, internet, limpeza, outros
        )

        cursor.execute(sql, valores)

        # Commitando a transação (salvando no banco de dados)
        conn.commit()

        # Fechar a conexão
        conn.close()

        messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
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
   
# Função para fechar a janela
def fechar_janela(janela):
    janela.destroy()  # Fecha a janela



# Função para abrir a janela de cadastro de cliente
def abrir_janela_inclusao_cliente():
    janela_inclusao = tk.Toplevel(janela_principal)
    janela_inclusao.title("Cadastro de Cliente")
    janela_inclusao.geometry("600x750+5+5")  # Aumentar a altura para caber mais campos
    janela_inclusao.resizable(False, False)

    # Garantir que a janela de inclusão fique na frente da janela principal
    janela_inclusao.lift()  # Coloca a janela em primeiro plano
    janela_inclusao.attributes("-topmost", True)  # Fica sempre na frente até ser minimizada
    

    # Garantir que as colunas e linhas da grid se ajustem ao tamanho da janela
    janela_inclusao.grid_columnconfigure(0, weight=1, minsize=100)
    janela_inclusao.grid_columnconfigure(1, weight=3, minsize=200)
    janela_inclusao.grid_rowconfigure(22, weight=1, minsize=50)  # Ajuste para o botão final

    # Definindo os campos de entrada
    tk.Label(janela_inclusao, text="NOME* :").grid(row=0, column=0, padx=10, pady=5, sticky='w')
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
    campo_contato_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_contato_inclusao.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="ALUGUEL* :").grid(row=5, column=0, padx=10, pady=5, sticky='w')
    global campo_aluguel_inclusao
    campo_aluguel_inclusao = tk.Entry(janela_inclusao, width=20)
    campo_aluguel_inclusao.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Endereço:").grid(row=6, column=0, padx=10, pady=5, sticky='w')
    global campo_endereco_inclusao
    campo_endereco_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_endereco_inclusao.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Nº:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    global campo_numero_inclusao
    campo_numero_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_numero_inclusao.grid(row=7, column=1, padx=10, pady=5)
    
    tk.Label(janela_inclusao, text="Nº   /    Compl.:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
    global campo_complemento_inclusao
    campo_complemento_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_complemento_inclusao.grid(row=7, column=3, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Bairro:").grid(row=9, column=0, padx=10, pady=5, sticky='w')
    global campo_bairro_inclusao
    campo_bairro_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_bairro_inclusao.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Cidade:").grid(row=10, column=0, padx=10, pady=5, sticky='w')
    global campo_cidade_inclusao
    campo_cidade_inclusao = tk.Entry(janela_inclusao, width=30)
    campo_cidade_inclusao.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Email:").grid(row=11, column=0, padx=10, pady=5, sticky='w')
    global campo_email_inclusao
    campo_email_inclusao = tk.Entry(janela_inclusao, width=60)
    campo_email_inclusao.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 1:").grid(row=12, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone1_inclusao
    campo_telefone1_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_telefone1_inclusao.grid(row=12, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Telefone 2:").grid(row=13, column=0, padx=10, pady=5, sticky='w')
    global campo_telefone2_inclusao
    campo_telefone2_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_telefone2_inclusao.grid(row=13, column=1, padx=10, pady=5)
     
    tk.Label(janela_inclusao, text="Água:").grid(row=14, column=0, padx=10, pady=5, sticky='w')
    global campo_agua_inclusao
    campo_agua_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_agua_inclusao.grid(row=14, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Luz:").grid(row=15, column=0, padx=10, pady=5, sticky='w')
    global campo_luz_inclusao
    campo_luz_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_luz_inclusao.grid(row=15, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Condomínio:").grid(row=16, column=0, padx=10, pady=5, sticky='w')
    global campo_condominio_inclusao
    campo_condominio_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_condominio_inclusao.grid(row=16, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="IPTU:").grid(row=17, column=0, padx=10, pady=5, sticky='w')
    global campo_iptu_inclusao
    campo_iptu_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_iptu_inclusao.grid(row=17, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Internet:").grid(row=18, column=0, padx=10, pady=5, sticky='w')
    global campo_internet_inclusao
    campo_internet_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_internet_inclusao.grid(row=18, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="Limpeza:").grid(row=19, column=0, padx=10, pady=5, sticky='w')
    global campo_limpeza_inclusao
    campo_limpeza_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_limpeza_inclusao.grid(row=19, column=1, padx=10, pady=5)

    tk.Label(janela_inclusao, text="OUTROS:").grid(row=20, column=0, padx=10, pady=5, sticky='w')
    global campo_outros_inclusao
    campo_outros_inclusao = tk.Entry(janela_inclusao, width=15)
    campo_outros_inclusao.grid(row=20, column=1, padx=10, pady=5)

    data = datetime.now().strftime("%d/%m/%Y")  # Agora você usa diretamente datetime.now()
    global campo_data_inclusao
    campo_data_inclusao = tk.Entry(janela_inclusao, width=12)
    campo_data_inclusao.grid(row=21, column=1, padx=10, pady=5)
    campo_data_inclusao.insert(0, data)

########### BOTOES INCLUIR CLIENTES
    # Botão para salvar as informações
    btn_incluir = tk.Button(janela_inclusao, text="SALVAR (Enter)", command=salvar_cliente, bg="green", fg="white", width=15)
    btn_incluir.grid(row=22, column=1, padx=10, pady=20)

    btn_incluir.focus_set()
    janela_inclusao.bind('<Return>', lambda event: salvar_cliente())
    

    btn_fechar = tk.Button(janela_inclusao, text="Fechar", command=janela_inclusao.destroy, bg="gray", fg="white", width=15)
    btn_fechar.grid(row=22, column=0, padx=10, pady=20)


######################################################################## CADASTRO DE CLIENTE ACIMA #######################

########################## JANELA CONSULTA CLIENTES, OUTRA JANELA SECUNDARIA
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def abrir_janela_consulta_clientes():
    janela_consulta = tk.Toplevel(janela_principal)  # Criando a janela de consulta
    janela_consulta.title("Consulta de Clientes")
    janela_consulta.geometry("1200x850+5+5")
    
    # Definindo as colunas para o Treeview
    cols = ("Codigo", "Nome", "FANTASIA", "CPFCNPJ", "Telefone", "Celular", "CONTATO", "E-mail", "Endereco", "Nº", "Bairro", "Cidade", "Aluguel")
    
    tree = ttk.Treeview(janela_consulta, columns=cols, show="headings")  # Usando apenas o "tree"
    
    larguras = [10, 130, 80, 80, 60, 60, 30, 100, 150, 20, 50, 100, 40]
    for col, largura in zip(cols, larguras):
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=largura)
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Campo de texto para procurar cliente
    lbl_nome_cliente = tk.Label(janela_consulta, text="Procurar Cliente:")
    lbl_nome_cliente.pack(side=tk.LEFT, padx=15, pady=35)

    entry_nome_cliente = tk.Entry(janela_consulta)
    entry_nome_cliente.pack(side=tk.LEFT, padx=10, pady=10)
    entry_nome_cliente.focus()

    def procurar_cliente():
        nome_cliente = entry_nome_cliente.get().strip()
        
        # Limpar a árvore (Treeview) para novos dados
        for item in tree.get_children():
            tree.delete(item)

        try:
            # Conectar ao banco de dados MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='mysql147',
                database='dados'
            )
            cursor = conn.cursor()

            if nome_cliente:  # Se o campo de nome não estiver vazio, buscar com filtro
                cursor.execute(""" 
                    SELECT id, nome, fantasia, cpfcnpj, telefone1, telefone2, contato, email, endereco, numero, bairro, cidade, aluguel
                    FROM pessoas WHERE nome LIKE %s
                """, ('%' + nome_cliente + '%',))  # Adiciona o filtro de nome
            else:  # Se o campo estiver vazio, buscar todos os clientes
                cursor.execute("""
                    SELECT id, nome, fantasia, cpfcnpj, telefone1, telefone2, contato, email, endereco, numero, bairro, cidade, aluguel
                    FROM pessoas
                """)

            clientes = cursor.fetchall()

            # Inserir os dados no Treeview
            for cliente in clientes:
                tree.insert("", tk.END, values=cliente)

            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao consultar os clientes: {err}")

    # Botoes para a Janela de Consulta de Clientes

    # Botão para procurar cliente
    btn_procurar = tk.Button(janela_consulta, text="PROCURAR (Enter)", command=procurar_cliente, bg="orange", fg="black")
    btn_procurar.pack(side=tk.LEFT, padx=10, pady=10)

    # Binding para tecla "Enter" ativar o procurar_cliente
    janela_consulta.bind('<Return>', lambda event: procurar_cliente())

    # Botão para incluir cliente
    btn_incluir_cliente = tk.Button(janela_consulta, text="INCLUIR", command=abrir_janela_inclusao_cliente, bg="green", fg="white")
    btn_incluir_cliente.pack(side=tk.LEFT, padx=10, pady=10)

    # Função para editar o cliente selecionado
    def editar_cliente_com_parametros():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um cliente para editar.")
            return

        cliente_id = tree.item(selected_item[0], "values")[0]  # Obtendo o ID do cliente
        editar_cliente(janela_consulta, tree, cliente_id)  # Chama a função de edição com o cliente_id

    # Botão para editar cliente
    btn_editar = tk.Button(janela_consulta, text="EDITAR", command=editar_cliente_com_parametros, bg="blue", fg="white")
    btn_editar.pack(side=tk.LEFT, padx=10, pady=10)

    # Função para excluir o cliente selecionado
    def excluir_cliente():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção", "Selecione um cliente para excluir.")
            return

        # Obter o ID do cliente selecionado
        cliente_id = tree.item(selected_item[0], "values")[0]

        # Criar uma nova janela para confirmação de exclusão
        senha_janela = tk.Toplevel(janela_consulta)
        senha_janela.title("Confirmar Exclusão")
        tk.Label(senha_janela, text="Digite a senha para excluir o cliente:").pack(padx=10, pady=10)
        
        senha_entry = tk.Entry(senha_janela, show="*")
        senha_entry.pack(padx=10, pady=5)

        def verificar_senha():
            senha = senha_entry.get()  # Pega a senha digitada

            if senha != "55":  # Senha para confirmar a exclusão
                messagebox.showerror("Erro", "Senha incorreta! Exclusão cancelada.")
                senha_janela.destroy()
                return

            confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja excluir o cliente com ID {cliente_id}?")
            if confirm:
                try:
                    conn = mysql.connector.connect(
                        host='localhost', user='root', password='mysql147', database='dados'
                    )
                    cursor = conn.cursor()

                    # Query para deletar o cliente com base no ID
                    query = "DELETE FROM pessoas WHERE id = %s"
                    cursor.execute(query, (cliente_id,))
                    conn.commit()  # Salvar a exclusão no banco
                    
                    # Fechar conexão
                    cursor.close()
                    conn.close()
                    
                    # Remover o item da interface (Treeview)
                    tree.delete(selected_item)
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao excluir cliente: {err}")

            senha_janela.destroy()  # Fecha a janela de senha após o processo de exclusão

        # Adicionar o botão para verificar a senha
        tk.Button(senha_janela, text="Confirmar", command=verificar_senha).pack(padx=10, pady=10)
        senha_janela.mainloop()

    # Botão para excluir cliente
    btn_excluir = tk.Button(janela_consulta, text="Excluir", command=excluir_cliente, bg="red", fg="white")
    btn_excluir.pack(side=tk.LEFT, padx=10, pady=10)

    janela_consulta.mainloop()





##################################################################BOTOES DA JANELA SECUNDARIA DE CADASTRO DE CLIENTES
#######################################################################################################################################################

#######################################################################################################################################################
########################################################################## FUNCAO DE EXCLUIR CLIENTES, ABAIXO mas não funcionou deixar provisorio


def excluir_cliente(janela_consulta, tree):
    try:
        # Obter o item selecionado (linha do Treeview)
        selected_item = tree.selection()  # Retorna a linha selecionada
        
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir!")
            return
        
        # Obter o ID_CLIENTE da linha selecionada
        id_cliente = tree.item(selected_item, 'values')[0]  # O ID_CLIENTE está na primeira coluna
        
        # Criar uma nova janela para a senha
        senha_janela = tk.Toplevel(janela_consulta)  # Cria uma janela secundária dentro de janela_consulta
        senha_janela.title("Confirmar Exclusão")
        
        # Garantir que a janela de senha fique em primeiro plano
        senha_janela.lift()  # Coloca a janela de senha acima da janela de consulta
        senha_janela.focus_force()  # Garante que a janela de senha receba o foco
        senha_janela.grab_set()  # Captura o foco e bloqueia as outras janelas até a interação terminar
        
        # Adicionando um rótulo (Label) e campo de entrada (Entry) para a senha
        tk.Label(senha_janela, text="Digite a senha para excluir o cliente:").pack(padx=10, pady=10)
        
        senha_entry = tk.Entry(senha_janela, show="*")  # O parâmetro 'show' oculta a senha
        senha_entry.pack(padx=10, pady=5)
        
        def verificar_senha():
            senha = senha_entry.get()  # Pega a senha digitada
            
            if senha != "55":  # Definindo a senha de confirmação como '55' (modifique conforme necessário)
                messagebox.showerror("Erro", "Senha incorreta! Exclusão cancelada.")
                senha_janela.destroy()  # Fecha a janela da senha
                return
            
            # Confirmar com o usuário antes de excluir
            confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja excluir o cliente com ID {id_cliente}?")
            
            if confirm:
                try:
                    # Conectando ao banco de dados MySQL
                    conn = mysql.connector.connect(
                        host="localhost", user="root", password="mysql147", database="Dados"
                    )
                    cursor = conn.cursor()
                    
                    # Query para deletar o cliente com base no ID
                    query = "DELETE FROM pessoas WHERE ID_CLIENTE = %s"
                    cursor.execute(query, (id_cliente,))
                    conn.commit()  # Salvar a exclusão no banco
                    
                    # Fechar conexão
                    cursor.close()
                    conn.close()
                    
                    # Remover o item da interface (Treeview)
                    tree.delete(selected_item)
                    
                    # Exibir mensagem de sucesso
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    
                    # Aqui, trazemos a janela_consulta de volta para frente após a exclusão
                    janela_consulta.lift()  # Traz a janela de consulta para frente
                    janela_consulta.focus_force()  # Coloca o foco na janela de consulta

                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao excluir cliente: {err}")
            
            senha_janela.destroy()  # Fecha a janela de senha após o processo de exclusão

        # Adicionando o botão para verificar a senha
        tk.Button(senha_janela, text="Confirmar", command=verificar_senha).pack(padx=10, pady=10)
        
        # Exibir a janela de senha
        senha_janela.mainloop()

        # Garantir que a janela de consulta fique na frente após o fechamento da janela de confirmação de exclusão
        janela_consulta.lift()  # Traz a janela de consulta para frente
        janela_consulta.focus_force()  # Coloca o foco na janela de consulta

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")













############################################################################ EDITAR CLIENTES
#######################################################################################################################
##########################################################################################################################


import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime


def editar_cliente(janela_consulta, tree, cliente_id):
    # Criar a janela de edição
    janela_edicao = tk.Toplevel(janela_consulta)
    janela_edicao.title(f"Editar Cliente - ID: {cliente_id}")
    janela_edicao.geometry("600x700")  # Aumentei o tamanho para caber todos os campos

    # Criar campos de entrada para editar os dados do cliente
    tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(janela_edicao)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Fantasia:").grid(row=1, column=0, padx=10, pady=5)
    entry_fantasia = tk.Entry(janela_edicao)
    entry_fantasia.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="CPF/CNPJ:").grid(row=2, column=0, padx=10, pady=5)
    entry_cpfcnpj = tk.Entry(janela_edicao)
    entry_cpfcnpj.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Telefone:").grid(row=3, column=0, padx=10, pady=5)
    entry_telefone = tk.Entry(janela_edicao)
    entry_telefone.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Celular:").grid(row=4, column=0, padx=10, pady=5)
    entry_celular = tk.Entry(janela_edicao)
    entry_celular.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="E-mail:").grid(row=5, column=0, padx=10, pady=5)
    entry_email = tk.Entry(janela_edicao)
    entry_email.grid(row=5, column=1, padx=10, pady=5)

    # Campos adicionais
    tk.Label(janela_edicao, text="Endereço:").grid(row=6, column=0, padx=10, pady=5)
    entry_endereco = tk.Entry(janela_edicao)
    entry_endereco.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Número:").grid(row=7, column=0, padx=10, pady=5)
    entry_numero = tk.Entry(janela_edicao)
    entry_numero.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Bairro:").grid(row=8, column=0, padx=10, pady=5)
    entry_bairro = tk.Entry(janela_edicao)
    entry_bairro.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Cidade:").grid(row=9, column=0, padx=10, pady=5)
    entry_cidade = tk.Entry(janela_edicao)
    entry_cidade.grid(row=9, column=1, padx=10, pady=5)

    # Campos de valores
    tk.Label(janela_edicao, text="Aluguel:").grid(row=10, column=0, padx=10, pady=5)
    entry_aluguel = tk.Entry(janela_edicao)
    entry_aluguel.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Água:").grid(row=11, column=0, padx=10, pady=5)
    entry_agua = tk.Entry(janela_edicao)
    entry_agua.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Luz:").grid(row=12, column=0, padx=10, pady=5)
    entry_luz = tk.Entry(janela_edicao)
    entry_luz.grid(row=12, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Condomínio:").grid(row=13, column=0, padx=10, pady=5)
    entry_condominio = tk.Entry(janela_edicao)
    entry_condominio.grid(row=13, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Internet:").grid(row=14, column=0, padx=10, pady=5)
    entry_internet = tk.Entry(janela_edicao)
    entry_internet.grid(row=14, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="IPTU:").grid(row=15, column=0, padx=10, pady=5)
    entry_iptu = tk.Entry(janela_edicao)
    entry_iptu.grid(row=15, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Limpeza:").grid(row=16, column=0, padx=10, pady=5)
    entry_limpeza = tk.Entry(janela_edicao)
    entry_limpeza.grid(row=16, column=1, padx=10, pady=5)

    tk.Label(janela_edicao, text="Outros:").grid(row=17, column=0, padx=10, pady=5)
    entry_outros = tk.Entry(janela_edicao)
    entry_outros.grid(row=17, column=1, padx=10, pady=5)

    # Conectar ao banco de dados e buscar os dados do cliente selecionado
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='mysql147', database='dados'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome, fantasia, cpfcnpj, telefone1, telefone2, email, endereco, numero, bairro, cidade, aluguel, agua, luz, condominio, internet, iptu, limpeza, outros
            FROM pessoas WHERE id = %s
        """, (cliente_id,))
        cliente = cursor.fetchone()

        if cliente:
            # Preencher os campos com os dados do cliente
            entry_nome.insert(0, cliente[0])
            entry_fantasia.insert(0, cliente[1])
            entry_cpfcnpj.insert(0, cliente[2])
            entry_telefone.insert(0, cliente[3])
            entry_celular.insert(0, cliente[4])
            entry_email.insert(0, cliente[5])
            entry_endereco.insert(0, cliente[6])
            entry_numero.insert(0, cliente[7])
            entry_bairro.insert(0, cliente[8])
            entry_cidade.insert(0, cliente[9])
            entry_aluguel.insert(0, cliente[10])
            entry_agua.insert(0, cliente[11])
            entry_luz.insert(0, cliente[12])
            entry_condominio.insert(0, cliente[13])
            entry_internet.insert(0, cliente[14])
            entry_iptu.insert(0, cliente[15])
            entry_limpeza.insert(0, cliente[16])
            entry_outros.insert(0, cliente[17])

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao carregar os dados do cliente: {err}")

    # Função para salvar as alterações
    def salvar_edicao():
        nome = entry_nome.get()
        fantasia = entry_fantasia.get()
        cpfcnpj = entry_cpfcnpj.get()
        telefone = entry_telefone.get()
        celular = entry_celular.get()
        email = entry_email.get()
        endereco = entry_endereco.get()
        numero = entry_numero.get()
        bairro = entry_bairro.get()
        cidade = entry_cidade.get()
        aluguel = entry_aluguel.get()
        agua = entry_agua.get()
        luz = entry_luz.get()
        condominio = entry_condominio.get()
        internet = entry_internet.get()
        iptu = entry_iptu.get()
        limpeza = entry_limpeza.get()
        outros = entry_outros.get()

        if not nome or not cpfcnpj:
            messagebox.showwarning("Campos Obrigatórios", "Nome e CPF/CNPJ são obrigatórios!")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost', user='root', password='mysql147', database='dados'
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pessoas SET nome = %s, fantasia = %s, cpfcnpj = %s, telefone1 = %s, telefone2 = %s, email = %s,
                    endereco = %s, numero = %s, bairro = %s, cidade = %s, aluguel = %s, agua = %s, luz = %s, condominio = %s, internet = %s, iptu = %s, limpeza = %s, outros = %s
                WHERE id = %s
            """, (nome, fantasia, cpfcnpj, telefone, celular, email, endereco, numero, bairro, cidade, aluguel, agua, luz, condominio, internet, iptu, limpeza, outros, cliente_id))
            conn.commit()
            conn.close()

            # Atualizar a Treeview na janela principal
            for item in tree.get_children():
                if tree.item(item, "values")[0] == cliente_id:
                    tree.item(item, values=(cliente_id, nome, fantasia, cpfcnpj, telefone, celular, "", email, endereco, numero, bairro, cidade, aluguel))

            messagebox.showinfo("Sucesso", "Cliente editado com sucesso!")
            janela_edicao.destroy()  # Fechar janela de edição

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar as alterações: {err}")

    # Função para cancelar a edição
    def cancelar_edicao():
        janela_edicao.destroy()  # Fechar a janela de edição sem salvar alterações

    # Botões de salvar e cancelar
    btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, bg="green", fg="white")
    btn_salvar.grid(row=18, column=0, padx=10, pady=20)

    btn_cancelar = tk.Button(janela_edicao, text="Cancelar", command=cancelar_edicao, bg="red", fg="white")
    btn_cancelar.grid(row=18, column=1, padx=10, pady=20)

    janela_edicao.mainloop()



####################################### GERANDO O PDF COM BOTAO DIREITO DO MOUSE MES
from tkinter import ttk, Menu, messagebox
import mysql.connector  # Importação correta para MySQL
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime  # Importando datetime para usar a data atual

# Função para gerar PDF
def gerar_mes():
    try:  
        item_selecionado = tree.selection()[0]  # Obtém o item selecionado na árvore
        id_recibo = tree.item(item_selecionado)['values'][0]  # Pegando o ID do recibo

        # Conectando ao banco de dados para pegar os dados do recibo
        conexao = mysql.connector.connect(
            host="localhost",       # Altere para o endereço do seu servidor MySQL
            user="root",     # Substitua pelo seu nome de usuário MySQL
            password="mysql147",   # Substitua pela sua senha MySQL
            database="dados"    # Substitua pelo nome do seu banco de dados
        )

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
            c.drawImage(logo_path, 100, 740, width=100, height=50)  # Ajuste o tamanho e posição conforme necessário

            # Título do Recibo
            c.setFont("Helvetica-Bold", 16)
            c.drawString(210, 760, f"Recibo Avulso N°: {recibos[0]}")
            
            # Adicionando informações do recibo
            c.setFont("Helvetica", 12)
            c.drawString(100, 725, f"Nome: {recibos[1]}")
            c.drawString(100, 705, f"CPF/CNPJ: {recibos[2]}")
            c.drawString(100, 685, f"Endereco: {recibos[3]}")
            c.drawString(100, 665, f"Valor Pago: R$ {recibos[5]:.2f}")
            c.drawString(100, 645, f"Aluguel: R$ {recibos[4]:.2f}")
            c.drawString(100, 625, f"Descontos: {recibos[15]}")
            c.drawString(100, 605, f"Referente: {recibos[6]}")
            c.drawString(100, 585, f"Observacao: {recibos[16]}")
            c.drawString(100, 555, f"Tipo: RECEBEMOS( )     PAGAMOS( )")
            c.drawString(100, 525, "PORTO XAVIER - RS IMOBILAIRA LIDER")
            c.drawString(100, 495, "ASS ---------------------------------------")

            # Obtendo a data atual
            data_atual = datetime.now().strftime("%d/%m/%Y")  # Formato: DD/MM/YYYY
            c.drawString(100, 475, f"Data Emissao: {data_atual}")  # Substituindo pela data atual

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
        conexao = mysql.connector.connect(
            host="localhost",       # Altere para o endereço do seu servidor MySQL
            user="root",     # Substitua pelo seu nome de usuário MySQL
            password="mysql147",   # Substitua pela sua senha MySQL
            database="dados"    # Substitua pelo nome do seu banco de dados
        )

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
        y_position -= 90  # Ajuste o valor para mover a segunda via para baixo

        y_position -= 10  # Ajuste maior se necessário

        desenhar_recibo(y_position, primeira_via=False)  # Segunda via

        # Salvar a página do PDF
        c.showPage()  # Chama o showPage após desenhar as duas vias
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

def gerar_recibo_padrao_data():  # SELECIONA O ID_RECIBO E PREVISUALIZA O RECIBO PADRAO = FUNCAO GERAR_RECIBO_PADRAO_DATA
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
        conexao = mysql.connector.connect(
            host="localhost",       # Altere para o endereço do seu servidor MySQL
            user="root",     # Substitua pelo seu nome de usuário MySQL
            password="mysql147",   # Substitua pela sua senha MySQL
            database="dados"    # Substitua pelo nome do seu banco de dados
        )

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

            # Nome do Recebedor e DATA

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

        y_position -= 10  # Ajuste maior se necessário

        desenhar_recibo(y_position, primeira_via=False)  # Segunda via

        # Salvar a página do PDF
        c.showPage()  # Chama o showPage após desenhar as duas vias
        c.save()

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Recibo Gerado", f"Recibo {id_recibo} , com DATA DE HOJE, Gerado com Sucesso!")
        os.startfile(nome_arquivo)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um Erro: {str(e)}")

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
        messagebox.showwarning("Atenção", "Selecione um item na GRID para gerar o PDF.")

# Função que gera o PDF e fecha o menu de contexto
def gerar_e_fechar():
    gerar_mes()  # Chama a função para gerar o PDF
    menu_post_click.unpost()  # Fecha o menu de contexto
################################################# USANDO O CLIC BOTAO DIREITO DO MOUSE ACIMA#################

######### FAZER BACKUP TOTAL DA PASTA DO SISTEMA
# Função para realizar o backup com robocopy
def realizar_backup():
    try:
        # Caminho de origem e destino do backup
        origem = "C:\\Sigeflex\\recibo"  # Diretório de origem
        destino = "C:\\Sigeflex\\Backup"  # Diretório de destino
        
        # Comando de backup usando xcopy (você pode mudar para robocopy se preferir)
        comando_backup = f'robocopy "{origem}" "{destino}" /E /Z /R:3 /W:5'

        # Executando o comando no sistema
        os.system(comando_backup)

        # Exibe uma mensagem de sucesso
        messagebox.showinfo("Backup Realizado com Sucesso", "Salvo na Pasta Backup(C:\Recibo\Backup), Recomendamos salvar em Midia Externa")
        
    except Exception as e:
        # Se houver um erro, exibe uma mensagem de erro
        messagebox.showerror("Erro", f"Erro ao realizar o backup: {e}")
################################################
# Função para criar a janela principal
def criar_janela_principal():
    janela_boas = ctk.CTk()
    janela_boas.title("Bem Vindo A GDI")
    janela_boas.geometry("690x250")
    janela_boas.resizable(False, False)

    ctk.CTkLabel(janela_boas, text="Seja Bem-Vindo aos Sistemas Desenvolvidos pela GDI", font=("Arial", 16)).pack(pady=10)
    ctk.CTkLabel(janela_boas, text="*** Agora em MYSQL, um Banco Muito Mais Robusto, e com Possibilidade também de Fazer Backup - Versão 2024.2***", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(janela_boas, text="DÚVIDAS: (54) 9 9104-1029", font=("Arial", 16)).pack(pady=10)

    # Botão para realizar o backup
    btn_backup = tk.Button(janela_boas, text="Realizar Backup Agora", command=realizar_backup, bg="green", fg="white", width=20)
    btn_backup.pack(padx=10, pady=10)

# Botão para fechar a janela
    btn_fechar = tk.Button(janela_boas, text="CONTINUAR - Fechar", command=janela_boas.destroy, bg="purple", fg="white", width=20)
    btn_fechar.pack(padx=10, pady=10)


  
    # Executar a janela
    janela_boas.mainloop()

# Chama a função para criar a janela principal
criar_janela_principal()



# BACKUP DENTRO DO SISTEMA QUE POSSO ESCOLHER QUAL PASTA SALVAR
import os
import subprocess
import threading
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter as tk

# Função para realizar o backup
def realizar_backup_2():
    # Abrir uma janela de diálogo para o usuário escolher o diretório de destino
    destino = filedialog.askdirectory(title="Escolha a Pasta de destino para o Fazer o Backup")

    # Verificar se o usuário escolheu um diretório
    if not destino:
        messagebox.showinfo("Backup", "Backup cancelado. Nenhuma Pasta Selecionado.")
        return

    # Criar a janela de progresso APÓS a seleção do diretório
    janela_progresso = tk.Toplevel()  # Cria uma janela nova, independente
    janela_progresso.title("Aguarde... Realizando Backup")
    janela_progresso.geometry("400x150")

    # Criar uma barra de progresso
    barra_progresso = ttk.Progressbar(janela_progresso, orient="horizontal", length=300, mode="indeterminate")
    barra_progresso.pack(padx=10, pady=20)
    barra_progresso.start()  # Inicia a barra de progresso (em modo indeterminado)

    # Certifique-se de que a janela de progresso está à frente
    janela_progresso.lift()  # Trazer a janela de progresso para a frente

    # Função para realizar o backup em uma thread separada
    def backup_thread():
        try:
            origem = "C:\\Sigeflex"  # Caminho de origem

            # Verificar se o diretório de destino existe, caso contrário, criar
            if not os.path.exists(destino):
                os.makedirs(destino)

            # Comando de backup usando xcopy
            comando_backup = f'xcopy /E /I /H /Y "{origem}" "{destino}"'

            # Executando o comando no sistema
            processo = subprocess.run(comando_backup, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Verificando se o comando foi executado com sucesso
            if processo.returncode == 0:
                messagebox.showinfo("Sucesso", "Backup Realizado com Sucesso!")
            else:
                messagebox.showerror("Erro", f"Erro ao realizar o backup: {processo.stderr.decode()}")
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro na execução do comando de backup: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
        finally:
            janela_progresso.destroy()  # Fecha a janela de progresso após o backup

    # Executar a função de backup em uma thread separada
    thread = threading.Thread(target=backup_thread)
    thread.start()

#################################### CRIADO ACIMA BACKUP INTERNO NO SISTEMA PARA SALVAR EM X PASTA QUE ESCOLHER


########################################## CRIANDO A JANELA PRINCIPAL ABAIXO#####################
# Criando a janela principal
janela_principal = tk.Tk()
janela_principal.title("Gerenciador de Recibos - GDI")
janela_principal.geometry("1220x650+5+5")

# Criando o menu
menu_bar = tk.Menu(janela_principal)

# Menu Cadastros
menu_Cadastro = tk.Menu(menu_bar, tearoff=0)
menu_Cadastro.add_command(label="CADASTRAR Clientes", command=abrir_janela_inclusao_cliente)
menu_Cadastro.add_separator()
menu_Cadastro.add_command(label="CONSULTAR Cliente", command=abrir_janela_consulta_clientes)
menu_Cadastro.add_separator()
menu_Cadastro.add_command(label="INCLUIR Recibo Manual", command=abrir_janela_inclusao)

# Menu Relatórios
menu_relatorios = tk.Menu(menu_bar, tearoff=0)
menu_relatorios.add_command(label="Relatório por Data", command=relatorio_por_data)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório Por Cliente", command=relatorio_geral)
menu_relatorios.add_separator()
menu_relatorios.add_command(label="Relatório Geral", command=relatorio_geral)
  # Se quiser uma linha separadora

# Menu Imprimir
menu_preferencias = tk.Menu(menu_bar, tearoff=0)
menu_preferencias.add_command(label="Opcoes do Sistema", command=fechar_janela)

# Menu Sair
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_ajuda.add_command(label="Fazer Backup", command=realizar_backup_2)
menu_ajuda.add_command(label="Sair", command=fechar_janela)


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
# Botões e campos de entrada para busca
tk.Label(janela_principal, text="NOME:").grid(row=0, column=0, padx=5, pady=10, sticky='w')
campo_busca_nome = tk.Entry(janela_principal, width=40)
campo_busca_nome.grid(row=0, column=0, padx=10, pady=10)
campo_busca_nome.bind("<Return>", buscar_recibos) # Pressionar ENTER ativa a busca


# # CODIGO PARA INSERIR DESCRIÇAO E CAMPO PARA inserir id_recibo para PROCURAR
tk.Label(janela_principal, text="NÚMERO:").grid(row=0, column=1, padx=8, pady=10, sticky='w')
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

# Criando a árvore (grid de dados)
cols = ("Codigo", "NOME", "CpfCnpj", "Endereco", "ALUGUEL", "VLR_PAGO", "REFERENTE", "DATA", "Agua", "Luz", "Condomínio", "IPTU", "Internet", "Limpeza", "OUTROS", "DESCONTO", "OBS")
tree = ttk.Treeview(janela_principal, columns=cols, show="headings")

# Definindo larguras
larguras = [10, 120, 30, 130, 30, 40, 80, 45, 20, 20, 20, 20, 20, 20, 20, 25, 25]

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
menu_post_click.add_command(label="Impressão com DATA HOJE", command=gerar_recibo_padrao_data)
menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="Imprimir PADRAO", command=gerar_recibo_padrao)
menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="Impressão Simples", command=gerar_e_fechar)
menu_post_click.add_separator()  # Adiciona uma linha de separação
menu_post_click.add_command(label="Fechar", command=fechar_menu)


# 
janela_principal.mainloop()