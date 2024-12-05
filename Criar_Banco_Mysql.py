import mysql.connector
from mysql.connector import Error

def inicializar_tabela():
    try:
        # Conectando ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host='localhost',  # Substitua com o seu host, ex: 'localhost'
            user='root',       # Substitua com o seu usuário
            password='mysql147',  # Substitua com a sua senha
            database='dados'  # Substitua com o nome do banco de dados
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            # CRIANDO TABELA USUARIOS
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) NULL,
                    login VARCHAR(60) NULL,
                    senha VARCHAR(10) NULL,
                    data date NULL                 
                              )
                           ''')
                           
            # CREATE TABLE IF NOT EXISTS pessoas (
            #         id INT AUTO_INCREMENT PRIMARY KEY,
            #         tipoPessoa char(1) NULL,
            #         nome VARCHAR(60) NOT NULL,
            #         fantasia VARCHAR(60) NOT NULL,
            #         cpfcnpj CHAR(18) NULL,
            #         ie CHAR(20) NULL,
            #         telefone1 VARCHAR(50) NULL, 
            #         telefone2 VARCHAR(50) NULL,                                
            #         contato VARCHAR(50) NULL,
            #         email VARCHAR(100) NULL,
            #         endereco VARCHAR(60) NULL,
            #         numero VARCHAR(20) NULL,
            #         complemento VARCHAR(20) NULL,       
            #         bairro VARCHAR(60) NULL,
            #         cidade VARCHAR(60) NULL,
            #         data date NULL,                                                          
            #         aluguel DECIMAL(10, 2) NULL,
            #         valor_liquido DECIMAL(10, 2) NULL,
            #         `agua` DECIMAL(10, 2) NULL,
            #         `luz` DECIMAL(10, 2) NULL,
            #         condominio DECIMAL(10, 2) NULL,
            #         iptu DECIMAL(10, 2) NULL,
            #         internet DECIMAL(10, 2) NULL,
            #         limpeza DECIMAL(10, 2) NULL,
            #         outros DECIMAL(10, 2) NULL,
            #         descontos DECIMAL(10, 2) NULL,
            #         referente VARCHAR(60) NULL,
            #         observacao VARCHAR(60) NULL,
            #         formaPag VARCHAR(50) NULL,
            #         situacao int(1) NULL
                           
            #    )
            # ''')

            # Criação da tabela, caso não exista
                 # Commit não é necessário quando usamos o "with" em MySQL, mas o commit é explícito aqui
            conexao.commit()

            print("Tabela criada ou já existe.")
    
    except Error as e:
        print(f"Erro ao inicializar a tabela: {e}")
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

# Chama a função para inicializar a tabela
inicializar_tabela()

















            # CRIANDO TABELA RECIBOS
            #cursor.execute('''
#                CREATE TABLE IF NOT EXISTS recibos (
                    # id_recibo INT AUTO_INCREMENT PRIMARY KEY,
                    # nome VARCHAR(255) NOT NULL,
                    # cnpj VARCHAR(20) NULL,
                    # endereco VARCHAR(255) NULL,
                    # aluguel DECIMAL(10, 2) NULL,
                    # valor_liquido DECIMAL(10, 2) NULL, 
                    # referente VARCHAR(255) NULL,                                
                    # dataEmissao DATE NULL,
                    # agua DECIMAL(10, 2) NULL,
                    # luz DECIMAL(10, 2) NULL,
                    # condominio DECIMAL(10, 2) NULL,
                    # iptu DECIMAL(10, 2) NULL,
                    # internet DECIMAL(10, 2) NULL,
                    # limpeza DECIMAL(10, 2) NULL,
                    # outros DECIMAL(10, 2) NULL,
                    # descontos DECIMAL(10, 2) NULL,
                    # observacao TEXT NULL,
                    # telefone INT(11) NULL,
                    # formaPag VARCHAR(50) NULL,
                    # tipo VARCHAR(50) NULL
#               )
#            ''')
