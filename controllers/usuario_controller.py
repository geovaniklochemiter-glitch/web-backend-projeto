from werkzeug.security import generate_password_hash, check_password_hash

from models.usuario import Usuario


def cadastrar_usuario(nome, email, senha):
    if not nome or not email or not senha:
        raise ValueError("Nome, email e senha são obrigatórios.")

    nome = nome.strip()
    email = email.strip().lower()

    if Usuario.buscar_por_email(email):
        raise ValueError("Já existe um usuário com este email.")

    senha_hash = generate_password_hash(senha)
    return Usuario.criar(nome, email, senha_hash)


def listar_usuarios():
    return Usuario.listar()


def buscar_usuario_por_email(email):
    if not email:
        raise ValueError("O email é obrigatório.")
    return Usuario.buscar_por_email(email.strip().lower())


def autenticar_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)
    if not usuario or not check_password_hash(usuario.senha or "", senha):
        return None
    return usuario