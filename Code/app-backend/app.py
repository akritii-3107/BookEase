import os 
from flask import Flask , render_template
from instance.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_mail import Mail,Message
from datetime import datetime,timedelta,date
from flask_caching import Cache
import time
import logging
from sqlalchemy import extract,func
from celery import Celery
from flask_mail import Mail,Message
import pdfkit
import csv


app=None 

#database name 
DB_NAME="ticket-booking_database.sqlite3"

#creating database and creating admin in the beginning 
def create_database():
    if not os.path.exists('./database/' + DB_NAME):
        db.create_all()
        print('Created Database!')
        from flask_bcrypt import Bcrypt 
        from jose import jwt
        from instance.config import ADMIN_PASSWORD,ADMIN_EMAIL,ADMIN_USERNAME
        from models.models import User,Role,RoleAssignment
        bcrypt=Bcrypt()
        username1=ADMIN_USERNAME
        email=ADMIN_EMAIL
        hashed_password=bcrypt.generate_password_hash(ADMIN_PASSWORD).decode('utf-8')
        user=User(username=username1,password_hash=hashed_password,email_id=email)
        role=Role(role_name='admin')
        role2=Role(role_name='user')
        db.session.add(user)
        db.session.add(role)
        db.session.add(role2)
        role_assign1=RoleAssignment(user=user,role=role)
        db.session.add(role_assign1)
        db.session.commit()
        print('created_admin')
        #initial_create()


#creating the application
def create_app():
    app=Flask(__name__,template_folder='./jinja_templates')
    CORS(app)
    print("Starting Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    print("app initialized")
    app.app_context().push()
    app.static_folder = 'uploads'
    from models.models import User,Theatre,Show,Role,RoleAssignment,Booking
    create_database()
    return app

#creating app and adding cache as flask cache 
app=create_app()
cache=Cache(app)

#setting up celery for batch jobs and scheduled tasks

client=Celery(app.name,broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)
mail=Mail(app)

#tasks for the app         

#sends daily reminder to inactive user
@client.task
def send_daily_reminder():
     yesterday=datetime.now()-timedelta(days=1)
     inactive_users=User.query.join(Booking).filter(Booking.date<yesterday).all()
     today=datetime.utcnow().date()
     recent_shows=Show.query.filter(Show.rating>7, Show.Date_start>today).order_by(Show.rating.desc()).group_by(Show.name).limit(5).all()
     pop_shows=[show.name for show in recent_shows]
     subject="Long Time No See(nima)!, Visit Bookease"
     for user in inactive_users:
          msg=Message(subject=subject,recipients=[user.email_id])
          msg.html=render_template('Daily_inactive_mail.html',upcoming_shows=pop_shows,username=user.username)
          with app.app_context():
               mail.send(msg)
     return "Email sent Successfully"

#sends welcome mail to new user 
@client.task
def new_user_email(user_id):
     user=User.query.get(user_id)
     subject="Welcome to Bookease. Book --> Watch --> Enjoy ---> Repeat"
     msg=Message(subject=subject,recipients=[user.email_id])
     msg.html=render_template('new_user_email.html',username=user.username)
     with app.app_context():
          mail.send(msg)
     return "Email Sent Successfully"



#sends entertainment monthly report to users
@client.task
def send_monthly_report():
     from models.models import User,Role,RoleAssignment
     users=User.query.join(RoleAssignment).join(Role).filter(Role.role_name=='user').all()
     current_month=datetime.now().month
     current_year=datetime.now().year
     if(current_month == 1):
          previous_month=12
          previous_year=current_year-1
     else:
          previous_month=current_month-1
          previous_year=current_year
     month_name=datetime(year=previous_year,month=previous_month,day=1).strftime('%B')
     upcoming_shows=[]
     all_shows_this_month=Show.query.filter(extract('year', Show.Date_start) == current_year) \
                              .filter(extract('month', Show.Date_start) == current_month) \
                              .group_by(Show.name)\
                              .all()
     for show in all_shows_this_month:
          show_dict={
               'name':show.name,
               'description':show.description,
               'image':show.img_path,
               'date':(show.Date_start).strftime('%d/%m/%Y'),
               'time':(show.time).strftime("%I:%M %p"),
          }
          upcoming_shows.append(show_dict)
     for user in users:
          username=user.username
          booked_shows=[]
          user_reviews=[]
          bookings=Booking.query.filter_by(user_id=user.user_id)\
                              .filter(extract('year',Booking.date) == previous_year)\
                              .filter(extract('month',Booking.date)==previous_month)\
                              .all()
          if bookings:
               for booking in bookings:
                    show=Show.query.get(booking.show_id)
                    show_dict={
                         'name':show.name,
                         'description':show.description,
                         'image':show.img_path,
                         'date':(show.Date_start).strftime('%d/%m/%Y'),
                         'time':(show.time).strftime("%I:%M %p"),
                         'num_tickets':booking.num_tickets,
                    }
                    review=Review.query.filter_by(show_id=show.show_id,user_id=user.user_id).first()
                    if review:
                         review_dict={
                              'rating':review.rating,
                              'comment':review.comment,
                         }
                         user_reviews.append(review_dict)
                    booked_shows.append(show_dict)
                    
          subject="Your Monthly Entertainment Report"
          msg=Message(subject=subject,recipients=[user.email_id])
          if(user.format=='HTML'):
               msg.html=render_template('monthly_report_email.html',username=username,month=month_name,booked_shows=booked_shows,user_reviews=user_reviews,upcoming_shows=upcoming_shows)
          if(user.format=='PDF'):
               rendered_template=render_template('monthly_report_email.html',username=username,month=month_name,booked_shows=booked_shows,user_reviews=user_reviews,upcoming_shows=upcoming_shows)
               options={"enable-local-file-access": ""}
               try:
                    pdf=pdfkit.from_string(rendered_template,False,options=options)
                    msg.attach('entertainment_report.pdf','application/pdf',pdf)
               except Exception as e:
                    logging.error("Could Not Generate PDF.")
                    pdf="Error"
          elif(user.format=='BOTH'):
               msg.html=render_template('monthly_report_email.html',username=username,month=month_name,booked_shows=booked_shows,user_reviews=user_reviews,upcoming_shows=upcoming_shows)
               rendered_template=render_template('monthly_report_email.html',username=username,month=month_name,booked_shows=booked_shows,user_reviews=user_reviews,upcoming_shows=upcoming_shows)
               options={"enable-local-file-access": ""}
               try:
                    pdf=pdfkit.from_string(rendered_template,False,options=options)
                    msg.attach('entertainment_report.pdf','application/pdf',pdf)
               except Exception as e:
                    logging.error("Could Not Generate PDF.")
                    pdf="Error"
          with app.app_context():
               mail.send(msg)


#updates rating of the show based on the user given ratings
@client.task
def daily_rating_update():
     shows=Show.query.all()
     for show in shows:
          average_rating=db.session.query(func.avg(Review.rating)).filter_by(show_id=show.show_id).scalar()
          if average_rating:
               show.rating=average_rating
          db.session.commit()


#sends email regarding the ticket to the user      
@client.task
def send_ticket_email(ticket_details,user_email):
     subject="Your Ticket Details"
     msg=Message(subject=subject,recipients=[user_email])
     msg.html=render_template('ticket_booking_email.html',ticketdetails=ticket_details)
     with app.app_context():
          mail.send(msg)

#exports the theatre report as a csv file
@client.task(bind=True)
def export_csv_task(self,theater_id):
     theater=Theatre.query.get(theater_id)
     if not theater:
          return {'success':False,'message':'Theater does not exist'}
     csv_filename=f'theater_{theater_id}_report.csv'
     csv_filepath = os.path.join('./csv_files/', csv_filename) 
     with open(csv_filepath,'w',newline='') as csvfile:
          csv_writer=csv.writer(csvfile)
          csv_writer.writerow(['Show Name','Number of Bookings','Average Rating','Viewer Comments','Genre','Ticket Price','Revenue','Show Timings','Date','Duration (mins)'])
          shows=theater.shows
          for show in shows:
               bookings=db.session.query(func.coalesce(db.func.sum(Booking.num_tickets),0)).filter(Booking.show_id==show.show_id).scalar()
               average_rating=db.session.query(func.avg(Review.rating)).filter_by(show_id=show.show_id).scalar()
               show_rating=show.rating
               if(average_rating):
                    show_rating=average_rating
               comments=[]
               reviews=Review.query.filter_by(show_id=show.show_id).all()
               for review in reviews:
                    comments.append(review.comment)
               revenue=show.ticket_price*bookings
               time1=show.time.strftime("%I:%M %p")
               date=show.Date_start.strftime('%d/%m/%Y')
               csv_writer.writerow([show.name, bookings, show_rating, comments, show.genre, show.ticket_price, revenue, time1, date,show.time_interval])
     return {'success':True,'message':'CSV export completed','csv_filename':csv_filename}

#at the end of day sends mail to the user to rate the show 
@client.task
def email_to_rate_show():
     today=date.today()
     end_of_day_shows=Show.query.filter(Show.Date_start==today).all()
     show_ids=[ show.show_id for show in end_of_day_shows]
     print(show_ids)
     bookings_info=Booking.query.filter(Booking.show_id.in_(show_ids)).all()

     #sending mail to rate 
     for booking in bookings_info:
          user=User.query.get(booking.user_id)
          username=user.username
          show=Show.query.get(booking.show_id)
          show_name=show.name
          subject="Bookease | Rate the Show."
          msg=Message(subject=subject,recipients=[user.email_id])
          msg.html=render_template('daily_rating.html',username=username,show_name=show_name)
          with app.app_context():
               mail.send(msg)
     return ("Successfully sent the Bookings email.")
          
#dynamically updates the prices

@client.task
def dynamic_pricing():
     shows=db.session.query(Show).filter(Show.Date_start == datetime.today()).all()
     for show in shows:
          theater=show.theatre
          total_capacity=theater.capacity
          booked=db.session.query(db.func.sum(Booking.num_tickets)).filter(Booking.show_id==show.show_id).scalar()
          if(not booked):
            booked=0
          if(total_capacity > booked):
               available=total_capacity-booked
          else:
               available=0
          if available < (total_capacity * 0.2):
               show.ticket_price=round(show.ticket_price*1.1) # 10% increase in price
               db.session.commit()
          elif available < (total_capacity*0.5):
               show.ticket_price=round(show.ticket_price*1.05) #5% increase in price
               db.session.commit()
     return ("All prices updated successfully")
          


          





     

          
from celery.schedules import crontab

#scheduled tasks 

client.conf.CELERYBEAT_SCHEDULE={
          'sending Daily Reminders' : {
               'task':'app.send_daily_reminder',
               'schedule':crontab(hour=21,minute=00),
          },
          'generate montly report':{
               'task':'app.send_monthly_report',
               'schedule':crontab(minute=25,hour=18,day_of_month=8),
          },
          'daily_rating_update':{
               'task':'app.daily_rating_update',
               'schedule':crontab(hour='0,12',minute=0),
          },
          'daily_booking_remainer':{
               'task':'app.email_to_rate_show',
               'schedule':crontab(minute=0,hour=22)
          },
          'daily_price_update':{
               'task':'app.dynamic_pricing',
               'schedule':crontab(minute=0,hour='*/1')
          }
     }

#importing all the routes

from routes.auth import *
from routes.dashboards import *
from routes.theater_routes import *
from routes.show_routes import *
from routes.booking_routes import *




#running the app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

    

