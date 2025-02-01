from flask import Flask
from routes.hospitacje_routes import hospitacje_bp
from routes.pracownik_routes import pracownik_bp
from routes.szablon_routes import szablon_bp
from routes.views_routes import views_bp

app = Flask(__name__)

# Rejestracja blueprintów
app.register_blueprint(hospitacje_bp)
app.register_blueprint(pracownik_bp)
app.register_blueprint(szablon_bp)
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(debug=True)