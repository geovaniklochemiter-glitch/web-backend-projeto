from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from controllers.usuario_controller import (
    autenticar_usuario,
    cadastrar_usuario,
)


usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/")
def index():
    return render_template("index.html")


@usuario_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "erro")
            return render_template("cadastro.html")

        try:
            cadastrar_usuario(nome, email, senha)
        except (ValueError, RuntimeError) as erro:
            flash(str(erro), "erro")
            return render_template("cadastro.html")

        flash("Cadastro realizado com sucesso.", "sucesso")
        return redirect(url_for("usuarios.login"))

    return render_template("cadastro.html")


@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        try:
            usuario = autenticar_usuario(email, senha)
        except ValueError as erro:
            flash(str(erro), "erro")
            return render_template("login.html")

        if not usuario:
            flash("E-mail ou senha inválidos.", "erro")
            return render_template("login.html")

        session.clear()
        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        session["usuario_email"] = usuario.email
        flash("Login realizado com sucesso.", "sucesso")
        return redirect(url_for("usuarios.index"))

    return render_template("login.html")


@usuario_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso.", "sucesso")
    return redirect(url_for("usuarios.login"))