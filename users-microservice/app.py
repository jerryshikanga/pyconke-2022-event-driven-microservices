from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import HOST, PORT, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return dict(id=self.id, name=self.name, active=self.active)


@app.route('/user/<user_id>')
def user_details(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user:
        return jsonify(user.to_dict())
    else:
        return {}, 404


@app.route('/users')
def all_users():
    users = db.session.query(User).all()
    users = [user.to_dict() for user in users]
    return jsonify(users)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
