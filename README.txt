##### SQL USED FOR DB CREATION #####

CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

CREATE TABLE "accounts" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"username"	VARCHAR NOT NULL,
	"password"	VARCHAR NOT NULL,
	"email"	VARCHAR NOT NULL
);

######QUERY FOR INSERTING VALUES IN DB#####

INSERT INTO accounts VALUES (NULL,'"+ username +"', '"+ password +"',  '"+ email +"');

The Route /pythonlogin/ is used for logging in a user who's already registered.
/pythonlogin/register is used for registering new user

In order to run this app 
Navigate to the project directory and run python main.py in the cmd 
Navigate to http://localhost:5000/pythonlogin/ in your web browser to see the app live


FOR DEMO YOU CAN USE
Username :abc
Password :abc

For Login