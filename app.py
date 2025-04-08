from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask('Cities List')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
db = SQLAlchemy(app)

class VisitedCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100))
    visit_date = db.Column(db.Date)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        town = request.form['town']
        visit_date_str = request.form['visit_date']
        
        try:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            new_city = VisitedCity(town=town, visit_date=visit_date)
            db.session.add(new_city)
            db.session.commit()
        except ValueError:
            pass
        
        return redirect(url_for('index'))
    
    cities = VisitedCity.query.order_by(VisitedCity.visit_date.desc()).all()
    return render_template('index.html', cities=cities)

@app.route('/delete/<int:id>')
def delete_city(id):
    city = VisitedCity.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(VisitedCity).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)