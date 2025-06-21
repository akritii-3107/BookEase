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


#API ROUTE to check the rate of seats filling 
@app.route('/api/prediction/chech_show_availability/<int:show_id>',method=['GET'])
def filling_rate(show_id):
    bookings=Booking.query.get(Booking.show_id == show_id)
    show=Show.query.get(show_id)
    available_seats=show.theatre.capacity - sum([booking['num_tickets'] for booking in bookings])
    filling_fast=False
    if available_seats < (show.theatre.capacity * 0.2):
        filling_fast = True
    return jsonify({'filling_fast':filling_fast})



