import sqlite3 as sql
import string
import random
import math

def pnr_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def release_train(train, date, ac, sl):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO train (train_no, journey_date, ac_coach_no, sl_coach_no, ac_last_filled, sl_last_filled) VALUES (?,?,?,?,?,?)", (train, date, ac, sl, 0, 0))
	con.commit()
	con.close()

def check_train(train, date):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT ac_coach_no, sl_coach_no, ac_last_filled, sl_last_filled FROM train WHERE train_no = ? AND journey_date = ?",(train, date))
	exist = cur.fetchone()
	con.close()
	return exist

def add_agent(agent_id, agent_name, credit_card, address):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO agent (id, name, cc_no, address) VALUES (?,?,?,?)", (agent_id, agent_name, credit_card, address))
	con.commit()
	con.close()

def check_agent(agent_id):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT name FROM agent WHERE id = ? ",(agent_id,))
	exist = cur.fetchall()
	con.close()
	return exist

def release_train_list():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT train_no, journey_date FROM train ")
	trains = cur.fetchall()
	con.close()
	return trains

def pnr_check(pnr):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT PNR FROM ticket WHERE PNR = ? ",(pnr,))
	exist = cur.fetchone()
	con.close()
	return exist

def add_ticket(pnr, train, date, Passengers, agent_id):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO ticket (PNR, train_no, journey_date, passenger_no, agent_id) VALUES (?,?,?,?,?)", (pnr, train, date, Passengers, agent_id))
	con.commit()
	con.close()

def exist_pnr(pnr):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT PNR, train_no, journey_date, passenger_no, agent_id FROM ticket WHERE PNR = ? ",(pnr,))
	exist = cur.fetchone()
	con.close()
	return exist

def exist_passenger(pnr):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT name, coach_type, coach_no, seat_position, seat_no FROM passenger WHERE PNR = ? ",(pnr,))
	exist = cur.fetchall()
	con.close()
	return exist

def fill_seat(train, date, coach_type):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT ac_last_filled, sl_last_filled FROM train WHERE train_no = ? AND journey_date = ?",(train, date))
	exist = cur.fetchone()

	if coach_type == "AC":
		cur.execute("UPDATE train SET ac_last_filled = ? WHERE train_no = ? AND journey_date = ?",(exist[0]+1,train, date))
		con.commit()
		con.close()
		return exist[0]+1
	else:
		cur.execute("UPDATE train SET sl_last_filled = ? WHERE train_no = ? AND journey_date = ?",(exist[1]+1,train, date))
		con.commit()
		con.close()
		return exist[1]+1

def add_passenger(pnr, coach_type, pass_name, given_seat):
	if coach_type == "AC":
		if (given_seat%18 == 0):
			seat_no = 18
		else:
			seat_no = given_seat%18
		
		if (seat_no%6 == 0):
			seat_position = "SU"
		if (seat_no%6 == 1 or seat_no%6 == 2):
			seat_position = "LB"
		if (seat_no%6 == 3 or seat_no%6 == 4):
			seat_position = "UB"
		if (seat_no%6 == 5):
			seat_position = "SL"

		coach_no = math.floor((given_seat-1)/18) + 1
	else:
		if (given_seat%24 == 0):
			seat_no = 24
		else:
			seat_no = given_seat%24
		
		if (seat_no%8 == 0):
			seat_position = "SU"
		if (seat_no%8 == 1 or seat_no%8 == 4):
			seat_position = "LB"
		if (seat_no%8 == 3 or seat_no%8 == 6):
			seat_position = "UB"
		if (seat_no%8 == 2 or seat_no%8 == 5):
			seat_position = "MB"
		if (seat_no%8 == 7):
			seat_position = "SL"

		coach_no = math.floor((given_seat-1)/24) + 1

	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("INSERT INTO passenger (PNR, coach_type, coach_no, seat_position, seat_no, name) VALUES (?,?,?,?,?,?)", (pnr, coach_type, coach_no, seat_position, seat_no, pass_name))
	con.commit()
	con.close()