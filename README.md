# PrimeHiring
Instructions:

Download XAMPP and set the MySQL port to 3306
Database creditentials are:
    user = "root",
    password = "",
    host = "localhost",
    port = 3306,
    database = "primehiringdb"
    
You can either make a new database with the same name yourself using the screenshots of the tables I've provided or you can use the .sql backup   

Install Python 3.9 and run 
pip install django
pip install mariadb
pip install flask
pip install werkzeug

Save the primehiring folder in the htdocs folder that's located in the XAMP directory (e.g. E:\Programs\XAMPP\htdocs)



Launch XAMPP and then start the Apache and MySQL services

Go to the directory of the project files in Powershell and run python primehiring.py

If you have done everything correctly the app should run and a powershell message will display telling you the port that it's running on (e.g. http://127.0.0.1:5000/developers).
