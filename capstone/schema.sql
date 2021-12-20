CREATE TABLE IF NOT EXISTS Users (
	user_id	INTEGER PRIMARY KEY AUTOINCREMENT ,
	first_name	TEXT NOT NULL,
	last_name	TEXT,
	phone	INTEGER,
	email	TEXT NOT NULL UNIQUE,
	password	TEXT NOT NULL,
	active INTEGER NOT NULL DEFAULT 1,
	date_created	TEXT,
	hire_date	TEXT,
	user_type	TEXT NOT NULL,
	UNIQUE(email)
);

CREATE TABLE IF NOT EXISTS Assessments (
	assessment_id	INTEGER PRIMARY KEY AUTOINCREMENT ,
	assessment_type	TEXT NOT NULL,
	assessment_description	TEXT NOT NULL,
	due_date	TEXT,
	creation_date	TEXT,
	competency_id	INTEGER,
	FOREIGN KEY(competency_id) REFERENCES Competencies(competency_id)
);

CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    competency_name TEXT NOT NULL UNIQUE,
    competency_description TEXT,
    scale_notes TEXT
);

CREATE TABLE IF NOT EXISTS AssessmentResults (
	result_id INTEGER PRIMARY KEY AUTOINCREMENT ,
	user_id	INTEGER,
	assessment_id	INTEGER,
	score	INTEGER DEFAULT 0,
	assessment_date	TEXT,
	manager_id	INTEGER,
	FOREIGN KEY(assessment_id) REFERENCES Assessments(assessment_id),
	FOREIGN KEY(user_id) REFERENCES Users(user_id),
	FOREIGN KEY(manager_id) REFERENCES Users(user_id)
);