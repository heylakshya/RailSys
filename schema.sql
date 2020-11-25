CREATE TABLE ticket (
	PNR INTEGER NOT NULL PRIMARY KEY,
	train_no INTEGER NOT NULL,
	journey_date DATE NOT NULL,
	passenger_no INTEGER NOT NULL,
	agent_id INTEGER NOT NULL,
	FOREIGN KEY(agent_id) REFERENCES agent(id),
	FOREIGN KEY(PNR) REFERENCES passenger(PNR)
	FOREIGN KEY(train_no) REFERENCES train(train_no),
	FOREIGN KEY(journey_date) REFERENCES train(journey_date)
);

CREATE TABLE agent (
	id INTEGER NOT NULL PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	address TEXT NOT NULL,
	cc_no INTEGER NOT NULL,
	FOREIGN KEY(id) REFERENCES ticket(agent_id)
);

CREATE TABLE passenger (
	PNR INTEGER NOT NULL,
	coach_type VARCHAR(2) NOT NULL,
	coach_no INTEGER NOT NULL,
	seat_position VARCHAR(2) NOT NULL,
	seat_no INTEGER NOT NULL,
	name VARCHAR(20) NOT NULL,
	PRIMARY KEY(coach_type,coach_no,seat_no,PNR),
	FOREIGN KEY(PNR) REFERENCES ticket(PNR)
);

CREATE TABLE train (
	train_no INTEGER NOT NULL,
	journey_date DATE NOT NULL,
	ac_coach_no INTEGER NOT NULL,
	sl_coach_no INTEGER NOT NULL,
	ac_last_filled INTEGER NOT NULL,
	sl_last_filled INTEGER NOT NULL,
	PRIMARY KEY(train_no,journey_date),
	FOREIGN KEY(train_no) REFERENCES ticket(train_no),
	FOREIGN KEY(journey_date) REFERENCES ticket(journey_date)
);

