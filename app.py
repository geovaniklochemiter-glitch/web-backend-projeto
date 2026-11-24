import os

from flask import Flask

from routes.usuario_routes import usuario_bp


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-marketplace-secret")
app.register_blueprint(usuario_bp)


if __name__ == "__main__":
    app.run(debug=True)