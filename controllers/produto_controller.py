from decimal import Decimal, InvalidOperation

from models.produto import Produto
from models.usuario import Usuario


def cadastrar_produto(usuario_id, nome, descricao, preco, estoque=0):
    if not usuario_id:
        raise ValueError("O usuário é obrigatório.")
    if not nome or not str(nome).strip():
        raise ValueError("O nome do produto é obrigatório.")

    usuario = Usuario.criar_por_id(usuario_id)
    if not usuario:
        raise ValueError("Usuário não encontrado.")

    try:
        preco = Decimal(str(preco))
    except (InvalidOperation, ValueError, TypeError) as erro:
        raise ValueError("Preço inválido.") from erro

    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")

    estoque = int(estoque)
    if estoque < 0:
        raise ValueError("O estoque não pode ser negativo.")

    return Produto.criar(usuario_id, str(nome).strip(), descricao, preco, estoque)


def listar_produtos():
    return Produto.listar()


def listar_produtos_do_usuario(usuario_id):
    return Produto.listar_por_usuario(usuario_id)