from flask import Flask, session, g
from flask_migrate import Migrate
import config
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from exts import db, mail
from models import *

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
