# Standard Library imports

# Core Flask imports
from flask import Blueprint, render_template, redirect, url_for

# Third-party imports

# App imports
from app import db_manager
from app import login_manager
from .views import (
    error_views,
    account_management_views,
    static_views,
)
from .models import User,Uzivatele, Logins
from sqlalchemy.sql import func

bp = Blueprint('routes', __name__)

# alias
db = db_manager.session
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length,InputRequired

class FormFormular(FlaskForm):
    name = StringField('Name', validators=[ InputRequired(message="You can't leave this empty")])
    surename = StringField('Surename', validators=[ InputRequired(message="You can't leave this empty")])

@bp.route("/formular", methods=["GET", "POST"])
def formular():
    form=FormFormular()
    if form.validate_on_submit():
        print(form.name.data)
        new_user = Uzivatele(name=form.name.data, surename=form.surename.data)
        db.add(new_user)
        db.commit()
        return "Formular submitted"
    return render_template("formular.html",form=form)
# Request management
@bp.before_app_request
def before_request():
    db()

@bp.teardown_app_request
def shutdown_session(response_or_exc):
    db.remove()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    if user_id and user_id != "None":
        return User.query.filter_by(user_id=user_id).first()

# Error views
bp.register_error_handler(404, error_views.not_found_error)

bp.register_error_handler(500, error_views.internal_error)

# Public views
bp.add_url_rule("/", view_func=static_views.index)

bp.add_url_rule("/register", view_func=static_views.register)

bp.add_url_rule("/login", view_func=static_views.login)

# Login required views
bp.add_url_rule("/settings", view_func=static_views.settings)

# Public API
bp.add_url_rule(
   "/api/login", view_func=account_management_views.login_account, methods=["POST"]
)

bp.add_url_rule("/logout", view_func=account_management_views.logout_account)

bp.add_url_rule(
   "/api/register",
   view_func=account_management_views.register_account,
   methods=["POST"],
)

# Login Required API
bp.add_url_rule("/api/user", view_func=account_management_views.user)

bp.add_url_rule(
   "/api/email", view_func=account_management_views.email, methods=["POST"]
)

# Admin required
bp.add_url_rule("/admin", view_func=static_views.admin)

class LoginsForm(FlaskForm):
    jmeno = StringField('Jméno', validators=[InputRequired(message="You can't leave this empty")])
    prijmeni = StringField('Příjmení', validators=[InputRequired(message="You can't leave this empty")])
    trida = StringField('Třída', validators=[InputRequired(message="You can't leave this empty")])

#login a list
@bp.route("/logins", methods=["GET", "POST"])
def logins():
    form = LoginsForm()
    if form.validate_on_submit():
        new_login = Logins(
            jmeno=form.jmeno.data,
            prijmeni=form.prijmeni.data,
            trida=form.trida.data,
            created_at=func.now()
        )
        db_manager.session.add(new_login)
        db_manager.session.commit()
        
    logins_list = db_manager.session.query(Logins).all()
    return render_template("logins.html", form=form, logins_list=logins_list, enumerate=enumerate)

#smazani
@bp.route("/logins/delete/<int:login_id>", methods=["POST"])
def delete_login(login_id):
    login_to_delete = db_manager.session.query(Logins).get(login_id)
    if login_to_delete:
        db_manager.session.delete(login_to_delete)
        db_manager.session.commit()
    return redirect(url_for("routes.logins"))

#editace
@bp.route("/logins/edit/<int:login_id>", methods=["GET", "POST"])
def edit_login(login_id):
    login_to_edit = db_manager.session.query(Logins).get(login_id)
    if not login_to_edit:
        return redirect(url_for("routes.logins"))

    form = LoginsForm(obj=login_to_edit)
    if form.validate_on_submit():
        login_to_edit.jmeno = form.jmeno.data
        login_to_edit.prijmeni = form.prijmeni.data
        login_to_edit.trida = form.trida.data
        db_manager.session.commit()
        return redirect(url_for("routes.logins"))

    logins_list = db_manager.session.query(Logins).all()
    return render_template("logins.html", form=form, logins_list=logins_list, enumerate=enumerate, edit_login_id=login_id)