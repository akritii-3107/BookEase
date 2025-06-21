from application.database import db 


class User(db.Model):
    __tablename__='user'
    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email_id=db.Column(db.String,unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    format=db.Column(db.String(25),nullable=True)


class Role(db.Model):
    __tablename__='role'
    role_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    role_name=db.Column(db.String(50),unique=True)

class RoleAssignment(db.Model):
    __tablename__='role_assignment'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
    role_id=db.Column(db.Integer,db.ForeignKey('role.role_id'))
    #relationships
    user=db.relationship('User',backref=db.backref('role_assignments', cascade='all, delete-orphan'))
    role=db.relationship('Role',backref=db.backref('role_assignments', cascade='all, delete-orphan'))


class Theatre(db.Model):
    __tablename__='theatre'
    theater_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    caption=db.Column(db.String(400),nullable=True)
    image_path=db.Column(db.String(200))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    city=db.Column(db.String(25),nullable=False)
    #relationship 
    location = db.relationship('Location', backref=db.backref('theaters'))


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(255), nullable=False)
    city=db.Column(db.String(25),nullable=False)
    latitude = db.Column(db.Float,unique=True)
    longitude = db.Column(db.Float,unique=True)
    address = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Location(name='{self.name}', latitude={self.latitude}, longitude={self.longitude})"


class Show(db.Model):
    __tablename__="show"
    show_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description=db.Column(db.String(500),nullable=True)
    rating = db.Column(db.Float, nullable=False)
    img_path = db.Column(db.String(200))
    tags = db.Column(db.String(255), nullable=True)
    ticket_price = db.Column(db.Float, nullable=False)
    time_interval=db.Column(db.Integer, nullable=False)
    Date_start=db.Column(db.Date,nullable=False)
    time=db.Column(db.Time,nullable=False)
    genre=db.Column(db.String(100),nullable=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.theater_id'), nullable=False)
    theatre = db.relationship('Theatre', backref=db.backref('shows', lazy=True, cascade='all, delete'))
    comments=db.relationship('Review',backref=db.backref('show'))


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    rating = db.Column(db.Integer)
    comment=db.Column(db.String(500))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    date=db.Column(db.Date,nullable=False)