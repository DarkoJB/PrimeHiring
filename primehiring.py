from os import write
from flask import Flask, render_template, url_for, request, redirect, session
from flask.wrappers import Response
from werkzeug.datastructures import UpdateDictMixin
from werkzeug.security import generate_password_hash, check_password_hash

import mariadb
import abc
import io
import csv

connection = mariadb.connect(
    user = "root",
    password = "",
    host = "localhost",
    port = 3306,
    database = "primehiringdb"
)

cursor = connection.cursor(dictionary = True)

app = Flask(__name__)

app.secret_key = "secret_key"

## DEVELOPERS ##

@app.route('/developers', methods = ['GET'])
def developers():
    query = "SELECT * FROM developers"
    cursor.execute(query)
    developers = cursor.fetchall()

    return render_template("developers.html", developers = developers)

## DEVELOPER ##
@app.route('/developer/<id>', methods = ['GET', 'POST'])
def developer(id):
    query = "SELECT * FROM developers WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    developer = cursor.fetchone()

    return render_template("developer.html", developer = developer)

## DEV HIRING ##
@app.route('/hiredev/<id>', methods = ['GET', 'POST'])
def hiredev(id):
    query = """INSERT INTO team(developers) WHERE id = %s SELECT %s
    FROM developers WHERE id = %s"""
    checks = request.form.getlist('check_devs')
    selects = request.form.get('team_id')
    values = (selects, checks, id)
    cursor.execute(query, values)
    developer = cursor.fetchall()
    teams = cursor.fetchall()
    team = cursor.fetchone()
    connection.commit()
    return redirect(url_for("developers.html", developer = developer, team = team, teams = teams))


## DEV_NEW ##
@app.route("/developer_new", methods=['GET', 'POST'])
def developer_new():
    if request.method == 'GET':
        return render_template("developer_new.html")
    elif request.method == 'POST':
        form = request.form
        values = (
            form["name"],
            form["email"],
            form["phone_number"],
            form["location"],
            form["price"],
            form["technology"],
            form["experience"],
            form["language"],
            id
        )
        query = """ INSERT INTO
        developers(name, email, phone_number, location, price, technology, experience, language)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, values)
        connection.commit()
        return redirect(url_for("developers"))


## DEV_EDIT ##
@app.route('/developer_edit/<id>', methods = ['GET', 'POST'])
def developer_edit(id):
    if request.method == 'GET':
        query = "SELECT * FROM developers WHERE id = %s"
        value = (id,)
        cursor.execute(query, value)
        developer = cursor.fetchone()
        return render_template("developer_edit.html", developer = developer)
    elif request.method == 'POST':
        form = request.form
        values = (
            form["name"],
            form["email"],
            form["phone_number"],
            form["location"],
            form["price"],
            form["technology"],
            form["experience"],
            form["language"],
            id
        )
        query = """UPDATE developers SET name = %s, email = %s, phone_number = %s, location = %s, price = %s, technology = %s, experience = %s, language = %s WHERE id = %s"""
        cursor.execute(query, values)
        connection.commit()
        return redirect(url_for("developers"))


## DEV_DELETE ##
@app.route('/developer_delete/<id>', methods = ['GET', 'POST'])
def developer_delete(id):
    query = """DELETE FROM developers WHERE id = %s"""
    value = (id,)
    cursor.execute(query, value)
    connection.commit()
    return redirect(url_for("developers"))


## TEAMS ##
@app.route('/teams', methods = ['GET'])
def teams():
    query = "SELECT * FROM team"
    cursor.execute(query)
    teams = cursor.fetchall()

    return render_template("teams.html", teams = teams)
## TEAM ##
@app.route('/team/<id>', methods = ['GET', 'POST'])
def team(id):
    query = "SELECT * FROM teams WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    team = cursor.fetchall()

    return render_template("team.html", team = team)

## TEAMS NEW ##
@app.route("/team_new", methods=['GET', 'POST'])
def team_new():
    if request.method == 'GET':
        return render_template("team_new.html")
    elif request.method == 'POST':
        form = request.form
        values = (
            form["team_name"],
            form["start_date"],
            form["end_date"],
            form["developers"],
            id
        )
        query = """ INSERT INTO
        team(team_name, start_date, end_date, developers)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, values)
        connection.commit()
        return redirect(url_for("teams"))


# ## ADD DEVS TO TEAM ##
# @app.route('/hire', methods = ['GET', 'POST'])
# def hire():
#     if request.method == 'GET':
#         return render_template("hire.html")
#     elif request.method == 'POST':
#         check_devs = request.form.getlist('check_devs')
#         query = """INSERT INTO team(developers)
#         VALUES (%s)
#         """, check_devs
#         cursor.execute(query, check_devs)
#         connection.commit()
#         return redirect(url_for("team"))

## TEAMS EDIT ##
@app.route('/team_edit/<id>', methods = ['GET', 'POST'])
def team_edit(id):
    if request.method == 'GET':
        query = "SELECT * FROM teams WHERE id = %s"
        value = (id,)
        cursor.execute(query, value)
        team = cursor.fetchone()
        return render_template("team_edit.html", team = team)
    elif request.method == 'POST':
        form = request.form
        values = (
            form["team_name"],
            form["start_date"],
            form["end_date"],
            id
        )
        query = """UPDATE teams SET
        team_name = %s,
        start_date = %s,
        end_date = %s
        WHERE id = %s
        """

        cursor.execute(query, values)
        connection.commit()
        return redirect(url_for("teams"))

## TEAM DELETE ##
@app.route('/team_delete/<id>', methods = ['GET', 'POST'])
def team_delete(id):
    query = """DELETE FROM teams WHERE id = %s"""

    value = (id,)
    cursor.execute(query, value)
    connection.commit()
    return redirect(url_for("teams"))




app.run(debug = True)
