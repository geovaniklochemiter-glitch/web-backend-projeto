from mysql.connector import Error

from database.conexao import obter_conexao


class Produto:
    def __init__(
        self,
        id=None,
        codigo="",
        usuario_id=None,
        titulo="",
        descricao=None,
        preco=0,
        estoque=0,
        categoria=None,
        estado="",
        imagem_url=None,
        cor_principal="#0b7a3b",
        cor_secundaria="#ffffff",
        padrao="v",
    ):
        self.id = id
        self.codigo = codigo
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.nome = titulo
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.categoria = categoria
        self.estado = estado
        self.imagem_url = imagem_url
        self.cor_principal = cor_principal
        self.cor_secundaria = cor_secundaria
        self.padrao = padrao

    @classmethod
    def criar(cls, usuario_id, nome, descricao, preco, estoque=0):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor()
            codigo = f"PROD-{__import__('uuid').uuid4().hex[:10].upper()}"
            cursor.execute(
                """
                INSERT INTO produtos
                    (codigo, titulo, usuario_id, descricao, preco, estoque, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (codigo, nome, usuario_id, descricao, preco, estoque, "SP"),
            )
            conexao.commit()
            return cls.buscar_por_id(cursor.lastrowid)
        except Error as erro:
            conexao.rollback()
            raise RuntimeError(f"Não foi possível criar o produto: {erro}") from erro
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_id(cls, id):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
            produto = cursor.fetchone()
            return cls(**produto) if produto else None
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def listar(cls):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produtos ORDER BY id")
            return [cls(**produto) for produto in cursor.fetchall()]
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        conexao = obter_conexao()
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM produtos WHERE usuario_id = %s ORDER BY id",
                (usuario_id,),
            )
            return [cls(**produto) for produto in cursor.fetchall()]
        finally:
            cursor.close()
            conexao.close()