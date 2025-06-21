from flask import Flask, redirect, request,flash,url_for,jsonify,abort,send_from_directory,send_file
from flask import current_app as app
from utils.decorators import token_required,admin_required
from werkzeug.utils import secure_filename
import uuid
import os
from models.models import Theatre,db
from app import cache,export_csv_task
import time
import logging

#getting theatre details about the theatre
@app.route('/api/theater/<int:theater_id>',methods=['GET'])
@cache.cached(timeout=30)
def get_theater_by_id(theater_id):
    try:
        theater=Theatre.query.get(theater_id)
        location=theater.location
        print(theater)
        print(location.address)
        print(theater.shows)
        detail_dict={
            'name':theater.name,
            'description':theater.caption,
            'capacity':theater.capacity,
            'image_path':theater.image_path,
            'city':theater.city,
            'address':location.address,
            'lat':location.latitude,
            'long':location.longitude,
            'shows':[{
                'id':show.show_id,
                'image_path':show.img_path,
                'name':show.name,
                'date':(show.Date_start).strftime('%d/%m/%Y'),
                'time':(show.time).strftime("%I:%M %p"),
            } for show in theater.shows],
        }
        print(detail_dict)
        return jsonify(detail_dict),201
    except:
        return jsonify(message="Error in fetching Theater"),401


#API to get all the theatres
@app.route('/api/theaters',methods=['GET'])
@cache.cached(timeout=30) 
def get_theaters():
    theaters=Theatre.query.all()
    theater_list=[]
    for theater in theaters:
        location=theater.location
        theater_dict={
            'id':theater.theater_id,
            'name':theater.name,
            'caption':theater.caption,
            'capacity':theater.city,
            'image_path':theater.image_path,
            'city':theater.city,
            'address':location.address,
            'shows':[{
                'id':show.show_id,
                'name':show.name,
                'description':show.description,
                'image_path':show.img_path
            } for show in theater.shows],
        }
        theater_list.append(theater_dict)
    return jsonify(theater_list)

#getting shows of all the theatres
@app.route('/api/theaters/shows',methods=['GET'])
@cache.cached(timeout=60) 
def get_theaters_with_shows():
    theaters=Theatre.query.filter(Theatre.shows.any()).all()
    theater_list=[]
    for theater in theaters:
        location=theater.location
        theater_dict={
            'id':theater.theater_id,
            'name':theater.name,
            'caption':theater.caption,
            'capacity':theater.city,
            'image_path':theater.image_path,
            'city':theater.city,
            'address':location.address,
            'shows':[{
                'id':show.show_id,
                'name':show.name,
                'description':show.description,
                'image_path':show.img_path
            } for show in theater.shows],
        }
        theater_list.append(theater_dict)
    return jsonify(theater_list),200

#creating a theatre
@app.route('/api/theaters/create',methods=['POST'])
@token_required
@admin_required
def create_theater(decoded_token):
    if request.method == 'POST':
        from models.models import Location
        name=request.form['name']
        caption=request.form['caption']
        image_file=request.files.get('image')
        if request.files:
            print(image_file)
        capacity=request.form['capacity']
        city=request.form['city']
        latitude=request.form['latitude']
        longitude=request.form['longitude']
        address=request.form['address']
        location=Location.query.filter_by(city=city,name=name).first() or Location.query.filter_by(latitude=latitude,longitude=longitude).first()
        if location:
            location_id=location.id
        else:
            location=Location(name=name,city=city,latitude=latitude,longitude=longitude,address=address)
            db.session.add(location)
            db.session.commit()
            location_id=location.id

        if image_file:
            theater_id=str(uuid.uuid4())
            filename=secure_filename(f"{name}_{theater_id}_{image_file.filename}")
            image_path=os.path.join(app.config['THEATER_UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
        else:
            image_path=None
        theater=Theatre.query.filter_by(city=city,name=name,location=location).first()
        if(theater):
            return jsonify({'message':"Theater Already exists"}),409
        else:
            theater=Theatre(name=name,caption=caption,location=location,image_path=image_path,capacity=capacity,city=city,location_id=location_id)
        try:
            db.session.add(theater)
            db.session.commit()
            return jsonify({'message':"Theater created successfuly"}),201
        except:
            return jsonify({'message':"Some Error Occured while creating theater"}),401
    return 'Create Theater'

#API to edit the theatre
@app.route('/api/theaters/edit/<int:theater_id>',methods=['GET','POST'])
@token_required
@admin_required
def edit_theater(decoded_token,theater_id):
    try:
        theater=Theatre.query.get(theater_id)
        print(theater)
    except:
        return jsonify({'message':'Theater Does not exist'}),404
    if request.method == 'POST':
        theater.name=request.form['name']
        theater.caption=request.form['caption']
        image_file=request.files.get('image')
        theater.capacity=request.form['capacity']
        print(request.form['capacity'])
        print(request.form['caption'])
        image_path=theater.image_path
        if image_file:
            unq_id=uuid.uuid4()
            filename=secure_filename(f"{theater.name}_{unq_id}_{image_file.filename}")
            image_path=os.path.join(app.config['THEATER_UPLOAD_FOLDER'],filename)
            image_file.save(image_path)
        theater.image_path=image_path
        try: 
            db.session.commit()
            return jsonify({'message':'Successfully Edited the Theater'}),201
        except:
            return jsonify({'message':"Some Error occured"}),401
    return ('Edit Theaters')


#deleting the theatres
@app.route('/api/theaters/delete/<int:theater_id>', methods=['GET', 'POST'])
@token_required
@admin_required
def delete_theater(decoded_token,theater_id):
    theater = Theatre.query.get(theater_id)
    if request.method == 'POST':
        db.session.delete(theater)
        db.session.commit()
        return jsonify({'message':'Successfully Deleted the Theater'}),201
    return ('Delete Theaters')


#getting the list of cities with the theatres
@app.route('/api/theaters/cities/',methods=['GET'])
@cache.cached(timeout=120) 
def get_cities():
    cities=Theatre.query.with_entities(Theatre.city).distinct().all()
    city_list=[city[0] for city in cities]
    return jsonify(city_list),202


#getting the images of the theatre
@app.route('/api/theater-imgs/<path:filepath>',methods=['GET'])
def send_theater_imgs(filepath):
    return send_file(filepath,mimetype='image/jpeg')
    

#API to export the CSV report about the theatre
@app.route('/api/export_csv/<int:theater_id>',methods=['POST'])
@token_required
@admin_required
def export_csv(decoded_token,theater_id):
    task=export_csv_task.delay(theater_id)
    return jsonify({'success':True,'message':'CSV report is getting created','id':task.id})


#getting the progress of the amount of task completed
@app.route('/api/get_progress/<task_id>',methods=['GET'])
@token_required
@admin_required
def get_progress(decoded_token,task_id):
    task=export_csv_task.AsyncResult(task_id)
    if task.status=='PENDING':
        return jsonify({'status':'PENDING','message':'TASK PENDING','progress':0}),200
    if task.state=='SUCCESS':
        return jsonify({'status':'SUCCESS','csv_filename':task.result['csv_filename'],'message':'TASK COMPLETED, YOU CAN DOWNLOAD FILE NOW.'}),200
    if task.state=='FAILURE':
        return jsonify({'message': 'CSV export failed','status':'FAILED'}),400
    progress=int((time.time() % 10) * 10)
    return jsonify({'message':'Export in Progress','status':'RUNNING','progress':progress}),200


#API to get the detailed CSV report for a theatre

@app.route('/api/get_report_download/<filename>',methods=['GET'])
@token_required
@admin_required
def download_report(decoded_token,filename):
    print(filename)
    filepath=os.path.join('csv_files',filename)
    return send_file(filepath,as_attachment=True),201


        


