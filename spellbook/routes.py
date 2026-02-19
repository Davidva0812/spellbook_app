from flask import render_template, redirect, url_for, flash, abort, request
from werkzeug.utils import secure_filename
import os
from spellbook import app, db
from spellbook import db
from spellbook.models import Spell, User
from spellbook.forms import NewSpellForm, NewUserForm, LoginForm
from spellbook import bcrypt
from flask_login import login_user, login_required, current_user, logout_user


@app.route('/')
def home():
    return render_template('home.html', title="Home")


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")


@app.route('/spells')
def show_spells():
    spells = Spell.query.all()
    return render_template('spells.html', spells=spells, title="Spells")


@app.route('/spell/new', methods=['GET', 'POST'])
@login_required
def create():
    form = NewSpellForm()
    if form.validate_on_submit():
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image_file.save(image_path)


        new_spell = Spell(
            name=form.name.data,
            school=form.school.data,
            level=form.level.data,
            description=form.description.data,
            image=filename,
            user_id = current_user.id
        )

        db.session.add(new_spell)
        db.session.commit()

        flash('Spell created successfully.', 'success')
        return redirect(url_for('show_spells'))

    return render_template('create.html', title="Create new spell", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account created successfully.', 'success')
        return redirect(url_for('show_spells'))

    return render_template('register.html', title="Create new account", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Log in failed. Please check your email address and password.', 'danger')
    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='User account')


@app.route('/spell/<int:spell_id>/update', methods=['GET', 'POST'])
@login_required
def update_spell(spell_id):
    spell = Spell.query.get_or_404(spell_id)

    # Modify only your own spell
    if spell.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        spell.name = request.form['name']
        spell.school = request.form['school']
        spell.level = request.form['level']
        spell.damage = request.form['damage']
        spell.duration = request.form['duration']
        spell.description = request.form['description']

        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            spell.image = filename

        db.session.commit()
        flash('Spell updated!', 'success')
        return redirect(url_for('show_spells'))

    return render_template('update_spell.html', spell=spell, title="Update spell")


@app.route('/spell/<int:spell_id>/delete', methods=['POST'])
@login_required
def delete_spell(spell_id):
    spell = Spell.query.get_or_404(spell_id)

    if spell.user_id != current_user.id:
        abort(403)

    db.session.delete(spell)
    db.session.commit()
    flash('Spell deleted.', 'info')
    return redirect(url_for('show_spells'))

