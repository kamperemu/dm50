# DM50: Direct Messaging Application

### [App Demo](https://kamperemu.pythonanywhere.com/)
### [Video Demo](https://youtu.be/atekcGGfayc)

---

## Project Summary

The project is a minimalistic text messaging application I made for the CS50 final project. The design of the webpages is minimalistic and mostly dark mode friendly. The design also makes sure that the app works on multiple screen sizes. The application uses Python, HTML, CSS, Javascript, and SQL for coding. A new user can register for a new account on the register page, and those with a registered account can log in on the login page. The user can open a direct message with a user of their choice. User-server interactions are done using the framework, Flask. Storage of data (including the user, password, and direct messages between them) is on the server. Flask SQLAlchemy ORM is the database used in the project.

 The sidebar design lets the user search for another user he wants to direct message. It also has a feature to change the password and sign out of the current user. 

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Ubuntu
- Python 3
- Package Manager for Python (pip)
- SQLite (optional)

#### Type this in the Ubuntu terminal
```
sudo apt install python3
sudo apt install python3-pip
sudo apt install sqlite3
```

### Installing

A step by step series of examples that tell you how to get a development env running

#### Install modules from requirements.txt with pip and creating the database

```
pip install -r requirments.txt
python3 create_db.py
```

#### MODULE ERROR THAT NEED TO BE FIXED
The python module file flask_session/sessions.py causes needless server error.\
This can be fixed by using a text editor to replace the following in sessions.py.
> app.session_cookie_name => app.config["SESSION_COOKIE_NAME"]

#### Check whether app runs

```
python3 -m flask run
```
or if you want to make it available to any device on the same network to open the site
```
flask run --host=0.0.0.0
```

---

## Detailed Description

### Register

The page lets the user register a user on the website. The necessary details are checked, and the password is asked twice for confirmation. Once the user registers, the server adds the user to the database of users. The password is also not stored in plain text but rather in sha256 encryption.

### Login

The page lets the user login. It asks for the username and password. It will query the database and check whether the details match. The password is checked by figuring out whether it matches the hash. Once the details are confirmed, the user is greeted with the index page and logged in using session cookies. If the user is not logged in, they are greeted with this page (unless they are accessing the register or login page).

### Apology

This page is made for unintended problems that have already been known. The user is greeted with this helpful message on this page.

### Index and Users

If there is no selected dm, the user is greeted with a list of users. The user is requested to select a user on this page. The sidebar will always have the same list of users available on all pages.

The fetch API updates the messages, and the user searches in real time without reloading the entire page. The same users are available at all times on the sidebar.

The sidebar also has the dm50 button, which brings the user back to the original index page. The sidebar also includes two user settings: change password and sign out. If required, more settings could be added to the same.

### Messages

When messaging, the user is greeted with a list of messages and a form to send messages. The messages update every second with the fetch API, not having to reload every second for the user to be able to see the messages.

### Things to Add:
- profile settings page
- profile picture
- change website color themes
- emoji integration
- sending files through the dm
- group dm
- Peer to Peer message encryption

---
## Built With

* [Flask](https://flask.palletsprojects.com/en/2.2.x/) - Web Framework used
* [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) - SQL Database ORM used
* [SQLite](https://www.sqlite.org/index.html) - SQL Database Engine used
* [Bootstrap](https://getbootstrap.com/) -  Frontend Toolkit used

---
## Authors
* **Vedang Patel** - *Initial work* - [kamperemu](https://github.com/kamperemu)
---
## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

---
## Acknowledgments

* CS50x Harvard
* My parents for being supportive ;)

---