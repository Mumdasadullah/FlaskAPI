from flask import Flask
from extension import db, jwt, cor, migrate
from  api.views import blueprint
from auth.views import auth_blueprint

app = Flask(__name__)
app.register_blueprint(blueprint=blueprint)
app.register_blueprint(blueprint=auth_blueprint)
app.config.from_object("config")
db.init_app(app)
cor.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")