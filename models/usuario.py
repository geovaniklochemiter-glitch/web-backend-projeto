from mysql.connector import Error

from database.conexao import obter_conexao


class Usuario:
    def __init__(self, id=None, nome="", email="", senha="", data_cadastro=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_cadastro = data_cadastro

    @classmethod
    def criar(cls, nome, email, senha):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha),
            )
            conexao.commit()
            return cls.criar_por_id(cursor.lastrowid)
        except Error as erro:
            conexao.rollback()
            raise RuntimeError(f"Não foi possível criar o usuário: {erro}") from erro
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def criar_por_id(cls, id):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            usuario = cursor.fetchone()
            if usuario:
                return cls(**usuario)
            return None
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_email(cls, email):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario:
                return cls(**usuario)
            return None
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def listar(cls):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios ORDER BY id")
            return [cls(**usuario) for usuario in cursor.fetchall()]
        finally:
            cursor.close()
            conexao.close()