PRAGMA foreign_keys = ON;
drop table if exists questionary;
create table questionary (
	id integer primary key autoincrement,
	name text not null,
	xAxis text not null,
	yAxis text not null,
	maxX float not null,
	maxY float not null
);

create table question (
	fk_id integer not null,
	qId integer primary key autoincrement,
	qText text not null,
	stronglyAgreeX float not null,
	stronglyAgreeY float not null,
	agreeX float not null,
	agreeY float not null,
	neutralX float not null,
	neutralY float not null,
	disagreeX float not null,
	disagreeY float not null,
	stronglyDisagreeX float not null,
	stronglyDisagreeY float not null,
	FOREIGN KEY(fk_id) REFERENCES questionary(id)
);
