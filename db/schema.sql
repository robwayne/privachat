DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	profile_img_url TEXT,
	isOnline BIT
);


CREATE TABLE messages (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	msg TEXT NOT NULL,
	sender TEXT NOT NULL,
	sender_id INTEGER NOT NULL,
	time_sent TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	profile_img_url TEXT,
	FOREIGN KEY (sender) REFERENCES users (username),
	FOREIGN KEY (sender_id) REFERENCES users(id),
	FOREIGN KEY (profile_img_url) REFERENCES users (profile_img_url)
);