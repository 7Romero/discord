USE Discord
go

CREATE TABLE Users(
	id varchar(50) primary key,
	name varchar(50),
	balance varchar(50) DEFAULT 0,
	box varchar(50) DEFAULT 0,
	voice_online varchar(50) DEFAULT 0,
	last_box_given varchar(50) DEFAULT 0,
	chat_message varchar(50) DEFAULT 0,
	couple varchar(50) DEFAULT 0,
	instagram varchar(50) DEFAULT 0,
	AboutMe Text,
	time_coin datetime,
	warn int DEFAULT 0,
	permision int DEFAULT 0
);

CREATE TABLE Moderator(
	id varchar(50) PRIMARY KEY,
	name varchar(50),
	permision_cls int DEFAULT 1,
	permision_mute int DEFAULT 1,
	permision_gethere int DEFAULT 1,
	permision_goto int DEFAULT 1,
	permision_kick int DEFAULT 0,
	permision_ban int DEFAULT 0,
	permision_warn int DEFAULT 0,
	permision_antiafk int DEFAULT 1,
	permision_disconect int DEFAULT 1,
	permision_hide int DEFAULT 1,
	permision_clear int DEFAULT 0,
	permision_owner int DEFAULT 0
);

CREATE TABLE Mine(
	id varchar(50) primary key,
	name varchar(50),
	minetype1 int DEFAULT 0,
	minetype2 int DEFAULT 0,
	minetype3 int DEFAULT 0,
	minetype4 int DEFAULT 0,
	minetype5 int DEFAULT 0,
	minetype6 int DEFAULT 0
);

CREATE TABLE Roles(
	id varchar(50),
	name varchar(50),
	roles_id varchar(50)
);

CREATE TABLE PrivateRole(
	id varchar(50) primary key,
	name varchar(50),
	role_id varchar(50),
	time datetime
);