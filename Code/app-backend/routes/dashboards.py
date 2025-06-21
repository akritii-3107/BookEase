from flask import Flask, redirect, request,flash,url_for,jsonify
from flask import current_app as app


from utils.decorators import user_required,admin_required,token_required

@app.route("/user_dashboard",methods=['GET'])
@token_required
@user_required
def user_dashboard():
    return("user_dashboard")

@app.route("/admin_dashboard")
@token_required
@admin_required
def admin_dashboard():
    return("Admin dashboard")
