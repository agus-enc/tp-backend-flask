from flask import Flask
from routes.partidos import partidos_bp
from routes.usuarios import usuarios_bp
from routes.ranking import ranking_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(ranking_bp, url_prefix="/ranking")

if __name__ == "__main__":
    app.run(port=5000, debug=True)