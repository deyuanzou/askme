from flask import Flask
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
import config

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run()
