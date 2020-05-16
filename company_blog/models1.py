from company_blog import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Doctors(db.Model,UserMixin):
     
    __tablename__ = 'Doctors'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(64),unique = True,index = True)
    visiting_hours = db.Column(db.String(20),nullable = False)
    qualification = db.Column(db.String(50),nullable = False)
    specializaton = db.Column(db.String(140),nullable = False)
    consultation_fees = db.Column(db.Integer, nullable = False)
    profile_image = db.Column(db.String(64),default = 'default_image.jpg')
    experience = db.Column(db.Text,nullable = False)
    contact_number = db.Column(db.String(10),nullable = False)
    description = db.Column(db.Text,nullable = False)

    reviews = db.realtionship('Reviews',backref = 'doctor', lazy = True)
    hospitals = db.realtionship('Hospitals',backref = 'doctor',lazy = True)


class Reviews(db.Model):

    doctors = db.realtionship(Doctors)

    id = db.Column(db.Integer,primary_key = True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctors.id'),nullable = False)
    reviews = db.Column(db.Text)
