import os

import mysql.connector


def obter_conexao():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "marketplace_db"),
    )


def testar_conexao():
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT DATABASE(), 1")
        banco, resultado = cursor.fetchone()
        cursor.close()
        return banco, resultado
    finally:
        conexao.close()