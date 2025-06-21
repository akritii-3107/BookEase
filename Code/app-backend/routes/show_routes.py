from flask import Flask, redirect, request,flash,url_for,jsonify,abort
from flask import current_app as app
from utils.decorators import token_required,admin_required,user_required
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from datetime import datetime,timedelta,date
import uuid
import os
from models.models import Show,db,Theatre,Booking,Review,User
import ast
import logging
logging.basicConfig(level=logging.DEBUG)
from app import cache
import json

#API to get the shows with their details and sorted by rating 
@app.route('/api/shows',methods=['GET']) 
@cache.cached(timeout=60)
def get_show_by_id():
    current_date=date.today()
    shows=db.session.query(Show).group_by(Show.name).order_by(Show.Date_start.desc()).order_by(desc(Show.rating)).all()
    show_list=[]
    for show in shows:
        theater=show.theatre
        theater_name=theater.name
        total_capacity=int(theater.capacity)
        booked=db.session.query(db.func.sum(Booking.num_tickets)).filter(Booking.show_id==show.show_id).scalar()
        if(not booked):
            booked=0
        if(total_capacity > booked):
            available=total_capacity-booked
            availability=True
        else:
            available=0
            availability=False
        filling_fast=False
        if available < (total_capacity * 0.2):
            filling_fast = True
        location=theater.location
        lat=location.latitude
        long=location.longitude
        theater_id=theater.theater_id
        city=theater.city
        time_1=(show.time).strftime("%I:%M %p")
        date_start=(show.Date_start).strftime('%d/%m/%Y')
        reviews = Review.query.filter_by(show_id=show.show_id).all()
        review_tuples = [(review.rating, review.comment) for review in reviews]
        show_dict={
            'id':show.show_id,
            'name':show.name,
            'description':show.description,
            'image_path':show.img_path,
            'time':time_1,
            'date_s':date_start,
            'genre':show.genre,
            'ticketPrice':show.ticket_price,
            'tags':show.tags,
            'theater_id':theater_id,
            'comments':review_tuples,
            'theater_name':theater_name,
            'city':city,
            'lat':lat,
            'long':long,
            'rating':show.rating,
            'duration':show.time_interval,
            'availability':availability,
            'available':available,
            'filling_fast':filling_fast
        }
        show_list.append(show_dict)

    return jsonify(show_list),201

#Api to get details of a show by the show id 
@app.route('/api/show/<int:show_id>',methods=['GET'])
@cache.cached(timeout=100) 
def get_shows(show_id):
    current_date=datetime.now()
    show=Show.query.get(show_id)
    theater=show.theatre
    theater_name=theater.name
    total_capacity=int(theater.capacity)
    booked=db.session.query(db.func.sum(Booking.num_tickets)).filter(Booking.show_id==show.show_id).scalar()
    if(not booked):
        booked=0
    if(total_capacity > booked):
        available=total_capacity-booked
        availability=True
    else:
        available=0
        availability=False
    location=theater.location
    lat=location.latitude
    long=location.longitude
    theater_id=theater.theater_id
    city=theater.city
    time_1=(show.time).strftime("%I:%M %p")
    date_start=(show.Date_start).strftime('%d/%m/%Y')
    reviews = Review.query.filter_by(show_id=show.show_id).all()
    review_tuples = [(review.rating, review.comment) for review in reviews]
    show_dict={
        'id':show.show_id,
        'name':show.name,
        'description':show.description,
        'image_path':show.img_path,
        'time':time_1,
        'date_s':date_start,
        'genre':show.genre,
        'ticketPrice':show.ticket_price,
        'tags':show.tags,
        'comments':review_tuples,
        'rating':show.rating,
        'duration':show.time_interval,
        'available':available,
        'availability':availability
    }

    return jsonify(show_dict)


#adding show to a theatre to with show details
@app.route('/api/shows/create/<int:theater_id>',methods=['POST'])
@token_required
@admin_required
def create_show(decoded_token,theater_id):
    if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        rating=request.form['rating']
        tags=request.form['tags']
        ticket_price=request.form['ticket_price']
        image_file=request.files.get('image')
        theater_id=theater_id
        genre=request.form['genre']
        interval=request.form['interval']
        Date_s=request.form['Date_s']
        time=request.form['time']
        time_2=datetime.strptime(time,"%H:%M").time()
        if image_file:
            show_id=str(uuid.uuid4())
            filename=secure_filename(f"{name}_{show_id}_{image_file.filename}")
            image_path=os.path.join(app.config['SHOW_UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
        else:
            image_path=None

        theater=Theatre.query.get(theater_id)
        date_start = datetime.strptime(Date_s, '%Y-%m-%d').date()
        show=Show(name=name,description=description,rating=rating,img_path=image_path,tags=tags,ticket_price=ticket_price,time_interval=interval,Date_start=date_start,genre=genre,time=time_2,theatre=theater)
        db.session.add(show)
        db.session.commit()
        return jsonify("Successfully Created show "),201
    return 'Create Show'

#adding show to multiple theatres at the same time and assign different prices to each 
@app.route('/api/shows/create',methods=['GET','POST'])
@token_required
@admin_required
def create_show2(decoded_token):
    if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        rating=request.form['rating']
        tags=request.form['tags']
        image_file=request.files['image']
        theater_id_p=request.form['theaters']
        interval=request.form['interval']
        Date_s=request.form['Date_s']
        genre=request.form['genre']
        priceList=request.form['ticketPricelist']
        print(priceList)
        time=request.form['time']
        time_2=datetime.strptime(time,"%H:%M").time()
        if image_file:
            show_id=str(uuid.uuid4())
            filename=secure_filename(f"{name}_{show_id}_{image_file.filename}")
            image_path=os.path.join(app.config['SHOW_UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
        else:
            image_path=None
        date_start = datetime.strptime(Date_s, '%Y-%m-%d').date()
        logging.info(theater_id_p)
        logging.info(type(theater_id_p))
        print(theater_id_p)
        theater_ids=ast.literal_eval(theater_id_p)
        prices=ast.literal_eval(priceList)
        print(prices)
        print(prices['1'])
        for item in theater_ids:
            theaterId=item
            theater=Theatre.query.get(theaterId)
            price_new=prices[str(theaterId)]
            show=Show(name=name,description=description,rating=rating,img_path=image_path,genre=genre,tags=tags,ticket_price=price_new,time_interval=interval,Date_start=date_start,time=time_2,theatre=theater)
            try:
                db.session.add(show)
                db.session.commit()
            except:
                print("i could not commit")
                print(type(item))
                logging.info(item)
                print(type(theater_id_p))
                return jsonify(message="The show couls not be added "),403
        return jsonify("Successfully Created show "),201
    return 'Create Show'

#editing the created show the image and the Description
@app.route('/api/shows/edit/<int:show_id>',methods=['GET','POST'])
@token_required
@admin_required
def edit_show(decoded_token,show_id):
    show=Show.query.get(show_id)
    if request.method == 'POST':
        show.name=request.form['name']
        show.description=request.form['description']
        image_file=request.files.get('image')
        if image_file:
            unq_id=uuid.uuid4()
            filename=secure_filename(f"{show.name}_{unq_id}_{image_file.filename}")
            image_path=os.path.join(app.config['SHOW_UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
            show.image_path=image_path
        db.session.commit()
        return jsonify({'message':'Successfully edited theatre'}),201
    return ('Edit Shows')

#API to delete the already existing show 
@app.route('/api/shows/delete/<int:show_id>', methods=['GET', 'POST'])
@token_required
@admin_required
def delete_show(decoded_token,show_id):
    show = Show.query.get(show_id)
    if request.method == 'POST':
        db.session.delete(show)
        db.session.commit()

        return redirect(('/api/shows'))
    
    return ('Delete Shows')


#get the user rating and comments about a show 
@app.route('/api/shows/<int:show_id>/comments',methods=['GET'])
@cache.cached(timeout=60)
def get_comments(show_id):
    from models.models import Show
    show=Show.query.get(show_id)
    if not show:
        return jsonify({'message':'Show Not Found'}),404
    comments=[]
    for rating in show.comments:
        comment=rating.comment
        comments.append(comment)
    return jsonify({'comments':comments}),200


