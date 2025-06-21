from flask import Flask, redirect, request,flash,url_for,jsonify,abort
from flask import current_app as app
from utils.decorators import token_required,admin_required,user_required
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta
import uuid
import os
from models.models import Show,db,User,Theatre,Booking,Review
import ast
import logging
logging.basicConfig(level=logging.DEBUG)
from datetime import datetime
from app import cache,send_ticket_email

#to book tickets
@app.route('/api/user/book/<int:show_id>',methods=['POST'])
@token_required
@user_required
def book_tickets(decoded_token,show_id):
    username=decoded_token['username']
    show=Show.query.get(show_id)
    data=request.get_json()
    num_tickets=data['number']
    date=datetime.now()
    user=User.query.filter_by(username=username).first()
    if(user): 
        logging.info('user exists')
        book=Booking(user_id=user.user_id,show_id=show_id,num_tickets=num_tickets,date=date)
        db.session.add(book)
        db.session.commit()
        time2=(show.time).strftime("%I:%M %p")
        ticket_details={
            'username':username,
            'event_name':show.name,
            'num_tickets':num_tickets,
            'date_of_show':show.Date_start,
            'time':time2
        }
        email=user.email_id
        #sending ticket email batch job
        send_ticket_email.delay(ticket_details,email)
        return jsonify(message="Successufully Booked Tickets,Your Tickets will be mailed to you "),201
    else:
        logging.error('User does not exist ')
        return jsonify(message="Cannot Book Tickets , user Not present"),404


#to get the user bookings
@app.route('/api/user/bookings',methods=['GET'])
@cache.cached(timeout=60) 
@token_required
@user_required
def get_bookings(decoded_token):
    user_name=decoded_token['username']
    user=User.query.filter_by(username=user_name).first()
    if(user):
        bookings=Booking.query.filter_by(user_id=user.user_id).all()
        if(bookings):
            bookings_list=[]
            for booking in bookings:
                show_id=booking.show_id
                show=Show.query.get(show_id)
                name=show.name
                theater=show.theatre.name
                date_real=booking.date
                date=booking.date.strftime('%d/%m/%Y')
                image_path=show.img_path
                city=show.theatre.city
                booking_dict={
                    'show_id':show_id,
                    'show_name':name,
                    'theater_name':theater,
                    'num_tickets':booking.num_tickets,
                    'image_path':image_path,
                    'city':city,
                    'booking_date':date
                }
                bookings_list.append(booking_dict)
            return jsonify(bookings_list)
        else:
            return jsonify(message='no Bookings Yet'),202
    else:
        return jsonify(message="User does not exist"),404
    

#API to rate the booked show by the user 
@app.route('/api/user/rate/<int:show_id>',methods=['POST'])
@token_required
@user_required
def rate_show_comments(decoded_token,show_id):
    user_name=decoded_token['username']
    user=User.query.filter_by(username=user_name).first()
    if(user):
        review=Review.query.filter_by(user_id=user.user_id,show_id=show_id).first()
        if(review):
            return jsonify(message="Already Reviewed "),405
        data=request.get_json()
        rating=data['rating']
        comment=data['comment']
        review=Review(user_id=user.user_id,show_id=show_id,rating=rating,comment=comment)
        try:
            db.session.add(review)
            db.session.commit()
            return jsonify(message="Review Posted"),201
        except:
            return jsonify(message="Cannot Post Review"),401
    else:
        return jsonify(message="User does not exist"),402
    






