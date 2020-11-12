from app import app
from flask import render_template, url_for

@app.route("/admin")
def booking_sys():
	return render_template("admin.html")