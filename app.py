from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session
from datetime import datetime
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dispatcher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'driver' or 'passenger'
    vehicle_number = db.Column(db.String(20))  # Only for drivers
    car_brand = db.Column(db.String(100))  # Only for drivers
    car_color = db.Column(db.String(100))  # Only for drivers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    discount = db.Column(db.Integer)

class DiscountEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

# Updated discount events
updated_events = [
    "Проблемы с автомобилем",
    "Задержка в пути",
    "Отмена поездки",
    "Проблемы с навигацией",
    "Проблемы с оплатой",
    "Проблемы с безопасностью",
    "Проблемы с обслуживанием",
    "Проблемы с приложением",
    "Проблемы с багажом",
    "Проблемы с бронированием",
    "Проблемы с клиентом",
    "Проблемы с погодой",
    "Проблемы с дорожными работами",
    "Проблемы с парковкой",
    "Проблемы с доступностью"
]

with app.app_context():
    db.create_all()
    # Add updated events to the database if they don't exist
    for event_name in updated_events:
        if not DiscountEvent.query.filter_by(name=event_name).first():
            new_event = DiscountEvent(name=event_name)
            db.session.add(new_event)
    db.session.commit()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form.get('middle_name', '')
        phone = request.form['phone']
        user_type = request.form['user_type']
        vehicle_number = request.form.get('vehicle_number', None)

        if user_type == 'driver' and not vehicle_number:
            flash('Vehicle number is required for drivers', 'error')
            return redirect(url_for('add_user'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone=phone,
            user_type=user_type,
            vehicle_number=vehicle_number
        )

        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_user.html')

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.middle_name = request.form.get('middle_name', '')
        user.phone = request.form['phone']
        user.user_type = request.form['user_type']
        user.vehicle_number = request.form.get('vehicle_number', '')
        user.car_brand = request.form.get('car_brand', '')
        user.car_color = request.form.get('car_color', '')
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_user.html', user=user)

@app.route('/add_bonus/<int:id>', methods=['POST'])
def add_bonus(id):
    user = User.query.get_or_404(id)
    bonus = request.form['bonus']
    # Logic to add bonus
    flash('Bonus added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/apply_discount/<int:id>', methods=['GET', 'POST'])
def apply_discount(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        custom_discount = request.form['custom_discount']
        reason = request.form['reason']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        user.discount = custom_discount
        # Логика для обработки причины скидки и времени действия
        flash(f'Скидка {custom_discount}% применена по причине: {reason} с {start_date} по {end_date}', 'success')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('apply_discount.html', user=user)

@app.route('/filter/<user_type>')
def filter_users(user_type):
    if user_type == 'all':
        users = User.query.all()
    else:
        users = User.query.filter_by(user_type=user_type).all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True) 