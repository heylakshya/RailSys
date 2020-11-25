from flask import Flask
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/ad')
def ad():
	trains = dbHandler.release_train_list()
	return render_template('admin.html', trains=trains)

@app.route('/register')
def register():
	return render_template('agent_registration.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
	if request.method=='POST':
		train = request.form['train']
		date = request.form['date']
		ac = request.form['ac']
		sl = request.form['sl']
		exist = dbHandler.check_train(train, date)
		if exist:
			return render_template('console.html', message="Train already added previously.")
		else:
			dbHandler.release_train(train, date, ac, sl)
			return render_template('console.html', message="Train added successfully.")
	else:
		return render_template('admin.html')

@app.route('/agent', methods=['POST', 'GET'])
def agent():
	if request.method=='POST':
		agent_id = request.form['agent_id']
		agent_name = request.form['agent_name']
		credit_card = request.form['credit_card']
		address = request.form['address']
		exist = dbHandler.check_agent(agent_id)
		if exist:
			return render_template('console.html', message="Agent already exists. Try with different agent id.")
		else:
			dbHandler.add_agent(agent_id, agent_name, credit_card, address)
			return render_template('console.html', message="New agent added.")
	else:
		return render_template('agent_registration.html')

@app.route('/book', methods=['POST', 'GET'])
def book():
	if request.method=='POST':
		agent_id = request.form['agent_id']
		train = request.form['train']
		date = request.form['date']
		coach_type = request.form['coach_type']
		Passengers = request.form['Passengers']
		
		exist_agent = dbHandler.check_agent(agent_id)
		if not exist_agent:
			return render_template('console.html', message="New agent register first.")
		
		exist_train = dbHandler.check_train(train, date)
		if not exist_train:
			return render_template('console.html', message="Train not released yet.")
		
		if (coach_type == "AC" and ((exist_train[2]+int(Passengers)) > (exist_train[0]*18))) or (coach_type == "SL" and ((exist_train[3]+int(Passengers)) > (exist_train[1]*24))) :
			return render_template('console.html', message="Seat not available.")

		else:
			# pnr generate
			pnr = dbHandler.pnr_generator(6)
			while(dbHandler.pnr_check(pnr)):
				pnr = dbHandler.pnr_generator(6)

			# insert row in ticket
			dbHandler.add_ticket(pnr, train, date, Passengers, agent_id)
			return render_template('booking.html', pnr=pnr, passengers=int(Passengers), coach_type=coach_type)
	else:
		return render_template('index.html')

@app.route('/passen', methods=['POST', 'GET'])
def passen():
	if request.method=='POST':
		passenger_count = request.form['passenger_count']
		pnr = request.form['pnr']
		coach_type = request.form['coach_type']
		pass_name = request.form['pass_name']
		# get other details
		exist_pnr = dbHandler.exist_pnr(pnr)
		# fill the seat
		given_seat = dbHandler.fill_seat(exist_pnr[1], exist_pnr[2], coach_type)
		# add passenger
		dbHandler.add_passenger(pnr, coach_type, pass_name, given_seat)

		if int(passenger_count)-1:
			return render_template('booking.html', pnr=pnr, passengers=int(passenger_count)-1, coach_type=coach_type)
		else:
			return render_template('console.html', message="Ticket generated with PNR: "+pnr)
	else:
		return render_template('booking.html')

@app.route('/view', methods=['POST', 'GET'])
def view():
	if request.method=='POST':
		pnr = request.form['pnr']
		ticket = dbHandler.exist_pnr(pnr)
		passengers = dbHandler.exist_passenger(pnr)
		if (ticket):
			return render_template('view_ticket.html', ticket=ticket, passengers=passengers)
		else:
			return render_template('console.html', message="Invalid PNR!")
	else:
		return render_template('view_ticket.html')

if __name__ == '__main__':
	app.run(debug=False, host='127.0.0.1')