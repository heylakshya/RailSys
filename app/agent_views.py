from app import app
from flask import render_template, url_for

@app.route("/agent")
def booking_agent():
	return render_template("agent.html")