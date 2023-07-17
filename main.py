from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
bootstrap = Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-projects.db"
db.init_app(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String, unique=True, nullable=False)
    done = db.Column(db.String)


# with app.app_context():
#     db.create_all()


class AddToDo(FlaskForm):
    to_do = StringField("Write down your task", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = AddToDo()
    if request.method == "POST":
        new_to_do = ToDo(to_do=request.form.get("to_do"))
        with app.app_context():
            db.session.add(new_to_do)
            db.session.commit()
    to_dos = db.session.query(ToDo)
    return render_template("index.html", form=form, to_dos=to_dos)


@app.route("/delete")
def delete():
    task_id = request.args.get('id')
    task_to_delete = db.get_or_404(ToDo, task_id)
    with app.app_context():
        current_db_sessions = db.session.object_session(task_to_delete)
        current_db_sessions.delete(task_to_delete)
        current_db_sessions.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)