# -*- coding: utf-8 -*-
import hashlib, datetime

from flask import Blueprint, url_for, flash, request
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, Address, Pet,Card
from app.db_info import Session
from app.subapps.home.forms import LoginForm, RegisterForm, UserProfileForm,PetForm,CardForm

homeRoute = Blueprint('homeRoute', __name__,
                      template_folder='templates', static_folder='static')


@homeRoute.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html', current_page="home")


@homeRoute.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        email = form.email.data
        md5 = hashlib.md5()
        md5.update(form.password.data.encode('utf-8'))
        # password = md5.hexdigest()
        password = form.password.data
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user, remember=True)
            flash("Login Successfully.","success")
            next = request.args.get('next')
            return redirect(next or url_for('homeRoute.index'))

        else:
            flash("User ID or Password invalid.","danger")

    return render_template('home/login.html', form=form)


@homeRoute.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("homeRoute.index"))


@homeRoute.route('/appointment')
@login_required
def appointment():
    return render_template('home/appointment.html', form=None, current_page="appointment")


@homeRoute.route('/pet')
@login_required
def pet():
    session = Session()
    pet_list = session.query(Pet).filter(Pet.owner_id == current_user.id).all()
    form = PetForm()
    return render_template('home/pet.html', form=form, current_page="user",pet_list = pet_list,user_tab="pet")


@homeRoute.route('/pet_add', methods=['POST'])
@login_required
def pet_add():
    form = PetForm()
    if form.validate_on_submit():
        name = form.name.data
        breed = form.breed.data
        gender = form.gender.data
        dob = form.dob.data

        try:
            session = Session()
            this_pet = Pet(current_user.id,name,breed,gender,dob)
            session.add(this_pet)
            session.commit()
            session.close()
            flash("Add pet sucessfully", "success")
        except Exception  as e:
            flash("Add pet failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.pet"))
        return redirect(url_for("homeRoute.pet"))
    flash("Add pet failed", "danger")
    return redirect(url_for("homeRoute.pet"))

@homeRoute.route('/pet_update', methods=['POST'])
@login_required
def pet_update():
    form = PetForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        breed = form.breed.data
        gender = form.gender.data
        dob = form.dob.data

        try:
            session = Session()
            this_pet = session.query(Pet).filter(Pet.id == id, Pet.owner_id == current_user.id)
            if this_pet.count() > 0:
                this_pet.update(
                    {
                        'name': name,
                        'breed': breed,
                        'gender': gender,
                        'dob': dob,
                    },
                    synchronize_session='evaluate'
                )
                session.commit()
                session.close()
            else:
                flash(("Pet %s is not found under user %s" % name,current_user.email), "danger")

        except Exception  as e:
            flash("Update pet information failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.pet"))

        flash("Update pet information Successfully.", "success")
        return redirect(url_for("homeRoute.pet"))
    return redirect(url_for("homeRoute.pet"))

@homeRoute.route('/pet_delete/<int:pet_id>',methods=['GET'])
@login_required
def pet_delete(pet_id):
    session = Session()
    this_pet = session.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == current_user.id)
    if this_pet.count() > 0:
        this_pet.delete()
        session.commit()
        session.close()
        flash(("Pet %d is deleted successfully" % pet_id), "success")
    else:
        flash(("Pet %d is not found under user %s" % pet_id, current_user.email), "danger")
    return redirect(url_for("homeRoute.pet"))

@homeRoute.route('/user', methods=['GET', 'POST'])
@login_required
def user_update():
    form = UserProfileForm()
    if form.validate_on_submit():
        # address info
        # address_id = form.address_id.data
        city = form.city.data
        street = form.street.data
        post = form.post_code.data
        # address = Address(city, street, post_code=post)

        # User info
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        home_numaber = form.home_number.data
        work_number = form.work_number.data
        gender = form.gender.data
        dob = form.dob.data

        # md5 = hashlib.md5()
        # md5.update(form.password.data.encode('utf-8')) # TODO encrypt password
        # password = md5.hexdigest()
        # password = form.password.data

        try:

            session = Session()
            session.query(Address).filter(Address.id == current_user.address.id).update(
                {
                    'city': city,
                    'street': street,
                    'post_code': post,
                },
                synchronize_session='evaluate'
            )
            session.query(User).filter(User.id == current_user.id).update(
                {
                    "first_name": first_name,
                    'last_name': last_name,
                    'phone':phone,
                    'home_number':home_numaber,
                    'work_number':work_number,
                    'dob': dob,
                    'gender': gender
                }
                , synchronize_session='evaluate'
            )

            session.commit()
            session.close()

        except Exception  as e:
            flash("Update user profile failed","danger")
            flash(e)
            return render_template('home/user.html', form=form)

        flash("Update Successfully.","success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.user_update'))
    return render_template('home/user.html', form=form, current_page="user",user_tab="user")


@homeRoute.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # address info
        city = form.city.data
        street = form.street.data
        post = form.post_code.data
        address = Address(city, street, post_code=post)

        # User info
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        dob = form.dob.data
        email = form.email.data
        phone = form.phone.data
        home_numaber = form.home_number.data
        work_number = form.work_number.data
        # md5 = hashlib.md5()
        # md5.update(form.password.data.encode('utf-8'))  # TODO encrypt password
        # password = md5.hexdigest()
        password = form.password.data
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, dob=dob, gender=gender,
                    address=address,phone=phone,home_number=home_numaber,work_number=work_number)

        try:
            session = Session()
            session.add(address)
            session.add(user)
            session.commit()
            user = session.query(User).filter(User.email == email).first()
            session.close()
            login_user(user, remember=True)
        except Exception  as e:
            flash("Register Failed, check again later", "danger")
            flash(e)
            return render_template('home/register.html', form=form)


        flash("Register Successfully.","success")
        next = request.args.get('next')
        return redirect(next or url_for('homeRoute.index'))

    return render_template('home/register.html', form=form)

#############

@homeRoute.route('/card')
@login_required
def card():
    session = Session()
    card_list = session.query(Card).filter(Card.owner_id == current_user.id).all()
    form = CardForm()
    return render_template('home/card.html', form=form, current_page="user",card_list = card_list,user_tab="card")


@homeRoute.route('/card_add', methods=['POST'])
@login_required
def card_add():
    form = CardForm()
    if form.validate_on_submit():
        card_num = form.card_num.data
        bank = form.bank.data

        try:
            session = Session()
            this_card = Card(current_user,card_num,bank)
            session.add(this_card)
            session.commit()
            session.close()
            flash("Add Card sucessfully", "success")
        except Exception  as e:
            flash("Add card failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.card"))
        return redirect(url_for("homeRoute.card"))
    flash("Add card failed", "danger")
    return redirect(url_for("homeRoute.card"))

@homeRoute.route('/card_update', methods=['POST'])
@login_required
def card_update():
    form = CardForm()
    if form.validate_on_submit():
        id = form.id.data
        card_num = form.card_num.data
        bank = form.bank.data

        try:
            session = Session()
            this_card = session.query(Card).filter(Card.id == id, Card.owner_id == current_user.id)
            if this_card.count() > 0:
                this_card.update(
                    {
                        'card_num': card_num,
                        'bank': bank
                    },
                    synchronize_session='evaluate'
                )
                session.commit()
                session.close()
            else:
                flash(("Card is not found under user %s" % current_user.email), "danger")

        except Exception  as e:
            flash("Update Card information failed", "danger")
            flash(e)
            redirect(url_for("homeRoute.card"))

        flash("Update Card information Successfully.", "success")
        return redirect(url_for("homeRoute.card"))
    return redirect(url_for("homeRoute.card"))

@homeRoute.route('/card_delete/<int:card_id>',methods=['GET'])
@login_required
def card_delete(card_id):
    session = Session()
    this_card = session.query(Card).filter(Card.id == card_id, Card.owner_id == current_user.id)
    if this_card.count() > 0:
        this_card.delete()
        session.commit()
        session.close()
        flash(("Card is deleted successfully"), "success")
    else:
        flash(("Card is not found under user %s" % current_user.email), "danger")
    return redirect(url_for("homeRoute.card"))
