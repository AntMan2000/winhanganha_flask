First Nations Winhanganha Archive Flask Project

Project structure
-----------------
run.py
project/
  __init__.py        Flask app, Bootstrap, MySQL and Flask-Login setup
  views.py           Routes and page handlers
  models.py          Database helper functions, user model and login loader
  forms.py           WTForms classes
  database.sql       MySQL schema and starter data
  templates/         Jinja templates
  static/            CSS and images

Setup
-----
1. Create and activate a virtual environment.

2. Install dependencies:
   pip install Flask Flask-Login Flask-WTF Flask-MySQLdb bootstrap-flask python-dotenv email-validator

3. Create a .env file beside run.py:
   SECRET_KEY=replace_with_a_long_random_secret
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=winhanganha_archive
   FLASK_HOST=127.0.0.1
   FLASK_PORT=5000
   FLASK_DEBUG=true

4. Create the database:
   mysql -u root -p < project/database.sql

5. Run the app:
   python run.py

Notes
-----
The seeded reviewer user in database.sql has a placeholder password hash. Register a new user through the site, or replace the seeded passwordHash with a real Werkzeug generated hash before testing login for that account.
