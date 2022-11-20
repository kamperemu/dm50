# DM50: Direct Messaging Application
#### Video Demo:  <URL HERE>
#### Description:


#### ERROR THAT NEED TO BE FIXED AFTER INSTALLATION
The python module file flask_session/sessions.py causes needless server error\
This can be fixed by using a text editor to replace the following in sessions.py
> app.session_cookie_name => app.config["SESSION_COOKIE_NAME"]


