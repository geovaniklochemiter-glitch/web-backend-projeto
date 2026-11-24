import time

from app import app
from database.conexao import obter_conexao


def limpar_usuario(email):
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()


def testar_fluxo_autenticacao():
    email = f"login_teste_{time.time_ns()}@exemplo.com"
    app.config.update(TESTING=True)

    client = app.test_client()
    try:
        cadastro = client.post(
            "/cadastro",
            data={
                "nome": "Login Teste",
                "email": email,
                "senha": "senha123",
                "confirmar_senha": "senha123",
            },
            follow_redirects=False,
        )
        assert cadastro.status_code == 302
        assert cadastro.headers["Location"].endswith("/login")

        login_correto = client.post(
            "/login",
            data={"email": email, "senha": "senha123"},
            follow_redirects=False,
        )
        assert login_correto.status_code == 302

        pagina = client.get("/", follow_redirects=True)
        assert b"Bem-vindo, Login Teste" in pagina.data

        login_incorreto = client.post(
            "/login",
            data={"email": email, "senha": "senha-incorreta"},
            follow_redirects=False,
        )
        assert login_incorreto.status_code == 200

        logout = client.get("/logout", follow_redirects=False)
        assert logout.status_code == 302

        pagina_final = client.get("/", follow_redirects=True)
        assert b"Marketplace" in pagina_final.data
    finally:
        limpar_usuario(email)

    print("Cadastro: OK")
    print("Login correto: OK")
    print("Login incorreto: OK")
    print("Sessao: OK")
    print("Logout: OK")


if __name__ == "__main__":
    testar_fluxo_autenticacao()
